#!/bin/bash
# Docker-based installation for ComfyUI Log Debugger

echo "🐳 ComfyUI Log Debugger - Docker Installation"
echo "============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    echo "   Download from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is ready"

# Build the Docker image
echo ""
echo "📦 Building Docker image..."
docker build -t comfy-guru:latest . || {
    echo "❌ Failed to build Docker image"
    exit 1
}

echo "✅ Docker image built successfully"

# Test the container
echo ""
echo "🧪 Testing container..."
docker run --rm -v "D:/:/mnt/d:ro" comfy-guru:latest python -c "
from src.smart_log_discovery import SmartComfyUIDiscovery
d = SmartComfyUIDiscovery()
r = d.discover_smart()
print(f'✅ Discovery working! Found {len(r[\"installations\"])} installations')
" || {
    echo "❌ Container test failed"
    exit 1
}

# Create MCP configuration
echo ""
echo "📝 Creating MCP configuration..."

# Determine the right config location
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows Git Bash
    CONFIG_DIR="$APPDATA/Claude"
elif [[ -n "$WSL_DISTRO_NAME" ]]; then
    # WSL
    CONFIG_DIR="$HOME/.config/claude"
else
    # Native Linux/Mac
    CONFIG_DIR="$HOME/.config/claude"
fi

mkdir -p "$CONFIG_DIR"
CONFIG_FILE="$CONFIG_DIR/claude.json"

# Create or update config
if [ -f "$CONFIG_FILE" ]; then
    echo "📋 Updating existing Claude configuration..."
    # Backup existing config
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
    
    # Add our server using jq if available, otherwise use Python
    if command -v jq &> /dev/null; then
        jq '.mcpServers["comfy-guru-docker"] = {
            "command": "docker",
            "args": ["run", "-i", "--rm", "-v", "C:/:/mnt/c:ro", "-v", "D:/:/mnt/d:ro", "comfy-guru:latest"]
        }' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    else
        python3 -c "
import json
with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)
if 'mcpServers' not in config:
    config['mcpServers'] = {}
config['mcpServers']['comfy-guru-docker'] = {
    'command': 'docker',
    'args': ['run', '-i', '--rm', '-v', 'C:/:/mnt/c:ro', '-v', 'D:/:/mnt/d:ro', 'comfy-guru:latest']
}
with open('$CONFIG_FILE', 'w') as f:
    json.dump(config, f, indent=2)
"
    fi
else
    echo "📋 Creating new Claude configuration..."
    cp docker-mcp.json "$CONFIG_FILE"
fi

echo "✅ Configuration saved to: $CONFIG_FILE"

# Show usage instructions
echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo ""
echo "Next steps:"
echo "1. Restart Claude Code"
echo "2. The 'comfy-guru-docker' MCP server will be available"
echo "3. Your Windows drives are accessible at /mnt/c and /mnt/d"
echo ""
echo "To test manually:"
echo "  docker run -it --rm -v D:/:/mnt/d:ro comfy-guru:latest python test_installation.py"
echo ""
echo "To use docker-compose instead:"
echo "  docker-compose up -d"