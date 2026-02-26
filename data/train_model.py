import pathlib

import joblib
import pandas

import challenge.model

_REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DATASET_PATH = _REPOSITORY_ROOT / "data" / "data.csv"
_MODEL_ARTIFACT_PATH = _REPOSITORY_ROOT / "data" / "model.joblib"


def train_delay_model(
    dataset_path: pathlib.Path,
) -> challenge.model.DelayModel:
    dataset = pandas.read_csv(dataset_path, low_memory=False)

    delay_model = challenge.model.DelayModel()
    features, target = delay_model.preprocess(
        data=dataset,
        target_column="delay",
    )
    delay_model.fit(features=features, target=target)

    return delay_model


def save_delay_model(
    delay_model: challenge.model.DelayModel,
    artifact_path: pathlib.Path,
) -> None:
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(delay_model, artifact_path)


def main() -> None:
    trained_model = train_delay_model(dataset_path=_DATASET_PATH)
    save_delay_model(delay_model=trained_model, artifact_path=_MODEL_ARTIFACT_PATH)
    print(f"Trained model saved at '{_MODEL_ARTIFACT_PATH}'.")


if __name__ == "__main__":
    main()
