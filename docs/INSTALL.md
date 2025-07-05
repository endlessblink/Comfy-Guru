# ComfyUI Log Debugger (comfy-guru) - Installation Guide

This MCP server helps you debug ComfyUI installations by discovering and analyzing log files through Claude Desktop.

## Quick Installation

### Windows
```batch
git clone https://github.com/endlessblink/comfy-guru.git
cd comfy-guru
install.bat
```

### Linux/Mac
```bash
git clone https://github.com/endlessblink/comfy-guru.git
cd comfy-guru
./install.sh
```

The installer will:
- Create a Python virtual environment
- Install all dependencies
- Configure Claude Desktop automatically
- Test the installation

### Option 2: Docker Installation

```bash
# Clone the repository
git clone https://github.com/endlessblink/comfy-guru.git
cd comfy-guru

# Build Docker image
docker build -t comfy-guru:latest .

# Add to Claude Code (adjust paths for your system)
claude mcp add comfy-guru docker run --rm -v C:\:/mnt/c:ro -v D:\:/mnt/d:ro comfy-guru:latest
```

## Manual Claude Desktop Configuration

If the automatic installer doesn't work, manually edit your Claude Desktop MCP configuration:

### Windows
Edit: `%APPDATA%\Claude\claude_desktop_config.json`

### macOS
Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Linux
Edit: `~/.config/claude/claude_desktop_config.json`

Add this to the `mcpServers` section:

```json
{
  "mcpServers": {
    "comfy-guru": {
      "command": "python",
      "args": [
        "/full/path/to/comfy-guru/run_with_venv.py"
      ]
    }
  }
}
```

Note: The `run_with_venv.py` script ensures the virtual environment is activated before running the server.

## Configuration

### 1. Create `.env` file (Optional)
Create a `.env` file in the project root to specify your ComfyUI paths:

```env
# ComfyUI installation paths (comma-separated)
COMFYUI_PATHS=C:\ComfyUI,D:\AI\ComfyUI,C:\Users\YourName\ComfyUI

# Search directories for deep discovery
COMFYUI_SEARCH_DIRS=C:\,D:\,C:\Program Files\

# Enable deep search (slower but more thorough)
COMFYUI_DEEP_SEARCH=true

# Log file patterns to search for
COMFYUI_LOG_PATTERNS=*.log,console.txt,output.txt,stderr.txt,stdout.txt

# Maximum search depth
COMFYUI_MAX_DEPTH=3
```

### 2. Test Installation

```bash
# Test the installation
python test_installation.py

# Or with Docker
docker run --rm -v C:\:/mnt/c:ro -v D:\:/mnt/d:ro comfy-guru:latest python test_installation.py
```

## Using in Claude Code

Once installed and Claude Code is restarted, you can use these commands:

1. **Find ComfyUI logs**
   ```
   Find all my ComfyUI log files
   ```

2. **Analyze errors**
   ```
   Check my ComfyUI logs for CUDA memory errors
   What errors happened in the last 30 minutes?
   ```

3. **Monitor logs**
   ```
   Tail my ComfyUI log and watch for errors
   ```

## Features

- **Automatic Discovery**: Finds ComfyUI installations and log files
- **Error Analysis**: Categorizes errors (CUDA, Node execution, Dependencies, etc.)
- **Real-time Monitoring**: Watch logs as they update
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Smart Detection**: Uses registry, process detection, and deep search

## Troubleshooting

### "comfy-guru not found" in Claude Code
- Restart Claude Code after installation
- Verify the configuration file was updated correctly
- Check that Python is in your PATH

### No logs found
- Create a `.env` file with your ComfyUI paths
- Ensure ComfyUI has been run at least once to generate logs
- Check file permissions

### Permission errors
- On Windows: Run as administrator if needed
- On Linux/macOS: Check file ownership and permissions
- Docker: Ensure volume mounts have read permissions

## Requirements

- Python 3.8+
- Claude Code (Claude Desktop)
- ComfyUI installation (for log analysis)

## Support

For issues or questions:
- Open an issue on GitHub
- Check the test output: `python test_installation.py`
- Review logs in Claude Code's developer console