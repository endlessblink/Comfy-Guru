# Desktop Extension Installation

The easiest way to install ComfyUI Log Debugger in Claude Desktop!

## 🚀 One-Click Installation

Starting with Claude Desktop 0.7.0, you can install ComfyUI Log Debugger as a desktop extension:

### Step 1: Build the Extension
```bash
# Windows
build_extension.bat

# macOS/Linux
python build_extension.py
```

This creates `build/comfy-guru.dxt` - your installable extension file.

### Step 2: Install in Claude Desktop

1. Open Claude Desktop
2. Go to **Settings** → **Developer** → **Edit Config**
3. Click **Install Extension...**
4. Select the `comfy-guru.dxt` file from the `build` folder
5. Configure your settings if prompted
6. Restart Claude Desktop

That's it! 🎉

## ⚙️ Configuration

When installing, you can configure:

- **ComfyUI Path**: Auto-detects by default, or specify manually
- **Real-time Monitoring**: Enable/disable live log watching
- **Log Retention**: How many days to keep analysis history (1-30)
- **Custom Patterns**: Path to your custom error patterns file

## 🔒 Security

Desktop extensions are secure by design:
- Runs in isolation from other extensions
- Sensitive data stored in OS keychain
- Clear capability declarations
- No network access beyond MCP protocol

## 🆚 Manual Installation

If you prefer manual installation or need more control, see [INSTALL.md](INSTALL.md) for traditional setup instructions.

## 🤝 Enterprise Deployment

For enterprise users:
- Extensions can be pre-installed via Group Policy
- Private extension directories supported
- Blocklist capability for security compliance

## 📚 More Information

- [Anthropic Desktop Extensions](https://www.anthropic.com/engineering/desktop-extensions)
- [MCP Documentation](https://modelcontextprotocol.io)
- [ComfyUI Log Debugger GitHub](https://github.com/Shiba-2-shiba/comfy-guru)