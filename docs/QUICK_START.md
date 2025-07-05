# 🚀 ComfyUI Log Debugger - Quick Start Guide

## For Users: How to Install (2 minutes)

### Step 1: Get the Code
```bash
git clone https://github.com/endlessblink/comfy-guru.git
cd comfy-guru
```

### Step 2: Run Easy Installer
```bash
python easy_install.py
```

The installer will:
- ✅ Install Python dependencies
- ✅ Find your ComfyUI installations
- ✅ Add the server to Claude Code
- ✅ Create a config file

### Step 3: Restart Claude Code
Close and reopen Claude Code completely.

### Step 4: Test It!
In Claude Code, type:
```
Find my ComfyUI logs
```

## 🎯 What You Can Ask Claude

### Find Logs
- "Show me all my ComfyUI log files"
- "Where are my ComfyUI logs located?"
- "Find ComfyUI installations on my system"

### Analyze Errors
- "Check my ComfyUI logs for errors"
- "What CUDA errors are in my logs?"
- "Show me node execution failures"
- "Find dependency errors in ComfyUI"

### Recent Issues
- "What errors happened in the last hour?"
- "Show me today's ComfyUI errors"
- "Check recent log entries"

### Real-time Monitoring
- "Monitor my ComfyUI log file"
- "Watch for new errors in real-time"
- "Tail the ComfyUI log"

## 🔧 Customization

### Tell It Where ComfyUI Is
Edit the `.env` file created by the installer:

```env
# Add your ComfyUI paths here
COMFYUI_PATHS=C:\ComfyUI,D:\AI\ComfyUI,E:\Projects\ComfyUI

# Add folders to search
COMFYUI_SEARCH_DIRS=C:\,D:\,E:\
```

### Add Custom Error Patterns
Edit `src/error_patterns.json` to add new error types:

```json
{
  "MyCustomError": [
    "pattern to match",
    "another pattern"
  ]
}
```

## 📊 Example Output

When you ask "Check my ComfyUI logs for errors", Claude will show:

```
Found 99 errors in your ComfyUI logs:

CUDA_OUT_OF_MEMORY (15 occurrences):
- Line 1234: CUDA out of memory. Tried to allocate 2.00 GiB
- Line 2345: torch.cuda.OutOfMemoryError

NodeExecutionFailure (23 occurrences):
- Line 3456: Error occurred when executing KSampler
- Line 4567: Failed to execute node ComfyUI_IPAdapter

DependencyNotFound (61 occurrences):
- Line 5678: ModuleNotFoundError: No module named 'insightface'
- Line 6789: Cannot import 'onnxruntime'
```

## 🐳 Alternative: Docker Installation

If Python installation fails, use Docker:

```bash
# Build
docker build -t comfy-guru .

# Windows
docker run --rm -v C:\:/mnt/c:ro -v D:\:/mnt/d:ro comfy-guru:latest

# Linux/Mac
docker run --rm -v /home:/mnt/home:ro comfy-guru:latest
```

## ❓ Troubleshooting

### "Can't find comfy-guru"
1. Make sure you restarted Claude Code
2. Run `python easy_install.py` again
3. Check if Python is in your PATH

### "No logs found"
1. Edit `.env` with your ComfyUI location
2. Make sure ComfyUI created log files
3. Check file permissions

### "Permission denied"
- Windows: Run as Administrator
- Linux/Mac: Use `sudo python easy_install.py`

## 🆘 Need Help?

1. Run the test: `python test_installation.py`
2. Check the logs: `src/mcp_server_output.log`
3. Open an issue on GitHub

---

**Pro Tip**: The more specific your ComfyUI paths in `.env`, the faster log discovery will be!