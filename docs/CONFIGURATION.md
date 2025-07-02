# Configuration Guide for Comfy-Guru

## Environment File (.env)

The `.env` file controls how comfy-guru discovers and monitors your ComfyUI installations.

## Configuration Options

### COMFYUI_PATHS
**Default**: Empty  
**Recommended**: Add all your known ComfyUI installation paths

```env
# Single path
COMFYUI_PATHS=C:\ComfyUI

# Multiple paths (comma-separated)
COMFYUI_PATHS=C:\ComfyUI,D:\Projects\ComfyUI,E:\AI\ComfyUI_portable
```

**Tips**:
- Use full absolute paths
- Separate multiple paths with commas
- No quotes needed, even for paths with spaces
- These paths are checked first and fastest

### COMFYUI_DEEP_SEARCH
**Default**: `false`  
**Options**: `true` or `false`

```env
# Keep it OFF for best performance
COMFYUI_DEEP_SEARCH=false
```

**When OFF** (Recommended):
- Only checks paths in COMFYUI_PATHS
- Checks for running ComfyUI processes
- Discovery takes 1-10 seconds

**When ON**:
- Searches entire drives for ComfyUI
- Can take 30-100+ seconds
- May encounter permission errors
- Useful for finding unknown installations

### COMFYUI_SEARCH_DIRS
**Default**: `C:\,D:\,E:\`  
**Only used when**: `COMFYUI_DEEP_SEARCH=true`

```env
# Directories to search for ComfyUI installations
COMFYUI_SEARCH_DIRS=C:\,D:\,C:\Program Files\,C:\Users\
```

### COMFYUI_LOG_PATTERNS
**Default**: `*.log,console.txt,output.txt,stderr.txt,stdout.txt,*.out`

```env
# File patterns to consider as log files
COMFYUI_LOG_PATTERNS=*.log,console.txt,output.txt,*.err
```

### COMFYUI_MAX_DEPTH
**Default**: `2`  
**Only used when**: `COMFYUI_DEEP_SEARCH=true`

```env
# How many folder levels deep to search
COMFYUI_MAX_DEPTH=3
```

## Common Configurations

### Fast & Reliable (Recommended)
```env
COMFYUI_PATHS=C:\ComfyUI,D:\AI\ComfyUI,E:\Projects\ComfyUI
COMFYUI_DEEP_SEARCH=false
```

### Find New Installations
```env
# Temporarily enable deep search
COMFYUI_DEEP_SEARCH=true
COMFYUI_SEARCH_DIRS=D:\,E:\
COMFYUI_MAX_DEPTH=4
```

### Minimal Setup
```env
# Just one installation
COMFYUI_PATHS=C:\ComfyUI_windows_portable
COMFYUI_DEEP_SEARCH=false
```

## How to Find All Your ComfyUI Installations

1. **Enable deep search temporarily**:
   ```env
   COMFYUI_DEEP_SEARCH=true
   ```

2. **Ask Claude Desktop**:
   > "Find all my ComfyUI installations"

3. **Wait for results** (30-100 seconds)

4. **Copy the found paths** to your `.env`:
   ```env
   COMFYUI_PATHS=path1,path2,path3,path4
   ```

5. **Disable deep search**:
   ```env
   COMFYUI_DEEP_SEARCH=false
   ```

## Troubleshooting

### "No installations found"
- Check your paths are correct in COMFYUI_PATHS
- Try enabling deep search temporarily
- Make sure ComfyUI folders contain `main.py`

### "Discovery is too slow"
- Set `COMFYUI_DEEP_SEARCH=false`
- Add paths manually to COMFYUI_PATHS
- Reduce COMFYUI_SEARCH_DIRS

### "Permission denied errors"
- Normal when deep search is ON
- Remove system directories from COMFYUI_SEARCH_DIRS
- Use manual paths instead

## Best Practices

1. **Always list known paths** in COMFYUI_PATHS
2. **Keep deep search OFF** for daily use
3. **Use deep search once** to find all installations
4. **Update paths** when you install new ComfyUI versions
5. **Test with**: "Find my ComfyUI logs" in Claude Desktop