## Why

The current challenge code solves the exercise but mixes concerns that make evolution, testing, and deployment harder than necessary for production use. We need a clear hexagonal structure now to stabilize the chosen model behind clean boundaries and allow implementation to grow without coupling business logic to framework details.

## What Changes

- Define a hexagonal architecture for model serving with explicit boundaries: entrypoint, application service, ports, and adapters.
- Establish an HTTP entrypoint layer for FastAPI concerns only (request/response mapping, validation, error translation).
- Establish an application service layer that orchestrates prediction use cases independently from framework and model runtime.
- Define ports (interfaces/contracts) for model inference and data transformation.
- Define adapter boundaries and placeholder wiring for model inference.
- Defer concrete selected-model adapter implementation to a follow-up change.
- Provide a fake predictor adapter for dependency injection in service-layer tests.
- Introduce domain-focused DTOs and custom exceptions so error handling and contracts are explicit.
- Keep `challenge/` as legacy reference for comparison during migration.
- Keep legacy tests in their current location for this scaffold iteration and defer relocation to follow-up change `model-adapter-cutover-plan`.
- Defer full challenge make target e2e verification to follow-up change `model-adapter-cutover-plan`.

## Capabilities

### New Capabilities

- `hexagonal-prediction-architecture`: Define and enforce the target architecture, boundaries, and responsibilities for productionized prediction flow.
- `prediction-http-entrypoint`: Provide a framework-specific HTTP entrypoint that translates transport concerns to application contracts.
- `model-port-and-adapter`: Provide a port for model inference and an adapter scaffold/contract, leaving concrete selected-model implementation pending.

### Modified Capabilities

- None in main specs yet (there are no existing baseline specs under `openspec/specs`).

## Impact

- Affected code:
  - New architecture-aligned package/module structure for entrypoint, service, ports, adapters, DTOs, and custom exceptions.
  - Composition/wiring for dependency injection between service and adapters.
  - Service-level tests for the new architecture using fake adapters.
  - Fake adapter implementation dedicated to service-layer tests.
- APIs:
  - Prediction API contract will be re-expressed through DTOs and consistent error mapping while preserving expected challenge behavior.
- Dependencies:
  - No mandatory dependency expansion in this iteration; focus is architectural shaping with current stack.
- Systems:
  - `challenge/` remains as legacy baseline for comparison.
  - Legacy test relocation is deferred to follow-up `model-adapter-cutover-plan`.
  - Makefile e2e verification is deferred to follow-up `model-adapter-cutover-plan`.
