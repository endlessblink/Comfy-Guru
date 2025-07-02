# ComfyUI Log Debugger MCP Server (comfy-guru)

A Model Context Protocol (MCP) server that helps you debug ComfyUI by discovering and analyzing log files through Claude Desktop.

## 🚀 Quick Installation (30 seconds)

### Windows
```batch
git clone https://github.com/yourusername/comfy-guru.git
cd comfy-guru
install.bat
```

### Linux/Mac
```bash
git clone https://github.com/yourusername/comfy-guru.git
cd comfy-guru
./install.sh
```

That's it! Restart Claude Desktop and type: **"Find my ComfyUI logs"**

## 🎯 What It Does

- **Finds all your ComfyUI installations** automatically
- **Discovers log files** (including rotated logs, port-specific logs, debug logs)
- **Analyzes errors** and categorizes them (CUDA, Node execution, Dependencies, etc.)
- **Monitors logs in real-time** for new errors
- **Works everywhere** - Windows, macOS, Linux, Docker

## 📋 Example Commands in Claude Desktop

Once installed, just ask Claude:

- 🔍 **"Find all my ComfyUI log files"**
- 🐛 **"Check my ComfyUI logs for CUDA memory errors"**
- 📊 **"What errors happened in the last 30 minutes?"**
- 👀 **"Monitor my ComfyUI log for new errors"**
- 🔧 **"Analyze my ComfyUI workflow execution errors"**

## 🛠️ Installation Options

### Option 1: Easy Install (Recommended)
```bash
python easy_install.py
```

### Option 2: Docker Install
```bash
# Windows
docker-install.bat

# Linux/Mac/WSL
./docker-install.sh
```

### Option 3: Manual Install
See [INSTALL.md](INSTALL.md) for manual configuration of Claude Desktop.

## ⚙️ Configuration

The installer creates a `.env` file. Edit it to add custom ComfyUI paths:

```env
# Your ComfyUI installations
COMFYUI_PATHS=C:\ComfyUI,D:\MY PROJECTS\AI\ComfyUI

# Search these directories for ComfyUI
COMFYUI_SEARCH_DIRS=C:\,D:\,E:\

# Enable deep search
COMFYUI_DEEP_SEARCH=true
```

## 🧪 Testing

```bash
# Test the installation
python test_installation.py
```

Expected output:
```
✅ All imports successful
✅ Found X ComfyUI installations
✅ Found Y log files
✅ Error detection working
```

## 📁 Project Structure

```
comfy-guru/
├── src/                    # Core source files
│   ├── standalone_mcp_server.py
│   ├── debugger_server.py
│   ├── smart_log_discovery.py
│   └── error_patterns.json
├── docs/                   # Documentation
├── examples/              # Example files
├── scripts/               # Helper scripts
├── easy_install.py       # Easy installer
├── install.py           # Standard installer
├── test_installation.py # Test suite
└── requirements.txt     # Dependencies
```

## 🔧 Troubleshooting

### "comfy-guru not found" in Claude Desktop
- Restart Claude Desktop after installation
- Run the installer again (`install.bat` or `./install.sh`)
- Check the config file manually (see INSTALL.md)

### No logs found
- Edit `.env` with your ComfyUI paths
- Make sure ComfyUI has been run at least once
- Try with `COMFYUI_DEEP_SEARCH=true`

### Permission errors
- Windows: Run as Administrator
- Linux/macOS: Check file permissions
- Docker: Ensure volumes are mounted with `:ro` flag

## 📦 What Gets Analyzed

- `comfyui.log` - Main log file
- `comfyui_8188.log` - Port-specific logs
- `debug.log` - Debug output
- `*.prev`, `*.prev2` - Rotated logs
- Custom node logs
- Console output logs

## 🤝 Contributing

Pull requests welcome! Areas for improvement:
- More error patterns
- Additional log file locations
- Performance optimizations
- New analysis features

## 📄 License

MIT - Use freely!

---

Made with ❤️ for the ComfyUI community. If this helps you debug ComfyUI issues faster, give it a ⭐!