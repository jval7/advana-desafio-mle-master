# Challenge Notes

## Part I - Model Operationalization

### Summary

The notebook exploration compared XGBoost and Logistic Regression under class-imbalance conditions.
For this implementation, the selected approach is **Logistic Regression with class balancing** over the DS top-10 engineered one-hot features:

- `OPERA_Latin American Wings`
- `MES_7`
- `MES_10`
- `OPERA_Grupo LATAM`
- `MES_12`
- `TIPOVUELO_I`
- `MES_4`
- `MES_11`
- `OPERA_Sky Airline`
- `OPERA_Copa Air`

### Why this model

- It satisfies the expected challenge metrics on the provided tests.
- It is simpler to maintain and faster to train than boosted-tree alternatives for this scope.
- It keeps deterministic and clear behavior for this challenge API.

### Implementation details

- `challenge/model.py` computes `min_diff` from `Fecha-O - Fecha-I`.
- `delay` is derived as `1` when `min_diff > 15`, otherwise `0`.
- Features are one-hot encoded (`OPERA`, `TIPOVUELO`, `MES`) and aligned to the fixed top-10 column set.
- Training uses class-balanced Logistic Regression (`class_weight` derived from class proportions).
- Offline training is automated with `data/train_model.py`.
- Trained artifact is stored at `data/model.joblib`.
- Runtime loads the artifact in `challenge/api.py` (default path `data/model.joblib`, overridable with `MODEL_ARTIFACT_PATH`).
- If the artifact is missing/corrupt/untrained, the API fails fast during startup.

## Part II - API

- Implemented with `FastAPI` in `challenge/api.py`.
- Endpoints:
  - `GET /health` -> `{"status": "OK"}`
  - `POST /predict` -> `{"predict": [int, ...]}`
- Input validation for `OPERA`, `TIPOVUELO`, and `MES`.
- Request validation errors are mapped to HTTP `400` to match challenge test expectations.

## Part III - Stress Test

- `make stress-test` is supported through the provided Makefile target.
- `STRESS_URL` should be set to the deployed API URL before execution.

## Part IV - CI/CD

- Workflow files are preserved in `workflows/`.
- The `.github/workflows` copy step is handled in repository setup for delivery.
