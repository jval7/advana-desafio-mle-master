## 1. Concrete Model Adapter

- [ ] 1.1 Implement selected-model predictor adapter conforming to `ModelPredictorPort`.
- [ ] 1.2 Integrate preprocessing output with concrete model input contract.
- [ ] 1.3 Add adapter-specific error mapping to existing domain exceptions.
- [ ] 1.4 Wire concrete adapter in composition root behind environment-safe toggle.

## 2. Legacy Test Separation

- [ ] 2.1 Create dedicated legacy reference test location outside `tests/`.
- [ ] 2.2 Move/copy legacy challenge tests preserving traceability and intent.
- [ ] 2.3 Keep challenge Makefile interface compatible after migration.

## 3. Verification And Operations

- [ ] 3.1 Execute `make model-test`, `make api-test`, and `make stress-test` end-to-end in a suitable environment.
- [ ] 3.2 Define cutover entry criteria (functional parity, reliability, operability).
- [ ] 3.3 Define rollback triggers and rollback procedure.
- [ ] 3.4 Document final testing policy (`tests/` final app only, legacy tests in reference location).
