#!/bin/bash
# ComfyUI Log Debugger - Quick Installer
# Usage: curl -sSL https://your-repo/quick_install.sh | bash

echo "🚀 Installing ComfyUI Log Debugger MCP Server..."

# Detect Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

# Create directory if needed
INSTALL_DIR="$HOME/.comfy-guru"
mkdir -p "$INSTALL_DIR"

# Download latest release (replace with actual URL)
echo "📥 Downloading..."
if command -v curl &> /dev/null; then
    curl -L https://github.com/endlessblink/comfy-guru/archive/main.zip -o /tmp/comfy-guru.zip
elif command -v wget &> /dev/null; then
    wget https://github.com/endlessblink/comfy-guru/archive/main.zip -O /tmp/comfy-guru.zip
else
    echo "❌ curl or wget required"
    exit 1
fi

# Extract
echo "📦 Extracting..."
cd /tmp && unzip -q comfy-guru.zip
cp -r comfy-guru-main/* "$INSTALL_DIR/"
rm -rf /tmp/comfy-guru.zip /tmp/comfy-guru-main

# Install
echo "🔧 Installing dependencies..."
cd "$INSTALL_DIR"
$PYTHON install.py

echo "✅ Installation complete!"
echo "📍 Installed to: $INSTALL_DIR"
echo "🔄 Restart Claude Code to use the MCP server"