#!/usr/bin/env python3
"""
Example 1: Basic Network Scan
Demonstrates simple network scanning with AIKAILNOV4
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.scanner import SecurityScanner
from src.utils.config import load_config
from src.utils.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)


def main():
    """Run a basic network scan example."""
    
    print("=" * 60)
    print("AIKAILNOV4 - Basic Network Scan Example")
    print("=" * 60)
    
    # Load configuration
    try:
        config = load_config('config/config.yaml')
    except FileNotFoundError:
        logger.warning("Config file not found, using defaults")
        config = {}
    
    # Initialize scanner
    scanner = SecurityScanner(config)
    
    # Target for demonstration (localhost)
    target = "127.0.0.1"
    ports = "80,443,22"
    
    print(f"\n[*] Starting scan on {target}")
    print(f"[*] Scanning ports: {ports}\n")
    
    # Perform scan
    try:
        results = scanner.scan(target, ports)
        
        # Display results
        print("\n" + "=" * 60)
        print("SCAN RESULTS")
        print("=" * 60)
        
        print(f"\nTarget: {results['target']}")
        print(f"Scan Time: {results['scan_time']}")
        print(f"Total Hosts: {len(results['hosts'])}")
        print(f"Total Open Ports: {results['total_open_ports']}")
        
        # Display host information
        for host in results['hosts']:
            print(f"\n[+] Host: {host['ip']}")
            print(f"    State: {host['state']}")
            
            if host.get('hostname'):
                print(f"    Hostname: {host['hostname']}")
            
            if host.get('os'):
                print(f"    OS: {host['os']}")
            
            # Display open ports
            if host['open_ports']:
                print(f"\n    Open Ports:")
                for port in host['open_ports']:
                    print(f"      - Port {port['port']}/{port['protocol']}")
                    print(f"        Service: {port['service']}")
                    if port.get('version'):
                        print(f"        Version: {port['version']}")
        
        # Display vulnerabilities
        if results['vulnerabilities']:
            print(f"\n\n[!] Potential Vulnerabilities: {len(results['vulnerabilities'])}")
            for vuln in results['vulnerabilities']:
                print(f"\n    - {vuln['description']}")
                print(f"      Severity: {vuln['severity'].upper()}")
                print(f"      Host: {vuln['host']}")
                print(f"      Port: {vuln['port']}")
        
        print("\n" + "=" * 60)
        print("[+] Scan completed successfully!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        logger.error(f"Error during scan: {str(e)}")
        print(f"\n[!] Error: {str(e)}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
