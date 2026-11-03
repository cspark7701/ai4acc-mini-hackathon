#!/usr/bin/env bash
# ==============================================================================
# scripts/docker_publish.sh — Build, Verify & Publish Hackathon Docker Image
# AI Applications in Accelerators Tutorial & Mini-Hackathon (KOMAC / KAERI)
# ==============================================================================
# Usage:
#   ./scripts/docker_publish.sh [DOCKERHUB_USERNAME] [TAG] [--multi-arch]
#
# Examples:
#   ./scripts/docker_publish.sh
#   ./scripts/docker_publish.sh kaeri-acc latest
#   ./scripts/docker_publish.sh kaeri-acc 2026.1 --multi-arch
# ==============================================================================

set -euo pipefail

# 1. Resolve repository root directory dynamically
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." >/dev/null 2>&1 && pwd)"
cd "${REPO_ROOT}"

# Show help if requested
if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
    echo "Usage: $0 [DOCKERHUB_USERNAME] [TAG] [--multi-arch]"
    echo ""
    echo "Arguments:"
    echo "  DOCKERHUB_USERNAME   Docker Hub username or organization (prompted if omitted)"
    echo "  TAG                  Image tag (default: latest)"
    echo "  --multi-arch         Build linux/amd64 and linux/arm64 multi-platform image via buildx"
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 kaeri-acc"
    echo "  $0 kaeri-acc latest"
    echo "  $0 kaeri-acc 2026.1 --multi-arch"
    exit 0
fi

IMAGE_NAME="ai4acc-hackathon-2026"

echo "===================================================================="
echo "   AI Applications in Accelerators Mini-Hackathon (KOMAC / KAERI)"
echo "   Docker Image Build & Hub Publication Tool"
echo "===================================================================="
echo "Repository Root: ${REPO_ROOT}"
echo ""

# 2. Pre-flight verification: Check Docker runtime
if ! command -v docker >/dev/null 2>&1; then
    echo "❌ Error: Docker is not installed or not available on PATH."
    echo "   Please install Docker Engine or Docker Desktop."
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo "❌ Error: Docker daemon is not running."
    echo "   Please start Docker Desktop or the Docker service (sudo systemctl start docker)."
    exit 1
fi

# 3. Resolve Docker Hub Username
USERNAME="${1:-${DOCKER_USERNAME:-}}"
while [ -z "${USERNAME}" ]; do
    read -rp "Enter Docker Hub username: " USERNAME
    USERNAME="$(echo "${USERNAME}" | tr -d '[:space:]')"
    if [ -z "${USERNAME}" ]; then
        echo "   Username cannot be empty. Please enter a valid Docker Hub username."
    fi
done

# 4. Resolve Image Tag
TAG="${2:-${DOCKER_TAG:-latest}}"
TARGET_IMAGE="${USERNAME}/${IMAGE_NAME}:${TAG}"
LOCAL_IMAGE="${IMAGE_NAME}:${TAG}"

# 5. Resolve Multi-Arch Flag
MULTI_ARCH=false
for arg in "$@"; do
    if [ "${arg}" = "--multi-arch" ]; then
        MULTI_ARCH=true
    fi
done

if [ "$#" -lt 3 ] && [ "${MULTI_ARCH}" = false ]; then
    echo ""
    echo "Select build mode:"
    echo "  1) Standard build (Single architecture: $(uname -m), fast)"
    echo "  2) Multi-architecture build (linux/amd64 + linux/arm64 for Intel/AMD & Apple Silicon)"
    read -rp "Choice [1/2, default: 1]: " BUILD_CHOICE
    if [ "${BUILD_CHOICE}" = "2" ]; then
        MULTI_ARCH=true
    fi
fi

echo ""
echo "--------------------------------------------------------------------"
echo "Target Image   : ${TARGET_IMAGE}"
echo "Local Alias    : ${LOCAL_IMAGE}"
echo "Architecture   : $( [ "${MULTI_ARCH}" = true ] && echo "linux/amd64,linux/arm64 (buildx)" || uname -m )"
echo "--------------------------------------------------------------------"
echo ""

# 6. Verify .dockerignore exists and excludes solution notebook
if [ ! -f "${REPO_ROOT}/.dockerignore" ] || ! grep -q "Solution" "${REPO_ROOT}/.dockerignore"; then
    echo "⚠️ Warning: .dockerignore does not contain a solution exclusion pattern."
    echo "   Aborting to prevent accidental leakage of reference solutions."
    exit 1
fi

# 7. Authenticate with Docker Hub
echo "🔑 Step 1: Docker Hub Authentication"
echo "   Logging in as '${USERNAME}'..."
docker login -u "${USERNAME}"
echo "   Authentication confirmed."
echo ""

# 8. Build Image
if [ "${MULTI_ARCH}" = true ]; then
    echo "🔨 Step 2: Multi-Architecture Build & Push via buildx (linux/amd64, linux/arm64)"
    
    # Ensure buildx builder exists and is active
    BUILDER_NAME="ai4acc-builder"
    if ! docker buildx inspect "${BUILDER_NAME}" >/dev/null 2>&1; then
        echo "   Creating dedicated buildx builder '${BUILDER_NAME}'..."
        docker buildx create --name "${BUILDER_NAME}" --use >/dev/null
    else
        docker buildx use "${BUILDER_NAME}" >/dev/null
    fi
    docker buildx inspect --bootstrap >/dev/null

    echo "   Compiling and pushing multi-platform image..."
    docker buildx build \
        --platform linux/amd64,linux/arm64 \
        -t "${TARGET_IMAGE}" \
        --push \
        .
    
    echo "   Multi-architecture manifest pushed successfully!"
else
    echo "🔨 Step 2: Building Local Image"
    # Build once with both local name and Hub namespace tag
    docker build \
        -t "${LOCAL_IMAGE}" \
        -t "${TARGET_IMAGE}" \
        .
    echo "   Local build complete: ${LOCAL_IMAGE} & ${TARGET_IMAGE}"
    echo ""

    # 9. Automated Sanity Inspection (Solution isolation check)
    echo "🔍 Step 3: Verifying Solution Isolation in Built Image"
    SOLUTION_FOUND="$(docker run --rm "${LOCAL_IMAGE}" find /workspace/notebooks -name "*Solution*" 2>/dev/null || true)"
    if [ -n "${SOLUTION_FOUND}" ]; then
        echo "❌ SECURITY ALERT: Reference solution file detected inside container image:"
        echo "   ${SOLUTION_FOUND}"
        echo "   Aborting push to Docker Hub to protect hackathon integrity!"
        exit 1
    fi

    NOTEBOOK_COUNT="$(docker run --rm "${LOCAL_IMAGE}" sh -c 'ls -1 /workspace/notebooks/*.ipynb 2>/dev/null | wc -l')"
    echo "   Verified: Solution notebook is absent from container."
    echo "   Participant notebook count in /workspace/notebooks: ${NOTEBOOK_COUNT}"
    echo ""

    # 10. Push to Docker Hub
    echo "🚀 Step 4: Pushing Image to Docker Hub"
    docker push "${TARGET_IMAGE}"
    echo "   Image successfully pushed to: ${TARGET_IMAGE}"
fi

echo ""
echo "===================================================================="
echo "   🎉 DOCKER IMAGE PUBLISHED SUCCESSFULLY!"
echo "===================================================================="
echo "Image Name: ${TARGET_IMAGE}"
echo ""
echo "Participants can now launch the official environment directly:"
echo ""
echo "  docker run -it --rm \\"
echo "    -p 8888:8888 \\"
echo "    -v \"\${PWD}/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb:/workspace/notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb\" \\"
echo "    -v \"\${PWD}/src:/workspace/src\" \\"
echo "    ${TARGET_IMAGE}"
echo ""
echo "===================================================================="
