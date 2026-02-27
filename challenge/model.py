import numpy
import pandas
import xgboost


class DelayModel:
    _feature_columns = [
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

    def __init__(
        self,
    ) -> None:
        self._model: xgboost.XGBClassifier | None = None

    def _get_min_diff(self, data: pandas.DataFrame) -> pandas.Series:
        scheduled_date = pandas.to_datetime(data["Fecha-I"], errors="coerce")
        operation_date = pandas.to_datetime(data["Fecha-O"], errors="coerce")
        min_diff = (operation_date - scheduled_date).dt.total_seconds() / 60
        return min_diff.fillna(0)

    def _get_dummies_features(self, data: pandas.DataFrame) -> pandas.DataFrame:
        encoded_features = pandas.concat(
            [
                pandas.get_dummies(data["OPERA"], prefix="OPERA"),
                pandas.get_dummies(data["TIPOVUELO"], prefix="TIPOVUELO"),
                pandas.get_dummies(data["MES"], prefix="MES"),
            ],
            axis=1,
        )

        return encoded_features.reindex(columns=self._feature_columns, fill_value=0)

    def preprocess(
        self,
        data: pandas.DataFrame,
        target_column: str | None = None,
    ) -> tuple[pandas.DataFrame, pandas.DataFrame] | pandas.DataFrame:
        prepared_data = data.copy()

        features = self._get_dummies_features(data=prepared_data)

        if target_column is None:
            return features

        if target_column not in prepared_data.columns:
            prepared_data["min_diff"] = self._get_min_diff(data=prepared_data)
            prepared_data[target_column] = numpy.where(
                prepared_data["min_diff"] > 15,
                1,
                0,
            )

        target = prepared_data[[target_column]]
        return features, target

    def fit(
        self,
        features: pandas.DataFrame,
        target: pandas.DataFrame,
    ) -> None:
        target_series = target.iloc[:, 0]
        n_y0 = int((target_series == 0).sum())
        n_y1 = int((target_series == 1).sum())

        scale_pos_weight = 1.0
        if n_y0 > 0 and n_y1 > 0:
            scale_pos_weight = n_y0 / n_y1

        self._model = xgboost.XGBClassifier(
            random_state=1,
            learning_rate=0.01,
            scale_pos_weight=scale_pos_weight,
        )
        self._model.fit(features, target_series)

    def predict(
        self,
        features: pandas.DataFrame,
    ) -> list[int]:
        if self._model is None:
            return [0] * len(features)

        predicted_values = self._model.predict(features)
        return [int(prediction) for prediction in predicted_values]
