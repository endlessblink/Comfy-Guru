@echo off
setlocal enabledelayedexpansion

REM Windows launcher for MCP server with extensive debugging
echo [DEBUG] Starting Windows MCP launcher... >> mcp_debug.log 2>&1
echo [DEBUG] Time: %date% %time% >> mcp_debug.log 2>&1
echo [DEBUG] Current directory: %CD% >> mcp_debug.log 2>&1

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
echo [DEBUG] Script directory: %SCRIPT_DIR% >> mcp_debug.log 2>&1

REM Change to script directory
cd /d "%SCRIPT_DIR%"
echo [DEBUG] Changed to: %CD% >> mcp_debug.log 2>&1

REM Find Python - try multiple locations
set "PYTHON_EXE="

REM Try python from PATH first
where python >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=*" %%i in ('where python') do (
        set "PYTHON_EXE=%%i"
        goto :found_python
    )
)

REM Try common Python locations
for %%p in (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "C:\Python39\python.exe"
    "%ProgramFiles%\Python312\python.exe"
    "%ProgramFiles%\Python311\python.exe"
    "%ProgramFiles%\Python310\python.exe"
    "%ProgramFiles%\Python39\python.exe"
    "%ProgramFiles(x86)%\Python312\python.exe"
    "%ProgramFiles(x86)%\Python311\python.exe"
    "%ProgramFiles(x86)%\Python310\python.exe"
    "%ProgramFiles(x86)%\Python39\python.exe"
) do (
    if exist %%p (
        set "PYTHON_EXE=%%~p"
        goto :found_python
    )
)

REM Try python3
where python3 >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=*" %%i in ('where python3') do (
        set "PYTHON_EXE=%%i"
        goto :found_python
    )
)

:found_python
if not defined PYTHON_EXE (
    echo [ERROR] Python not found! >> mcp_debug.log 2>&1
    echo Error: Python is not installed or not in PATH >&2
    exit /b 1
)

echo [DEBUG] Found Python: %PYTHON_EXE% >> mcp_debug.log 2>&1

REM Get Python version
"%PYTHON_EXE%" --version >> mcp_debug.log 2>&1

REM Set environment
set "PYTHONUNBUFFERED=1"
set "PYTHONIOENCODING=utf-8"
set "PYTHONPATH=%SCRIPT_DIR%;%SCRIPT_DIR%\lib"

echo [DEBUG] PYTHONPATH: %PYTHONPATH% >> mcp_debug.log 2>&1

REM Check if lib directory exists
if not exist "%SCRIPT_DIR%\lib" (
    echo [DEBUG] Creating lib directory... >> mcp_debug.log 2>&1
    mkdir "%SCRIPT_DIR%\lib"
)

REM Check if dependencies are installed
if not exist "%SCRIPT_DIR%\lib\fastmcp" (
    echo [DEBUG] Installing dependencies... >> mcp_debug.log 2>&1
    echo Installing dependencies... >&2
    
    "%PYTHON_EXE%" -m pip install --target "%SCRIPT_DIR%\lib" fastmcp python-dotenv aiofiles psutil --quiet --disable-pip-version-check >> mcp_debug.log 2>&1
    
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install dependencies >> mcp_debug.log 2>&1
        echo Error: Failed to install dependencies >&2
        exit /b 1
    )
    
    echo [DEBUG] Dependencies installed successfully >> mcp_debug.log 2>&1
)

REM Run the server
echo [DEBUG] Starting MCP server... >> mcp_debug.log 2>&1
echo Starting MCP server... >&2

"%PYTHON_EXE%" -u "%SCRIPT_DIR%\standalone_mcp_server.py" 2>> mcp_debug.log

set "EXIT_CODE=!errorlevel!"
echo [DEBUG] Server exited with code: !EXIT_CODE! >> mcp_debug.log 2>&1

exit /b !EXIT_CODE!