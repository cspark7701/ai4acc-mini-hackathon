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
echo -e "${BLUE}          AI Accelerator Mini-Hackathon 2026${NC}"
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

# 3. Load the bundled image when it is missing or differs from the installed one
#    (image-id.txt records the ID of the image in ai4acc-image.tar.gz)
INSTALLED_ID="$(docker image inspect --format '{{.Id}}' cspark7701/ai4acc-hackathon-2026:latest 2>/dev/null || true)"
BUNDLED_ID="$(cat "${SCRIPT_DIR}/image-id.txt" 2>/dev/null || true)"
if [ -f "${SCRIPT_DIR}/ai4acc-image.tar.gz" ] && { [ -z "${INSTALLED_ID}" ] || [ "${INSTALLED_ID}" != "${BUNDLED_ID}" ]; }; then
    echo -e "[*] Loading the workshop Docker image from this folder..."
    echo "    (This takes about 30-45 seconds, please wait)"
    docker load -i "${SCRIPT_DIR}/ai4acc-image.tar.gz"
    echo -e "${GREEN}[OK] Image successfully installed into Docker!${NC}"
    echo ""
elif [ -z "${INSTALLED_ID}" ]; then
    echo -e "[*] Pulling image from Docker Hub..."
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
# Optional shared W&B leaderboard key: taken from the environment or from
# wandb.apikey next to this script, and passed to the container by name so
# the key itself never appears on the command line.
WANDB_ARGS=()
if [ -z "${WANDB_API_KEY:-}" ] && [ -f "${SCRIPT_DIR}/wandb.apikey" ]; then
    WANDB_API_KEY="$(tr -d '[:space:]' < "${SCRIPT_DIR}/wandb.apikey")"
fi
if [ -n "${WANDB_API_KEY:-}" ]; then
    export WANDB_API_KEY
    WANDB_ARGS=(-e WANDB_API_KEY)
    echo -e "${GREEN}[OK] W&B leaderboard key loaded.${NC}"
else
    echo -e "${YELLOW}[!] No W&B key found: scores will be reported locally unless you run wandb.login().${NC}"
fi
echo ""

docker run -it --rm -p 8888:8888 ${WANDB_ARGS[@]+"${WANDB_ARGS[@]}"} cspark7701/ai4acc-hackathon-2026:latest

echo ""
echo -e "${BLUE}======================================================================${NC}"
echo "Container stopped."
echo -e "${BLUE}======================================================================${NC}"
