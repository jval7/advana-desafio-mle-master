## ADDED Requirements

### Requirement: Concrete selected-model predictor adapter
The system MUST implement a concrete selected-model predictor adapter that conforms to `ModelPredictorPort` and produces one binary prediction per preprocessed feature row.

#### Scenario: Concrete predictor responds for valid feature batch
- **WHEN** the service invokes the concrete predictor adapter with a valid preprocessed batch
- **THEN** the adapter returns one integer prediction per input row

### Requirement: Runtime wiring cutover support
The composition root MUST support wiring the concrete predictor adapter as runtime implementation once cutover criteria are met.

#### Scenario: Runtime wiring uses concrete predictor after cutover
- **WHEN** cutover conditions are explicitly enabled
- **THEN** the application wiring resolves the concrete predictor adapter instead of pending adapter behavior
