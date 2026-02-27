output "service_name" {
  description = "Cloud Run service name."
  value       = google_cloud_run_v2_service.api.name
}

output "service_url" {
  description = "Cloud Run service URL."
  value       = google_cloud_run_v2_service.api.uri
}

output "artifact_repository" {
  description = "Artifact Registry repository id."
  value       = google_artifact_registry_repository.docker.repository_id
}
