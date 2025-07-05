#!/usr/bin/env python3
"""
Setup script to install dependencies in server/lib for the extension
"""
import os
import sys
import subprocess
import shutil

def setup_lib():
    """Install dependencies in the lib directory"""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    lib_dir = os.path.join(script_dir, 'lib')
    
    # Create lib directory if it doesn't exist
    os.makedirs(lib_dir, exist_ok=True)
    
    # Path to requirements.txt
    req_file = os.path.join(parent_dir, 'requirements.txt')
    
    if not os.path.exists(req_file):
        print(f"Error: requirements.txt not found at {req_file}")
        return False
    
    print(f"Installing dependencies to {lib_dir}...")
    
    # Install dependencies to lib directory
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install',
            '-r', req_file,
            '--target', lib_dir,
            '--upgrade'
        ])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

if __name__ == "__main__":
    success = setup_lib()
    sys.exit(0 if success else 1)