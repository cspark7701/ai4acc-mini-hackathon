#!/usr/bin/env bash
# ==============================================================================
# scripts/create_bundle.sh — Package Offline Distribution Bundle for Participants
# AI Applications in Accelerators Tutorial & Mini-Hackathon (KOMAC / KAERI)
# ==============================================================================
# Usage:
#   ./scripts/create_bundle.sh [IMAGE_TAG]
#
# Generates:
#   dist/ai4acc-hackathon/
#     ├── ai4acc-image.tar.gz      (Compressed Docker image)
#     ├── run_windows.bat          (Double-click launcher for Windows)
#     ├── run_mac_linux.sh         (Launcher for macOS & Linux)
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
echo "   KOMAC / KAERI AI Accelerator Mini-Hackathon 2026"
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

# 6. Generate run_windows.bat
cat << 'EOF' > "${OUTPUT_DIR}/run_windows.bat"
@echo off
title AI4ACC Mini-Hackathon 2026 - Launcher
color 0A

echo ======================================================================
echo      KOMAC / KAERI AI Accelerator Mini-Hackathon 2026
echo                Docker Environment Launcher
echo ======================================================================
echo.

:: 1. Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    color 0C
    echo [ERROR] Docker was not found on your system.
    echo Please make sure Docker Desktop is installed:
    echo   https://www.docker.com/products/docker-desktop/
    echo.
    echo If you just installed Docker, try restarting your terminal or PC.
    echo.
    pause
    exit /b 1
)

:: 2. Check if Docker daemon is running
echo [*] Checking Docker daemon status...
docker info >nul 2>nul
if %ERRORLEVEL% neq 0 (
    color 0C
    echo [ERROR] Docker Desktop is installed, but the Docker engine is not running!
    echo.
    echo Please:
    echo   1. Open 'Docker Desktop' from your Start Menu or taskbar.
    echo   2. Wait until the whale icon stops animating and shows 'Engine running'.
    echo   3. Run this script again.
    echo.
    pause
    exit /b 1
)

echo [OK] Docker daemon is running.
echo.

:: 3. Check if image is loaded; if not, load from offline archive
docker image inspect cspark7701/ai4acc-hackathon-2026:latest >nul 2>nul
if %ERRORLEVEL% neq 0 (
    if exist "%~dp0ai4acc-image.tar.gz" (
        echo [*] First-time setup: Loading offline Docker image...
        echo     (This takes about 30-45 seconds, please wait)
        docker load -i "%~dp0ai4acc-image.tar.gz"
        if %ERRORLEVEL% neq 0 (
            color 0C
            echo [ERROR] Failed to load ai4acc-image.tar.gz!
            pause
            exit /b 1
        )
        echo [OK] Image successfully installed into Docker!
        echo.
    ) else (
        echo [*] Downloading image from Docker Hub: cspark7701/ai4acc-hackathon-2026:latest ...
    )
)

echo [*] Launching container: cspark7701/ai4acc-hackathon-2026:latest ...
echo [*] Opening JupyterLab automatically in your default browser...
echo [*] If it does not open, visit: http://localhost:8888/lab
echo [*] Press Ctrl+C in this window when you wish to stop the environment.
echo ======================================================================
echo.

:: 4. Launch browser automatically in parallel after 3 seconds
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8888/lab"

:: 5. Launch container
docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest

echo.
echo ======================================================================
echo Container stopped.
echo ======================================================================
pause
EOF

# 7. Generate run_mac_linux.sh
cat << 'EOF' > "${OUTPUT_DIR}/run_mac_linux.sh"
#!/usr/bin/env bash
# ==============================================================================
# AI4ACC Mini-Hackathon 2026 - Launcher for macOS & Linux
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# Terminal color helpers
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}     KOMAC / KAERI AI Accelerator Mini-Hackathon 2026${NC}"
echo -e "${BLUE}               Docker Environment Launcher${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo ""

# 1. Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}[ERROR] Docker command was not found.${NC}"
    echo "Please install Docker Desktop (or Docker Engine on Linux):"
    echo "  https://www.docker.com/products/docker-desktop/"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# 2. Check if Docker daemon is running
echo -e "[*] Checking Docker daemon status..."
if ! docker info &> /dev/null; then
    echo -e "${RED}[ERROR] Docker daemon is not running!${NC}"
    echo ""
    echo "Please:"
    echo "  1. Start Docker Desktop (or run: sudo systemctl start docker on Linux)."
    echo "  2. Wait until the Docker engine is running."
    echo "  3. Re-run this script."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo -e "${GREEN}[OK] Docker daemon is running.${NC}"
echo ""

# 3. Check if image is loaded; if not, load from offline archive
if ! docker image inspect cspark7701/ai4acc-hackathon-2026:latest &> /dev/null; then
    if [ -f "${SCRIPT_DIR}/ai4acc-image.tar.gz" ]; then
        echo -e "[*] First-time setup: Loading offline Docker image..."
        echo "    (This takes about 30-45 seconds, please wait)"
        docker load -i "${SCRIPT_DIR}/ai4acc-image.tar.gz"
        echo -e "${GREEN}[OK] Image successfully installed into Docker!${NC}"
        echo ""
    else
        echo -e "[*] Pulling image from Docker Hub..."
    fi
fi

echo -e "[*] Launching container: ${YELLOW}cspark7701/ai4acc-hackathon-2026:latest${NC} ..."
echo -e "[*] Opening JupyterLab automatically in your default browser..."
echo -e "[*] If it does not open, visit: ${GREEN}http://localhost:8888/lab${NC}"
echo -e "[*] Press ${YELLOW}Ctrl+C${NC} in this terminal when you wish to stop the environment."
echo -e "${BLUE}======================================================================${NC}"
echo ""

# 4. Open browser in background after delay (macOS: open, Linux: xdg-open)
(
    sleep 3
    if command -v open &> /dev/null; then
        open "http://localhost:8888/lab"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:8888/lab" &> /dev/null
    fi
) &

# 5. Launch container
docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest

echo ""
echo -e "${BLUE}======================================================================${NC}"
echo "Container stopped."
echo -e "${BLUE}======================================================================${NC}"
EOF
chmod +x "${OUTPUT_DIR}/run_mac_linux.sh"

# 8. Generate README.txt
cat << 'EOF' > "${OUTPUT_DIR}/README.txt"
================================================================================
AI Applications in Accelerators Tutorial & Mini-Hackathon (KOMAC / KAERI)
Offline Participant Package
================================================================================

HOW TO RUN:

1. Windows:
   - Make sure Docker Desktop is running (whale icon in system tray).
   - Double-click 'run_windows.bat'.
   - The first run will automatically load the image and open JupyterLab in your browser.

2. macOS / Linux:
   - Make sure Docker Desktop or Docker Engine is running.
   - Open terminal in this folder and run:
       ./run_mac_linux.sh
   - JupyterLab will launch and open automatically at: http://localhost:8888/lab

NOTES:
- Works 100% offline without Wi-Fi or internet connection.
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
