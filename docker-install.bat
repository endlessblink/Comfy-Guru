@echo off
REM Docker installation for Windows

echo ============================================
echo ComfyUI Log Debugger - Docker Installation
echo ============================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running.
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo Docker is ready!
echo.

REM Build the image
echo Building Docker image...
docker build -t comfy-guru:latest .
if %errorlevel% neq 0 (
    echo ERROR: Failed to build Docker image
    pause
    exit /b 1
)

echo Docker image built successfully!
echo.

REM Test the container
echo Testing container...
docker run --rm -v D:\:/mnt/d:ro comfy-guru:latest python -c "print('Container works!')"
if %errorlevel% neq 0 (
    echo ERROR: Container test failed
    pause
    exit /b 1
)

REM Create MCP config
echo.
echo Creating MCP configuration...

set CONFIG_DIR=%APPDATA%\Claude
if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"
set CONFIG_FILE=%CONFIG_DIR%\claude.json

REM Copy config
copy /Y docker-mcp.json "%CONFIG_FILE%" >nul

echo Configuration saved to: %CONFIG_FILE%
echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Restart Claude Code
echo 2. The 'comfy-guru-docker' server will be available
echo 3. Your drives are mounted at /mnt/c and /mnt/d
echo.
echo To test manually:
echo   docker run -it --rm -v D:\:/mnt/d:ro comfy-guru:latest python test_installation.py
echo.
pause