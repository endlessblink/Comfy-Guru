#!/bin/bash
#
# Test the desktop extension in Docker
#

echo "🐳 Testing ComfyUI Log Debugger Desktop Extension"
echo "================================================"
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Build the test image
echo "📦 Building test Docker image..."
docker build -f test/Dockerfile.test -t comfy-guru-test . || {
    echo "❌ Failed to build Docker image"
    exit 1
}

echo
echo "🧪 Running extension tests..."
echo

# Run the tests
docker run --rm comfy-guru-test

# Capture exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo
    echo "✅ Extension test completed successfully!"
    echo "The .dxt file is ready for distribution."
else
    echo
    echo "❌ Extension test failed. Please check the errors above."
fi

exit $EXIT_CODE