#!/bin/bash
# Quick start script for WiFi Network Analyzer

set -e

echo "=========================================="
echo "WiFi Network Security Analyzer - Quick Start"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker daemon is not running"
    exit 1
fi

# Build the image
echo "[*] Building WiFi Analyzer image..."
docker build -t wifi-analyzer:latest .
echo "[+] Build complete!"
echo ""

# Create output directory
mkdir -p output
chmod 777 output

echo "[*] Image built successfully!"
echo ""
echo "Usage Examples:"
echo "==============="
echo ""
echo "1. Basic scan:"
echo "   docker run --rm --privileged --network host \\"
echo "     -v \$(pwd)/output:/output \\"
echo "     wifi-analyzer:latest 192.168.1.0/24"
echo ""
echo "2. Scan with credential testing:"
echo "   docker run --rm --privileged --network host \\"
echo "     -v \$(pwd)/output:/output \\"
echo "     wifi-analyzer:latest 192.168.1.0/24 -c"
echo ""
echo "3. Aggressive scan with full analysis:"
echo "   docker run --rm --privileged --network host \\"
echo "     -v \$(pwd)/output:/output \\"
echo "     wifi-analyzer:latest 192.168.1.0/24 -a -c"
echo ""
echo "4. Using Docker Compose:"
echo "   docker-compose run --rm wifi-analyzer 192.168.1.0/24"
echo ""
echo "Reports will be saved in ./output/ directory"
echo ""
echo "=========================================="
