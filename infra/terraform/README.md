# Terraform Deployment (GCP)

This folder manages the challenge deployment infrastructure with Terraform:

- Required project APIs
- Artifact Registry repository (Docker)
- Cloud Run service (v2)
- Public invoker IAM policy (optional)

## 1) Prerequisites

```bash
gcloud auth login
gcloud config set project <PROJECT_ID>
gcloud auth application-default login
```

## 2) Initialize

```bash
cd infra/terraform
terraform init
```

## 3) Use variables

```bash
cp terraform.tfvars.example terraform.tfvars
```

Update at least:

- `project_id`
- `image_uri`

## 4) Import existing resources (recommended for this repo)

If resources were created manually first, import them before first `apply`.

Set helper variables:

```bash
export PROJECT_ID="advana-fd-jv7-02261522"
export REGION="us-central1"
export AR_REPO="flight-delay-predictor"
export SERVICE="flight-delay-predictor-api"
```

Import required APIs:

```bash
terraform import 'google_project_service.required["run.googleapis.com"]' "projects/${PROJECT_ID}/services/run.googleapis.com"
terraform import 'google_project_service.required["artifactregistry.googleapis.com"]' "projects/${PROJECT_ID}/services/artifactregistry.googleapis.com"
terraform import 'google_project_service.required["cloudbuild.googleapis.com"]' "projects/${PROJECT_ID}/services/cloudbuild.googleapis.com"
terraform import 'google_project_service.required["iam.googleapis.com"]' "projects/${PROJECT_ID}/services/iam.googleapis.com"
```

Import Artifact Registry:

```bash
terraform import google_artifact_registry_repository.docker "projects/${PROJECT_ID}/locations/${REGION}/repositories/${AR_REPO}"
```

Import Cloud Run service:

```bash
terraform import google_cloud_run_v2_service.api "projects/${PROJECT_ID}/locations/${REGION}/services/${SERVICE}"
```

Import public invoker policy (if already public):

```bash
terraform import 'google_cloud_run_v2_service_iam_member.public_invoker[0]' "projects/${PROJECT_ID}/locations/${REGION}/services/${SERVICE} roles/run.invoker allUsers"
```

## 5) Plan and apply

```bash
terraform plan
terraform apply
```

## 6) Update deployment to a new image

Build and push new image first, then set `image_uri` in `terraform.tfvars` and apply:

```bash
terraform plan
terraform apply
```

## 7) Outputs

```bash
terraform output service_url
terraform output service_name
```
