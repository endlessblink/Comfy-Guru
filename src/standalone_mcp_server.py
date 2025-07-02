#!/usr/bin/env python3
"""
Standalone MCP server for ComfyUI Log Debugger
"""

import sys
import os
# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastmcp import FastMCP
from debugger_server import ComfyUILogDebugger

def main():
    # Create the MCP server
    mcp = FastMCP("Comfy Guru")
    debugger = ComfyUILogDebugger()
    
    # Register the debugger methods as tools
    mcp.tool()(debugger.get_logs)
    mcp.tool()(debugger.find_errors) 
    mcp.tool()(debugger.tail_log)
    
    # Run the server
    mcp.run()

if __name__ == "__main__":
    main()