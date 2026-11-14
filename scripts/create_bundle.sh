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
#     ├── ai4acc-image.tar.gz      (Compressed Docker image)
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

# 3. Check if local image exists; if not, build it
if ! docker image inspect "${FULL_IMAGE}" >/dev/null 2>&1; then
    echo "[*] Image '${FULL_IMAGE}' not found locally. Building image..."
    docker build -t "${FULL_IMAGE}" .
else
    echo "[OK] Found local image '${FULL_IMAGE}'."
fi

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
   - The first run will automatically load the image and open JupyterLab in your browser.

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
