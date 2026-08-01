#!/usr/bin/env python3
"""
WiFi Network Security Analyzer - Quick Test Version
This is a lightweight version that works immediately without Docker
"""

import subprocess
import json
import argparse
import sys
import os
from datetime import datetime
import io

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def run_quick_test():
    """Run a quick test to verify nmap is available"""
    print("=" * 70)
    print("WiFi NETWORK SECURITY ANALYZER - QUICK TEST")
    print("=" * 70)
    print()
    
    # Test 1: Check Python
    print("[*] Python Version:")
    print(f"    {sys.version}")
    print()
    
    # Test 2: Check Nmap
    print("[*] Checking Nmap...")
    try:
        result = subprocess.run(["nmap", "-V"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"    [+] Nmap installed")
            print(f"    {result.stdout.split(chr(10))[0]}")
        else:
            print("    [-] Nmap not found or error")
    except FileNotFoundError:
        print("    [-] Nmap not found - need to install or run in Docker")
    except Exception as e:
        print(f"    [-] Error: {e}")
    print()
    
    # Test 3: Check Hydra
    print("[*] Checking Hydra...")
    try:
        result = subprocess.run(["hydra", "-h"], capture_output=True, text=True, timeout=5)
        if "Hydra" in result.stdout or "hydra" in result.stdout:
            print("    [+] Hydra installed")
        else:
            print("    [-] Hydra output unclear")
    except FileNotFoundError:
        print("    [-] Hydra not found - need to install or run in Docker")
    except Exception as e:
        print(f"    [-] Error: {e}")
    print()
    
    # Test 4: Create sample report
    print("[*] Creating sample report...")
    os.makedirs("output", exist_ok=True)
    
    sample_report = {
        "scan_time": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "target": "192.168.1.0/24",
        "status": "SAMPLE_DATA",
        "message": "This is sample data. Run actual scan once Docker image is ready.",
        "vulnerabilities": [
            {
                "service": "telnet",
                "port": "23",
                "risk_level": "CRITICAL",
                "description": "Unencrypted protocol - credentials transmitted in plaintext"
            },
            {
                "service": "ftp",
                "port": "21",
                "risk_level": "HIGH",
                "description": "File transfer unencrypted - use SFTP instead"
            },
            {
                "service": "http",
                "port": "80",
                "risk_level": "MEDIUM",
                "description": "Web traffic unencrypted - use HTTPS"
            }
        ],
        "nmap_results": {
            "example_services": [
                {"port": "22", "service": "ssh", "state": "open"},
                {"port": "80", "service": "http", "state": "open"},
                {"port": "443", "service": "https", "state": "open"}
            ]
        }
    }
    
    report_file = f"output/sample_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(sample_report, f, indent=2)
    
    print(f"    [+] Sample report created: {report_file}")
    print()
    
    # Test 5: Show status
    print("=" * 70)
    print("STATUS SUMMARY")
    print("=" * 70)
    print()
    print("📊 Docker Image Build Status:")
    try:
        result = subprocess.run(["docker", "images"], capture_output=True, text=True, timeout=5)
        if "wifi-analyzer" in result.stdout:
            print("    [+] wifi-analyzer image is READY")
            print("    Status: BUILD COMPLETE - Ready to use!")
        else:
            print("    [*] wifi-analyzer image still building...")
            print("    Status: Building (5-10 minutes typical)")
            print("    Check back in a few minutes")
    except FileNotFoundError:
        print("    [-] Docker not found - please install Docker Desktop")
    except Exception as e:
        print(f"    [?] Could not check: {e}")
    print()
    
    print("📝 Next Steps:")
    print("    1. Wait for Docker image to complete building")
    if sys.platform == "win32":
        print("    2. Check: docker images | findstr wifi-analyzer")
        print("    3. Run: docker run --rm --privileged --network host ^")
        print("            -v %cd%/output:/output ^")
        print("            wifi-analyzer:latest 192.168.1.0/24")
    else:
        print("    2. Check: docker images | grep wifi-analyzer")
        print("    3. Run: docker run --rm --privileged --network host \\")
        print("            -v $(pwd)/output:/output \\")
        print("            wifi-analyzer:latest 192.168.1.0/24")
    print()
    
    print("=" * 70)
    print()


def main():
    parser = argparse.ArgumentParser(description="WiFi Analyzer - Quick Test")
    parser.add_argument("-t", "--test", action="store_true", help="Run test")
    parser.add_argument("-s", "--status", action="store_true", help="Check status")
    parser.add_argument("-r", "--report", action="store_true", help="Show sample report")
    
    args = parser.parse_args()
    
    if args.test or (not args.status and not args.report):
        run_quick_test()
    
    if args.status:
        print("Checking Docker status...")
        if sys.platform == "win32":
            os.system("docker images | findstr wifi-analyzer")
        else:
            os.system("docker images | grep wifi-analyzer")
    
    if args.report:
        print("Sample report location: output/")
        if sys.platform == "win32":
            os.system("dir output/")
        else:
            os.system("ls -la output/")


if __name__ == "__main__":
    main()
