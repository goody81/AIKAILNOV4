#!/usr/bin/env python3
"""
System verification script for AIKAILNOV4
Checks if the system is properly configured and all dependencies are installed
"""

import sys
import subprocess
from pathlib import Path

# Colors for output
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color


def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"{GREEN}✓{NC} Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"{RED}✗{NC} Python version must be 3.8 or higher")
        return False


def check_command(command):
    """Check if a command is available."""
    try:
        subprocess.run([command, '--version'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE,
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_system_dependencies():
    """Check system dependencies."""
    print("\nChecking system dependencies...")
    
    dependencies = {
        'nmap': 'Network scanning tool',
        'git': 'Version control system',
    }
    
    all_ok = True
    for cmd, desc in dependencies.items():
        if check_command(cmd):
            print(f"{GREEN}✓{NC} {cmd} - {desc}")
        else:
            print(f"{RED}✗{NC} {cmd} - {desc} (NOT FOUND)")
            all_ok = False
    
    return all_ok


def check_python_packages():
    """Check Python packages."""
    print("\nChecking Python packages...")
    
    packages = [
        'yaml',
        'click',
        'nmap',
        'flask',
        'requests',
    ]
    
    all_ok = True
    for package in packages:
        try:
            __import__(package)
            print(f"{GREEN}✓{NC} {package}")
        except ImportError:
            print(f"{RED}✗{NC} {package} (NOT INSTALLED)")
            all_ok = False
    
    return all_ok


def check_directories():
    """Check required directories."""
    print("\nChecking directories...")
    
    dirs = ['src', 'config', 'docs', 'examples', 'tests']
    
    all_ok = True
    for directory in dirs:
        path = Path(directory)
        if path.exists() and path.is_dir():
            print(f"{GREEN}✓{NC} {directory}/")
        else:
            print(f"{RED}✗{NC} {directory}/ (NOT FOUND)")
            all_ok = False
    
    return all_ok


def check_config():
    """Check configuration files."""
    print("\nChecking configuration...")
    
    config_file = Path('config/config.yaml')
    example_file = Path('config/config.example.yaml')
    
    if config_file.exists():
        print(f"{GREEN}✓{NC} config/config.yaml")
        return True
    elif example_file.exists():
        print(f"{YELLOW}ℹ{NC} config/config.yaml not found (use config.example.yaml as template)")
        return True
    else:
        print(f"{RED}✗{NC} No configuration file found")
        return False


def check_database():
    """Check database."""
    print("\nChecking database...")
    
    db_file = Path('data/aikail.db')
    if db_file.exists():
        print(f"{GREEN}✓{NC} Database initialized (data/aikail.db)")
        return True
    else:
        print(f"{YELLOW}ℹ{NC} Database not initialized (run: python3 scripts/init_db.py)")
        return True


def main():
    """Main verification function."""
    print("=" * 50)
    print("AIKAILNOV4 System Verification")
    print("=" * 50)
    print()
    
    checks = [
        check_python_version(),
        check_system_dependencies(),
        check_python_packages(),
        check_directories(),
        check_config(),
        check_database(),
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print(f"{GREEN}✓ All checks passed!{NC}")
        print("=" * 50)
        print("\nYour system is ready to use AIKAILNOV4!")
        return 0
    else:
        print(f"{RED}✗ Some checks failed{NC}")
        print("=" * 50)
        print("\nPlease fix the issues above before using AIKAILNOV4.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
