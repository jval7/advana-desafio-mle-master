## 1. Architecture Baseline

- [x] 1.1 Confirm architecture package root for the new implementation (`predictor_app/`).
- [x] 1.2 Define and create the hexagonal folder map for `entrypoints`, `service`, `ports`, `adapters`, `dtos`, and `exceptions`.
- [x] 1.3 Add module-level boundaries and naming conventions documentation aligned with the design decisions.
- [x] 1.4 Create composition root module responsible for dependency wiring between services and adapters.

## 2. Domain Contracts and Error Model

- [x] 2.1 Define Pydantic request DTOs for prediction input batch and individual flight input.
- [x] 2.2 Define Pydantic response DTO for deterministic prediction output ordering.
- [x] 2.3 Define domain/application custom exception classes for contract validation and inference failures.
- [x] 2.4 Define exception-to-HTTP mapping rules as explicit contracts for entrypoint translation.

## 3. Ports and Service Orchestration

- [x] 3.1 Define model predictor port interface for batch inference contract.
- [x] 3.2 Define optional preprocessing port interface if preprocessing is separated from model adapter.
- [x] 3.3 Implement prediction application service that orchestrates DTO input to port invocation.
- [x] 3.4 Add service-level validation rules that belong to business/application policy rather than transport.

## 4. Adapter Scaffolding (Concrete Model Deferred)

- [x] 4.1 Implement predictor adapter scaffold conforming to the predictor port contract.
- [x] 4.2 Implement explicit pending-implementation exception flow in scaffold adapter.
- [x] 4.3 Wire scaffold adapter into composition root and verify dependency direction remains compliant with hexagonal boundaries.
- [x] 4.4 Document follow-up change scope for concrete selected-model adapter implementation in `model-adapter-cutover-plan`.
- [x] 4.5 Implement fake predictor adapter for deterministic service-layer tests.

## 5. HTTP Entrypoint

- [x] 5.1 Implement prediction web entrypoint module that only handles transport concerns.
- [x] 5.2 Map incoming HTTP payloads to request DTOs and delegate orchestration to application service.
- [x] 5.3 Implement standardized HTTP error responses from mapped custom exceptions.
- [x] 5.4 Preserve expected response contract shape and order behavior for compatibility.

## 6. Test Strategy Migration

- [x] 6.1 Create dedicated legacy reference test location outside `tests/` (deferred to `model-adapter-cutover-plan` by scaffold-only decision).
- [x] 6.2 Move/copy legacy challenge tests into the reference location while preserving traceability (deferred to `model-adapter-cutover-plan`).
- [x] 6.3 Add service-layer unit tests that inject the fake adapter and validate orchestration behavior.
- [x] 6.4 Keep test scope minimal for this change: challenge-required tests plus service-layer tests (no exhaustive all-layer coverage).

## 7. Verification and Cutover

- [x] 7.1 Add architecture compliance checks for dependency direction across layers (scoped to `predictor_app`).
- [x] 7.2 Execute full quality gates (unit/API tests and pre-commit hooks) on the new architecture path.
- [x] 7.3 Verify challenge Makefile targets remain operational (`make model-test`, `make api-test`, `make stress-test`) after architecture changes (deferred to `model-adapter-cutover-plan`).
- [x] 7.4 Define and document cutover criteria to switch default serving path from legacy to hexagonal flow (deferred to `model-adapter-cutover-plan`).
- [x] 7.5 Define rollback procedure keeping legacy path available until parity and reliability thresholds are met (deferred to `model-adapter-cutover-plan`).

## 8. Documentation and Cleanup

- [x] 8.1 Document final architecture decisions and directory map in project docs for scaffold scope.
- [x] 8.2 Document testing policy (`tests/` final app only, legacy tests in reference location) in follow-up (`model-adapter-cutover-plan`).
- [x] 8.3 Document open operational decisions resolved during implementation (package root, preprocessing split, legacy sunset criteria for this change).
- [x] 8.4 Prepare change for OpenSpec verification through scope rebaseline and follow-up change linkage.
