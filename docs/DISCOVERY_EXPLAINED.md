# ComfyUI Discovery System Explained

## How comfy-guru Finds Your ComfyUI Installations

The MCP server uses multiple methods to discover ComfyUI installations:

### 1. **Known Paths (Always Works)**
- Reads paths from `.env` file
- These are always checked first
- Reliable and fast

### 2. **Active Process Detection**
- Finds **running** ComfyUI instances
- Only works when ComfyUI is actively running
- Automatically discovers new installations when you start them

### 3. **Smart Search (Optional)**
- Deep file system search
- Can be slow on large drives
- Disabled by default for performance

## Configuration Options

### Basic Setup (.env file)
```env
# List your ComfyUI installations
COMFYUI_PATHS=C:\ComfyUI,D:\AI\ComfyUI,D:\MY PROJECTS\AI\ComfyUI

# Disable deep search for faster performance
COMFYUI_DEEP_SEARCH=false
```

### For New Installations

#### Option 1: Add to .env (Recommended)
Edit `.env` and add the new path:
```env
COMFYUI_PATHS=C:\ComfyUI,D:\NewComfyUI,E:\AnotherComfyUI
```

#### Option 2: Run ComfyUI First
1. Start your new ComfyUI installation
2. The MCP server will detect it automatically
3. It will be remembered for future sessions

## Performance Tips

1. **Keep Deep Search Disabled** 
   - Set `COMFYUI_DEEP_SEARCH=false`
   - Avoids long search times

2. **List All Known Paths**
   - Add all your ComfyUI installations to `.env`
   - Fastest and most reliable method

3. **Process Detection is Optional**
   - Works only when ComfyUI is running
   - Good for discovering new installations
   - Not required if paths are in `.env`

## Typical Discovery Times

- **Known paths only**: < 1 second
- **With process detection**: 5-10 seconds
- **With deep search**: 30+ seconds (not recommended)

## Troubleshooting

### "No installations found"
1. Add your ComfyUI path to `.env`
2. Or start ComfyUI and try again

### "Discovery is slow"
1. Set `COMFYUI_DEEP_SEARCH=false`
2. Remove unnecessary paths from `COMFYUI_SEARCH_DIRS`

### "New installation not detected"
1. Add it to `.env` manually
2. Or ensure ComfyUI is running when you use the MCP server

## Best Practice

For best performance and reliability:

1. **Initial Setup**: Add all known ComfyUI paths to `.env`
2. **New Installations**: Either:
   - Add to `.env` immediately, or
   - Run the new ComfyUI once for auto-discovery
3. **Keep deep search disabled** unless absolutely needed