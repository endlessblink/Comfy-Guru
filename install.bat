@echo off
setlocal enabledelayedexpansion

echo ComfyUI Log Debugger - Easy Installer for Claude Desktop
echo ========================================================
echo.

REM Get script directory and change to it
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"
echo Working directory: %CD%
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Show Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo.

REM Check if we're in a virtual environment already
if defined VIRTUAL_ENV (
    echo Using existing virtual environment: %VIRTUAL_ENV%
) else (
    REM Check if venv exists
    if exist "venv\Scripts\python.exe" (
        echo Activating virtual environment...
        call venv\Scripts\activate.bat
    ) else (
        echo Creating virtual environment...
        python -m venv venv
        if errorlevel 1 (
            echo ERROR: Failed to create virtual environment
            pause
            exit /b 1
        )
        echo Activating virtual environment...
        call venv\Scripts\activate.bat
    )
)
echo.

REM Install/upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

REM Install requirements if they exist
if exist "requirements.txt" (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Please check your internet connection and try again
        pause
        exit /b 1
    )
)
echo.

REM Run the installer
echo Running installer...
python install.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo Installation failed!
    echo ========================================
    echo.
    echo Troubleshooting tips:
    echo 1. Try running as Administrator
    echo 2. Check your Python version (3.8+ required)
    echo 3. Ensure you have internet connectivity
    echo 4. Check the error messages above
    echo.
    echo For more help, visit:
    echo https://github.com/Shiba-2-shiba/comfy-guru
    pause
    exit /b 1
)

echo.
echo ============================================
echo Installation complete!
echo ============================================
echo.
echo Next steps:
echo 1. Restart Claude Desktop completely
echo 2. Try asking: "Find my ComfyUI logs"
echo.
echo Virtual environment created in: %CD%\venv
echo.
pause