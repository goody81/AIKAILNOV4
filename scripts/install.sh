#!/bin/bash
# Installation script for AIKAILNOV4

set -e

echo "================================"
echo "AIKAILNOV4 Installation Script"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo -e "${YELLOW}Warning: Running as root. This is not recommended for normal use.${NC}"
fi

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${GREEN}✓${NC} Linux detected"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${GREEN}✓${NC} macOS detected"
else
    echo -e "${RED}✗${NC} Unsupported operating system"
    exit 1
fi

# Check Python version
echo -e "\nChecking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo -e "${GREEN}✓${NC} Python $(python3 --version) found"
    
    # Check if version is 3.8 or higher
    if (( $(echo "$PYTHON_VERSION >= 3.8" | bc -l) )); then
        echo -e "${GREEN}✓${NC} Python version meets requirements (>=3.8)"
    else
        echo -e "${RED}✗${NC} Python version must be 3.8 or higher"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Install system dependencies
echo -e "\n${YELLOW}Installing system dependencies...${NC}"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3-pip python3-dev nmap git build-essential
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-pip python3-devel nmap git gcc
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python-pip nmap git base-devel
    else
        echo -e "${YELLOW}Warning: Could not detect package manager. Please install dependencies manually.${NC}"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v brew &> /dev/null; then
        brew install python@3.11 nmap git
    else
        echo -e "${YELLOW}Warning: Homebrew not found. Please install dependencies manually.${NC}"
    fi
fi

echo -e "${GREEN}✓${NC} System dependencies installed"

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
echo -e "${GREEN}✓${NC} Virtual environment created"

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip
echo -e "${GREEN}✓${NC} pip upgraded"

# Install Python dependencies
echo -e "\n${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Python dependencies installed"

# Create necessary directories
echo -e "\n${YELLOW}Creating directories...${NC}"
mkdir -p data logs reports
echo -e "${GREEN}✓${NC} Directories created"

# Copy configuration file
echo -e "\n${YELLOW}Setting up configuration...${NC}"
if [ ! -f config/config.yaml ]; then
    cp config/config.example.yaml config/config.yaml
    echo -e "${GREEN}✓${NC} Configuration file created"
else
    echo -e "${YELLOW}ℹ${NC} Configuration file already exists"
fi

# Initialize database
echo -e "\n${YELLOW}Initializing database...${NC}"
python3 scripts/init_db.py
echo -e "${GREEN}✓${NC} Database initialized"

# Verify installation
echo -e "\n${YELLOW}Verifying installation...${NC}"
if python3 src/core/aikail.py --version &> /dev/null; then
    echo -e "${GREEN}✓${NC} Installation verified successfully"
else
    echo -e "${RED}✗${NC} Installation verification failed"
    exit 1
fi

# Print success message
echo ""
echo "================================"
echo -e "${GREEN}Installation completed successfully!${NC}"
echo "================================"
echo ""
echo "To use AIKAILNOV4:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: python3 src/core/aikail.py --help"
echo ""
echo "For more information, see the documentation in docs/"
echo ""
