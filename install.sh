#!/bin/bash

echo "ComfyUI Log Debugger - Easy Installer for Claude Desktop"
echo "========================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi

# Run the easy installer
python3 easy_install.py

if [ $? -ne 0 ]; then
    echo
    echo "Installation failed. Please check the error messages above."
    exit 1
fi

echo
echo "Installation complete! Please restart Claude Desktop."