#!/usr/bin/env python3
"""
WiFi Network Security Analyzer - Standalone Version
Works immediately without waiting for Docker build
"""

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

# Vulnerability database (works locally without nmap)
VULNERABILITIES_DB = {
    "telnet": {
        "port": 23,
        "risk": "CRITICAL",
        "reason": "Unencrypted protocol - all traffic in plaintext including credentials"
    },
    "ftp": {
        "port": 21,
        "risk": "HIGH",
        "reason": "Unencrypted file transfer - use SFTP or SCP instead"
    },
    "http": {
        "port": 80,
        "risk": "MEDIUM",
        "reason": "Unencrypted web traffic - use HTTPS (port 443) instead"
    },
    "smtp": {
        "port": 25,
        "risk": "MEDIUM",
        "reason": "Email without encryption - verify TLS is enabled"
    },
    "mysql": {
        "port": 3306,
        "risk": "HIGH",
        "reason": "Database exposed to network - should be firewalled"
    },
    "rdp": {
        "port": 3389,
        "risk": "CRITICAL",
        "reason": "Remote Desktop exposed - high brute-force target"
    },
    "smb": {
        "port": 445,
        "risk": "CRITICAL",
        "reason": "SMB exposure - ransomware and lateral movement risk"
    },
    "ssh": {
        "port": 22,
        "risk": "LOW",
        "reason": "SSH generally secure if patched - verify version and disable root login"
    }
}

class WiFiAnalyzerStandalone:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_sample_report(self, target):
        """Generate a realistic sample report"""
        report = {
            "scan_time": self.timestamp,
            "target": target,
            "scan_type": "SAMPLE_DATA",
            "note": "This is sample data. Run actual Docker scan for real results.",
            "sample_vulnerabilities": [
                {
                    "service": "telnet",
                    "port": 23,
                    "risk_level": "CRITICAL",
                    "description": VULNERABILITIES_DB["telnet"]["reason"],
                    "recommendation": "Disable telnet. Use SSH instead."
                },
                {
                    "service": "ftp",
                    "port": 21,
                    "risk_level": "HIGH",
                    "description": VULNERABILITIES_DB["ftp"]["reason"],
                    "recommendation": "Replace with SFTP or SCP"
                },
                {
                    "service": "http",
                    "port": 80,
                    "risk_level": "MEDIUM",
                    "description": VULNERABILITIES_DB["http"]["reason"],
                    "recommendation": "Redirect to HTTPS only"
                },
                {
                    "service": "mysql",
                    "port": 3306,
                    "risk_level": "HIGH",
                    "description": VULNERABILITIES_DB["mysql"]["reason"],
                    "recommendation": "Firewall database access to trusted IPs only"
                },
                {
                    "service": "rdp",
                    "port": 3389,
                    "risk_level": "CRITICAL",
                    "description": VULNERABILITIES_DB["rdp"]["reason"],
                    "recommendation": "Use VPN for remote access, disable public RDP"
                },
                {
                    "service": "smb",
                    "port": 445,
                    "risk_level": "CRITICAL",
                    "description": VULNERABILITIES_DB["smb"]["reason"],
                    "recommendation": "Block SMB from internet, use VPN for access"
                }
            ],
            "sample_services": [
                {"port": 22, "service": "ssh", "state": "open"},
                {"port": 80, "service": "http", "state": "open"},
                {"port": 443, "service": "https", "state": "open"},
                {"port": 3306, "service": "mysql", "state": "open"},
                {"port": 3389, "service": "rdp", "state": "open"}
            ],
            "summary": {
                "total_services": 5,
                "critical_vulnerabilities": 2,
                "high_vulnerabilities": 2,
                "medium_vulnerabilities": 1,
                "low_vulnerabilities": 0
            },
            "how_to_run_real_scan": {
                "step_1_wait": "Wait for Docker image to build (docker images | grep wifi-analyzer)",
                "step_2_run": "docker run --rm --privileged --network host -v $(pwd)/output:/output wifi-analyzer:latest 192.168.1.0/24",
                "step_3_view": "cat output/wifi_analysis_*.json"
            }
        }
        return report
    
    def save_report(self, target):
        """Save sample report"""
        report = self.generate_sample_report(target)
        filename = f"{self.output_dir}/wifi_analysis_SAMPLE_{self.timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filename
    
    def run(self, target):
        """Run the analyzer"""
        print("\n" + "="*80)
        print("WiFi NETWORK SECURITY ANALYZER - Standalone Demo")
        print("="*80 + "\n")
        
        print(f"Target: {target}")
        print(f"Timestamp: {self.timestamp}\n")
        
        filename = self.save_report(target)
        print(f"[+] Sample report generated: {filename}\n")
        
        print("="*80)
        print("IMPORTANT: This is SAMPLE DATA")
        print("="*80)
        print("\nTo run REAL scans:\n")
        print("1. Wait for Docker image (5-10 minutes):")
        print("   docker images | grep wifi-analyzer\n")
        print("2. Run the actual scanner:")
        print("   docker run --rm --privileged --network host \\")
        print("     -v $(pwd)/output:/output \\")
        print("     wifi-analyzer:latest 192.168.1.0/24\n")
        print("3. Add options:")
        print("   -c : Test credentials")
        print("   -a : Aggressive scan\n")
        
        print("="*80)
        print("Documentation:")
        print("="*80)
        print("\nRead these files:")
        print("  - README.md")
        print("  - USAGE_GUIDE.md")
        print("  - PROJECT_SUMMARY.md\n")
        
        # Load and display the report
        with open(filename, 'r') as f:
            report = json.load(f)
        
        print("="*80)
        print("SAMPLE VULNERABILITIES DETECTED")
        print("="*80 + "\n")
        
        for vuln in report["sample_vulnerabilities"]:
            print(f"[{vuln['risk_level']}] Port {vuln['port']}/{vuln['service']}")
            print(f"  -> {vuln['description']}")
            print(f"  [*] Fix: {vuln['recommendation']}\n")
        
        print("="*80)
        print(f"\nReport saved to: {filename}")
        print("\n" + "="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="WiFi Network Security Analyzer - Standalone Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  
  # Demo scan
  python wifi_analyzer_standalone.py 192.168.1.0/24
  
  # Once Docker is ready, use the real tool:
  docker run --rm --privileged --network host \\
    -v $(pwd)/output:/output \\
    wifi-analyzer:latest 192.168.1.0/24 -c -a
        """
    )
    
    parser.add_argument(
        "target",
        nargs="?",
        default="192.168.1.0/24",
        help="Target network (default: 192.168.1.0/24)"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="Output directory (default: output)"
    )
    
    args = parser.parse_args()
    
    analyzer = WiFiAnalyzerStandalone(args.output)
    analyzer.run(args.target)


if __name__ == "__main__":
    main()
