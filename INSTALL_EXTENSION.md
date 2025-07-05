# How to Install ComfyUI Log Debugger Extension

## ⚠️ Important: Don't Double-Click the .dxt File!

The .dxt file is a Claude Desktop extension that must be installed through Claude Desktop's interface.

## 📋 Installation Steps:

### 1. Download the Extension
- Go to: https://github.com/endlessblink/comfy-guru
- Click on `comfy-guru.dxt`
- Click "Download" button
- Save it somewhere you can find it (e.g., Downloads folder)

### 2. Open Claude Desktop Settings
- Launch Claude Desktop
- Click on your name/avatar in the bottom left
- Select **"Settings"**

### 3. Navigate to Extensions
- In Settings, click on **"Developer"** tab
- Click **"Edit Config"** button

### 4. Install the Extension
- Click the **"Install Extension..."** button
- Browse to where you saved `comfy-guru.dxt`
- Select the file and click "Open"

### 5. Restart Claude Desktop
- Close Claude Desktop completely
- Reopen it

### 6. Test It!
Try asking Claude:
- "Find my ComfyUI logs"
- "Check for CUDA errors in my ComfyUI logs"
- "Monitor my ComfyUI log for new errors"

## 🔧 Troubleshooting

**"Windows doesn't know how to open this file"**
- This happens if you double-click the .dxt file
- Follow the steps above to install through Claude Desktop instead

**"Extension not found after installation"**
- Make sure you restarted Claude Desktop
- Check Settings → Developer → Edit Config to see if it's listed

**"Installation failed"**
- Ensure you have Claude Desktop 0.7.0 or newer
- Try downloading the file again
- Check that Python 3.8+ is installed on your system

## 🎯 Alternative: Traditional Installation

If the extension method doesn't work, you can use the traditional installation:

```batch
git clone https://github.com/endlessblink/comfy-guru.git
cd comfy-guru
install.bat
```

This requires Git and Python to be installed on your system.