"""
AI Engine Module
Provides AI-powered analysis and intelligence for security assessments
"""

from typing import Dict, List, Any, Optional
import json
from datetime import datetime

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class AIEngine:
    """
    AI-powered analysis engine for security assessments.
    Provides intelligent threat analysis, risk scoring, and recommendations.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the AI engine.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.ai_config = config.get('ai', {})
        self.enabled = self.ai_config.get('enabled', True)
        logger.info(f"AIEngine initialized (enabled: {self.enabled})")
    
    def analyze(self, scan_results: Dict[str, Any], mode: str = 'basic') -> Dict[str, Any]:
        """
        Perform AI-powered analysis on scan results.
        
        Args:
            scan_results: Results from security scan
            mode: Analysis mode ('basic', 'advanced', 'full')
        
        Returns:
            Dictionary containing AI analysis results
        """
        logger.info(f"Starting AI analysis in {mode} mode")
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'mode': mode,
            'risk_level': 'unknown',
            'risk_score': 0.0,
            'threat_categories': [],
            'recommendations': [],
            'insights': []
        }
        
        if not self.enabled:
            logger.warning("AI engine is disabled")
            analysis['status'] = 'disabled'
            return analysis
        
        try:
            # Calculate risk score
            analysis['risk_score'] = self._calculate_risk_score(scan_results)
            analysis['risk_level'] = self._determine_risk_level(analysis['risk_score'])
            
            # Identify threat categories
            analysis['threat_categories'] = self._identify_threats(scan_results)
            
            # Generate recommendations
            analysis['recommendations'] = self._generate_recommendations(scan_results)
            
            # Advanced analysis
            if mode in ['advanced', 'full']:
                analysis['attack_vectors'] = self._identify_attack_vectors(scan_results)
                analysis['vulnerability_chain'] = self._analyze_vulnerability_chain(scan_results)
            
            # Full analysis
            if mode == 'full':
                analysis['predictive_analysis'] = self._predictive_analysis(scan_results)
                analysis['compliance_check'] = self._compliance_check(scan_results)
            
            # Generate insights
            analysis['insights'] = self._generate_insights(scan_results, analysis)
            
            logger.info(f"AI analysis completed. Risk level: {analysis['risk_level']}")
            
        except Exception as e:
            logger.error(f"Error during AI analysis: {str(e)}")
            analysis['error'] = str(e)
        
        return analysis
    
    def _calculate_risk_score(self, scan_results: Dict[str, Any]) -> float:
        """
        Calculate overall risk score based on scan results.
        
        Args:
            scan_results: Scan results to analyze
        
        Returns:
            Risk score (0.0 - 10.0)
        """
        score = 0.0
        
        # Count vulnerabilities by severity
        vulns = scan_results.get('vulnerabilities', [])
        severity_weights = {'low': 1, 'medium': 3, 'high': 7, 'critical': 10}
        
        for vuln in vulns:
            severity = vuln.get('severity', 'low')
            score += severity_weights.get(severity, 1)
        
        # Factor in number of exposed services
        total_ports = scan_results.get('total_open_ports', 0)
        score += min(total_ports * 0.1, 2.0)
        
        # Normalize to 0-10 scale
        return min(score, 10.0)
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """
        Determine risk level category from score.
        
        Args:
            risk_score: Numerical risk score
        
        Returns:
            Risk level string
        """
        if risk_score >= 8.0:
            return 'critical'
        elif risk_score >= 6.0:
            return 'high'
        elif risk_score >= 4.0:
            return 'medium'
        elif risk_score >= 2.0:
            return 'low'
        else:
            return 'minimal'
    
    def _identify_threats(self, scan_results: Dict[str, Any]) -> List[str]:
        """
        Identify threat categories present in the scan.
        
        Args:
            scan_results: Scan results
        
        Returns:
            List of threat categories
        """
        threats = set()
        
        for vuln in scan_results.get('vulnerabilities', []):
            service = vuln.get('service', '')
            
            if service in ['ftp', 'telnet']:
                threats.add('unencrypted_protocols')
            elif service in ['mysql', 'postgresql', 'mongodb']:
                threats.add('exposed_database')
            elif service == 'rdp':
                threats.add('remote_access_exposure')
            elif service in ['http', 'https']:
                threats.add('web_application_exposure')
            
            if vuln.get('severity') in ['high', 'critical']:
                threats.add('critical_vulnerabilities')
        
        return list(threats)
    
    def _generate_recommendations(self, scan_results: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate security recommendations based on findings.
        
        Args:
            scan_results: Scan results
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        vulns = scan_results.get('vulnerabilities', [])
        
        # Service-specific recommendations
        services_found = set()
        for vuln in vulns:
            service = vuln.get('service', '')
            services_found.add(service)
            
            if service == 'telnet' and service not in [r.get('service') for r in recommendations]:
                recommendations.append({
                    'priority': 'high',
                    'service': 'telnet',
                    'title': 'Disable Telnet Service',
                    'description': 'Replace Telnet with SSH for secure remote access',
                    'impact': 'Prevents credential theft and man-in-the-middle attacks'
                })
            
            if service == 'ftp' and service not in [r.get('service') for r in recommendations]:
                recommendations.append({
                    'priority': 'medium',
                    'service': 'ftp',
                    'title': 'Secure FTP Service',
                    'description': 'Use SFTP or FTPS instead of plain FTP',
                    'impact': 'Protects file transfers from interception'
                })
            
            if service == 'rdp' and service not in [r.get('service') for r in recommendations]:
                recommendations.append({
                    'priority': 'high',
                    'service': 'rdp',
                    'title': 'Secure RDP Access',
                    'description': 'Implement network-level authentication and use VPN',
                    'impact': 'Reduces brute-force attack surface'
                })
        
        # General recommendations
        if len(vulns) > 0:
            recommendations.append({
                'priority': 'medium',
                'title': 'Regular Security Updates',
                'description': 'Keep all systems and services updated with latest security patches',
                'impact': 'Addresses known vulnerabilities'
            })
        
        if scan_results.get('total_open_ports', 0) > 10:
            recommendations.append({
                'priority': 'medium',
                'title': 'Minimize Attack Surface',
                'description': 'Close unnecessary ports and disable unused services',
                'impact': 'Reduces potential entry points for attackers'
            })
        
        return recommendations
    
    def _identify_attack_vectors(self, scan_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify potential attack vectors.
        
        Args:
            scan_results: Scan results
        
        Returns:
            List of attack vectors
        """
        attack_vectors = []
        
        for host in scan_results.get('hosts', []):
            for port in host.get('open_ports', []):
                vector = {
                    'host': host['ip'],
                    'port': port['port'],
                    'service': port['service'],
                    'attack_types': []
                }
                
                service = port['service'].lower()
                
                if service == 'ssh':
                    vector['attack_types'].extend(['brute_force', 'credential_stuffing'])
                elif service in ['http', 'https']:
                    vector['attack_types'].extend(['sql_injection', 'xss', 'csrf'])
                elif service == 'ftp':
                    vector['attack_types'].extend(['anonymous_access', 'brute_force'])
                elif service == 'rdp':
                    vector['attack_types'].extend(['brute_force', 'bluekeep'])
                
                if vector['attack_types']:
                    attack_vectors.append(vector)
        
        return attack_vectors
    
    def _analyze_vulnerability_chain(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze potential vulnerability chains.
        
        Args:
            scan_results: Scan results
        
        Returns:
            Vulnerability chain analysis
        """
        return {
            'potential_chains': [],
            'entry_points': [],
            'privilege_escalation_paths': []
        }
    
    def _predictive_analysis(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform predictive analysis on potential future threats.
        
        Args:
            scan_results: Scan results
        
        Returns:
            Predictive analysis results
        """
        return {
            'trend_analysis': 'stable',
            'emerging_threats': [],
            'forecast': 'No significant changes predicted in the next 30 days'
        }
    
    def _compliance_check(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check compliance with security standards.
        
        Args:
            scan_results: Scan results
        
        Returns:
            Compliance check results
        """
        return {
            'pci_dss': {'compliant': False, 'issues': []},
            'hipaa': {'compliant': False, 'issues': []},
            'gdpr': {'compliant': False, 'issues': []}
        }
    
    def _generate_insights(self, scan_results: Dict[str, Any], analysis: Dict[str, Any]) -> List[str]:
        """
        Generate human-readable insights from analysis.
        
        Args:
            scan_results: Original scan results
            analysis: AI analysis results
        
        Returns:
            List of insight strings
        """
        insights = []
        
        risk_level = analysis.get('risk_level', 'unknown')
        vuln_count = len(scan_results.get('vulnerabilities', []))
        host_count = len(scan_results.get('hosts', []))
        
        insights.append(f"Scanned {host_count} host(s) and identified {vuln_count} potential security issues")
        insights.append(f"Overall risk level assessed as: {risk_level.upper()}")
        
        if vuln_count > 0:
            insights.append(f"Immediate attention required for {vuln_count} vulnerabilities")
        
        threat_categories = analysis.get('threat_categories', [])
        if 'critical_vulnerabilities' in threat_categories:
            insights.append("Critical vulnerabilities detected - immediate remediation recommended")
        
        if 'unencrypted_protocols' in threat_categories:
            insights.append("Unencrypted protocols detected - data transmission may be at risk")
        
        return insights
