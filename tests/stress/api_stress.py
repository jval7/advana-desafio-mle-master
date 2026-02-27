import locust


class StressUser(locust.HttpUser):  # type: ignore[misc]
    @locust.task  # type: ignore[misc]
    def predict_argentinas(self) -> None:
        self.client.post(
            "/predict",
            json={
                "flights": [
                    {"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "N", "MES": 3}
                ]
            },
        )

    @locust.task  # type: ignore[misc]
    def predict_latam(self) -> None:
        self.client.post(
            "/predict",
            json={"flights": [{"OPERA": "Grupo LATAM", "TIPOVUELO": "N", "MES": 3}]},
        )
