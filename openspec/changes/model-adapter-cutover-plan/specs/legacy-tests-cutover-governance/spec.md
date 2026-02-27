## ADDED Requirements

### Requirement: Legacy test reference separation
The system MUST maintain legacy challenge tests in a dedicated reference location outside `tests/`, and `tests/` MUST remain focused on final-application tests.

#### Scenario: Test locations are purpose-specific
- **WHEN** engineers inspect repository test directories
- **THEN** legacy reference tests are outside `tests/` and final app tests remain under `tests/`

### Requirement: Challenge Makefile verification evidence
The system MUST provide explicit verification evidence that `make model-test`, `make api-test`, and `make stress-test` remain operational after migration steps.

#### Scenario: Make targets execute successfully
- **WHEN** engineers run challenge make targets in the designated validation environment
- **THEN** each target finishes successfully without requiring renamed commands

### Requirement: Cutover and rollback criteria
The system MUST define cutover entry criteria and rollback triggers before switching default runtime from legacy to new architecture.

#### Scenario: Cutover decision is criteria-driven
- **WHEN** rollout readiness is assessed
- **THEN** cutover proceeds only when documented criteria are met, otherwise legacy path remains default
