#!/usr/bin/env python3
"""
Build script to create a .dxt desktop extension file for Claude Desktop
"""
import os
import json
import zipfile
import shutil
from pathlib import Path
import sys

def create_extension():
    """Create the .dxt extension file"""
    print("Building ComfyUI Log Debugger Desktop Extension...")
    
    # Project root directory
    root_dir = Path(__file__).parent
    
    # Create build directory
    build_dir = root_dir / "build"
    build_dir.mkdir(exist_ok=True)
    
    # Extension staging directory
    staging_dir = build_dir / "comfy-guru-extension"
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir()
    
    # Copy manifest.json to root
    manifest_src = root_dir / "extension" / "manifest.json"
    manifest_dst = staging_dir / "manifest.json"
    if manifest_src.exists():
        shutil.copy2(manifest_src, manifest_dst)
        print(f"  Added: manifest.json")
    else:
        print("  ERROR: manifest.json not found!")
        return None
    
    # Create server directory and copy Python files
    server_dir = staging_dir / "server"
    server_dir.mkdir(exist_ok=True)
    
    # Python server files to include
    python_files = [
        ("src/standalone_mcp_server.py", "server/standalone_mcp_server.py"),
        ("src/debugger_server.py", "server/debugger_server.py"),
        ("src/simple_active_discovery.py", "server/simple_active_discovery.py"),
        ("src/error_patterns.json", "server/error_patterns.json"),
        ("src/server_launcher.py", "server/server_launcher.py"),
        ("src/windows_launcher.bat", "server/windows_launcher.bat"),
        ("src/minimal_test_server.py", "server/minimal_test_server.py"),
        ("src/start_server.bat", "server/start_server.bat"),
        ("src/setup_lib.bat", "server/setup_lib.bat"),
        ("src/setup_lib.py", "server/setup_lib.py"),
    ]
    
    for src, dst in python_files:
        src_path = root_dir / src
        dst_path = staging_dir / dst
        if src_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)
            print(f"  Added: {dst}")
        else:
            print(f"  Warning: {src} not found, skipping...")
    
    # Create server/lib directory for dependencies (empty, will be populated on first run)
    lib_dir = staging_dir / "server" / "lib"
    lib_dir.mkdir(exist_ok=True)
    print("  Created: server/lib (dependencies will be installed on first run)")
    
    # Copy icon if it exists
    icon_src = root_dir / "docs" / "Images" / "Comfy-Guru.png"
    icon_dst = staging_dir / "icon.png"
    if icon_src.exists():
        shutil.copy2(icon_src, icon_dst)
        print(f"  Added: icon.png")
    
    # Copy optional files
    optional_files = [
        ("requirements.txt", "requirements.txt"),
        ("README.md", "README.md"),
        ("LICENSE", "LICENSE")
    ]
    
    for src, dst in optional_files:
        src_path = root_dir / src
        dst_path = staging_dir / dst
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            print(f"  Added: {dst}")
    
    # Create the .dxt file (ZIP archive)
    dxt_file = build_dir / "comfy-guru.dxt"
    
    print(f"\nCreating extension archive: {dxt_file.name}")
    
    with zipfile.ZipFile(dxt_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(staging_dir):
            for file in files:
                file_path = Path(root) / file
                arc_name = file_path.relative_to(staging_dir)
                zf.write(file_path, arc_name)
                print(f"  Compressed: {arc_name}")
    
    # Clean up staging directory
    shutil.rmtree(staging_dir)
    
    # Get file size
    size_mb = dxt_file.stat().st_size / (1024 * 1024)
    
    print(f"\n✅ Extension built successfully!")
    print(f"📦 File: {dxt_file}")
    print(f"📏 Size: {size_mb:.2f} MB")
    print(f"\n🚀 To install in Claude Desktop:")
    print(f"   1. Open Claude Desktop")
    print(f"   2. Go to Settings > Extensions")
    print(f"   3. Click 'Install Extension'")
    print(f"   4. Select: {dxt_file.absolute()}")
    
    return dxt_file

def verify_extension(dxt_file):
    """Verify the extension file is valid"""
    print(f"\nVerifying extension...")
    
    try:
        with zipfile.ZipFile(dxt_file, 'r') as zf:
            # Check for manifest.json
            if 'manifest.json' not in zf.namelist():
                print("❌ Error: manifest.json not found in root")
                return False
            
            # Validate manifest
            with zf.open('manifest.json') as f:
                manifest = json.load(f)
                required_fields = ['dxt_version', 'name', 'description', 'version', 'author', 'server']
                for field in required_fields:
                    if field not in manifest:
                        print(f"❌ Error: Required field '{field}' missing from manifest")
                        return False
                
                # Validate dxt_version
                if manifest.get('dxt_version') != '0.1':
                    print(f"❌ Error: dxt_version must be '0.1', got '{manifest.get('dxt_version')}'")
                    return False
                
                # Validate author is an object with name
                if not isinstance(manifest.get('author'), dict) or 'name' not in manifest['author']:
                    print("❌ Error: 'author' must be an object with 'name' field")
                    return False
                
                # Validate server has required fields
                server = manifest.get('server', {})
                if 'type' not in server:
                    print("❌ Error: 'server.type' is required")
                    return False
                
                # For stdio type servers, command and args are required
                if server['type'] == 'stdio':
                    if 'command' not in server:
                        print("❌ Error: 'server.command' is required for stdio type servers")
                        return False
                    if 'args' not in server:
                        print("❌ Error: 'server.args' is required for stdio type servers")
                        return False
                else:
                    if 'entry_point' not in server:
                        print("❌ Error: 'server.entry_point' is required")
                        return False
            
            print("✅ Extension verified successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error verifying extension: {e}")
        return False

if __name__ == "__main__":
    try:
        dxt_file = create_extension()
        if verify_extension(dxt_file):
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)