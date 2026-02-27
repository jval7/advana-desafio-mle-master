import json
import os
import pathlib
import typing
import zipfile

import fastapi
import fastapi.exceptions
import fastapi.responses
import pandas
import pydantic
import skops.io
import skops.io.exceptions

import challenge.model
import challenge.model_artifact


_ALLOWED_OPERATORS = frozenset(
    [
        "Aerolineas Argentinas",
        "Aeromexico",
        "Air Canada",
        "Air France",
        "Alitalia",
        "American Airlines",
        "Austral",
        "Avianca",
        "British Airways",
        "Copa Air",
        "Delta Air",
        "Gol Trans",
        "Grupo LATAM",
        "Iberia",
        "JetSmart SPA",
        "K.L.M.",
        "Lacsa",
        "Latin American Wings",
        "Oceanair Linhas Aereas",
        "Plus Ultra Lineas Aereas",
        "Qantas Airways",
        "Sky Airline",
        "United Airlines",
    ],
)
_ALLOWED_FLIGHT_TYPES = frozenset(["I", "N"])
_DEFAULT_MODEL_ARTIFACT_PATH = str(
    challenge.model_artifact.default_model_artifact_relative_path()
)
_MODEL_ARTIFACT_TRUSTED_TYPES_ENV_VAR = "MODEL_ARTIFACT_TRUSTED_TYPES"


class ModelArtifactError(RuntimeError):
    pass


class ModelArtifactNotFoundError(ModelArtifactError):
    pass


class ModelArtifactLoadError(ModelArtifactError):
    pass


class ModelArtifactTypeError(ModelArtifactError):
    pass


class ModelArtifactUntrainedError(ModelArtifactError):
    pass


class Flight(pydantic.BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int


class PredictRequest(pydantic.BaseModel):
    flights: list[Flight]


def _resolve_model_artifact_path() -> pathlib.Path:
    configured_path = os.getenv("MODEL_ARTIFACT_PATH", _DEFAULT_MODEL_ARTIFACT_PATH)
    raw_path = pathlib.Path(configured_path)

    if raw_path.is_absolute():
        return raw_path

    repository_root = pathlib.Path(__file__).resolve().parent.parent
    return repository_root / raw_path


def _resolve_model_artifact_trusted_types() -> tuple[str, ...]:
    trusted_types = set(challenge.model_artifact.default_trusted_types())
    configured_trusted_types = os.getenv(_MODEL_ARTIFACT_TRUSTED_TYPES_ENV_VAR, "")

    if configured_trusted_types:
        for raw_trusted_type in configured_trusted_types.split(","):
            trusted_type = raw_trusted_type.strip()
            if trusted_type:
                trusted_types.add(trusted_type)

    return tuple(sorted(trusted_types))


def _load_untrusted_types_from_artifact(artifact_path: pathlib.Path) -> set[str]:
    try:
        return set(skops.io.get_untrusted_types(file=artifact_path))
    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
    ) as exception:
        raise ModelArtifactLoadError(
            f"Could not inspect trusted types from model artifact at '{artifact_path}'.",
        ) from exception


def _load_delay_model_from_artifact(
    artifact_path: pathlib.Path,
) -> challenge.model.DelayModel:
    if not artifact_path.exists():
        raise ModelArtifactNotFoundError(
            f"Trained model artifact was not found at '{artifact_path}'.",
        )

    trusted_types = _resolve_model_artifact_trusted_types()
    artifact_untrusted_types = _load_untrusted_types_from_artifact(
        artifact_path=artifact_path
    )
    unknown_untrusted_types = sorted(artifact_untrusted_types - set(trusted_types))
    if unknown_untrusted_types:
        raise ModelArtifactLoadError(
            "Model artifact contains untrusted types that are not explicitly "
            f"allowed: {unknown_untrusted_types}. Configure "
            f"'{_MODEL_ARTIFACT_TRUSTED_TYPES_ENV_VAR}' only after reviewing "
            "each type."
        )

    try:
        loaded_object = skops.io.load(file=artifact_path, trusted=trusted_types)
    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
        skops.io.exceptions.UntrustedTypesFoundException,
    ) as exception:
        raise ModelArtifactLoadError(
            f"Could not load trained model artifact from '{artifact_path}'.",
        ) from exception

    if not isinstance(loaded_object, challenge.model.DelayModel):
        raise ModelArtifactTypeError(
            f"Model artifact at '{artifact_path}' does not contain DelayModel.",
        )

    if loaded_object._model is None:
        raise ModelArtifactUntrainedError(
            f"DelayModel loaded from '{artifact_path}' is not trained.",
        )

    return loaded_object


def _ensure_delay_model_loaded(app: fastapi.FastAPI) -> challenge.model.DelayModel:
    current_model = typing.cast(
        challenge.model.DelayModel | None, app.state.delay_model
    )
    if current_model is not None:
        return current_model

    artifact_path = _resolve_model_artifact_path()
    loaded_model = _load_delay_model_from_artifact(artifact_path=artifact_path)
    app.state.delay_model = loaded_model
    return loaded_model


def get_delay_model(request: fastapi.Request) -> challenge.model.DelayModel:
    return _ensure_delay_model_loaded(app=request.app)


def create_app(
    delay_model: challenge.model.DelayModel | None = None,
) -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    app.state.delay_model = delay_model

    @app.on_event("startup")
    async def load_model_on_startup() -> None:
        _ensure_delay_model_loaded(app=app)

    @app.exception_handler(fastapi.exceptions.RequestValidationError)
    async def handle_request_validation_error(
        request: fastapi.Request,
        exception: fastapi.exceptions.RequestValidationError,
    ) -> fastapi.responses.JSONResponse:
        del request
        return fastapi.responses.JSONResponse(
            status_code=400,
            content={"detail": exception.errors()},
        )

    @app.get("/health", status_code=200)
    async def get_health() -> dict[str, str]:
        return {"status": "OK"}

    @app.post("/predict", status_code=200)
    async def post_predict(
        request_dto: PredictRequest,
        prediction_model: challenge.model.DelayModel = fastapi.Depends(get_delay_model),
    ) -> dict[str, list[int]]:
        flight_rows: list[dict[str, str | int]] = []

        for flight in request_dto.flights:
            if flight.OPERA not in _ALLOWED_OPERATORS:
                raise fastapi.HTTPException(
                    status_code=400,
                    detail="Invalid OPERA value.",
                )
            if flight.TIPOVUELO not in _ALLOWED_FLIGHT_TYPES:
                raise fastapi.HTTPException(
                    status_code=400,
                    detail="Invalid TIPOVUELO value.",
                )
            if flight.MES < 1 or flight.MES > 12:
                raise fastapi.HTTPException(
                    status_code=400, detail="Invalid MES value."
                )

            flight_rows.append(flight.dict())

        request_data = pandas.DataFrame(flight_rows)
        features = prediction_model.preprocess(data=request_data)
        predictions = prediction_model.predict(features=features)

        return {"predict": predictions}

    return app


app = create_app()
