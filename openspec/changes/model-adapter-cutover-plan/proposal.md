## Why

The scaffold architecture is now in place, but production behavior and migration responsibilities are intentionally deferred. We need a focused follow-up change that implements the selected model adapter, completes test-suite migration policy, and defines safe cutover/rollback operations.

## What Changes

- Implement the concrete selected-model predictor adapter behind existing ports.
- Complete legacy test relocation outside `tests/` while preserving traceability.
- Verify challenge Makefile targets (`make model-test`, `make api-test`, `make stress-test`) end-to-end in a suitable environment.
- Define explicit cutover and rollback criteria for switching serving path.
- Finalize testing policy documentation for final app vs legacy reference tests.

## Capabilities

### New Capabilities

- `selected-model-adapter-runtime`: Concrete model adapter implementation and runtime readiness.
- `legacy-tests-cutover-governance`: Legacy test migration and operational cutover/rollback governance.

## Impact

- Affected code:
  - Predictor adapter implementation and preprocessing integration.
  - Test folder organization and documentation.
  - Operational runbook for rollout and rollback.
- APIs:
  - New architecture `/predict` path transitions from pending (503) to concrete inference behavior.
- Systems:
  - CI/local verification path includes make target execution evidence.
