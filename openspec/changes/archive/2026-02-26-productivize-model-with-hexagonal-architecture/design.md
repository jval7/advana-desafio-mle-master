## Context

This change is intentionally scoped as a **scaffold-first** iteration to lock architecture decisions and contracts without forcing full migration in one step.

Constraints and current state:
- Keep existing `challenge/` implementation untouched as legacy reference.
- Keep current challenge test locations unchanged in this iteration.
- Preserve challenge Makefile command names.
- Keep architecture and contracts explicit through ports, DTOs, and custom exceptions.

## Goals / Non-Goals

**Goals:**
- Define and implement a hexagonal scaffold under `predictor_app/`.
- Isolate web transport concerns from use-case orchestration.
- Split preprocessing and prediction through separate ports.
- Keep runtime behavior explicit while concrete model adapter is pending.
- Add minimal architecture-direction checks for `predictor_app`.

**Non-Goals:**
- Implement concrete selected-model adapter.
- Move legacy tests out of `tests/` in this change.
- Define and execute final cutover/rollback in this change.
- Execute full make target e2e verification in offline-constrained local environment.

## Closed Decisions (Rebaseline)

### 1) Official package root

Decision:
- `predictor_app/` is the official package root for the new hexagonal scaffold.

Rationale:
- It allows incremental migration without touching `challenge/`.

### 2) Runtime behavior before concrete adapter

Decision:
- Runtime wiring uses a passthrough preprocess adapter and a pending predictor adapter.
- `/predict` in the new entrypoint maps `PredictorNotReadyError` to HTTP 503.

Rationale:
- It prevents fake predictions in production-like runtime while preserving executable wiring.

### 3) Preprocessing separation

Decision:
- Preprocessing is separated now via `PreprocessPort`.
- `ModelPredictorPort` receives preprocessed feature DTOs, not raw flight DTOs.

Rationale:
- It prevents early coupling between input contracts and model adapter internals.

### 4) Legacy tests strategy in this iteration

Decision:
- Legacy tests remain where they are in this change.
- Migration to legacy reference location is deferred to follow-up change `model-adapter-cutover-plan`.

Rationale:
- It keeps this iteration focused on architecture contracts and service-level behavior.

### 5) Follow-up scope ownership

Decision:
- A single follow-up change, `model-adapter-cutover-plan`, owns:
  - Concrete selected-model adapter implementation.
  - Legacy test relocation strategy execution.
  - Make target e2e verification.
  - Cutover and rollback criteria.

Rationale:
- Keeps change boundaries clear and archive-ready for scaffold work.

## Risks / Trade-offs

- [Risk] Deferred legacy test migration can look inconsistent with end-state architecture.
  - Mitigation: keep explicit deferment notes in tasks/specs and follow-up change.

- [Risk] Pending runtime returns 503 until concrete adapter exists.
  - Mitigation: this is intentional and explicit for scaffold phase.

- [Risk] Minimal architecture checks may not cover every cross-layer violation.
  - Mitigation: start with strict rules for `predictor_app`; expand in follow-up if needed.

## Migration Plan (This Change)

1. Finalize contracts for request/response and preprocessing/prediction ports.
2. Update service orchestration: validate -> preprocess -> predict -> contract checks.
3. Wire runtime to pending predictor behavior.
4. Add minimal architecture check rules for layer import direction.
5. Add service-layer tests with fake adapters and contract mismatch coverage.
6. Rebaseline OpenSpec tasks/specs to reflect scaffold-only scope.
7. Create follow-up change `model-adapter-cutover-plan`.

## Deferred To Follow-Up (`model-adapter-cutover-plan`)

- Concrete model adapter implementation.
- Legacy test relocation outside `tests/`.
- Challenge make target e2e verification.
- Cutover/rollback criteria and final testing policy.
