#!/usr/bin/env bash
# ==============================================================================
# AI4ACC Mini-Hackathon 2026 - Launcher for macOS & Linux
# ==============================================================================

set -e

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
echo -e "[*] Launching container: ${YELLOW}cspark7701/ai4acc-hackathon-2026:latest${NC} ..."
echo -e "[*] Opening JupyterLab automatically in your default browser..."
echo -e "[*] If it does not open, visit: ${GREEN}http://localhost:8888/lab${NC}"
echo -e "[*] Press ${YELLOW}Ctrl+C${NC} in this terminal when you wish to stop the environment."
echo -e "${BLUE}======================================================================${NC}"
echo ""

# 3. Open browser in background after delay (macOS: open, Linux: xdg-open)
(
    sleep 3
    if command -v open &> /dev/null; then
        open "http://localhost:8888/lab"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:8888/lab" &> /dev/null
    fi
) &

# 4. Launch container
docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest

echo ""
echo -e "${BLUE}======================================================================${NC}"
echo "Container stopped."
echo -e "${BLUE}======================================================================${NC}"
