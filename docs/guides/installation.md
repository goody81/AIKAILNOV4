# Installation Guide

Complete guide for installing AIKAILNOV4 on various platforms.

## Table of Contents
- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Post-Installation](#post-installation)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Operating System**: Kali Linux 2023.1+ or Debian-based Linux
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 10GB free space
- **Python**: 3.8 or higher

### Recommended Requirements
- **Operating System**: Kali Linux 2024.1+
- **CPU**: 4+ cores
- **RAM**: 8GB or more
- **Storage**: 20GB free space
- **Python**: 3.10 or higher
- **Network**: Stable internet connection

### Software Dependencies
- Python 3.8+
- pip (Python package manager)
- Git
- Nmap
- Root/sudo access (for some features)

## Installation Methods

### Method 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/goody81/AIKAILNOV4.git
cd AIKAILNOV4

# Run the installation script
sudo bash scripts/install.sh
```

### Method 2: Manual Installation

#### Step 1: Clone Repository
```bash
git clone https://github.com/goody81/AIKAILNOV4.git
cd AIKAILNOV4
```

#### Step 2: Install System Dependencies
```bash
sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    nmap \
    git \
    build-essential
```

#### Step 3: Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 4: Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

#### Step 5: Configure the System
```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml

# Edit configuration
nano config/config.yaml
```

#### Step 6: Initialize Database
```bash
python3 scripts/init_db.py
```

#### Step 7: Verify Installation
```bash
python3 src/core/aikail.py --version
```

### Method 3: Docker Installation

```bash
# Build Docker image
docker build -t aikailnov4 .

# Run container
docker run -it aikailnov4

# With persistent storage
docker run -it -v $(pwd)/data:/app/data aikailnov4
```

### Method 4: Development Installation

```bash
# Clone and enter directory
git clone https://github.com/goody81/AIKAILNOV4.git
cd AIKAILNOV4

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .

# Install pre-commit hooks
pre-commit install
```

## Platform-Specific Instructions

### Kali Linux

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies (most are pre-installed)
sudo apt install -y python3-pip python3-venv

# Clone and install
git clone https://github.com/goody81/AIKAILNOV4.git
cd AIKAILNOV4
pip3 install -r requirements.txt
```

### Ubuntu/Debian

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nmap \
    nikto \
    git

# Clone and install
git clone https://github.com/goody81/AIKAILNOV4.git
cd AIKAILNOV4
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Arch Linux

```bash
# Update system
sudo pacman -Syu

# Install dependencies
sudo pacman -S python python-pip nmap git

# Clone and install
git clone https://github.com/goody81/AIKAILNOV4.git
cd AIKAILNOV4
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.11 nmap git

# Clone and install
git clone https://github.com/goody81/AIKAILNOV4.git
cd AIKAILNOV4
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows (WSL2)

```bash
# Enable WSL2 and install Kali Linux
wsl --install -d kali-linux

# Inside WSL2, follow Kali Linux instructions
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip nmap git
git clone https://github.com/goody81/AIKAILNOV4.git
cd AIKAILNOV4
pip3 install -r requirements.txt
```

## Post-Installation

### 1. Configuration

Edit the configuration file:
```bash
nano config/config.yaml
```

Set essential parameters:
- API keys (if using AI features)
- Database settings
- Network configuration
- Module preferences

### 2. Environment Variables

Create `.env` file:
```bash
cat > .env << EOF
OPENAI_API_KEY=your_api_key_here
SHODAN_API_KEY=your_shodan_key
VIRUSTOTAL_API_KEY=your_vt_key
DB_PASSWORD=secure_password
API_SECRET_KEY=random_secret_key
ENCRYPTION_KEY=encryption_key
EOF
```

### 3. Test Installation

Run basic test:
```bash
python3 src/core/aikail.py --help
```

Test with a safe target:
```bash
python3 src/core/aikail.py scan -t 127.0.0.1
```

### 4. Create Shortcuts (Optional)

Add to `.bashrc` or `.zshrc`:
```bash
alias aikail='python3 /path/to/AIKAILNOV4/src/core/aikail.py'
```

Or install system-wide:
```bash
sudo pip3 install -e .
```

### 5. Set Up Logging

Create log directory:
```bash
mkdir -p logs
chmod 755 logs
```

### 6. Configure Firewall (If Needed)

```bash
# Allow outgoing connections
sudo ufw allow out 80/tcp
sudo ufw allow out 443/tcp

# Allow API server (if running)
sudo ufw allow 8080/tcp
```

## Troubleshooting

### Common Issues

#### Issue: Import Error - Module Not Found

**Solution:**
```bash
# Ensure you're in virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: Permission Denied

**Solution:**
```bash
# Some scans require root privileges
sudo python3 src/core/aikail.py scan -t target

# Or add user to sudo group
sudo usermod -aG sudo $USER
```

#### Issue: Nmap Not Found

**Solution:**
```bash
# Install nmap
sudo apt install nmap

# Verify installation
nmap --version
```

#### Issue: Database Connection Error

**Solution:**
```bash
# Reinitialize database
rm data/aikail.db
python3 scripts/init_db.py
```

#### Issue: AI Features Not Working

**Solution:**
```bash
# Check API key configuration
grep OPENAI_API_KEY .env

# Verify AI is enabled in config
grep "enabled: true" config/config.yaml
```

#### Issue: Slow Performance

**Solution:**
```bash
# Install Redis for caching
sudo apt install redis-server
sudo systemctl start redis

# Update config to use Redis cache
nano config/config.yaml
```

### Getting Help

If you encounter issues not listed here:

1. Check the [GitHub Issues](https://github.com/goody81/AIKAILNOV4/issues)
2. Review the [documentation](../README.md)
3. Join our [Discord community](https://discord.gg/aikailnov4)
4. Email: support@aikailnov4.com

### System Verification

Run the verification script:
```bash
python3 scripts/verify_installation.py
```

This will check:
- Python version
- Dependencies installed
- Configuration validity
- Database connectivity
- Network accessibility

## Upgrading

### Upgrade to Latest Version

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run database migrations (if any)
python3 scripts/migrate_db.py

# Verify upgrade
python3 src/core/aikail.py --version
```

## Uninstallation

### Complete Removal

```bash
# Deactivate virtual environment
deactivate

# Remove installation directory
rm -rf /path/to/AIKAILNOV4

# Remove configuration (optional)
rm -rf ~/.aikailnov4

# Remove system-wide installation (if installed)
sudo pip3 uninstall aikailnov4
```

---

**Next Steps**: After installation, see the [User Guide](user_guide.md) for usage instructions.
