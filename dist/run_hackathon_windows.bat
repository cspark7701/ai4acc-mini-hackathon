@echo off
title AI4ACC Mini-Hackathon 2026 - Launcher
color 0A

echo ======================================================================
echo      KOMAC / KAERI AI Accelerator Mini-Hackathon 2026
echo                Docker Environment Launcher
echo ======================================================================
echo.

:: 1. Check if Docker is installed and in PATH
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
echo [*] Launching container: cspark7701/ai4acc-hackathon-2026:latest ...
echo [*] Opening JupyterLab automatically in your default browser...
echo [*] If it does not open, visit: http://localhost:8888/lab
echo [*] Press Ctrl+C in this window when you wish to stop the environment.
echo ======================================================================
echo.

:: 3. Launch browser automatically in parallel after a 3-second delay
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8888/lab"

:: 4. Launch container
docker run -it --rm -p 8888:8888 cspark7701/ai4acc-hackathon-2026:latest

:: 5. Prevent window from closing abruptly on exit or failure
echo.
echo ======================================================================
echo Container stopped.
echo ======================================================================
pause
