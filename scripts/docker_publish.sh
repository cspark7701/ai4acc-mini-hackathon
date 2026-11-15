#!/usr/bin/env bash
# ==============================================================================
# scripts/docker_publish.sh — Build, Verify & Publish the Hackathon Docker Image
# AI Applications in Accelerators Tutorial & Mini-Hackathon
# ==============================================================================
# Always builds a fresh image from the current repository, verifies its contents,
# pushes it to Docker Hub, and then checks that Docker Hub carries that commit.
#
# Usage:
#   ./scripts/docker_publish.sh [options]
#
# Options:
#   --user NAME       Docker Hub namespace (default: cspark7701, or $DOCKER_USERNAME)
#   --tag TAG         Image tag (default: latest, or $DOCKER_TAG)
#   --single-arch     Push only the local architecture ($(uname -m))
#   --multi-arch      Push linux/amd64 + linux/arm64 via buildx (default)
#   --allow-dirty     Allow publishing with uncommitted changes (refused by default)
#   --dry-run         Build and verify only; do not log in or push
#   -h, --help        Show this help
#
# Examples:
#   ./scripts/docker_publish.sh                        # cspark7701/ai4acc-hackathon-2026:latest, multi-arch
#   ./scripts/docker_publish.sh --tag 2026.1
#   ./scripts/docker_publish.sh --single-arch --dry-run
# ==============================================================================

set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)/image_common.sh"
cd "${REPO_ROOT}"

USERNAME="${DOCKER_USERNAME:-${DEFAULT_IMAGE_REPO%%/*}}"
TAG="${DOCKER_TAG:-latest}"
MULTI_ARCH=true
ALLOW_DIRTY=false
DRY_RUN=false

usage() { sed -n '/^# Usage:/,/^# =====/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; }

while [ "$#" -gt 0 ]; do
    case "$1" in
        --user) USERNAME="$2"; shift 2 ;;
        --tag) TAG="$2"; shift 2 ;;
        --single-arch) MULTI_ARCH=false; shift ;;
        --multi-arch) MULTI_ARCH=true; shift ;;
        --allow-dirty) ALLOW_DIRTY=true; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "❌ Unknown option: $1"; usage; exit 1 ;;
    esac
done

TARGET_IMAGE="${USERNAME}/${DEFAULT_IMAGE_REPO#*/}:${TAG}"

echo "===================================================================="
echo "   AI Applications in Accelerators Mini-Hackathon"
echo "   Docker Image Build & Docker Hub Publication"
echo "===================================================================="

# 1. Pre-flight: Docker, solution exclusion, git state
image_preflight
echo "Target Image : ${TARGET_IMAGE}"
echo "Commit       : ${GIT_COMMIT}"
echo "Architecture : $( [ "${MULTI_ARCH}" = true ] && echo "linux/amd64 + linux/arm64 (buildx)" || echo "$(uname -m) only" )"
echo "Mode         : $( [ "${DRY_RUN}" = true ] && echo "dry run (build and verify only)" || echo "build, verify and push" )"
echo ""
if [ "${GIT_DIRTY}" = true ] && [ "${ALLOW_DIRTY}" = false ] && [ "${DRY_RUN}" = false ]; then
    echo "❌ Error: the repository has uncommitted changes. Commit them first, or pass --allow-dirty."
    exit 1
fi

# 2. Build a fresh local image and verify it (this also refreshes the local image used by bundles)
image_build "${TARGET_IMAGE}"
image_verify "${TARGET_IMAGE}"
echo ""

if [ "${DRY_RUN}" = true ]; then
    echo "[OK] Dry run complete: '${TARGET_IMAGE}' was built and verified locally; nothing was pushed."
    exit 0
fi

# 3. Authenticate with Docker Hub (reuses stored credentials when present)
echo "🔑 Logging in to Docker Hub as '${USERNAME}' ..."
docker login -u "${USERNAME}"
echo ""

# 4. Push
if [ "${MULTI_ARCH}" = true ]; then
    echo "🚀 Building and pushing linux/amd64 + linux/arm64 via buildx ..."
    BUILDER_NAME="ai4acc-builder"
    if ! docker buildx inspect "${BUILDER_NAME}" >/dev/null 2>&1; then
        docker buildx create --name "${BUILDER_NAME}" >/dev/null
    fi
    docker buildx build \
        --builder "${BUILDER_NAME}" \
        --platform linux/amd64,linux/arm64 \
        --label "org.opencontainers.image.revision=${GIT_COMMIT}" \
        --label "org.opencontainers.image.created=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        -t "${TARGET_IMAGE}" \
        --push \
        "${REPO_ROOT}"
else
    echo "🚀 Pushing ${TARGET_IMAGE} ..."
    docker push "${TARGET_IMAGE}"
fi
echo ""

# 5. Confirm that every architecture on Docker Hub carries this commit
echo "[*] Checking the published image on Docker Hub ..."
REMOTE_COMMITS="$(docker buildx imagetools inspect "${TARGET_IMAGE}" --format '{{json .Image}}' | python3 -c '
import json, sys
data = json.load(sys.stdin)
images = data if "config" not in data else {"single": data}
for platform, img in images.items():
    labels = (img.get("config") or {}).get("Labels") or {}
    print(platform, labels.get("org.opencontainers.image.revision", "none"))
')"
echo "${REMOTE_COMMITS}" | sed 's/^/    /'
if echo "${REMOTE_COMMITS}" | awk -v c="${GIT_COMMIT}" '$2 != c {bad=1} END {exit !bad}'; then
    echo "❌ Error: Docker Hub does not carry commit ${GIT_COMMIT} for every architecture."
    exit 1
fi

echo ""
echo "===================================================================="
echo "   🎉 Published ${TARGET_IMAGE} (commit ${GIT_COMMIT})"
echo "===================================================================="
echo "Participants can launch it with:"
echo "  docker run -it --rm -p 127.0.0.1:8888:8888 ${TARGET_IMAGE}"
echo "===================================================================="
