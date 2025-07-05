# Reddit Post for r/comfyui (Updated Version)

**Title:** "🔍 I built Comfy-Guru: Debug ComfyUI errors with Claude Desktop - Now even easier to use!"

**Post:**

Hey r/comfyui! 👋

I've been working on a tool to solve one of my biggest frustrations with ComfyUI - trying to figure out what went wrong when workflows fail. So I built **Comfy-Guru**, an MCP server that connects your ComfyUI logs directly to Claude Desktop for intelligent debugging.

## 🚨 NEW: Super Easy Setup!

**Just tell Claude where your ComfyUI is installed:**
```
"My ComfyUI is at D:\AI\ComfyUI_windows_portable"
```

That's it! No complex configuration needed. Claude will immediately start analyzing your logs.

## What it does:

- 🔍 **Reads and analyzes your ComfyUI logs** - finds errors, warnings, and performance issues
- 📊 **Categorizes problems** - CUDA errors, missing nodes, dependency issues, etc.
- 🤖 **Provides solutions** - Claude explains what went wrong and how to fix it
- ⏰ **Real-time monitoring** - watch for errors as they happen
- 💬 **Natural language** - just ask "What errors happened in the last hour?"

## Quick install (30 seconds):

### Option 1: Desktop Extension (NEW! ✨)
1. **[Download comfy-guru.dxt](https://github.com/endlessblink/comfy-guru/releases/latest)**
2. Open Claude Desktop → Settings → Extensions
3. Click "Install Extension" and select the .dxt file
4. Done!

### Option 2: Traditional Install
```bash
git clone https://github.com/endlessblink/comfy-guru.git
cd comfy-guru
install.bat  # Windows
./install.sh # Mac/Linux
```

## Example usage:

Once installed, just tell Claude:
- "My ComfyUI is at C:\ComfyUI_portable, check for errors"
- "Find CUDA memory issues in D:\AI\ComfyUI\comfyui.log"
- "Monitor my ComfyUI at C:\Users\Me\ComfyUI for new errors"
- "What's causing my workflows to fail?"

## Real example from today:

A user had performance issues, and Comfy-Guru instantly found:
- 15 missing custom node dependencies
- Conflicting ControlNet versions
- Deprecated PyTorch functions
- Slow-loading custom nodes affecting startup

## Why I built this:

Got tired of manually digging through logs trying to understand cryptic error messages. Now Claude can instantly tell me "You're missing the ControlNetPreprocessor nodes - install comfyui_controlnet_aux to fix this."

## Current features:

- ✅ Works with ANY ComfyUI installation (portable, git, Stability Matrix)
- ✅ No modifications to ComfyUI needed
- ✅ Analyzes historical logs (not just real-time)
- ✅ Cross-platform (Windows/Mac/Linux)
- ✅ Privacy-focused (logs stay local)

## Looking for feedback on:

1. What other ComfyUI debugging pain points do you have?
2. Would workflow execution analysis be useful?
3. Interest in performance profiling features?
4. Any specific error types you struggle with?

**GitHub:** https://github.com/endlessblink/comfy-guru

This is my first MCP project and I'm really excited about how it's helping people debug ComfyUI issues. The ability to just tell Claude where ComfyUI is installed has made it super accessible.

Thanks for being such an awesome community! 🙏

**Edit:** Just to clarify - this gives Claude the ability to read your ComfyUI logs (with your permission) to help debug issues. Your logs stay completely local and private.