# Dropoff Prompt - ComfyUI Log Debugger Project

## Current Project State

You are working on a **ComfyUI Log Debugger MCP Server** project. This is a Model Context Protocol (MCP) server that provides tools for debugging ComfyUI installations by analyzing log files.

### Project Structure
- **Location**: `/mnt/d/APPSNospaces/comfy-guru/`
- **Main Files**:
  - `debugger_server.py` - Core MCP server with log analysis functionality
  - `mcp_server_runner.py` - Background server management script
  - `log_discovery.py` - Auto-discovery of ComfyUI log files
  - `error_patterns.json` - Error pattern definitions for log analysis
  - `mcp.json` - MCP server configuration file
  - `CLAUDE.md` - Project documentation for future Claude instances

### Key Functionality
- **Log Discovery**: Finds ComfyUI logs from portable installs, custom builds, standard locations, and active processes
- **Error Analysis**: Categorizes errors (CUDA OOM, node failures, dependency issues, etc.)
- **Real-time Monitoring**: Cross-platform log tailing
- **Background Server**: Manages MCP server lifecycle with PID tracking

## Current Issue: MCP Server Configuration

**Problem**: The MCP servers are configured in `mcp.json` but Claude Code doesn't recognize them. The `/mcp` slash command shows "No MCP servers configured."

**Root Cause**: Claude Code's MCP configuration is separate from the project's `mcp.json` file. The servers need to be added to Claude Code's global configuration.

## Required Actions

### 1. Configure MCP Servers in Claude Code

You need to add the MCP servers from `mcp.json` to Claude Code's configuration. The following servers were attempted to be added but may need verification:

```bash
# Core servers that should work:
claude mcp add log_debugger python3 debugger_server.py
claude mcp add like-i-said-memory node /mnt/d/APPSNospaces/Like-I-said-mcp-server-v2/server.js
claude mcp add like-i-said-v2 node /mnt/d/APPSNospaces/Like-I-said-mcp-server-v2/server-markdown.js
claude mcp add puppeteer npx @modelcontextprotocol/server-puppeteer
claude mcp add playwright-mcp npx @playwright/mcp@latest
claude mcp add perplexity-ask npx server-perplexity-ask
claude mcp add site-control-mcp node ./Site-Control-MCP-Export/server.js
```

### 2. Verify Server Paths

Before adding servers, verify these paths exist:
- `/mnt/d/APPSNospaces/Like-I-said-mcp-server-v2/server.js`
- `/mnt/d/APPSNospaces/Like-I-said-mcp-server-v2/server-markdown.js`
- `./Site-Control-MCP-Export/server.js`

### 3. Handle Complex Servers

These servers have complex configurations that may need manual setup:

**GitHub Server (with Docker)**:
```bash
# Requires GITHUB_PERSONAL_ACCESS_TOKEN environment variable
claude mcp add github docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server
```

**Contentful Server**:
```bash
# Requires management token
claude mcp add contentful npx @ivotoby/contentful-management-mcp-server --management-token YOUR_TOKEN --host http://api.contentful.com
```

**Sequential Thinking Server**:
```bash
# May need to be added differently due to complex args
claude mcp add server-sequential-thinking npx @smithery/cli@latest
```

### 4. Test Memory Server Access

Once configured, you should be able to access the memory server functionality. The memory server (`like-i-said-memory`) provides persistent memory capabilities across sessions.

## Development Commands

```bash
# Start the local MCP server
python3 mcp_server_runner.py start

# Stop the server
python3 mcp_server_runner.py stop

# Run in foreground (for debugging)
python3 mcp_server_runner.py run

# Test log discovery
python3 log_discovery.py

# Environment management
./activate.sh    # Start server with environment
./deactivate.sh  # Stop server and clean up
```

## Expected Workflow

1. **Configure MCP servers** in Claude Code using the commands above
2. **Verify `/mcp` slash command** shows configured servers
3. **Test memory server access** to ensure it's working
4. **Continue development** with full MCP server capabilities

## Next Steps

After MCP server configuration is working:
- Test the log debugger functionality
- Verify memory server capabilities
- Enhance error pattern detection
- Add more ComfyUI-specific debugging features

The project is well-structured and ready for development once the MCP server configuration issue is resolved.