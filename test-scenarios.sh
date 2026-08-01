#!/bin/bash
# Test scenarios for WiFi Network Security Analyzer

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "=============================================="
echo "WiFi Security Analyzer - Test Scenarios"
echo "=============================================="
echo -e "${NC}"
echo ""

# Check if image exists
if ! docker images | grep -q wifi-analyzer; then
    echo -e "${RED}[!] Image not found. Building...${NC}"
    docker build -t wifi-analyzer:latest .
    echo -e "${GREEN}[+] Image built${NC}"
fi

# Create output directory
mkdir -p output
chmod 777 output

echo -e "${YELLOW}[*] Test environments available:${NC}"
echo ""

# Scenario 1: Help
echo -e "${BLUE}Scenario 1: Show Help${NC}"
echo "Command:"
echo "  docker run --rm wifi-analyzer:latest -h"
echo ""
read -p "Run? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker run --rm wifi-analyzer:latest -h
fi
echo ""

# Scenario 2: Invalid target
echo -e "${BLUE}Scenario 2: Test Invalid Target (Error Handling)${NC}"
echo "Command:"
echo "  docker run --rm wifi-analyzer:latest invalid.target"
echo "Expected: Error message about invalid format"
echo ""
read -p "Run? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker run --rm wifi-analyzer:latest invalid.target 2>&1 || true
fi
echo ""

# Scenario 3: Localhost scan
echo -e "${BLUE}Scenario 3: Scan Localhost (Quick Test)${NC}"
echo "Command:"
echo "  docker run --rm --privileged --network host \\"
echo "    -v \$(pwd)/output:/output \\"
echo "    wifi-analyzer:latest 127.0.0.1"
echo ""
echo "Note: This scans your loopback interface"
echo "Expected: Quick scan with minimal results"
echo ""
read -p "Run? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker run --rm --privileged --network host \
      -v $(pwd)/output:/output \
      wifi-analyzer:latest 127.0.0.1
fi
echo ""

# Scenario 4: Your network (requires authorization)
echo -e "${BLUE}Scenario 4: Scan Your Network (REQUIRES AUTHORIZATION)${NC}"
echo ""
echo -e "${YELLOW}[!] IMPORTANT: Only proceed if you have authorization to scan this network!${NC}"
echo ""
read -p "Enter target network (e.g., 192.168.1.0/24) or press Enter to skip: " target_network

if [ ! -z "$target_network" ]; then
    echo ""
    echo -e "${YELLOW}[*] Starting scan of: $target_network${NC}"
    echo "This may take several minutes..."
    echo ""
    
    docker run --rm --privileged --network host \
      -v $(pwd)/output:/output \
      wifi-analyzer:latest "$target_network"
    
    echo ""
    echo -e "${GREEN}[+] Scan complete!${NC}"
fi
echo ""

# Scenario 5: View reports
echo -e "${BLUE}Scenario 5: View Generated Reports${NC}"
if ls output/wifi_analysis_*.json 1> /dev/null 2>&1; then
    echo -e "${GREEN}[+] Found reports:${NC}"
    ls -lah output/wifi_analysis_*.json
    echo ""
    echo -e "${YELLOW}[*] Vulnerabilities found:${NC}"
    jq '.vulnerabilities' output/wifi_analysis_*.json 2>/dev/null | head -20 || echo "No JSON parsing available"
else
    echo -e "${YELLOW}[*] No reports found yet. Run a scan first.${NC}"
fi
echo ""

# Scenario 6: Docker Compose
echo -e "${BLUE}Scenario 6: Using Docker Compose${NC}"
echo "Commands:"
echo "  # Build"
echo "  docker-compose build"
echo ""
echo "  # Run with default target (192.168.1.0/24)"
echo "  docker-compose run --rm wifi-analyzer"
echo ""
echo "  # Run with custom target"
echo "  docker-compose run --rm wifi-analyzer 10.0.0.0/24"
echo ""
echo "  # Run with all options"
echo "  docker-compose run --rm wifi-analyzer 192.168.1.0/24 -c -a"
echo ""

# Scenario 7: Analysis tips
echo -e "${BLUE}Scenario 7: Report Analysis Tips${NC}"
cat << 'EOF'

View all vulnerabilities:
  jq '.vulnerabilities' output/wifi_analysis_*.json

Count by risk level:
  jq '.vulnerabilities[] | .risk_level' output/wifi_analysis_*.json | sort | uniq -c

Find CRITICAL issues:
  jq '.vulnerabilities[] | select(.risk_level=="CRITICAL")' output/wifi_analysis_*.json

View all services found:
  jq '.nmap_results.services' output/wifi_analysis_*.json

Count open services:
  jq '.nmap_results.services[] | select(.state=="open") | .service' output/wifi_analysis_*.json | sort | uniq -c

Pretty print report:
  cat output/wifi_analysis_*.json | jq '.'

Export to CSV (vulnerabilities):
  jq -r '.vulnerabilities[] | [.service, .port, .risk_level, .description] | @csv' output/wifi_analysis_*.json

EOF
echo ""

# Scenario 8: Cleanup
echo -e "${BLUE}Scenario 8: Cleanup${NC}"
echo "To remove all outputs:"
echo "  rm -rf output/wifi_analysis_*.json"
echo ""
echo "To remove Docker image:"
echo "  docker rmi wifi-analyzer:latest"
echo ""
echo "To remove all images and containers:"
echo "  docker system prune -a"
echo ""

# Summary
echo -e "${BLUE}=============================================="
echo "Test Scenarios Complete"
echo "=============================================="
echo -e "${NC}"
echo ""
echo "Next steps:"
echo "1. Review reports in ./output/ directory"
echo "2. Analyze vulnerabilities with jq"
echo "3. Follow up on critical findings"
echo "4. Document and remediate issues"
echo ""
