# ComfyUI Guru - Prompt Template for Publishing

## Extension Description

ComfyUI Guru is an AI-powered log analyzer that helps debug ComfyUI errors, performance issues, and workflow problems. It automatically searches for ComfyUI installations but works best when you tell it where your ComfyUI is located.

## Suggested First Message to Users

```
Welcome! I'm ComfyUI Guru, your debugging assistant for ComfyUI.

To get started, please tell me:
1. Where is ComfyUI installed on your system? (e.g., C:\ComfyUI_windows_portable)
2. What issue are you experiencing?

Common locations I check:
- C:\ComfyUI_windows_portable
- C:\Users\[Username]\ComfyUI  
- D:\AI\ComfyUI
- C:\StabilityMatrix\Packages\ComfyUI

Just say something like: "My ComfyUI is at C:\ComfyUI_windows_portable and I'm getting CUDA out of memory errors"
```

## Example User Prompts

Users can interact naturally:
- "Check for errors in C:\ComfyUI_windows_portable"
- "My ComfyUI at D:\AI\ComfyUI keeps crashing"
- "Monitor GPU memory in my portable ComfyUI installation"
- "Find workflow 123456 in C:\Users\Me\ComfyUI\logs"

## Key Features to Highlight

1. **Automatic Discovery** - Finds running ComfyUI instances
2. **Manual Path Support** - Users can specify exact locations
3. **Real-time Monitoring** - Can tail logs as they're generated
4. **Error Analysis** - Categorizes and explains common errors
5. **GPU Memory Tracking** - Monitors VRAM usage issues

## Publishing Notes

When publishing, emphasize:
- Users should mention their ComfyUI installation path for best results
- The tool works with all ComfyUI versions (portable, git, Stability Matrix)
- It can analyze both current and historical log files
- No configuration needed - just tell Claude where ComfyUI is installed