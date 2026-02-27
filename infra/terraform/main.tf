locals {
  labels = {
    managed_by = "terraform"
    project    = "advana-challenge"
  }
  cloud_run_runtime_service_account_email_input  = var.cloud_run_runtime_service_account_email == null ? "" : trimspace(var.cloud_run_runtime_service_account_email)
  terraform_deployer_service_account_email_input = var.terraform_deployer_service_account_email == null ? "" : trimspace(var.terraform_deployer_service_account_email)
  runtime_service_account_email                  = local.cloud_run_runtime_service_account_email_input != "" ? local.cloud_run_runtime_service_account_email_input : null
  terraform_deployer_member                      = local.terraform_deployer_service_account_email_input != "" ? "serviceAccount:${local.terraform_deployer_service_account_email_input}" : null
}

resource "google_project_service" "required" {
  for_each = toset(var.required_apis)

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "docker" {
  project       = var.project_id
  location      = var.region
  repository_id = var.artifact_registry_repository_id
  description   = "Docker images for flight delay predictor"
  format        = "DOCKER"
  labels        = local.labels

  depends_on = [google_project_service.required]
}

resource "google_service_account_iam_member" "terraform_act_as_runtime" {
  count = local.terraform_deployer_member == null || local.runtime_service_account_email == null ? 0 : 1

  service_account_id = "projects/${var.project_id}/serviceAccounts/${local.runtime_service_account_email}"
  role               = "roles/iam.serviceAccountUser"
  member             = local.terraform_deployer_member

  depends_on = [google_project_service.required]
}

resource "google_cloud_run_v2_service" "api" {
  project  = var.project_id
  location = var.region
  name     = var.cloud_run_service_name
  ingress  = "INGRESS_TRAFFIC_ALL"
  labels   = local.labels

  scaling {
    manual_instance_count = var.cloud_run_manual_instance_count
    min_instance_count    = var.cloud_run_service_min_instance_count
  }

  template {
    service_account = local.runtime_service_account_email

    scaling {
      min_instance_count = var.cloud_run_min_instance_count
      max_instance_count = var.cloud_run_max_instance_count
    }

    containers {
      image = var.image_uri

      ports {
        container_port = var.container_port
      }

      env {
        name  = "MODEL_ARTIFACT_PATH"
        value = var.model_artifact_path
      }
    }
  }

  traffic {
    percent = 100
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  }

  depends_on = [
    google_project_service.required,
    google_artifact_registry_repository.docker,
    google_service_account_iam_member.terraform_act_as_runtime,
  ]
}

resource "google_cloud_run_v2_service_iam_member" "public_invoker" {
  count = var.allow_unauthenticated ? 1 : 0

  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
