@echo off
echo === MCP Server Debug Tool for Windows ===
echo.

REM Check Python installation
echo Checking Python installation...
python --version 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.9+ and add it to PATH
    pause
    exit /b 1
)

echo.
echo Python location:
where python

echo.
echo Testing MCP server directly...
echo Press Ctrl+C to stop the test
echo.

cd /d "%APPDATA%\Claude\Claude Extensions\local.dxt.endlessblink.comfy-guru\server"
if %errorlevel% neq 0 (
    echo ERROR: Extension directory not found
    echo Please install the extension first
    pause
    exit /b 1
)

echo Current directory: %CD%
echo.
echo Starting minimal test server...
python -u minimal_test_server.py

pause