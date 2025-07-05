#!/usr/bin/env python3
"""
Test script to validate the desktop extension works correctly
"""
import json
import sys
import os
import subprocess
import asyncio
from pathlib import Path

def test_manifest():
    """Test that manifest.json is valid"""
    print("✓ Testing manifest.json...")
    
    manifest_path = Path("/test/extension/manifest.json")
    if not manifest_path.exists():
        print("✗ manifest.json not found!")
        return False
    
    try:
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        # Check required fields
        required = ['name', 'description', 'version', 'runtime', 'main']
        for field in required:
            if field not in manifest:
                print(f"✗ Missing required field: {field}")
                return False
        
        print(f"  Name: {manifest['name']}")
        print(f"  Version: {manifest['version']}")
        print(f"  Runtime: {manifest['runtime']}")
        print(f"  Main: {manifest['main']}")
        
        # Verify main file exists
        main_file = Path("/test/extension") / manifest['main']
        if not main_file.exists():
            print(f"✗ Main file not found: {manifest['main']}")
            return False
            
        print("✓ Manifest is valid!")
        return True
        
    except Exception as e:
        print(f"✗ Error reading manifest: {e}")
        return False

def test_dependencies():
    """Test that all Python dependencies can be imported"""
    print("\n✓ Testing dependencies...")
    
    try:
        import mcp
        print("  ✓ mcp imported successfully")
        
        import aiofiles
        print("  ✓ aiofiles imported successfully")
        
        import psutil
        print("  ✓ psutil imported successfully")
        
        import watchdog
        print("  ✓ watchdog imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Failed to import dependency: {e}")
        return False

def test_server_syntax():
    """Test that the server files have valid Python syntax"""
    print("\n✓ Testing Python syntax...")
    
    python_files = [
        "/test/extension/src/standalone_mcp_server.py",
        "/test/extension/src/debugger_server.py",
        "/test/extension/src/simple_active_discovery.py"
    ]
    
    for file_path in python_files:
        if not Path(file_path).exists():
            print(f"✗ File not found: {file_path}")
            return False
            
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", file_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"✗ Syntax error in {file_path}:")
            print(result.stderr)
            return False
        else:
            print(f"  ✓ {Path(file_path).name} - syntax OK")
    
    return True

async def test_server_startup():
    """Test that the MCP server can start"""
    print("\n✓ Testing server startup...")
    
    # Set required environment variables
    env = os.environ.copy()
    env.update({
        'COMFYUI_PATH': '/tmp/test_comfyui',
        'ENABLE_REALTIME': 'false',
        'LOG_RETENTION_DAYS': '7'
    })
    
    # Create a test ComfyUI directory
    test_dir = Path('/tmp/test_comfyui')
    test_dir.mkdir(exist_ok=True)
    (test_dir / 'comfyui.log').write_text('Test log entry\n')
    
    try:
        # Start the server process
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            '/test/extension/src/standalone_mcp_server.py',
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait a bit for startup
        await asyncio.sleep(2)
        
        # Check if process is still running
        if proc.returncode is not None:
            stdout, stderr = await proc.communicate()
            # Server exiting with code 0 is expected for stdio transport
            if proc.returncode == 0 and "Starting MCP server" in stderr.decode():
                print("  ✓ Server started and exited normally (stdio transport)")
                return True
            else:
                print(f"✗ Server exited with code {proc.returncode}")
                if stderr:
                    print(f"  Error: {stderr.decode()}")
                return False
        
        print("  ✓ Server started successfully")
        
        # Terminate the server
        proc.terminate()
        await proc.wait()
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to start server: {e}")
        return False

def test_file_structure():
    """Test that all expected files are present"""
    print("\n✓ Testing file structure...")
    
    expected_files = [
        "manifest.json",
        "src/standalone_mcp_server.py",
        "src/debugger_server.py",
        "src/simple_active_discovery.py",
        "src/error_patterns.json",
        "requirements.txt",
        "README.md"
    ]
    
    base_path = Path("/test/extension")
    
    for file_path in expected_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ Missing: {file_path}")
            return False
    
    return True

async def main():
    """Run all tests"""
    print("🧪 Testing ComfyUI Log Debugger Desktop Extension")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Manifest", test_manifest),
        ("Dependencies", test_dependencies),
        ("Python Syntax", test_server_syntax),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Run async test
    try:
        startup_result = await test_server_startup()
        results.append(("Server Startup", startup_result))
    except Exception as e:
        print(f"✗ Server Startup failed with exception: {e}")
        results.append(("Server Startup", False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:<20} {status}")
    
    print("=" * 50)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Extension is ready for use.")
        return 0
    else:
        print(f"\n❌ {total - passed} tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)