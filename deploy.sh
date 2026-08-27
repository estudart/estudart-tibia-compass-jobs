#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="estudart-tibia-compass"
REGION="us-central1"
REPO="tibia-compass"
TAG="${TAG:-$(date +%s)}"

JOBS=(
  "killstatistics-job:src/jobs/killstatistics/Dockerfile"
  "creatures-job:src/jobs/creatures/Dockerfile"
)

for entry in "${JOBS[@]}"; do
  JOB_NAME="${entry%%:*}"
  DOCKERFILE="${entry#*:}"
  IMAGE="us-central1-docker.pkg.dev/${PROJECT_ID}/${REPO}/${JOB_NAME}:${TAG}"

  echo "Building ${IMAGE}..."
  docker build --platform linux/amd64 -t "${JOB_NAME}" -f "${DOCKERFILE}" .

  echo "Tagging..."
  docker tag "${JOB_NAME}" "${IMAGE}"

  echo "Pushing..."
  docker push "${IMAGE}"

  echo "Deploying to Cloud Run Jobs..."
  gcloud run jobs deploy "${JOB_NAME}" \
    --image="${IMAGE}" \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --network=tibia-vpc \
    --subnet=tibia-vpc \
    --vpc-egress=private-ranges-only
  echo "Done: ${IMAGE}"
done
