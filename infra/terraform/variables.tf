variable "project_id" {
  description = "GCP project id where resources are managed."
  type        = string
}

variable "region" {
  description = "GCP region for Artifact Registry and Cloud Run."
  type        = string
  default     = "us-central1"
}

variable "artifact_registry_repository_id" {
  description = "Artifact Registry repository id for Docker images."
  type        = string
  default     = "flight-delay-predictor"
}

variable "cloud_run_service_name" {
  description = "Cloud Run service name."
  type        = string
  default     = "flight-delay-predictor-api"
}

variable "cloud_run_runtime_service_account_email" {
  description = "Runtime service account email for Cloud Run. Defaults to Compute Engine default service account when unset."
  type        = string
  default     = null
}

variable "image_uri" {
  description = "Full container image URI to deploy in Cloud Run."
  type        = string
}

variable "model_artifact_path" {
  description = "Model artifact path passed as MODEL_ARTIFACT_PATH env var."
  type        = string
  default     = "data/model.skops"
}

variable "container_port" {
  description = "Container port exposed by the application."
  type        = number
  default     = 8080
}

variable "cloud_run_min_instance_count" {
  description = "Minimum number of Cloud Run instances."
  type        = number
  default     = 0
}

variable "cloud_run_max_instance_count" {
  description = "Maximum number of Cloud Run instances."
  type        = number
  default     = 2
}

variable "cloud_run_service_min_instance_count" {
  description = "Service-level minimum number of Cloud Run instances."
  type        = number
  default     = 0
}

variable "cloud_run_manual_instance_count" {
  description = "Service-level manual instance count for Cloud Run."
  type        = number
  default     = 0
}

variable "allow_unauthenticated" {
  description = "Whether to allow unauthenticated invocations in Cloud Run."
  type        = bool
  default     = true
}

variable "required_apis" {
  description = "List of project APIs required by this deployment."
  type        = list(string)
  default = [
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "iam.googleapis.com",
  ]
}
