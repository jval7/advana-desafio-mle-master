import pathlib


_DEFAULT_MODEL_ARTIFACT_RELATIVE_PATH = pathlib.Path("data/model.skops")
_DEFAULT_TRUSTED_TYPES = (
    "challenge.model.DelayModel",
    "xgboost.core.Booster",
    "xgboost.sklearn.XGBClassifier",
)


def default_model_artifact_relative_path() -> pathlib.Path:
    return _DEFAULT_MODEL_ARTIFACT_RELATIVE_PATH


def default_trusted_types() -> tuple[str, ...]:
    return _DEFAULT_TRUSTED_TYPES
