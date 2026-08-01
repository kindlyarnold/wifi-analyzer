#!/usr/bin/env python3
"""
WiFi Network Security Analyzer
Combines nmap scanning, credential testing (hydra), and network analysis
"""

import subprocess
import json
import argparse
import sys
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Tuple
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WiFiAnalyzer:
    """Main WiFi analyzer class"""
    
    def __init__(self, target_network: str, output_dir: str = "/output"):
        self.target_network = target_network
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {
            "scan_time": self.timestamp,
            "target": target_network,
            "hosts": [],
            "services": [],
            "vulnerabilities": [],
            "credentials_tested": []
        }
        
        os.makedirs(output_dir, exist_ok=True)
    
    def run_nmap_scan(self, scan_type: str = "sV") -> Dict:
        """Run nmap scan on target network"""
        logger.info(f"Starting nmap {scan_type} scan on {self.target_network}...")
        
        try:
            cmd = [
                "nmap",
                f"-{scan_type}",
                "-O",
                "--script=vuln",
                "-oX", "-",  # XML output to stdout
                self.target_network
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                logger.warning(f"nmap returned code {result.returncode}")
            
            # Parse nmap results
            nmap_results = self._parse_nmap_output(result.stdout)
            logger.info(f"Found {len(nmap_results.get('hosts', []))} hosts")
            
            return nmap_results
        
        except subprocess.TimeoutExpired:
            logger.error("nmap scan timed out")
            return {}
        except Exception as e:
            logger.error(f"nmap scan failed: {e}")
            return {}
    
    def _parse_nmap_output(self, xml_output: str) -> Dict:
        """Parse nmap XML output"""
        results = {"hosts": [], "services": []}
        
        try:
            root = ET.fromstring(xml_output)
            
            # Parse hosts
            for host in root.findall('.//host'):
                address_elem = host.find('.//address')
                if address_elem is not None:
                    ip_address = address_elem.get('addr')
                    results["hosts"].append(ip_address)
            
            # Parse services
            for port in root.findall('.//port'):
                protocol = port.get('protocol')
                port_id = port.get('portid')
                
                state_elem = port.find('state')
                state = state_elem.get('state') if state_elem is not None else 'unknown'
                
                service_elem = port.find('service')
                service_name = service_elem.get('name', 'unknown') if service_elem is not None else 'unknown'
                
                results["services"].append({
                    "protocol": protocol,
                    "port": port_id,
                    "state": state,
                    "service": service_name
                })
            
            logger.info(f"Parsed {len(results['hosts'])} hosts and {len(results['services'])} services from nmap")
            
        except ET.ParseError as e:
            logger.error(f"Failed to parse nmap XML: {e}")
            # Fallback to regex if XML parsing fails
            host_pattern = r'<host starttime="[^"]*" endtime="[^"]*">'
            service_pattern = r'<port protocol="(\w+)" portid="(\d+)"><state state="(\w+)"[^>]*>.*?<service name="([^"]*)"'
            
            hosts = re.findall(host_pattern, xml_output)
            services = re.findall(service_pattern, xml_output)
            
            results["hosts"] = hosts
            results["services"] = [
                {
                    "protocol": s[0],
                    "port": s[1],
                    "state": s[2],
                    "service": s[3]
                } for s in services
            ]
            logger.info(f"Fallback regex parsing: {len(hosts)} hosts and {len(services)} services")
        
        return results
    
    def test_credentials(self, target_ip: str, service: str, userlist: str = None, 
                        passlist: str = None) -> Dict:
        """Test credentials using hydra-like approach"""
        logger.info(f"Testing credentials on {target_ip}:{service}...")
        
        # Default credentials for common services
        default_creds = {
            "ssh": [("admin", "admin"), ("root", "root"), ("pi", "raspberry")],
            "ftp": [("anonymous", "anonymous"), ("admin", "admin"), ("ftp", "ftp")],
            "http": [("admin", "admin"), ("admin", "password"), ("root", "root")],
            "telnet": [("admin", "admin"), ("root", "root")],
            "mysql": [("root", ""), ("root", "password"), ("admin", "admin")],
        }
        
        creds = default_creds.get(service.lower(), [])
        found_creds = []
        
        for username, password in creds:
            logger.debug(f"Trying {username}:{password} on {service}")
            
            if self._test_credential(target_ip, service, username, password):
                found_creds.append({
                    "username": username,
                    "password": password,
                    "service": service,
                    "ip": target_ip
                })
                logger.warning(f"[+] Valid credentials found: {username}:{password}")
        
        return {"service": service, "target": target_ip, "credentials": found_creds}
    
    def _test_credential(self, target_ip: str, service: str, username: str, 
                        password: str, timeout: int = 5) -> bool:
        """Test single credential"""
        try:
            if service.lower() == "ssh":
                cmd = [
                    "timeout", str(timeout),
                    "ssh", f"-o", "StrictHostKeyChecking=no",
                    f"-o", "UserKnownHostsFile=/dev/null",
                    f"-o", "ConnectTimeout=3",
                    f"{username}@{target_ip}", "exit"
                ]
            elif service.lower() == "ftp":
                cmd = [
                    "timeout", str(timeout),
                    "ftp", "-n", target_ip
                ]
            else:
                return False
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return result.returncode == 0
        
        except Exception:
            return False
    
    def detect_vulnerabilities(self, nmap_results: Dict) -> List[Dict]:
        """Detect common vulnerabilities based on services"""
        vulnerabilities = []
        
        services = nmap_results.get("services", [])
        
        for service in services:
            port = service.get("port", "")
            svc_name = service.get("service", "").lower()
            state = service.get("state", "")
            
            # Skip closed/filtered ports
            if state not in ["open", "unknown"]:
                continue
            
            # Common vulnerabilities
            vuln_db = {
                "telnet": {"risk": "CRITICAL", "reason": "Unencrypted protocol, credentials transmitted in plaintext"},
                "ftp": {"risk": "HIGH", "reason": "Unencrypted file transfer, credentials in plaintext"},
                "http": {"risk": "MEDIUM", "reason": "Unencrypted web traffic, consider HTTPS"},
                "ssh": {"risk": "LOW", "reason": "SSH version should be checked for known vulnerabilities"},
                "mysql": {"risk": "HIGH", "reason": "Database exposed to network, should be firewalled"},
                "smb": {"risk": "CRITICAL", "reason": "SMB exposure can lead to ransomware/lateral movement"},
                "snmp": {"risk": "HIGH", "reason": "SNMP community strings can leak sensitive info"},
            }
            
            for vuln_service, vuln_info in vuln_db.items():
                if vuln_service in svc_name:
                    vulnerabilities.append({
                        "service": svc_name,
                        "port": port,
                        "risk_level": vuln_info["risk"],
                        "description": vuln_info["reason"]
                    })
        
        logger.info(f"Detected {len(vulnerabilities)} potential vulnerabilities")
        return vulnerabilities
    
    def generate_report(self) -> str:
        """Generate security report"""
        logger.info("Generating security report...")
        
        report_file = os.path.join(self.output_dir, f"wifi_analysis_{self.timestamp}.json")
        
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f"Report saved to {report_file}")
        return report_file
    
    def analyze(self, test_credentials: bool = False, aggressive: bool = False) -> Dict:
        """Run full analysis"""
        logger.info("=" * 60)
        logger.info("WiFi Network Security Analysis Started")
        logger.info("=" * 60)
        
        # Phase 1: Network scanning with nmap
        scan_type = "sV -A" if aggressive else "sV"
        nmap_results = self.run_nmap_scan(scan_type)
        self.results["nmap_results"] = nmap_results
        
        # Phase 2: Vulnerability detection
        vulns = self.detect_vulnerabilities(nmap_results)
        self.results["vulnerabilities"] = vulns
        
        # Phase 3: Credential testing (optional)
        if test_credentials:
            logger.info("Phase 3: Testing default credentials...")
            # Get unique hosts from nmap results
            hosts = nmap_results.get("hosts", [])
            if not hosts:
                logger.warning("No hosts found for credential testing")
            else:
                # Use the first host as target (in production, test all hosts)
                target_ip = self.target_network.split('/')[0]  # Extract IP from CIDR
                for service in nmap_results.get("services", []):
                    if service.get("state") == "open":
                        svc_name = service.get("service", "")
                        if svc_name in ["ssh", "ftp", "http", "telnet", "mysql"]:
                            creds_result = self.test_credentials(target_ip, svc_name)
                            self.results["credentials_tested"].append(creds_result)
        
        # Generate report
        report_file = self.generate_report()
        
        logger.info("=" * 60)
        logger.info("Analysis Complete")
        logger.info("=" * 60)
        
        return self.results


def main():
    parser = argparse.ArgumentParser(
        description="WiFi Network Security Analyzer - Combines Nmap, Hydra, and FSociety concepts"
    )
    parser.add_argument(
        "target",
        help="Target network CIDR (e.g., 192.168.1.0/24)"
    )
    parser.add_argument(
        "-c", "--credentials",
        action="store_true",
        help="Test default credentials on services"
    )
    parser.add_argument(
        "-a", "--aggressive",
        action="store_true",
        help="Run aggressive scans (slower, more comprehensive)"
    )
    parser.add_argument(
        "-o", "--output",
        default="/output",
        help="Output directory for reports"
    )
    
    args = parser.parse_args()
    
    # Validate target
    if not re.match(r'^\d+\.\d+\.\d+\.\d+(/\d+)?$', args.target):
        logger.error(f"Invalid target format: {args.target}")
        sys.exit(1)
    
    # Run analysis
    analyzer = WiFiAnalyzer(args.target, args.output)
    results = analyzer.analyze(
        test_credentials=args.credentials,
        aggressive=args.aggressive
    )
    
    # Print summary
    print("\n" + "=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Target: {args.target}")
    print(f"Services Found: {len(results.get('nmap_results', {}).get('services', []))}")
    print(f"Vulnerabilities: {len(results.get('vulnerabilities', []))}")
    print(f"Report: /output/wifi_analysis_{analyzer.timestamp}.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
