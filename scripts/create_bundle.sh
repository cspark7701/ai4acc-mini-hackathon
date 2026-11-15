#!/usr/bin/env bash
# ==============================================================================
# scripts/create_bundle.sh — Package Offline Distribution Bundle for Participants
# AI Applications in Accelerators Tutorial & Mini-Hackathon
# ==============================================================================
# Usage:
#   ./scripts/create_bundle.sh [IMAGE_TAG]
#
# Generates:
#   dist/ai4acc-hackathon/
#     ├── ai4acc-image.tar.gz      (Compressed Docker image, rebuilt from the current repository)
#     ├── image-id.txt             (ID of that image; the launchers load it when it differs)
#     ├── BUILD_INFO.txt           (Image ID, git commit and build date)
#     ├── run_hackathon_windows.bat          (Double-click launcher for Windows)
#     ├── run_hackathon_mac_linux.sh         (Launcher for macOS & Linux)
#     ├── wandb.apikey            (Shared W&B leaderboard key, if dist/wandb.apikey exists)
#     └── README.txt               (Quick offline instructions)
#   dist/ai4acc-hackathon.zip      (Compressed distribution archive)
# ==============================================================================

set -euo pipefail

# 1. Resolve directory paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." >/dev/null 2>&1 && pwd)"
cd "${REPO_ROOT}"

IMAGE_NAME="cspark7701/ai4acc-hackathon-2026"
TAG="${1:-latest}"
FULL_IMAGE="${IMAGE_NAME}:${TAG}"
OUTPUT_DIR="${REPO_ROOT}/dist/ai4acc-hackathon"
ZIP_FILE="${REPO_ROOT}/dist/ai4acc-hackathon.zip"

echo "===================================================================="
echo "          AI Accelerator Mini-Hackathon 2026"
echo "   Offline Participant Bundle Creator"
echo "===================================================================="
echo "Target Image : ${FULL_IMAGE}"
echo "Output Folder: ${OUTPUT_DIR}"
echo ""

# 2. Check Docker availability
if ! command -v docker >/dev/null 2>&1; then
    echo "❌ Error: Docker is not installed or not available in PATH."
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo "❌ Error: Docker daemon is not running."
    exit 1
fi

# 3. Always build the image from the current repository, so the bundle never ships
#    an older local image. Unchanged layers come from the Docker cache.
GIT_COMMIT="$(git -C "${REPO_ROOT}" rev-parse --short HEAD 2>/dev/null || echo unknown)"
if [ -n "$(git -C "${REPO_ROOT}" status --porcelain --untracked-files=no 2>/dev/null)" ]; then
    echo "[!] Warning: the repository has uncommitted changes; they will be included in the image."
    GIT_COMMIT="${GIT_COMMIT}-dirty"
fi
echo "[*] Building image '${FULL_IMAGE}' from the current repository (commit ${GIT_COMMIT}) ..."
docker build --label "org.opencontainers.image.revision=${GIT_COMMIT}" -t "${FULL_IMAGE}" .

# 3b. Verify that the image contains the current participant notebook, benchmark code and slides
echo "[*] Verifying image contents against the repository ..."
verify() {  # verify <repo file> <path inside image>
    local want got
    want="$(sha256sum "${REPO_ROOT}/$1" | cut -d' ' -f1)"
    got="$(docker run --rm --entrypoint sha256sum "${FULL_IMAGE}" "$2" 2>/dev/null | cut -d' ' -f1)"
    if [ "${want}" != "${got}" ]; then
        echo "❌ Error: $2 in the image does not match $1 in the repository."
        exit 1
    fi
    echo "    [OK] $1"
}
SRC_DIR="$(docker run --rm --entrypoint python "${FULL_IMAGE}" -c 'import os, src.benchmark as b; print(os.path.dirname(b.__file__))')"
verify notebooks/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb /workspace/Single_Notebook_Beam_Orbit_Predictor_Participant.ipynb
verify src/benchmark.py "${SRC_DIR}/benchmark.py"
verify src/environment.py "${SRC_DIR}/environment.py"
verify presentations/Lecture_1_AI_ML_Foundations_and_Control.pdf /workspace/Lecture_1_AI_ML_Foundations_and_Control.pdf
verify lecture_notes/Lecture_1_AI_ML_Techniques_for_Accelerators.pdf /workspace/Lecture_1_AI_ML_Techniques_for_Accelerators.pdf
IMAGE_ID="$(docker image inspect --format '{{.Id}}' "${FULL_IMAGE}")"
echo "[OK] Image ${IMAGE_ID:7:12} matches the repository."

# 4. Prepare distribution directory
echo "[*] Setting up bundle directory: ${OUTPUT_DIR} ..."
rm -rf "${OUTPUT_DIR}"
mkdir -p "${OUTPUT_DIR}"

# 5. Export and compress Docker image
IMAGE_TAR_GZ="${OUTPUT_DIR}/ai4acc-image.tar.gz"
echo "[*] Exporting and compressing Docker image to ${IMAGE_TAR_GZ} ..."
echo "    (This may take 1–2 minutes; please wait)"

if command -v pigz >/dev/null 2>&1; then
    # Use multi-threaded pigz for fast compression if available
    docker save "${FULL_IMAGE}" | pigz > "${IMAGE_TAR_GZ}"
else
    docker save "${FULL_IMAGE}" | gzip > "${IMAGE_TAR_GZ}"
fi

FILE_SIZE=$(du -h "${IMAGE_TAR_GZ}" | cut -f1)
echo "[OK] Docker image exported successfully! Compressed size: ${FILE_SIZE}"

# Record the image ID so the launchers can tell whether the installed image is this one,
# plus build information for the organizer.
echo "${IMAGE_ID}" > "${OUTPUT_DIR}/image-id.txt"
cat > "${OUTPUT_DIR}/BUILD_INFO.txt" << EOF
Image:   ${FULL_IMAGE}
ImageID: ${IMAGE_ID}
Commit:  ${GIT_COMMIT}
Built:   $(date '+%Y-%m-%d %H:%M %Z')
EOF
echo ""

# 6-7. Copy the tracked launchers (single source of truth: dist/run_hackathon_*)
LAUNCHER_WIN="${REPO_ROOT}/dist/run_hackathon_windows.bat"
LAUNCHER_UNIX="${REPO_ROOT}/dist/run_hackathon_mac_linux.sh"
for launcher in "${LAUNCHER_WIN}" "${LAUNCHER_UNIX}"; do
    if [ ! -f "${launcher}" ]; then
        echo "❌ Error: Launcher not found: ${launcher}"
        exit 1
    fi
done
cp "${LAUNCHER_WIN}" "${OUTPUT_DIR}/run_hackathon_windows.bat"
cp "${LAUNCHER_UNIX}" "${OUTPUT_DIR}/run_hackathon_mac_linux.sh"
chmod +x "${OUTPUT_DIR}/run_hackathon_mac_linux.sh"

# Include the shared W&B leaderboard key if the organizer has placed it in dist/.
# The key file is git-ignored and must never be committed or baked into the image.
WANDB_KEY_FILE="${REPO_ROOT}/dist/wandb.apikey"
if [ -f "${WANDB_KEY_FILE}" ]; then
    cp "${WANDB_KEY_FILE}" "${OUTPUT_DIR}/wandb.apikey"
    echo "[OK] Included shared W&B leaderboard key (wandb.apikey)."
else
    echo "[!] dist/wandb.apikey not found: bundle will not submit to the leaderboard automatically."
fi

# 8. Generate README.txt
cat << 'EOF' > "${OUTPUT_DIR}/README.txt"
================================================================================
AI Applications in Accelerators Tutorial & Mini-Hackathon
Offline Participant Package
================================================================================

HOW TO RUN:

1. Windows:
   - Make sure Docker Desktop is running (whale icon in system tray).
   - Double-click 'run_hackathon_windows.bat'.
   - The launcher loads the bundled image when it is newer than the one installed,
     then opens JupyterLab in your browser.

2. macOS / Linux:
   - Make sure Docker Desktop or Docker Engine is running.
   - Open terminal in this folder and run:
       ./run_hackathon_mac_linux.sh
   - JupyterLab will launch and open automatically at: http://localhost:8888/lab

NOTES:
- Works 100% offline without Wi-Fi or internet connection.
- Keep wandb.apikey in the same folder as the launcher. It lets your runs reach
  the leaderboard; do not share it outside the workshop.
- When connected to Wi-Fi, benchmark runs will automatically sync live scores to
  the Weights & Biases (W&B) competition leaderboard.
- To shut down, press Ctrl+C in the command prompt / terminal window.
================================================================================
EOF

# 9. Create Zip Archive for easy distribution
echo "[*] Creating zip archive: ${ZIP_FILE} ..."
rm -f "${ZIP_FILE}"
(cd "${REPO_ROOT}/dist" && zip -r -q "ai4acc-hackathon.zip" "ai4acc-hackathon")
ZIP_SIZE=$(du -h "${ZIP_FILE}" | cut -f1)

echo ""
echo "===================================================================="
echo "   🎉 OFFLINE BUNDLE CREATED SUCCESSFULLY!"
echo "===================================================================="
echo "Folder : ${OUTPUT_DIR}"
echo "Archive: ${ZIP_FILE} (${ZIP_SIZE})"
echo ""
echo "Files included:"
ls -lh "${OUTPUT_DIR}"
echo "===================================================================="
