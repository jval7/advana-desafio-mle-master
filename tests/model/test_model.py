import unittest

import challenge.model
import pandas as pd
import sklearn.metrics
import sklearn.model_selection


class TestModel(unittest.TestCase):
    FEATURES_COLS = [
        "OPERA_Latin American Wings",
        "MES_7",
        "MES_10",
        "OPERA_Grupo LATAM",
        "MES_12",
        "TIPOVUELO_I",
        "MES_4",
        "MES_11",
        "OPERA_Sky Airline",
        "OPERA_Copa Air",
    ]

    TARGET_COL = ["delay"]

    def setUp(self) -> None:
        super().setUp()
        self.model = challenge.model.DelayModel()
        self.data = pd.read_csv(filepath_or_buffer="../data/data.csv")

    def test_model_preprocess_for_training(self) -> None:
        preprocess_result = self.model.preprocess(data=self.data, target_column="delay")
        if not isinstance(preprocess_result, tuple):
            self.fail("Expected tuple[features, target] during training preprocess.")
        features, target = preprocess_result

        assert isinstance(features, pd.DataFrame)
        assert features.shape[1] == len(self.FEATURES_COLS)
        assert set(features.columns) == set(self.FEATURES_COLS)

        assert isinstance(target, pd.DataFrame)
        assert target.shape[1] == len(self.TARGET_COL)
        assert set(target.columns) == set(self.TARGET_COL)

    def test_model_preprocess_for_serving(self) -> None:
        features = self.model.preprocess(data=self.data)
        assert isinstance(features, pd.DataFrame)

        assert features.shape[1] == len(self.FEATURES_COLS)
        assert set(features.columns) == set(self.FEATURES_COLS)

    def test_model_fit(self) -> None:
        preprocess_result = self.model.preprocess(data=self.data, target_column="delay")
        if not isinstance(preprocess_result, tuple):
            self.fail("Expected tuple[features, target] during fit preprocess.")
        features, target = preprocess_result

        _, features_validation, _, target_validation = (
            sklearn.model_selection.train_test_split(
                features, target, test_size=0.33, random_state=42
            )
        )

        self.model.fit(features=features, target=target)
        assert self.model._model is not None

        predicted_target = self.model._model.predict(features_validation)

        report = sklearn.metrics.classification_report(
            target_validation, predicted_target, output_dict=True
        )

        assert report["0"]["recall"] < 0.60
        assert report["0"]["f1-score"] < 0.70
        assert report["1"]["recall"] > 0.60
        assert report["1"]["f1-score"] > 0.30

    def test_model_predict(self) -> None:
        features = self.model.preprocess(data=self.data)
        assert isinstance(features, pd.DataFrame)

        predicted_targets = self.model.predict(features=features)

        assert isinstance(predicted_targets, list)
        assert len(predicted_targets) == features.shape[0]
        assert all(
            isinstance(predicted_target, int) for predicted_target in predicted_targets
        )
