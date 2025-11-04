"""
Reporter Module
Generates comprehensive security reports
"""

from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import json

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ReportGenerator:
    """
    Generates security reports in various formats.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the report generator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.report_config = config.get('reporting', {})
        logger.info("ReportGenerator initialized")
    
    def generate(
        self,
        scan_data: Dict[str, Any],
        output_path: str,
        format: str = 'html'
    ) -> bool:
        """
        Generate a security report.
        
        Args:
            scan_data: Scan results and analysis data
            output_path: Path to save the report
            format: Report format ('html', 'pdf', 'json', 'xml')
        
        Returns:
            True if report generated successfully
        """
        logger.info(f"Generating {format} report to {output_path}")
        
        try:
            if format == 'json':
                return self._generate_json(scan_data, output_path)
            elif format == 'html':
                return self._generate_html(scan_data, output_path)
            elif format == 'pdf':
                return self._generate_pdf(scan_data, output_path)
            elif format == 'xml':
                return self._generate_xml(scan_data, output_path)
            else:
                logger.error(f"Unsupported format: {format}")
                return False
        
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return False
    
    def _generate_json(self, scan_data: Dict[str, Any], output_path: str) -> bool:
        """Generate JSON format report."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(scan_data, f, indent=2)
        
        logger.info(f"JSON report generated: {output_path}")
        return True
    
    def _generate_html(self, scan_data: Dict[str, Any], output_path: str) -> bool:
        """Generate HTML format report."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        html_content = self._create_html_template(scan_data)
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        logger.info(f"HTML report generated: {output_path}")
        return True
    
    def _generate_pdf(self, scan_data: Dict[str, Any], output_path: str) -> bool:
        """Generate PDF format report."""
        # Placeholder for PDF generation
        logger.warning("PDF generation not yet implemented")
        return False
    
    def _generate_xml(self, scan_data: Dict[str, Any], output_path: str) -> bool:
        """Generate XML format report."""
        # Placeholder for XML generation
        logger.warning("XML generation not yet implemented")
        return False
    
    def _create_html_template(self, scan_data: Dict[str, Any]) -> str:
        """Create HTML report template."""
        target = scan_data.get('target', 'Unknown')
        scan_time = scan_data.get('scan_time', datetime.now().isoformat())
        hosts = scan_data.get('hosts', [])
        vulnerabilities = scan_data.get('vulnerabilities', [])
        ai_analysis = scan_data.get('ai_analysis', {})
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AIKAILNOV4 Security Report - {target}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .summary {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .risk-critical {{ color: #e74c3c; font-weight: bold; }}
        .risk-high {{ color: #e67e22; font-weight: bold; }}
        .risk-medium {{ color: #f39c12; font-weight: bold; }}
        .risk-low {{ color: #27ae60; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #34495e; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f5f5f5; }}
        .footer {{ margin-top: 40px; text-align: center; color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>AIKAILNOV4 Security Assessment Report</h1>
        
        <div class="summary">
            <h2>Executive Summary</h2>
            <p><strong>Target:</strong> {target}</p>
            <p><strong>Scan Date:</strong> {scan_time}</p>
            <p><strong>Hosts Scanned:</strong> {len(hosts)}</p>
            <p><strong>Total Open Ports:</strong> {scan_data.get('total_open_ports', 0)}</p>
            <p><strong>Vulnerabilities Found:</strong> {len(vulnerabilities)}</p>
        </div>
        
        {"<h2>AI Risk Assessment</h2>" if ai_analysis else ""}
        {"<p><strong>Risk Score:</strong> " + str(ai_analysis.get('risk_score', 'N/A')) + "/10.0</p>" if ai_analysis else ""}
        {"<p><strong>Risk Level:</strong> <span class='risk-" + ai_analysis.get('risk_level', 'unknown').lower() + "'>" + ai_analysis.get('risk_level', 'N/A').upper() + "</span></p>" if ai_analysis else ""}
        
        <h2>Discovered Hosts</h2>
        <table>
            <tr>
                <th>IP Address</th>
                <th>Hostname</th>
                <th>State</th>
                <th>Open Ports</th>
                <th>OS</th>
            </tr>
            {"".join([f"<tr><td>{h.get('ip')}</td><td>{h.get('hostname', 'N/A')}</td><td>{h.get('state')}</td><td>{len(h.get('open_ports', []))}</td><td>{h.get('os', 'Unknown')}</td></tr>" for h in hosts])}
        </table>
        
        {"<h2>Vulnerabilities</h2>" if vulnerabilities else ""}
        {"<table><tr><th>Host</th><th>Port</th><th>Service</th><th>Severity</th><th>Description</th></tr>" if vulnerabilities else ""}
        {"".join([f"<tr><td>{v.get('host')}</td><td>{v.get('port')}</td><td>{v.get('service')}</td><td class='risk-{v.get('severity')}'>{v.get('severity', '').upper()}</td><td>{v.get('description')}</td></tr>" for v in vulnerabilities])}
        {"</table>" if vulnerabilities else ""}
        
        <div class="footer">
            <p>Generated by AIKAILNOV4 v1.0.0 | AI-Powered Security Assessment</p>
            <p>Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        return html
