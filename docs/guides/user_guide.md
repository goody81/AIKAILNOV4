# User Guide

Complete guide for using AIKAILNOV4.

## Table of Contents
- [Getting Started](#getting-started)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Command Reference](#command-reference)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Getting Started

### First Steps

After installation, verify your setup:

```bash
# Activate virtual environment
source venv/bin/activate

# Verify installation
python3 src/core/aikail.py --version

# View help
python3 src/core/aikail.py --help
```

### Quick Start

Perform your first scan:

```bash
# Scan localhost
python3 src/core/aikail.py scan -t 127.0.0.1

# Scan with AI analysis
python3 src/core/aikail.py scan -t 192.168.1.100 --ai-mode advanced
```

## Basic Usage

### Scanning Targets

#### Single Host

```bash
python3 src/core/aikail.py scan -t 192.168.1.100
```

#### Multiple Hosts

```bash
python3 src/core/aikail.py scan -t 192.168.1.0/24
```

#### With Specific Ports

```bash
python3 src/core/aikail.py scan -t example.com -p 80,443,8080
```

### AI Analysis Modes

#### Basic Mode
Quick AI analysis with essential insights:
```bash
python3 src/core/aikail.py scan -t 192.168.1.100 --ai-mode basic
```

#### Advanced Mode
Comprehensive AI analysis with attack vectors:
```bash
python3 src/core/aikail.py scan -t 192.168.1.100 --ai-mode advanced
```

#### Full Mode
Complete AI analysis including predictive and compliance checks:
```bash
python3 src/core/aikail.py scan -t 192.168.1.100 --ai-mode full
```

### Report Generation

#### HTML Report

```bash
python3 src/core/aikail.py scan -t 192.168.1.100 -o report.html --report-format html
```

#### JSON Report

```bash
python3 src/core/aikail.py scan -t 192.168.1.100 -o report.json --report-format json
```

#### PDF Report

```bash
python3 src/core/aikail.py scan -t 192.168.1.100 -o report.pdf --report-format pdf
```

## Advanced Features

### Using Specific Modules

```bash
# Port scanner module
python3 src/core/aikail.py module -n port_scanner -t 192.168.1.100

# Web scanner module
python3 src/core/aikail.py module -n web_scanner -t https://example.com

# Vulnerability scanner
python3 src/core/aikail.py module -n vulnerability_scanner -t 192.168.1.100
```

### Interactive Mode

Launch the interactive shell:

```bash
python3 src/core/aikail.py interactive
```

In interactive mode:
```
aikail> scan 192.168.1.100
aikail> analyze scan_abc123
aikail> report scan_abc123
aikail> help
aikail> exit
```

### Updating Databases

```bash
# Update threat intelligence
python3 src/core/aikail.py update --threats

# Update vulnerability signatures
python3 src/core/aikail.py update --signatures

# Update everything
python3 src/core/aikail.py update --all
```

### Configuration

Edit `config/config.yaml`:

```yaml
# Enable/disable AI
ai:
  enabled: true
  model: "gpt-4"

# Scanning settings
scanning:
  aggressive_mode: false
  stealth_mode: true
  rate_limit: 100

# Reporting
reporting:
  format: "html"
  include_raw_data: false
```

## Command Reference

### Main Commands

| Command | Description |
|---------|-------------|
| `scan` | Perform security scan |
| `module` | Run specific module |
| `modules` | List available modules |
| `interactive` | Launch interactive mode |
| `update` | Update databases |
| `report` | Generate report |

### Global Options

| Option | Description |
|--------|-------------|
| `--config, -c` | Configuration file path |
| `--debug, -d` | Enable debug mode |
| `--version` | Show version |
| `--help` | Show help |

### Scan Options

| Option | Description |
|--------|-------------|
| `--target, -t` | Target to scan (required) |
| `--ports, -p` | Port range or list |
| `--ai-mode` | AI analysis mode |
| `--output, -o` | Output file path |
| `--report-format` | Report format |

## Best Practices

### Legal and Ethical Use

1. **Always get permission** before scanning any system
2. **Follow local laws** regarding security testing
3. **Respect privacy** and handle data responsibly
4. **Document authorization** for all testing activities

### Security

1. **Protect API keys** - Never commit to version control
2. **Use strong passwords** for API authentication
3. **Enable encryption** for sensitive data
4. **Rotate credentials** regularly
5. **Monitor access logs** for suspicious activity

### Performance

1. **Start with quick scans** before deep scans
2. **Use stealth mode** to avoid detection
3. **Limit concurrent scans** to prevent overload
4. **Cache results** when possible
5. **Schedule heavy scans** during off-peak hours

### Reporting

1. **Generate reports regularly** for audit trail
2. **Archive old reports** securely
3. **Share reports securely** using encryption
4. **Include timestamps** for traceability
5. **Document remediation** actions

## Troubleshooting

### Common Issues

#### "Permission denied" errors

**Problem:** Some scans require elevated privileges.

**Solution:**
```bash
sudo python3 src/core/aikail.py scan -t 192.168.1.100
```

#### "Target unreachable" errors

**Problem:** Target may be offline or firewalled.

**Solutions:**
- Verify target is online: `ping 192.168.1.100`
- Check firewall rules
- Try different port ranges
- Use stealth mode

#### "Module not found" errors

**Problem:** Trying to use unavailable module.

**Solution:**
```bash
# List available modules
python3 src/core/aikail.py modules --list
```

#### Slow scan performance

**Solutions:**
- Reduce port range
- Decrease concurrent threads in config
- Use quick scan mode
- Check network connectivity

#### AI features not working

**Problem:** Missing or invalid API keys.

**Solution:**
1. Set API key: `export OPENAI_API_KEY=your_key`
2. Verify in config: Check `config/config.yaml`
3. Test connection: Run simple scan with AI

### Debug Mode

Enable debug mode for detailed logs:

```bash
python3 src/core/aikail.py --debug scan -t 192.168.1.100
```

### Getting Help

If you need assistance:

1. Check documentation: `docs/`
2. Search issues: [GitHub Issues](https://github.com/goody81/AIKAILNOV4/issues)
3. Run verification: `python3 scripts/verify_installation.py`
4. Join Discord: [Community Discord](https://discord.gg/aikailnov4)
5. Email support: support@aikailnov4.com

## Example Workflows

### Basic Network Assessment

```bash
# 1. Quick scan to identify hosts
python3 src/core/aikail.py scan -t 192.168.1.0/24 -p 21-23,80,443

# 2. Deep scan on specific host
python3 src/core/aikail.py scan -t 192.168.1.100 -p 1-65535 --ai-mode advanced

# 3. Generate comprehensive report
python3 src/core/aikail.py report --scan-id abc123 --format pdf
```

### Web Application Testing

```bash
# 1. Initial reconnaissance
python3 src/core/aikail.py module -n port_scanner -t example.com

# 2. Web application scan
python3 src/core/aikail.py module -n web_scanner -t https://example.com

# 3. AI analysis
python3 src/core/aikail.py scan -t example.com --ai-mode full
```

### Continuous Monitoring

```bash
# 1. Baseline scan
python3 src/core/aikail.py scan -t 192.168.1.100 -o baseline.json

# 2. Regular scans (schedule with cron)
*/30 * * * * python3 /path/to/aikail.py scan -t 192.168.1.100

# 3. Compare results and alert on changes
```

## Tips and Tricks

1. **Create aliases** for common commands:
   ```bash
   alias aikail='python3 /path/to/src/core/aikail.py'
   ```

2. **Use configuration profiles** for different scenarios:
   ```bash
   python3 src/core/aikail.py -c config/stealth.yaml scan -t target
   ```

3. **Combine with other tools**:
   ```bash
   python3 src/core/aikail.py scan -t 192.168.1.100 | jq '.vulnerabilities'
   ```

4. **Automate with scripts**:
   ```python
   from src.core.aikail import AIKail
   aikail = AIKail()
   results = aikail.scan('192.168.1.100')
   ```

---

For more detailed information, see the [API Documentation](../api/README.md) and [Architecture Guide](../architecture/README.md).
