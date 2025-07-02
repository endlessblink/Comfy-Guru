# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a ComfyUI Log Debugger - an MCP (Model Context Protocol) server that provides tools for debugging ComfyUI installations by analyzing log files. The project helps users discover, monitor, and analyze ComfyUI logs across different installation types (portable, custom builds, standard installs).

## Architecture

### Core Components

- **`debugger_server.py`**: Main MCP server class (`ComfyUILogDebugger`) that provides log analysis functionality
- **`mcp_server_runner.py`**: Server management script that handles starting/stopping the MCP server in background
- **`log_discovery.py`**: Log file discovery engine that finds ComfyUI logs across different installation patterns
- **`error_patterns.json`**: Configuration file containing regex patterns for different error types
- **`mcp.json`**: MCP server configuration file

### Key Functionality

1. **Log Discovery**: Automatically finds ComfyUI logs from:
   - Portable installations (`ComfyUI_windows_portable*`)
   - Custom builds (detected via `extra_model_paths.yaml`)
   - Standard OS-specific locations
   - Active running processes

2. **Error Analysis**: Categorizes errors using predefined patterns:
   - CUDA out of memory errors
   - Node execution failures
   - Dependency/import errors
   - Prompt execution errors
   - General exceptions

3. **Real-time Monitoring**: Can tail log files in real-time across platforms (Linux, macOS, Windows)

## Common Commands

### Server Management
```bash
# Start MCP server
python3 mcp_server_runner.py

# Start server explicitly  
python3 mcp_server_runner.py start

# Stop server
python3 mcp_server_runner.py stop

# Run server in foreground (for debugging)
python3 mcp_server_runner.py run
```

### Environment Scripts
```bash
# Activate environment and start server
./activate.sh

# Deactivate environment and stop server  
./deactivate.sh
```

### Testing Log Discovery
```bash
# Test log discovery directly
python3 log_discovery.py
```

## Development Notes

- No package.json, requirements.txt, or formal dependency management - relies on system Python
- Uses `fastmcp` library for MCP server implementation
- Cross-platform support with OS-specific logic for Windows/Linux/macOS
- Server runs as background process with PID file management
- Log output redirected to `mcp_server_output.log`

## Error Pattern Configuration

Error patterns are defined in `error_patterns.json` and can be extended by adding new categories and regex patterns. The system searches for these patterns in log files and provides contextual lines around matches.