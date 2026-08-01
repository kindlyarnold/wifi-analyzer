# WiFi Network Security Analyzer - Complete Setup Guide

## Overview

This integrated security toolkit combines three powerful tools:
- **Nmap** — Network reconnaissance and service discovery
- **THC-Hydra** — Credential testing and brute-force attacks
- **FSociety Concepts** — Social engineering intelligence gathering

### What It Does

1. **Scans networks** for active hosts and services
2. **Identifies vulnerabilities** in exposed services
3. **Tests default credentials** on discovered services
4. **Generates reports** in JSON format for analysis

---

## Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+ (optional)
- Network access to target WiFi
- Administrator/sudo access (for privileged mode)

### Installation

```bash
# Clone or extract the project
cd wifi-analyzer

# Make the quickstart script executable
chmod +x quickstart.sh

# Build the image
./quickstart.sh
# OR manually:
docker build -t wifi-analyzer:latest .
```

---

## Usage

### 1. **Basic Network Scan**

```bash
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest \
  192.168.1.0/24
```

**What it does:**
- Scans all IPs in the 192.168.1.0/24 subnet
- Detects open ports and running services
- Identifies common vulnerabilities
- Saves report to `./output/wifi_analysis_*.json`

**Output:**
```json
{
  "scan_time": "20240115_143022",
  "target": "192.168.1.0/24",
  "nmap_results": {
    "hosts": ["192.168.1.1", "192.168.1.50", "192.168.1.100"],
    "services": [
      {"port": "22", "state": "open", "service": "ssh"},
      {"port": "80", "state": "open", "service": "http"}
    ]
  },
  "vulnerabilities": [
    {
      "service": "telnet",
      "port": "23",
      "risk_level": "CRITICAL",
      "description": "Unencrypted protocol..."
    }
  ]
}
```

---

### 2. **Scan with Credential Testing**

```bash
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest \
  192.168.1.0/24 -c
```

**What it does:**
- Performs basic scan
- Tests default credentials on discovered services
- Attempts: admin/admin, root/root, etc.
- Reports successful credentials found

**⚠️ WARNING:** Only run on networks you own or have permission to test!

---

### 3. **Aggressive Comprehensive Scan**

```bash
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest \
  192.168.1.0/24 -a -c
```

**What it does:**
- Aggressive nmap probing
- Full vulnerability detection
- Comprehensive credential testing
- Takes significantly longer but more thorough

---

### 4. **Using Docker Compose**

```bash
# Edit docker-compose.yml to change target network
# Then run:
docker-compose run --rm wifi-analyzer 192.168.1.0/24 -c -a
```

---

## Command Reference

```
usage: wifi_analyzer.py [-h] [-c] [-a] [-o OUTPUT] TARGET

Positional Arguments:
  TARGET                Target network in CIDR notation (e.g., 192.168.1.0/24)

Optional Arguments:
  -h, --help           Show help message
  -c, --credentials    Test default credentials on services (slower)
  -a, --aggressive     Run aggressive scans (much slower, more thorough)
  -o OUTPUT, --output  Output directory (default: /output)
```

### Examples

```bash
# Single host
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest 192.168.1.100

# Subnet with credential testing
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest 192.168.1.0/24 --credentials

# Full analysis
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest 192.168.1.0/24 -c -a

# Custom output directory
docker run --rm --privileged --network host \
  -v /custom/path:/output \
  wifi-analyzer:latest 192.168.1.0/24 -o /output
```

---

## Understanding Results

### Risk Levels

| Level | Description |
|-------|-------------|
| **CRITICAL** | Immediate exploitation risk (Telnet, SMB, RDP exposed) |
| **HIGH** | Significant vulnerability (FTP, unencrypted DB, exposed APIs) |
| **MEDIUM** | Moderate risk requiring additional context (HTTP, weak services) |
| **LOW** | Minor issue or configuration problem (outdated SSH version) |

### Vulnerability Examples

**Telnet (Port 23) - CRITICAL**
- Unencrypted authentication
- All traffic in plaintext
- Immediately exploitable

**FTP (Port 21) - HIGH**
- Credentials transmitted unencrypted
- File operations expose sensitive data
- Consider SFTP instead

**MySQL (Port 3306) - HIGH**
- Database exposed to network
- Default credentials common (root/root)
- Should be firewalled to trusted IPs only

**HTTP (Port 80) - MEDIUM**
- Web traffic unencrypted
- Use HTTPS (port 443) instead

**SSH (Port 22) - LOW**
- Generally secure if patched
- Check version for known vulnerabilities
- Disable root login

---

## Advanced Usage

### Scanning Multiple Networks

```bash
# Network 1
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest 192.168.1.0/24

# Network 2
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest 10.0.0.0/24
```

### Processing Reports

```bash
# View report summary
cat output/wifi_analysis_*.json | jq '.vulnerabilities'

# Count vulnerabilities by risk level
cat output/wifi_analysis_*.json | jq '.vulnerabilities[] | .risk_level' | sort | uniq -c

# Find all critical issues
cat output/wifi_analysis_*.json | jq '.vulnerabilities[] | select(.risk_level=="CRITICAL")'
```

---

## Troubleshooting

### Issue: "Permission denied" on scan
**Solution:** Ensure you're running with `--privileged`:
```bash
docker run --rm --privileged --network host ...
```

### Issue: "Cannot connect to network"
**Solution:** Verify target is reachable:
```bash
# Inside container, test connectivity
ping -c 1 192.168.1.1
nmap -sn 192.168.1.0/24
```

### Issue: Scan is very slow
**Solution:** Reduce scope or timeout:
```bash
# Scan fewer hosts
docker run --rm --privileged --network host \
  wifi-analyzer:latest 192.168.1.100 -c

# Don't use -a flag (aggressive mode)
```

### Issue: "Port already in use"
**Solution:** The container may not have exited properly:
```bash
docker ps -a | grep wifi-analyzer
docker rm <container-id>
```

---

## Security Considerations

### ⚠️ Legal Requirements

- **Only scan networks you own or have written permission to test**
- Unauthorized network scanning is illegal in most jurisdictions
- Obtain documented authorization before testing
- This tool is for defensive/authorized security testing only

### Best Practices

1. **Run in isolated environment** when possible
2. **Log all activity** for audit trails
3. **Document authorization** before testing
4. **Secure reports** containing sensitive information
5. **Dispose of reports** after analysis
6. **Inform network administrators** before scanning

### Data Protection

The container does NOT:
- Store credentials persistently
- Send data to external servers
- Log passwords in plaintext
- Access personal data beyond network layer

Reports should be treated as sensitive security data.

---

## Architecture Details

### Dockerfile Stages

**Stage 1: Builder** (not included in final image)
- Compiles nmap, hydra, SSH client
- Handles dependencies

**Stage 2: Runtime** (final image ~400MB)
- Minimal Debian environment
- Nmap + Hydra binaries
- Python3 for analyzer
- Non-privileged user (analyzer)

### How It Works

```
1. Network Layer
   ├── Nmap scans subnet for active hosts
   ├── Identifies services on each host
   └── Detects OS and service versions

2. Vulnerability Analysis
   ├── Cross-references known vulnerabilities
   ├── Assigns risk levels
   └── Generates recommendations

3. Credential Testing
   ├── Tests default credentials
   ├── Common weak passwords
   └── Service-specific defaults

4. Report Generation
   ├── Aggregates findings
   ├── Formats as JSON
   └── Saves to /output volume
```

---

## Performance Tips

| Task | Time | Tips |
|------|------|------|
| Single host scan | 5-10s | Fast baseline |
| /24 subnet (254 hosts) | 2-5 min | Standard network |
| /23 subnet (512 hosts) | 5-15 min | Skip -a flag |
| /22 subnet (1024 hosts) | 20-60 min | Run overnight |

Reduce time with:
- Smaller target (`/25` instead of `/24`)
- Skip credential testing (remove `-c`)
- Remove aggressive flag (remove `-a`)

---

## Example Workflow

```bash
# 1. Initial reconnaissance
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest 192.168.1.0/24

# 2. Review findings
cat output/wifi_analysis_*.json | jq '.vulnerabilities'

# 3. Follow up on critical issues
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest 192.168.1.100 -c

# 4. Document findings
# Create ticket/report with results
```

---

## Support & Contributing

For issues:
1. Check troubleshooting section
2. Review Docker logs: `docker logs <container-id>`
3. Verify nmap/hydra are installed: `docker exec <id> nmap -V`

---

## Disclaimer

This tool is provided as-is for educational and authorized security testing purposes only. Users are responsible for:
- Compliance with local laws
- Obtaining proper authorization
- Ethical use of the tool
- Protecting sensitive information discovered

The developers assume no liability for misuse.

---

## License

See LICENSE file for details.
