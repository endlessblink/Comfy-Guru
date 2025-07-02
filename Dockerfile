# ComfyUI Log Debugger MCP Server
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY src/ ./src/
COPY install.py .
COPY test_installation.py .

# Create volume mount points for Windows access
# These will be mounted to Windows drives
VOLUME ["/mnt/c", "/mnt/d", "/mnt/e"]

# Expose MCP server port (stdio mode doesn't need ports, but useful for future HTTP mode)
EXPOSE 8765

# Default to running the MCP server
CMD ["python", "src/standalone_mcp_server.py"]