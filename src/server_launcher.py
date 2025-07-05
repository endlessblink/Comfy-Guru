#!/usr/bin/env python3
"""
Launcher script for ComfyUI Log Debugger MCP Server
Handles dependency installation and proper path setup
"""
import os
import sys
import subprocess
import json

def check_and_install_dependencies():
    """Check if dependencies are installed, install if not"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lib_dir = os.path.join(script_dir, 'lib')
    
    # Create lib directory if it doesn't exist
    os.makedirs(lib_dir, exist_ok=True)
    
    # Check if fastmcp is installed
    fastmcp_path = os.path.join(lib_dir, 'fastmcp')
    if not os.path.exists(fastmcp_path):
        print("Installing dependencies for first run...", file=sys.stderr)
        try:
            # Install minimal dependencies
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                'fastmcp>=2.9.0', 'python-dotenv', 'aiofiles', 'psutil',
                '--target', lib_dir,
                '--quiet', '--disable-pip-version-check'
            ])
            print("Dependencies installed successfully!", file=sys.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Add lib directory to Python path
    sys.path.insert(0, lib_dir)
    sys.path.insert(0, script_dir)

def main():
    """Main entry point"""
    # Setup dependencies
    check_and_install_dependencies()
    
    # Import and run the server
    try:
        from standalone_mcp_server import main as server_main
        server_main()
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()