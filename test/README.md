# Testing the Desktop Extension

This directory contains tests to validate the ComfyUI Log Debugger desktop extension (.dxt file).

## Quick Test

Run the automated test suite:

```bash
./test-extension.sh
```

## What It Tests

The test suite validates:

1. **File Structure** - All required files are present in the .dxt
2. **Manifest Validation** - manifest.json has all required fields
3. **Dependencies** - All Python packages can be imported
4. **Syntax Check** - All Python files have valid syntax
5. **Server Startup** - The MCP server can initialize without errors

## Manual Docker Test

To run tests manually:

```bash
# Build test image
docker build -f test/Dockerfile.test -t comfy-guru-test .

# Run tests
docker run --rm comfy-guru-test

# Interactive testing
docker run --rm -it comfy-guru-test bash
```

## Test Output

A successful test run looks like:

```
🧪 Testing ComfyUI Log Debugger Desktop Extension
==================================================

✓ Testing file structure...
  ✓ manifest.json
  ✓ src/standalone_mcp_server.py
  ✓ requirements.txt
  ...

✓ Testing manifest.json...
  Name: ComfyUI Log Debugger
  Version: 1.0.0
  Runtime: python
  Main: src/standalone_mcp_server.py

📊 Test Summary:
==================================================
File Structure       ✓ PASS
Manifest            ✓ PASS
Dependencies        ✓ PASS
Python Syntax       ✓ PASS
Server Startup      ✓ PASS
==================================================
Total: 5/5 tests passed

🎉 All tests passed! Extension is ready for use.
```

## Continuous Integration

You can add this to your CI/CD pipeline:

```yaml
# .github/workflows/test-extension.yml
name: Test Desktop Extension

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test Extension
        run: ./test-extension.sh
```