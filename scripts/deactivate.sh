#!/bin/bash

# This script stops the MCP server when the conda environment is deactivated.

# Navigate to the comfyui-log-debugger directory
# Adjust this path if your project structure changes
PROJECT_DIR="/mnt/d/APPSNospaces/comfy-guru/comfyui-log-debugger"

if [ -f "$PROJECT_DIR/.mcp_server.pid" ]; then
    PID=$(cat "$PROJECT_DIR/.mcp_server.pid")
    if ps -p $PID > /dev/null; then
        echo "Stopping ComfyUI Log Debugger MCP server (PID $PID)."
        (cd "$PROJECT_DIR" && python3 mcp_server_runner.py stop)
    else
        echo "ComfyUI Log Debugger MCP server not running, cleaning up stale PID file."
        rm -f "$PROJECT_DIR/.mcp_server.pid"
    fi
else
    echo "ComfyUI Log Debugger MCP server not running (PID file not found)."
fi
