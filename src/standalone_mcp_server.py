#!/usr/bin/env python3
"""
Standalone MCP server for ComfyUI Log Debugger
"""

import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Also add lib directory (handle both Unix and Windows paths)
lib_dir = os.path.join(current_dir, 'lib')
if os.path.exists(lib_dir):
    sys.path.insert(0, lib_dir)

# For Windows, also check parent directory
parent_dir = os.path.dirname(current_dir)
parent_lib_dir = os.path.join(parent_dir, 'lib')
if os.path.exists(parent_lib_dir):
    sys.path.insert(0, parent_lib_dir)

try:
    from fastmcp import FastMCP
except ImportError as e:
    print(f"Error importing FastMCP: {e}", file=sys.stderr)
    print(f"Python path: {sys.path}", file=sys.stderr)
    print(f"Current directory: {current_dir}", file=sys.stderr)
    sys.exit(1)

from debugger_server import ComfyUILogDebugger

def main():
    # Create the MCP server
    mcp = FastMCP("Comfy Guru")
    debugger = ComfyUILogDebugger()
    
    # Register the debugger methods as tools
    mcp.tool()(debugger.get_logs)
    mcp.tool()(debugger.find_errors) 
    mcp.tool()(debugger.tail_log)
    mcp.tool()(debugger.monitor_gpu_memory_warnings)
    mcp.tool()(debugger.find_workflow_by_id)
    
    # Run the server
    mcp.run()

if __name__ == "__main__":
    main()