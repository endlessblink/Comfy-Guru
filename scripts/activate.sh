#!/bin/bash

# This script starts the MCP server when the conda environment is activated.

# Navigate to the comfyui-log-debugger directory
# Adjust this path if your project structure changes
PROJECT_DIR="/mnt/d/APPSNospaces/comfy-guru"

# Setup conda environment for Windows miniconda
WINDOWS_CONDA="/mnt/c/pinokio/bin/miniconda"
CONDA_EXE="$WINDOWS_CONDA/Scripts/conda.exe"

if [ -f "$CONDA_EXE" ]; then
    echo "Found Windows conda at $CONDA_EXE"
    
    # Use Windows paths for conda commands
    WIN_PROJECT_DIR="D:\\APPSNospaces\\comfy-guru"
    WIN_ENV_FILE="$WIN_PROJECT_DIR\\environment.yml"
    
    # Check if environment exists
    if ! $CONDA_EXE env list | grep -q "comfy-guru"; then
        echo "Creating conda environment 'comfy-guru'..."
        $CONDA_EXE env create -f "$WIN_ENV_FILE"
    fi
    
    # Activate environment and install fastmcp
    echo "Activating environment and ensuring fastmcp is installed..."
    export PATH="$WINDOWS_CONDA/Scripts:$WINDOWS_CONDA/envs/comfy-guru/Scripts:$PATH"
    
    # Use the Python from the conda environment
    CONDA_PYTHON="$WINDOWS_CONDA/envs/comfy-guru/python.exe"
    if [ -f "$CONDA_PYTHON" ]; then
        echo "Using conda Python: $CONDA_PYTHON"
        # Install fastmcp if needed
        $CONDA_PYTHON -m pip install fastmcp 2>/dev/null || echo "fastmcp already installed or installation failed"
    else
        echo "Conda environment Python not found, using system Python"
    fi
else
    echo "Windows conda not found at $CONDA_EXE"
    echo "Please install miniconda at C:\\pinokio\\bin\\miniconda"
fi

# Check if the server is already running
if [ -f "$PROJECT_DIR/.mcp_server.pid" ]; then
    PID=$(cat "$PROJECT_DIR/.mcp_server.pid")
    if ps -p $PID > /dev/null; then
        echo "ComfyUI Log Debugger MCP server already running (PID $PID)."
        exit 0
    else
        # Stale PID file, remove it
        rm -f "$PROJECT_DIR/.mcp_server.pid"
    fi
fi

# Start the server in the background using conda python
if [ -f "$CONDA_PYTHON" ]; then
    (cd "$PROJECT_DIR" && "$CONDA_PYTHON" mcp_server_runner.py start) &
else
    (cd "$PROJECT_DIR" && python3 mcp_server_runner.py start) &
fi

# Give it a moment to start and write the PID file
sleep 2

if [ -f "$PROJECT_DIR/.mcp_server.pid" ]; then
    PID=$(cat "$PROJECT_DIR/.mcp_server.pid")
    echo "ComfyUI Log Debugger MCP server started (PID $PID)."
else
    echo "Failed to start ComfyUI Log Debugger MCP server. Check $PROJECT_DIR/mcp_server_output.log for details."
fi
