@echo off
title AI4ACC Mini-Hackathon 2026 - Launcher
color 0A

echo ======================================================================
echo           AI Accelerator Mini-Hackathon 2026
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

:: 3. Load the bundled image when it is missing or differs from the installed one
::    (image-id.txt records the ID of the image in ai4acc-image.tar.gz)
set "INSTALLED_ID="
set "BUNDLED_ID="
for /f "delims=" %%i in ('docker image inspect --format "{{.Id}}" cspark7701/ai4acc-hackathon-2026:latest 2^>nul') do set "INSTALLED_ID=%%i"
if exist "%~dp0image-id.txt" set /p BUNDLED_ID=<"%~dp0image-id.txt"
set "NEED_LOAD=0"
if not defined INSTALLED_ID set "NEED_LOAD=1"
if defined BUNDLED_ID if not "%INSTALLED_ID%"=="%BUNDLED_ID%" set "NEED_LOAD=1"
if "%NEED_LOAD%"=="1" (
    if exist "%~dp0ai4acc-image.tar.gz" (
        echo [*] Loading the workshop Docker image from this folder...
        echo     (This takes about 30-45 seconds, please wait)
        docker load -i "%~dp0ai4acc-image.tar.gz"
        if errorlevel 1 (
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
:: Optional shared W&B leaderboard key: taken from the environment or from
:: wandb.apikey next to this script, and passed to the container by name so
:: the key itself never appears on the command line.
set "WANDB_ARGS="
if not defined WANDB_API_KEY if exist "%~dp0wandb.apikey" set /p WANDB_API_KEY=<"%~dp0wandb.apikey"
if defined WANDB_API_KEY (
    set "WANDB_ARGS=-e WANDB_API_KEY"
    echo [OK] W^&B leaderboard key loaded.
) else (
    echo [!] No W^&B key found: scores will be reported locally unless you run wandb.login^(^).
)
echo.

docker run -it --rm -p 8888:8888 %WANDB_ARGS% cspark7701/ai4acc-hackathon-2026:latest

echo.
echo ======================================================================
echo Container stopped.
echo ======================================================================
pause
