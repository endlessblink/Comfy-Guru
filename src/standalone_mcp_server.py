#!/usr/bin/env python3
"""
Standalone MCP server for ComfyUI Log Debugger
"""

import sys
import os
import subprocess
import traceback

# Enable debug logging to stderr
def debug_log(msg):
    print(f"[ComfyUI MCP Debug] {msg}", file=sys.stderr)
    sys.stderr.flush()

debug_log("Starting MCP server...")
debug_log(f"Python version: {sys.version}")
debug_log(f"Executable: {sys.executable}")

# Get the directory of this script
current_dir = os.path.dirname(os.path.abspath(__file__))
debug_log(f"Current directory: {current_dir}")

# Setup Python path
sys.path.insert(0, current_dir)

# Check for lib directory and install dependencies if needed
lib_dir = os.path.join(current_dir, 'lib')
fastmcp_path = os.path.join(lib_dir, 'fastmcp')

if not os.path.exists(fastmcp_path):
    debug_log("Dependencies not found, installing...")
    os.makedirs(lib_dir, exist_ok=True)
    
    try:
        # Install minimal dependencies
        cmd = [
            sys.executable, '-m', 'pip', 'install', 
            'fastmcp>=2.9.0', 'python-dotenv', 'aiofiles', 'psutil',
            '--target', lib_dir,
            '--quiet', '--disable-pip-version-check'
        ]
        debug_log(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            debug_log(f"pip install failed with return code {result.returncode}")
            debug_log(f"stdout: {result.stdout}")
            debug_log(f"stderr: {result.stderr}")
            # Try alternative pip command
            debug_log("Trying alternative pip installation...")
            cmd2 = [sys.executable, '-m', 'ensurepip', '--default-pip']
            subprocess.run(cmd2, capture_output=True)
            # Retry original command
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                debug_log("Failed to install dependencies after retry")
                sys.exit(1)
        
        debug_log("Dependencies installed successfully!")
    except Exception as e:
        debug_log(f"Failed to install dependencies: {e}")
        debug_log(traceback.format_exc())
        sys.exit(1)

# Add lib directory to path
if os.path.exists(lib_dir):
    sys.path.insert(0, lib_dir)
    debug_log(f"Added to path: {lib_dir}")

# Try to import FastMCP
try:
    debug_log("Importing FastMCP...")
    from fastmcp import FastMCP
    debug_log("FastMCP imported successfully")
except ImportError as e:
    debug_log(f"Error importing FastMCP: {e}")
    debug_log(f"Python path: {sys.path}")
    debug_log(f"Lib directory contents: {os.listdir(lib_dir) if os.path.exists(lib_dir) else 'Does not exist'}")
    sys.exit(1)

# Import debugger server
try:
    debug_log("Importing debugger_server...")
    from debugger_server import ComfyUILogDebugger
    debug_log("debugger_server imported successfully")
except Exception as e:
    debug_log(f"Error importing debugger_server: {e}")
    debug_log(traceback.format_exc())
    sys.exit(1)

def main():
    try:
        debug_log("Creating MCP server...")
        # Create the MCP server
        mcp = FastMCP("Comfy Guru")
        debugger = ComfyUILogDebugger()
        
        debug_log("Registering tools...")
        # Register the debugger methods as tools
        mcp.tool()(debugger.get_logs)
        mcp.tool()(debugger.find_errors) 
        mcp.tool()(debugger.tail_log)
        mcp.tool()(debugger.monitor_gpu_memory_warnings)
        mcp.tool()(debugger.find_workflow_by_id)
        
        debug_log("Starting server with stdio transport...")
        # Run the server
        mcp.run()
    except Exception as e:
        debug_log(f"Error in main: {e}")
        debug_log(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()