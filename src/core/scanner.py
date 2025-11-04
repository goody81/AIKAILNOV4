"""
Security Scanner Module
Handles core scanning functionality for AIKAILNOV4
"""

import nmap
from typing import Dict, List, Optional, Any
from datetime import datetime
import socket
import concurrent.futures
from dataclasses import dataclass, asdict

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class ScanResult:
    """Data class for scan results."""
    target: str
    scan_time: str
    hosts: List[Dict[str, Any]]
    total_open_ports: int
    vulnerabilities: List[Dict[str, Any]]
    metadata: Dict[str, Any]


class SecurityScanner:
    """
    Main security scanner class that orchestrates various scanning operations.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the security scanner.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.scanner = nmap.PortScanner()
        logger.info("SecurityScanner initialized")
    
    def scan(self, target: str, ports: str = "1-1000") -> Dict[str, Any]:
        """
        Perform a comprehensive security scan on the target.
        
        Args:
            target: IP address, hostname, or network range
            ports: Port range to scan (e.g., "1-1000" or "80,443,8080")
        
        Returns:
            Dictionary containing scan results
        """
        logger.info(f"Starting scan on target: {target}, ports: {ports}")
        
        scan_start = datetime.now()
        results = {
            'target': target,
            'scan_time': scan_start.isoformat(),
            'hosts': [],
            'total_open_ports': 0,
            'vulnerabilities': [],
            'metadata': {
                'scanner_version': '1.0.0',
                'scan_type': 'comprehensive'
            }
        }
        
        try:
            # Perform port scan
            logger.info("Performing port scan...")
            self.scanner.scan(target, ports, arguments='-sV -sC -T4')
            
            # Process results for each host
            for host in self.scanner.all_hosts():
                host_info = self._process_host(host)
                results['hosts'].append(host_info)
                results['total_open_ports'] += len(host_info.get('open_ports', []))
            
            # Detect potential vulnerabilities
            results['vulnerabilities'] = self._detect_vulnerabilities(results)
            
            scan_duration = (datetime.now() - scan_start).total_seconds()
            results['metadata']['scan_duration'] = scan_duration
            
            logger.info(f"Scan completed in {scan_duration:.2f} seconds")
            logger.info(f"Found {len(results['hosts'])} hosts with {results['total_open_ports']} open ports")
            
        except Exception as e:
            logger.error(f"Error during scan: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _process_host(self, host: str) -> Dict[str, Any]:
        """
        Process scan results for a single host.
        
        Args:
            host: IP address of the host
        
        Returns:
            Dictionary containing host information
        """
        host_info = {
            'ip': host,
            'hostname': self._resolve_hostname(host),
            'state': self.scanner[host].state(),
            'open_ports': [],
            'os': None,
            'services': []
        }
        
        # Extract port information
        for proto in self.scanner[host].all_protocols():
            ports = self.scanner[host][proto].keys()
            
            for port in ports:
                port_info = self.scanner[host][proto][port]
                
                if port_info['state'] == 'open':
                    port_data = {
                        'port': port,
                        'protocol': proto,
                        'state': port_info['state'],
                        'service': port_info.get('name', 'unknown'),
                        'version': port_info.get('version', ''),
                        'product': port_info.get('product', ''),
                        'extrainfo': port_info.get('extrainfo', '')
                    }
                    host_info['open_ports'].append(port_data)
                    host_info['services'].append(port_info.get('name', 'unknown'))
        
        # OS Detection
        if 'osmatch' in self.scanner[host]:
            if self.scanner[host]['osmatch']:
                host_info['os'] = self.scanner[host]['osmatch'][0]['name']
        
        return host_info
    
    def _resolve_hostname(self, ip: str) -> Optional[str]:
        """
        Resolve hostname from IP address.
        
        Args:
            ip: IP address
        
        Returns:
            Hostname or None if resolution fails
        """
        try:
            return socket.gethostbyaddr(ip)[0]
        except (socket.herror, socket.gaierror):
            return None
    
    def _detect_vulnerabilities(self, scan_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect potential vulnerabilities based on scan results.
        
        Args:
            scan_results: Complete scan results
        
        Returns:
            List of detected vulnerabilities
        """
        vulnerabilities = []
        
        # Check for common vulnerable services
        vulnerable_services = {
            'ftp': {'port': 21, 'severity': 'medium', 'description': 'FTP service detected - may allow anonymous access'},
            'telnet': {'port': 23, 'severity': 'high', 'description': 'Telnet service detected - unencrypted protocol'},
            'ssh': {'port': 22, 'severity': 'low', 'description': 'SSH service detected - ensure strong authentication'},
            'http': {'port': 80, 'severity': 'low', 'description': 'HTTP service detected - unencrypted web traffic'},
            'mysql': {'port': 3306, 'severity': 'medium', 'description': 'MySQL database exposed'},
            'postgresql': {'port': 5432, 'severity': 'medium', 'description': 'PostgreSQL database exposed'},
            'rdp': {'port': 3389, 'severity': 'high', 'description': 'RDP service detected - common attack vector'},
        }
        
        for host in scan_results.get('hosts', []):
            for port_info in host.get('open_ports', []):
                service = port_info.get('service', '').lower()
                port = port_info.get('port')
                
                if service in vulnerable_services:
                    vuln = vulnerable_services[service].copy()
                    vuln.update({
                        'host': host['ip'],
                        'port': port,
                        'service': service,
                        'detected_version': port_info.get('version', 'unknown')
                    })
                    vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def quick_scan(self, target: str) -> Dict[str, Any]:
        """
        Perform a quick scan with reduced scope.
        
        Args:
            target: Target to scan
        
        Returns:
            Quick scan results
        """
        logger.info(f"Performing quick scan on {target}")
        return self.scan(target, ports="21-23,80,443,3306,3389,8080")
    
    def deep_scan(self, target: str) -> Dict[str, Any]:
        """
        Perform a comprehensive deep scan.
        
        Args:
            target: Target to scan
        
        Returns:
            Deep scan results
        """
        logger.info(f"Performing deep scan on {target}")
        return self.scan(target, ports="1-65535")
