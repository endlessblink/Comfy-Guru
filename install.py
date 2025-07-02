#!/usr/bin/env python3
"""
ComfyUI Log Debugger MCP Server - Installation Script
Handles installation across different environments including conda
"""
import os
import sys
import subprocess
import json
import platform
from pathlib import Path

class MCPInstaller:
    def __init__(self):
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.system = platform.system()
        self.is_wsl = self._detect_wsl()
        
    def _detect_wsl(self):
        """Detect if running under WSL"""
        try:
            with open('/proc/version', 'r') as f:
                return 'microsoft' in f.read().lower()
        except:
            return False
    
    def _find_python(self):
        """Find the best Python executable to use"""
        # Check if we're in a virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("✓ Virtual environment detected")
            return sys.executable
            
        # Check for conda
        conda_exe = os.environ.get('CONDA_EXE')
        if conda_exe:
            print("✓ Conda environment detected")
            return sys.executable
            
        # Default to current Python
        return sys.executable
    
    def _check_python_version(self):
        """Ensure Python version is adequate"""
        if sys.version_info < (3, 8):
            print("❌ Python 3.8 or higher is required")
            print(f"   Current version: {sys.version}")
            return False
        print(f"✓ Python {sys.version.split()[0]} detected")
        return True
    
    def _install_dependencies(self):
        """Install required Python packages"""
        python_exe = self._find_python()
        
        print("\nInstalling dependencies...")
        
        # First ensure pip is available
        try:
            subprocess.run([python_exe, '-m', 'pip', '--version'], 
                         check=True, capture_output=True)
        except:
            print("❌ pip not found. Installing pip...")
            try:
                subprocess.run([python_exe, '-m', 'ensurepip'], check=True)
            except:
                print("❌ Failed to install pip. Please install pip manually.")
                return False
        
        # Install requirements
        req_file = os.path.join(self.project_dir, 'requirements.txt')
        try:
            print("  Installing fastmcp and dependencies...")
            result = subprocess.run(
                [python_exe, '-m', 'pip', 'install', '-r', req_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                # Try with --user flag
                print("  Trying with --user flag...")
                result = subprocess.run(
                    [python_exe, '-m', 'pip', 'install', '--user', '-r', req_file],
                    capture_output=True,
                    text=True
                )
                
            if result.returncode != 0:
                # Try with --break-system-packages for newer systems
                print("  Trying with --break-system-packages...")
                result = subprocess.run(
                    [python_exe, '-m', 'pip', 'install', '--break-system-packages', '-r', req_file],
                    capture_output=True,
                    text=True
                )
                
            if result.returncode == 0:
                print("✓ Dependencies installed successfully")
                return True
            else:
                print("❌ Failed to install dependencies")
                print(f"   Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False
    
    def _create_mcp_config(self):
        """Create or update MCP configuration"""
        print("\nConfiguring MCP server...")
        
        # Determine config location
        if self.system == "Windows" or self.is_wsl:
            # Check for Claude Code config location
            config_dirs = [
                os.path.expanduser("~/AppData/Roaming/Claude/claude.json"),
                os.path.expanduser("~/.config/claude/claude.json"),
                os.path.join(self.project_dir, "mcp.json")
            ]
        else:
            config_dirs = [
                os.path.expanduser("~/.config/claude/claude.json"),
                os.path.join(self.project_dir, "mcp.json")
            ]
        
        # Find existing config or create new one
        config_file = None
        for path in config_dirs:
            if os.path.exists(path):
                config_file = path
                break
                
        if not config_file:
            # Create in project directory
            config_file = os.path.join(self.project_dir, "mcp.json")
            
        # Load or create config
        config = {"mcpServers": {}}
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            except:
                pass
        
        # Add comfy-guru server configuration
        python_exe = self._find_python()
        server_script = os.path.join(self.project_dir, "src", "standalone_mcp_server.py")
        
        config["mcpServers"]["comfy-guru"] = {
            "command": python_exe,
            "args": [server_script]
        }
        
        # Save config
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
        print(f"✓ MCP configuration saved to: {config_file}")
        return config_file
    
    def _test_server(self):
        """Test if the server can start"""
        print("\nTesting server...")
        
        python_exe = self._find_python()
        server_script = os.path.join(self.project_dir, "src", "standalone_mcp_server.py")
        
        try:
            # Test import
            result = subprocess.run(
                [python_exe, '-c', 'import fastmcp; print("✓ FastMCP imported successfully")'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(result.stdout.strip())
            else:
                print("❌ Failed to import fastmcp")
                return False
                
            # Test server startup
            print("  Testing server startup...")
            result = subprocess.run(
                [python_exe, server_script],
                capture_output=True,
                text=True,
                timeout=3
            )
            
        except subprocess.TimeoutExpired:
            # This is expected - server runs indefinitely
            print("✓ Server starts successfully")
            return True
        except Exception as e:
            print(f"❌ Server test failed: {e}")
            return False
            
        return True
    
    def _create_activation_script(self):
        """Create easy activation scripts"""
        print("\nCreating activation scripts...")
        
        python_exe = self._find_python()
        
        # Create run script for different platforms
        if self.system == "Windows":
            # Windows batch file
            script_path = os.path.join(self.project_dir, "run_server.bat")
            content = f"""@echo off
echo Starting ComfyUI Log Debugger MCP Server...
"{python_exe}" "{os.path.join(self.project_dir, 'standalone_mcp_server.py')}"
pause
"""
            with open(script_path, 'w') as f:
                f.write(content)
            print(f"✓ Created: {script_path}")
            
        # Unix shell script (works for Linux, Mac, WSL)
        script_path = os.path.join(self.project_dir, "run_server.sh")
        content = f"""#!/bin/bash
echo "Starting ComfyUI Log Debugger MCP Server..."
"{python_exe}" "{os.path.join(self.project_dir, 'standalone_mcp_server.py')}"
"""
        with open(script_path, 'w') as f:
            f.write(content)
        os.chmod(script_path, 0o755)
        print(f"✓ Created: {script_path}")
    
    def install(self):
        """Run the complete installation"""
        print("ComfyUI Log Debugger MCP Server - Installation")
        print("=" * 50)
        
        # Check Python version
        if not self._check_python_version():
            return False
            
        # Install dependencies
        if not self._install_dependencies():
            print("\n⚠️  Failed to install dependencies automatically.")
            print("Please install manually:")
            print(f"  {self._find_python()} -m pip install fastmcp")
            
        # Create MCP configuration
        config_file = self._create_mcp_config()
        
        # Test server
        if self._test_server():
            print("\n✅ Installation completed successfully!")
        else:
            print("\n⚠️  Installation completed with warnings")
            
        # Create activation scripts
        self._create_activation_script()
        
        # Print usage instructions
        print("\n" + "="*50)
        print("USAGE INSTRUCTIONS")
        print("="*50)
        print("\n1. For Claude Code to use this MCP server:")
        print(f"   - Config file: {config_file}")
        print("   - Restart Claude Code to load the new configuration")
        print("\n2. To run the server manually:")
        print(f"   - {self._find_python()} standalone_mcp_server.py")
        print("\n3. To test discovery:")
        print(f"   - {self._find_python()} smart_log_discovery.py")
        
        return True


def main():
    """Main installation entry point"""
    installer = MCPInstaller()
    
    try:
        success = installer.install()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()