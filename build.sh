#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="estudart-tibia-compass"
REGION="us-central1"
REPO="tibia-compass"

# macOS ships bash 3.2 (no associative arrays), so we use "name:dockerfile"
# entries in a plain indexed array instead of `declare -A`.
JOBS=(
  "killstatistics-job:src/jobs/killstatistics/Dockerfile"
  "creatures-job:src/jobs/creatures/Dockerfile"
)

dockerfile_for_job() {
  local job_name="$1"
  local entry
  for entry in "${JOBS[@]}"; do
    if [[ "${entry%%:*}" == "${job_name}" ]]; then
      echo "${entry#*:}"
      return 0
    fi
  done
  return 1
}

available_jobs() {
  local entry
  for entry in "${JOBS[@]}"; do
    printf '%s ' "${entry%%:*}"
  done
}

# Builds and pushes the image for a single job.
# Sets LAST_IMAGE to the pushed image ref so callers (e.g. deploy.sh) can use it.
build_and_push() {
  local job_name="$1"
  local dockerfile
  if ! dockerfile="$(dockerfile_for_job "${job_name}")"; then
    echo "Unknown job '${job_name}'. Available: $(available_jobs)"
    exit 1
  fi

  local tag="${TAG:-$(date +%s)}"
  local image="us-central1-docker.pkg.dev/${PROJECT_ID}/${REPO}/${job_name}:${tag}"

  echo "Building ${image}..."
  docker build --platform linux/amd64 -t "${job_name}" -f "${dockerfile}" .

  echo "Tagging..."
  docker tag "${job_name}" "${image}"

  echo "Pushing..."
  docker push "${image}"

  echo "Done: ${image}"
  LAST_IMAGE="${image}"
}

# Only run standalone when executed directly, e.g. `./build.sh creatures-job`.
# When sourced by deploy.sh, this just defines JOBS/build_and_push above.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  JOB_NAME="${1:?Usage: ./build.sh <job-name>  (available: $(available_jobs))}"
  build_and_push "${JOB_NAME}"
fi
