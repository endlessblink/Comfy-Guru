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
    
    # Files and directories to include
    include_items = [
        "extension/manifest.json",
        "src/standalone_mcp_server.py",
        "src/debugger_server.py", 
        "src/simple_active_discovery.py",
        "src/error_patterns.json",
        "docs/Images/Comfy-Guru.png",
        "requirements.txt",
        "README.md",
        "LICENSE"
    ]
    
    # Copy files to staging directory
    for item in include_items:
        src_path = root_dir / item
        if src_path.exists():
            # Create directory structure in staging
            dst_path = staging_dir / item
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            if src_path.is_file():
                shutil.copy2(src_path, dst_path)
                print(f"  Added: {item}")
            else:
                shutil.copytree(src_path, dst_path)
                print(f"  Added directory: {item}")
        else:
            print(f"  Warning: {item} not found, skipping...")
    
    # Move manifest.json to root of staging directory
    manifest_src = staging_dir / "extension" / "manifest.json"
    manifest_dst = staging_dir / "manifest.json"
    if manifest_src.exists():
        shutil.move(str(manifest_src), str(manifest_dst))
        # Remove empty extension directory
        (staging_dir / "extension").rmdir()
    
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
                required_fields = ['name', 'description', 'version', 'runtime', 'main']
                for field in required_fields:
                    if field not in manifest:
                        print(f"❌ Error: Required field '{field}' missing from manifest")
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