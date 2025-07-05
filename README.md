![Comfy-Guru](docs/Images/Comfy-Guru.png)

# ComfyUI Log Debugger MCP Server (comfy-guru)

A Model Context Protocol (MCP) server that helps you debug ComfyUI by discovering and analyzing log files through Claude Desktop.

## 🚨 IMPORTANT: Tell Claude Where ComfyUI Is Located!

**If ComfyUI isn't found automatically, just tell Claude in chat:**
```
"My ComfyUI is at D:\MY PROJECTS\AI\STABLE DIFFUSION UI\ComfyUI"
```

Or configure it permanently - see [Setup Guide](SETUP_GUIDE.md)

## 🚀 Quick Installation (30 seconds)

### For Users:
1. **[Download comfy-guru.dxt](https://github.com/endlessblink/comfy-guru/releases/latest/download/comfy-guru.dxt)** (pre-built extension)
2. Open Claude Desktop and go to: **Settings → Extensions**
3. Click **"Install Extension..."** 
4. Select the downloaded `comfy-guru.dxt` file
5. Done! No git clone, no Python setup needed!

**Note:** Don't double-click the .dxt file - install it through Claude Desktop's settings.

**Important:** After installation, **fully restart Claude Desktop** for the MCP extension to work properly.

### For Developers:
- To modify and rebuild the extension: `python build_extension.py`
- This creates a new `comfy-guru.dxt` from source files

## 🎯 What It Does

- **Finds all your ComfyUI installations** automatically
- **Discovers log files** (including rotated logs, port-specific logs, debug logs)
- **Analyzes errors** and categorizes them (CUDA, Node execution, Dependencies, etc.)
- **Monitors logs in real-time** for new errors
- **Works everywhere** - Windows, macOS, Linux, Docker

![Comfy-Guru in action](docs/Images/comfy-guru-screen.png)

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

### Adding ComfyUI Paths Manually

Edit the `.env` file and add paths separated by commas:

```env
# Your ComfyUI installations (comma-separated)
COMFYUI_PATHS=C:\ComfyUI,D:\MY PROJECTS\AI\ComfyUI,E:\Another\ComfyUI

# Search directories (only used if deep search is enabled)
COMFYUI_SEARCH_DIRS=C:\,D:\,E:\

# Deep search is OFF by default for performance
COMFYUI_DEEP_SEARCH=false
```

### About Deep Search

**Deep search is OFF by default** because:
- ✅ Manual paths are found instantly (< 1 second)
- ❌ Deep search can take 30-100+ seconds
- ❌ Can cause permission errors on system folders

### How to Use Deep Search Temporarily

1. **Enable deep search** to find all installations:
   ```env
   COMFYUI_DEEP_SEARCH=true
   ```

2. **Run the discovery** in Claude Desktop:
   ```
   "Find all my ComfyUI installations"
   ```

3. **Note the paths** it finds

4. **Add them to COMFYUI_PATHS** manually:
   ```env
   COMFYUI_PATHS=path1,path2,path3,newly_found_path
   ```

5. **Turn deep search OFF** again:
   ```env
   COMFYUI_DEEP_SEARCH=false
   ```

This way you get the benefit of discovery without the performance penalty!

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