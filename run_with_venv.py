#!/usr/bin/env python3
"""
Wrapper to run MCP server with virtual environment activation
This ensures the venv is activated every time the MCP runs
"""
import os
import sys
import subprocess
from pathlib import Path

def get_venv_python():
    """Get the path to the virtual environment Python executable"""
    script_dir = Path(__file__).parent
    
    if sys.platform == "win32":
        venv_python = script_dir / "venv" / "Scripts" / "python.exe"
    else:
        venv_python = script_dir / "venv" / "bin" / "python"
    
    return venv_python

def main():
    """Run the MCP server with activated venv"""
    script_dir = Path(__file__).parent
    venv_python = get_venv_python()
    server_script = script_dir / "src" / "standalone_mcp_server.py"
    
    # Check if venv exists
    if not venv_python.exists():
        print(f"Error: Virtual environment not found at {venv_python.parent.parent}")
        print("Please run easy_install.py first to set up the environment")
        sys.exit(1)
    
    # Run the server with the venv Python
    try:
        # Use subprocess.run to execute and pass through stdio
        result = subprocess.run(
            [str(venv_python), str(server_script)],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error running MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()