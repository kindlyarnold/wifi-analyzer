# WiFi Network Security Analyzer

A unified security toolkit that combines **Nmap**, **THC-Hydra**, and **FSociety** concepts to analyze WiFi networks comprehensively.

## Features

- **Network Scanning** (Nmap): Service detection, OS fingerprinting, vulnerability scripts
- **Credential Testing** (Hydra-like): Default credential checks on discovered services
- **Vulnerability Detection**: Common service vulnerabilities (Telnet, FTP, SMB, etc.)
- **Automated Analysis**: Full network mapping and risk assessment
- **JSON Reports**: Structured output for further analysis

## Build

```bash
docker build -t wifi-analyzer:latest .
```

## Usage

### Basic Network Scan
```bash
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest \
  192.168.1.0/24
```

### With Credential Testing
```bash
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest \
  192.168.1.0/24 -c
```

### Aggressive Scan (More comprehensive)
```bash
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest \
  192.168.1.0/24 -a
```

### Full Analysis
```bash
docker run --rm --privileged --network host \
  -v $(pwd)/output:/output \
  wifi-analyzer:latest \
  192.168.1.0/24 -c -a
```

### Using Docker Compose
```bash
docker-compose run --rm wifi-analyzer 192.168.1.0/24 -c -a
```

## Command-Line Options

```
usage: wifi_analyzer.py [-h] [-c] [-a] [-o OUTPUT] target

WiFi Network Security Analyzer

positional arguments:
  target                Target network CIDR (e.g., 192.168.1.0/24)

optional arguments:
  -h, --help           Show help message
  -c, --credentials    Test default credentials on services
  -a, --aggressive     Run aggressive scans (slower, more comprehensive)
  -o, --output         Output directory for reports (default: /output)
```

## Output

Reports are saved as JSON in `/output/`:

```
{
  "scan_time": "20240115_143022",
  "target": "192.168.1.0/24",
  "nmap_results": {
    "hosts": [...],
    "services": [
      {
        "protocol": "tcp",
        "port": "22",
        "state": "open",
        "service": "ssh"
      }
    ]
  },
  "vulnerabilities": [
    {
      "service": "telnet",
      "port": "23",
      "risk_level": "CRITICAL",
      "description": "Unencrypted protocol..."
    }
  ],
  "credentials_tested": [...]
}
```

## Architecture

### Stage 1: Builder
- Compiles dependencies
- Installed nmap, hydra, ssh-client

### Stage 2: Runtime
- Minimal image with only runtime requirements
- Non-privileged user (analyzer)
- Shared network namespace for WiFi access

## Permissions & Security

⚠️ **Important:**
- Requires `--privileged` flag for raw network access
- Requires `--network host` to access WiFi interfaces
- **Only use on networks you own or have authorization to test**
- Create `output/` directory with write permissions

## Legal Notice

This tool is for authorized security testing only. Unauthorized access to computer networks is illegal. Always obtain written permission before testing.

## Disclaimer

The developers are not responsible for misuse of this tool.
