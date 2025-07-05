@echo off
REM Windows startup script for ComfyUI Log Debugger MCP Server
REM This script handles both python and python3 commands

setlocal enabledelayedexpansion

REM Get the directory of this script
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Set PYTHONPATH to include current and lib directories
set "PYTHONPATH=%SCRIPT_DIR%;%SCRIPT_DIR%\lib;%PYTHONPATH%"

REM Check if python3 is available
python3 --version >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_CMD=python3"
    goto :run_server
)

REM Check if python is available
python --version >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_CMD=python"
    goto :run_server
)

REM No Python found
echo Error: Python is not installed or not in PATH
echo Please install Python 3.6 or higher
exit /b 1

:run_server
echo Starting ComfyUI Log Debugger MCP Server with %PYTHON_CMD%...
%PYTHON_CMD% -u "%SCRIPT_DIR%\standalone_mcp_server.py" %*
exit /b !errorlevel!