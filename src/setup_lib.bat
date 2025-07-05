@echo off
REM Setup script to install dependencies in server/lib for the extension on Windows

setlocal enabledelayedexpansion

REM Get the directory of this script
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Set the lib directory
set "LIB_DIR=%SCRIPT_DIR%\lib"

REM Set the parent directory
for %%A in ("%SCRIPT_DIR%\..") do set "PARENT_DIR=%%~fA"

REM Path to requirements.txt
set "REQ_FILE=%PARENT_DIR%\requirements.txt"

REM Create lib directory if it doesn't exist
if not exist "%LIB_DIR%" mkdir "%LIB_DIR%"

REM Check if requirements.txt exists
if not exist "%REQ_FILE%" (
    echo Error: requirements.txt not found at %REQ_FILE%
    exit /b 1
)

echo Installing dependencies to %LIB_DIR%...

REM Install dependencies to lib directory
python -m pip install -r "%REQ_FILE%" --target "%LIB_DIR%" --upgrade

if !errorlevel! neq 0 (
    echo Error installing dependencies
    exit /b 1
)

echo Dependencies installed successfully!
exit /b 0