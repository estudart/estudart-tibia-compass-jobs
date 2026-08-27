#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/build.sh"

for entry in "${JOBS[@]}"; do
  JOB_NAME="${entry%%:*}"
  build_and_push "${JOB_NAME}"

  echo "Deploying to Cloud Run Jobs..."
  gcloud run jobs deploy "${JOB_NAME}" \
    --image="${LAST_IMAGE}" \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --network=tibia-vpc \
    --subnet=tibia-vpc \
    --vpc-egress=private-ranges-only
  echo "Done: ${LAST_IMAGE}"
done
