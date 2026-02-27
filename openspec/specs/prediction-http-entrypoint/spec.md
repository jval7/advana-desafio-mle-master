# prediction-http-entrypoint Specification

## Purpose
TBD - created by archiving change productivize-model-with-hexagonal-architecture. Update Purpose after archive.
## Requirements
### Requirement: HTTP entrypoint transport isolation
The prediction HTTP entrypoint MUST handle only transport concerns: request validation, response mapping, and exception-to-HTTP translation, while delegating business orchestration to the application service.

#### Scenario: Route delegates orchestration
- **WHEN** a valid prediction request is received
- **THEN** the route validates DTOs and delegates prediction execution to the application service instead of executing model logic inline

### Requirement: Prediction request contract validation
The prediction flow MUST validate each incoming flight item with required fields and allowed value domains before inference execution.

#### Scenario: Invalid month is rejected
- **WHEN** a prediction request contains a flight with month outside the configured domain
- **THEN** the API returns a client error response for invalid request domain values

#### Scenario: Invalid flight type is rejected
- **WHEN** a prediction request contains a flight type outside allowed values
- **THEN** the API returns a client error response for invalid request domain values

### Requirement: Prediction response contract
The prediction endpoint MUST return a deterministic response schema containing one prediction per input flight in the same order.

#### Scenario: Response shape is preserved
- **WHEN** a valid request with N flights is processed
- **THEN** the response contains a prediction list with exactly N integer values aligned by input order

### Requirement: Pending predictor availability signaling
The prediction endpoint MUST translate pending predictor readiness errors into an explicit service-unavailable response.

#### Scenario: Pending predictor returns 503
- **WHEN** runtime wiring uses a pending predictor adapter and `/predict` is called
- **THEN** the endpoint responds with HTTP 503 and a mapped domain error payload
