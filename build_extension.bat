@echo off
echo ComfyUI Log Debugger - Desktop Extension Builder
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Run the build script
python build_extension.py

if errorlevel 1 (
    echo.
    echo Build failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Press any key to exit...
pause >nul