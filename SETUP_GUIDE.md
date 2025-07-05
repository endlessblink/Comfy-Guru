# ComfyUI Guru Setup Guide

## Quick Start

If ComfyUI Guru can't find your ComfyUI installation automatically, you need to tell it where to look.

### Method 1: Tell Claude Where ComfyUI Is Installed (Easiest)

Simply tell Claude in your chat:
```
My ComfyUI is installed at: C:\ComfyUI_windows_portable
```

Or:
```
Please check for ComfyUI logs in: D:\AI\ComfyUI
```

### Method 2: Configure Paths Permanently

1. Find the extension directory:
   ```
   C:\Users\[YourUsername]\AppData\Roaming\Claude\Claude Extensions\local.dxt.endlessblink.comfy-guru\
   ```

2. Create a `.env` file in that directory

3. Add your ComfyUI paths:
   ```
   COMFYUI_PATHS=C:\ComfyUI_windows_portable,D:\AI\ComfyUI,C:\Users\YourName\ComfyUI
   ```

## Common ComfyUI Installation Locations

- **Portable Version**: `C:\ComfyUI_windows_portable`
- **Git Clone**: `C:\Users\[Username]\ComfyUI`
- **Custom Install**: `D:\AI\ComfyUI` or similar
- **Stability Matrix**: `C:\Users\[Username]\StabilityMatrix\Packages\ComfyUI`

## Troubleshooting

### "No ComfyUI installations found"
1. Make sure ComfyUI has been run at least once to generate log files
2. Check that `.log` files exist in your ComfyUI directory
3. Try running ComfyUI while the extension is active (it detects running instances)

### Log File Locations
ComfyUI typically creates logs in:
- Main directory: `comfyui.log`, `output.log`
- Logs folder: `logs/comfyui.log`
- Console output: `console.txt`

## Example Prompts to Use

When chatting with Claude, you can say:

- "My ComfyUI is at C:\ComfyUI_windows_portable, can you check for errors?"
- "Find errors in my ComfyUI logs at D:\AI\ComfyUI"
- "Monitor the GPU memory warnings in C:\Users\Me\ComfyUI\comfyui.log"
- "I'm getting workflow errors, my ComfyUI is in the default portable location"