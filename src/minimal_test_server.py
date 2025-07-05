#!/usr/bin/env python3
"""
Minimal MCP test server for debugging Windows issues
"""
import sys
import os
import json

# Immediately log to stderr
print("[MCP Test] Starting minimal test server...", file=sys.stderr, flush=True)
print(f"[MCP Test] Python: {sys.version}", file=sys.stderr, flush=True)
print(f"[MCP Test] Executable: {sys.executable}", file=sys.stderr, flush=True)
print(f"[MCP Test] Current dir: {os.getcwd()}", file=sys.stderr, flush=True)
print(f"[MCP Test] Script dir: {os.path.dirname(os.path.abspath(__file__))}", file=sys.stderr, flush=True)

try:
    # Basic MCP server without dependencies
    def send_message(msg):
        """Send a JSON-RPC message"""
        json_msg = json.dumps(msg)
        sys.stdout.write(f"{json_msg}\n")
        sys.stdout.flush()
        print(f"[MCP Test] Sent: {json_msg}", file=sys.stderr, flush=True)
    
    # Send initialization response
    print("[MCP Test] Sending initialize response...", file=sys.stderr, flush=True)
    
    # Wait for initialize request
    while True:
        line = sys.stdin.readline()
        if not line:
            print("[MCP Test] EOF received", file=sys.stderr, flush=True)
            break
            
        print(f"[MCP Test] Received: {line.strip()}", file=sys.stderr, flush=True)
        
        try:
            msg = json.loads(line)
            if msg.get("method") == "initialize":
                # Send response
                response = {
                    "jsonrpc": "2.0",
                    "id": msg.get("id"),
                    "result": {
                        "protocolVersion": "0.1.0",
                        "capabilities": {
                            "tools": {
                                "listChanged": False
                            }
                        },
                        "serverInfo": {
                            "name": "minimal-test",
                            "version": "1.0.0"
                        }
                    }
                }
                send_message(response)
                
                # Send initialized notification
                initialized = {
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized"
                }
                send_message(initialized)
                
            elif msg.get("method") == "tools/list":
                # Return empty tools list
                response = {
                    "jsonrpc": "2.0",
                    "id": msg.get("id"),
                    "result": {
                        "tools": []
                    }
                }
                send_message(response)
                
        except json.JSONDecodeError as e:
            print(f"[MCP Test] JSON decode error: {e}", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"[MCP Test] Error: {e}", file=sys.stderr, flush=True)
            
except Exception as e:
    print(f"[MCP Test] Fatal error: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)