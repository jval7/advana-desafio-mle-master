# model-port-and-adapter Specification

## Purpose
TBD - created by archiving change productivize-model-with-hexagonal-architecture. Update Purpose after archive.
## Requirements
### Requirement: Preprocessing port contract
The system MUST define a preprocessing port that transforms a batch of flight DTOs into a batch of preprocessed feature DTOs.

#### Scenario: Preprocessing contract is batch-safe
- **WHEN** the application service invokes the preprocessing port with a batch of flight inputs
- **THEN** the returned feature batch length matches the input batch length

### Requirement: Model predictor port contract
The system MUST define a model predictor port that exposes a prediction operation for a batch of preprocessed feature DTOs and returns one binary delay prediction per input item.

#### Scenario: Predictor contract is batch-safe
- **WHEN** the application service invokes the predictor port with a batch of preprocessed features
- **THEN** the returned predictions list length matches the feature batch length

### Requirement: Adapter scaffold contract
The system MUST provide an adapter scaffold implementation of the predictor port for architecture wiring, while concrete selected-model inference is deferred to a follow-up change.

#### Scenario: Adapter scaffold indicates pending implementation
- **WHEN** the service requests predictions through the scaffold adapter
- **THEN** the adapter raises a specific domain/application pending-implementation exception

### Requirement: Composition root adapter wiring
The system MUST wire a predictor port implementation (including scaffold implementation) in the composition root so entrypoints and services can run through architecture boundaries.

#### Scenario: Service uses wired predictor implementation
- **WHEN** the web entrypoint invokes the prediction service
- **THEN** the service calls a predictor port implementation provided by composition root wiring

### Requirement: Fake adapter support for service tests
The system MUST provide fake preprocessing and prediction adapter implementations for service-layer tests, and the service MUST accept adapter implementations through dependency injection.

#### Scenario: Service test injects fake adapters
- **WHEN** a service-layer unit test injects fake preprocessing and fake predictor adapters
- **THEN** the service executes orchestration logic using deterministic predictions without requiring concrete model inference

### Requirement: Domain-specific error signaling
The adapter and service layers MUST raise explicit domain/application exceptions for prediction contract violations and MUST avoid generic exception contracts.

#### Scenario: Contract violation raises explicit error
- **WHEN** prediction input violates defined domain rules after transport validation
- **THEN** the adapter or service raises a specific domain/application exception that can be mapped by the entrypoint
