## Context

`productivize-model-with-hexagonal-architecture` established the scaffold and contracts. This follow-up implements concrete runtime behavior and migration closure items that were intentionally deferred.

## Goals / Non-Goals

**Goals:**
- Implement selected-model predictor adapter conforming to `ModelPredictorPort`.
- Keep `PreprocessPort`/predictor contract boundaries stable.
- Relocate legacy challenge tests outside `tests/`.
- Validate challenge Makefile targets end-to-end.
- Define cutover and rollback criteria for runtime transition.

**Non-Goals:**
- Re-defining architecture boundaries established in scaffold change.
- Rewriting challenge legacy implementation under `challenge/`.

## Decisions

### 1) Concrete model adapter remains behind existing ports

Decision:
- Implement selected-model inference only through adapter(s), without changing service/entrypoint responsibilities.

### 2) Legacy tests become explicit reference suite

Decision:
- Move/copy legacy tests to a dedicated reference location and keep `tests/` focused on final architecture tests.

### 3) Runtime cutover is criteria-driven

Decision:
- Switch default runtime path only after explicit parity and reliability criteria are met.

### 4) Rollback path remains available

Decision:
- Keep legacy serving path available until cutover criteria are met and stable in production-like checks.

## Risks / Trade-offs

- [Risk] Concrete adapter may diverge from expected challenge behavior.
  - Mitigation: parity checks against known fixtures and legacy outcomes.

- [Risk] Test migration may break developer expectations.
  - Mitigation: clear testing policy documentation and command aliases.

- [Risk] Cutover without guardrails can cause incidents.
  - Mitigation: explicit rollout checklist and rollback triggers.
