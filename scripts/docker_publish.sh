#!/usr/bin/env bash
# ==============================================================================
# scripts/docker_publish.sh — Build, Verify & Publish Hackathon Docker Image
# AI Applications in Accelerators Tutorial & Mini-Hackathon (KOMAC / KAERI)
# ==============================================================================
# Usage:
#   ./scripts/docker_publish.sh [DOCKERHUB_USERNAME] [TAG] [--single-arch|--multi-arch]
#
# Defaults:
#   Tag          : latest
#   Architecture : Multi-arch (linux/amd64 + linux/arm64) by default
#
# Examples:
#   ./scripts/docker_publish.sh                     # Interactively prompts for username (multi-arch)
#   ./scripts/docker_publish.sh <username>          # <username>/ai4acc-hackathon-2026:latest (multi-arch)
#   ./scripts/docker_publish.sh <username> 2026.1   # Custom tag (multi-arch)
#   ./scripts/docker_publish.sh <username> latest --single-arch
# ==============================================================================

set -euo pipefail

# 1. Resolve repository root directory dynamically
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." >/dev/null 2>&1 && pwd)"
cd "${REPO_ROOT}"

# Show help if requested
if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
    echo "Usage: $0 [DOCKERHUB_USERNAME] [TAG] [--single-arch|--multi-arch]"
    echo ""
    echo "Defaults:"
    echo "  Tag          : latest"
    echo "  Architecture : Multi-architecture (linux/amd64 + linux/arm64) via buildx"
    echo ""
    echo "Options:"
    echo "  --multi-arch   Build for both linux/amd64 and linux/arm64 (Default)"
    echo "  --single-arch  Build only for local host architecture ($(uname -m))"
    echo ""
    echo "Examples:"
    echo "  $0                                   # Interactively prompts for username, builds multi-arch"
    echo "  $0 <username>                        # Publishes <username>/ai4acc-hackathon-2026:latest (multi-arch)"
    echo "  $0 <username> 2026.1                 # Custom tag with multi-arch"
    echo "  $0 <username> latest --single-arch   # Local host architecture only"
    exit 0
fi

IMAGE_NAME="ai4acc-hackathon-2026"
DEFAULT_TAG="latest"

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

# 3. Resolve Docker Hub Username (prompt until non-empty)
USERNAME=""
if [ -n "${1:-}" ] && [ "${1:-}" != "--single-arch" ] && [ "${1:-}" != "--multi-arch" ]; then
    USERNAME="$1"
elif [ -n "${DOCKER_USERNAME:-}" ]; then
    USERNAME="${DOCKER_USERNAME}"
fi

while [ -z "${USERNAME}" ]; do
    read -rp "Enter Docker Hub username: " USERNAME
    USERNAME="$(echo "${USERNAME}" | tr -d '[:space:]')"
    if [ -z "${USERNAME}" ]; then
        echo "   Username cannot be empty. Please enter your Docker Hub username."
    fi
done

# 4. Resolve Image Tag (default: latest)
if [ -n "${2:-}" ] && [ "${2:-}" != "--single-arch" ] && [ "${2:-}" != "--multi-arch" ]; then
    TAG="$2"
elif [ -n "${DOCKER_TAG:-}" ]; then
    TAG="${DOCKER_TAG}"
else
    read -rp "Enter image tag [default: ${DEFAULT_TAG}]: " INPUT_TAG
    TAG="${INPUT_TAG:-${DEFAULT_TAG}}"
fi
TAG="$(echo "${TAG}" | tr -d '[:space:]')"

TARGET_IMAGE="${USERNAME}/${IMAGE_NAME}:${TAG}"
LOCAL_IMAGE="${IMAGE_NAME}:${TAG}"

# 5. Resolve Architecture Mode (default: multi-arch)
MULTI_ARCH=true
for arg in "$@"; do
    if [ "${arg}" = "--single-arch" ]; then
        MULTI_ARCH=false
    elif [ "${arg}" = "--multi-arch" ]; then
        MULTI_ARCH=true
    fi
done

if [ "$#" -eq 0 ]; then
    read -rp "Build multi-architecture image (linux/amd64 + linux/arm64)? [Y/n, default: Y]: " ARCH_CHOICE
    ARCH_CHOICE="$(echo "${ARCH_CHOICE:-Y}" | tr '[:upper:]' '[:lower:]')"
    if [ "${ARCH_CHOICE}" = "n" ] || [ "${ARCH_CHOICE}" = "no" ]; then
        MULTI_ARCH=false
    fi
fi

echo ""
echo "--------------------------------------------------------------------"
echo "Target Image   : ${TARGET_IMAGE}"
echo "Local Alias    : ${LOCAL_IMAGE}"
echo "Architecture   : $( [ "${MULTI_ARCH}" = true ] && echo "linux/amd64,linux/arm64 (buildx multi-arch)" || echo "$(uname -m) (single-arch)" )"
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
echo "   Authenticating as '${USERNAME}'..."
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

    echo "   Compiling and pushing multi-platform image manifest to Docker Hub..."
    docker buildx build \
        --platform linux/amd64,linux/arm64 \
        -t "${TARGET_IMAGE}" \
        --push \
        .
    
    echo "   Multi-architecture image manifest published successfully!"
else
    echo "🔨 Step 2: Building Local Image ($(uname -m))"
    docker build \
        -t "${LOCAL_IMAGE}" \
        -t "${TARGET_IMAGE}" \
        .
    echo "   Local build complete: ${LOCAL_IMAGE} & ${TARGET_IMAGE}"
    echo ""

    # 9. Automated Sanity Inspection (Solution isolation & participant files check)
    echo "🔍 Step 3: Verifying Solution Isolation & Participant Assets in Built Image"
    SOLUTION_FOUND="$(docker run --rm "${LOCAL_IMAGE}" find /workspace/notebooks -name "*Solution*" 2>/dev/null || true)"
    if [ -n "${SOLUTION_FOUND}" ]; then
        echo "❌ SECURITY ALERT: Reference solution file detected inside container image:"
        echo "   ${SOLUTION_FOUND}"
        echo "   Aborting push to Docker Hub to protect hackathon integrity!"
        exit 1
    fi

    NOTEBOOK_COUNT="$(docker run --rm "${LOCAL_IMAGE}" sh -c 'ls -1 /workspace/notebooks/*.ipynb 2>/dev/null | wc -l')"
    DIST_COUNT="$(docker run --rm "${LOCAL_IMAGE}" sh -c 'ls -1 /workspace/dist/* 2>/dev/null | wc -l')"
    echo "   Verified: Solution notebook is absent from container."
    echo "   Participant notebook count in /workspace/notebooks: ${NOTEBOOK_COUNT}"
    echo "   Launcher scripts count in /workspace/dist: ${DIST_COUNT}"
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
echo "  docker run -it --rm -p 8888:8888 ${TARGET_IMAGE}"
echo ""
echo "===================================================================="
