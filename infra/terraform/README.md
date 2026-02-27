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

## 8) GitHub Actions (CI/CD)

Workflow files:

- `.github/workflows/terraform.yml`
- `.github/workflows/release.yml`

What they do:

- `terraform.yml`: runs `terraform fmt`, `validate`, and `plan` on PR and push to `develop` when Terraform files change.
- `release.yml`: release sequence for `main` in this order:
  1) app validation and tests
  2) image build and push
  3) terraform apply with the new image
  4) smoke test (`/health` and `/predict`)
- Both workflows import existing resources before plan/apply (best effort) to support this repository bootstrap path.

### Required repository configuration

Create these **Repository Variables** (Settings -> Secrets and variables -> Actions -> Variables):

- `GCP_PROJECT_ID` (example: `advana-fd-jv7-02261522`)
- `GCP_REGION` (example: `us-central1`)
- `TF_ARTIFACT_REPO` (example: `flight-delay-predictor`)
- `TF_CLOUD_RUN_SERVICE` (example: `flight-delay-predictor-api`)
- `TF_IMAGE_URI` (full image URI currently deployed)
- `TF_IMAGE_NAME` (optional, default: `flight-delay-api`)
- `TF_MODEL_ARTIFACT_PATH` (example: `data/model.skops`)
- `TF_CI_ENABLED` (`true` to enable Terraform workflow, `false` or unset to skip it)
- `GCP_WORKLOAD_IDENTITY_PROVIDER` (full Workload Identity Provider resource path, for example: `projects/123456789012/locations/global/workloadIdentityPools/github/providers/github-oidc`)
- `GCP_SERVICE_ACCOUNT_EMAIL` (service account email to impersonate from GitHub Actions, for example: `github-deployer@<PROJECT_ID>.iam.gserviceaccount.com`)

No repository secret with service account JSON is required.
GitHub Actions uses OIDC (`google-github-actions/auth@v2`) with Workload Identity Federation.

If `TF_CI_ENABLED` is not set to `true`, the Terraform workflow is skipped automatically (it will not fail CI).

### Recommended protection

- Configure the GitHub `production` environment with required reviewers so manual apply needs approval.
