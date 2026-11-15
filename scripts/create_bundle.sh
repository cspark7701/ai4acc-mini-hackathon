#!/usr/bin/env bash
# ==============================================================================
# scripts/create_bundle.sh — Package Offline Distribution Bundle for Participants
# AI Applications in Accelerators Tutorial & Mini-Hackathon
# ==============================================================================
# Usage:
#   ./scripts/create_bundle.sh [--tag TAG] [--no-push] [--allow-dirty]
#
# Always builds a fresh image from the current repository, verifies it, writes the
# offline bundle, and then publishes the same commit to Docker Hub with
# docker_publish.sh, so the bundle and Docker Hub always carry the same image.
#
#   --tag TAG       Image tag (default: latest)
#   --no-push       Build the bundle only; do not publish to Docker Hub
#   --allow-dirty   Allow uncommitted changes (the bundle and image are then marked -dirty)
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

# 1. Resolve paths and options
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)/image_common.sh"
cd "${REPO_ROOT}"

TAG="latest"
PUSH=true
ALLOW_DIRTY=false
while [ "$#" -gt 0 ]; do
    case "$1" in
        --tag) TAG="$2"; shift 2 ;;
        --no-push) PUSH=false; shift ;;
        --allow-dirty) ALLOW_DIRTY=true; shift ;;
        -h|--help) sed -n '/^# Usage:/,/^# Generates:/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; exit 0 ;;
        -*) echo "❌ Unknown option: $1"; exit 1 ;;
        *) TAG="$1"; shift ;;   # positional tag, kept for backward compatibility
    esac
done
FULL_IMAGE="${DEFAULT_IMAGE_REPO}:${TAG}"
OUTPUT_DIR="${REPO_ROOT}/dist/ai4acc-hackathon"
ZIP_FILE="${REPO_ROOT}/dist/ai4acc-hackathon.zip"

echo "===================================================================="
echo "          AI Accelerator Mini-Hackathon 2026"
echo "   Offline Participant Bundle Creator"
echo "===================================================================="

# 2. Pre-flight: Docker, solution exclusion, git state
image_preflight
echo "Target Image : ${FULL_IMAGE}"
echo "Commit       : ${GIT_COMMIT}"
echo "Output Folder: ${OUTPUT_DIR}"
echo "Docker Hub   : $( [ "${PUSH}" = true ] && echo "publish this commit after bundling" || echo "not published (--no-push)" )"
echo ""
if [ "${GIT_DIRTY}" = true ] && [ "${ALLOW_DIRTY}" = false ]; then
    echo "❌ Error: the repository has uncommitted changes. Commit them first, or pass --allow-dirty."
    exit 1
fi

# 3. Always build a fresh image from the current repository and verify it
image_build "${FULL_IMAGE}"
image_verify "${FULL_IMAGE}"
IMAGE_ID="$(docker image inspect --format '{{.Id}}' "${FULL_IMAGE}")"
echo ""

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

# 10. Publish the same commit to Docker Hub so the bundle and Docker Hub match
if [ "${PUSH}" = true ]; then
    echo ""
    echo "[*] Publishing commit ${GIT_COMMIT} to Docker Hub ..."
    PUBLISH_ARGS=(--tag "${TAG}")
    [ "${ALLOW_DIRTY}" = true ] && PUBLISH_ARGS+=(--allow-dirty)
    "${REPO_ROOT}/scripts/docker_publish.sh" "${PUBLISH_ARGS[@]}"
else
    echo "[!] Docker Hub was not updated (--no-push). Run ./scripts/docker_publish.sh to publish this commit."
fi
