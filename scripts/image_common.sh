#!/usr/bin/env bash
# ==============================================================================
# scripts/image_common.sh — shared helpers for create_bundle.sh and docker_publish.sh
# AI Applications in Accelerators Tutorial & Mini-Hackathon
# ==============================================================================
# Source this file; do not run it. It guarantees that both scripts work from a
# freshly built image of the current repository, never from an older local image.
#
#   image_preflight                 check Docker, .dockerignore and the git state
#   image_build <image:tag>         build the image from the repository (labelled with the commit)
#   image_verify <image:tag>        compare files inside the image with the repository
# ==============================================================================

IMAGE_COMMON_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
REPO_ROOT="$(cd "${IMAGE_COMMON_DIR}/.." >/dev/null 2>&1 && pwd)"
DEFAULT_IMAGE_REPO="cspark7701/ai4acc-hackathon-2026"
PARTICIPANT_NOTEBOOK="Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb"

# Files that must be identical in the repository and in the image: "<repo path>:<image path>".
# SRCDIR is replaced by the installed location of the src package inside the image.
IMAGE_CHECK_FILES=(
    "notebooks/${PARTICIPANT_NOTEBOOK}:/workspace/${PARTICIPANT_NOTEBOOK}"
    "src/benchmark.py:SRCDIR/benchmark.py"
    "src/environment.py:SRCDIR/environment.py"
    "src/controllers.py:SRCDIR/controllers.py"
    "presentations/Lecture_1_AI_ML_Foundations_and_Control_Slides.pdf:/workspace/Lecture_1_AI_ML_Foundations_and_Control_Slides.pdf"
    "presentations/Mini_Hackathon_Beam_Orbit_Alignment_Slides.pdf:/workspace/Mini_Hackathon_Beam_Orbit_Alignment_Slides.pdf"
    "lecture_notes/Lecture_1_AI_ML_Foundations_and_Control_Notes.pdf:/workspace/Lecture_1_AI_ML_Foundations_and_Control_Notes.pdf"
    "docs/pdf/PARTICIPANT_MODIFICATION_GUIDE.pdf:/workspace/PARTICIPANT_MODIFICATION_GUIDE.pdf"
    "docs/pdf/CALLBACK_EXAMPLES.pdf:/workspace/CALLBACK_EXAMPLES.pdf"
    "notebooks/Transfer_Matrix_Surrogate_Phase_Space.ipynb:/workspace/Transfer_Matrix_Surrogate_Phase_Space.ipynb"
    "img/beamline.png:/workspace/img/beamline.png"
)

# Set by image_preflight
GIT_COMMIT="unknown"
GIT_DIRTY=false

image_preflight() {
    if ! command -v docker >/dev/null 2>&1; then
        echo "❌ Error: Docker is not installed or not available on PATH."
        exit 1
    fi
    if ! docker info >/dev/null 2>&1; then
        echo "❌ Error: Docker daemon is not running."
        exit 1
    fi
    if [ ! -f "${REPO_ROOT}/.dockerignore" ] || ! grep -q "Solution" "${REPO_ROOT}/.dockerignore"; then
        echo "❌ Error: .dockerignore does not exclude the solution notebook. Aborting."
        exit 1
    fi
    GIT_COMMIT="$(git -C "${REPO_ROOT}" rev-parse --short HEAD 2>/dev/null || echo unknown)"
    if [ -n "$(git -C "${REPO_ROOT}" status --porcelain --untracked-files=no 2>/dev/null)" ]; then
        GIT_DIRTY=true
        GIT_COMMIT="${GIT_COMMIT}-dirty"
    fi
}

# image_build <image:tag> — always rebuild from the current repository.
# Unchanged layers come from the Docker cache, so this is quick when little changed.
image_build() {
    local image="$1"
    echo "[*] Building '${image}' from the current repository (commit ${GIT_COMMIT}) ..."
    docker build \
        --label "org.opencontainers.image.revision=${GIT_COMMIT}" \
        --label "org.opencontainers.image.created=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        -t "${image}" \
        "${REPO_ROOT}"
}

# image_verify <image:tag> — exit with an error unless the image matches the repository
# and contains no reference solution.
image_verify() {
    local image="$1" pair repo_path image_path want got src_dir solutions
    echo "[*] Verifying '${image}' against the repository ..."
    solutions="$(docker run --rm --entrypoint sh "${image}" -c 'find / -xdev -iname "*Solution*.ipynb" 2>/dev/null' || true)"
    if [ -n "${solutions}" ]; then
        echo "❌ Error: reference solution found inside the image:"
        echo "${solutions}"
        exit 1
    fi
    echo "    [OK] no solution notebook in the image"
    if docker run --rm --entrypoint sh "${image}" -c '[ -d /workspace/tmp ]'; then
        echo "❌ Error: /workspace/tmp found inside the image."
        exit 1
    fi
    echo "    [OK] no /workspace/tmp in the image"
    src_dir="$(docker run --rm --entrypoint python "${image}" -c 'import os, src.benchmark as b; print(os.path.dirname(b.__file__))')"
    for pair in "${IMAGE_CHECK_FILES[@]}"; do
        repo_path="${pair%%:*}"
        image_path="${pair#*:}"
        image_path="${image_path/SRCDIR/${src_dir}}"
        want="$(sha256sum "${REPO_ROOT}/${repo_path}" | cut -d' ' -f1)"
        got="$(docker run --rm --entrypoint sha256sum "${image}" "${image_path}" 2>/dev/null | cut -d' ' -f1 || true)"
        if [ "${want}" != "${got}" ]; then
            echo "❌ Error: ${image_path} in the image does not match ${repo_path} in the repository."
            exit 1
        fi
        echo "    [OK] ${repo_path}"
    done
    echo "[OK] Image $(docker image inspect --format '{{.Id}}' "${image}" | cut -c8-19) matches the repository (commit ${GIT_COMMIT})."
}
