#!/usr/bin/env python3
"""
Example 2: AI-Enhanced Security Analysis
Demonstrates AI-powered vulnerability analysis
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.scanner import SecurityScanner
from src.core.ai_engine import AIEngine
from src.utils.config import load_config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Run an AI-enhanced security analysis example."""
    
    print("=" * 60)
    print("AIKAILNOV4 - AI-Enhanced Security Analysis Example")
    print("=" * 60)
    
    # Load configuration
    try:
        config = load_config('config/config.yaml')
    except FileNotFoundError:
        logger.warning("Config file not found, using defaults")
        config = {}
    
    # Initialize components
    scanner = SecurityScanner(config)
    ai_engine = AIEngine(config)
    
    # Target
    target = "127.0.0.1"
    
    print(f"\n[*] Step 1: Scanning target {target}...")
    
    # Perform initial scan
    scan_results = scanner.scan(target, "22,80,443,3306")
    
    print(f"[+] Scan completed. Found {len(scan_results['hosts'])} hosts")
    print(f"[+] Detected {scan_results['total_open_ports']} open ports")
    print(f"[+] Identified {len(scan_results['vulnerabilities'])} potential vulnerabilities")
    
    print(f"\n[*] Step 2: Performing AI analysis...")
    
    # Perform AI analysis
    ai_analysis = ai_engine.analyze(scan_results, mode='advanced')
    
    # Display AI analysis results
    print("\n" + "=" * 60)
    print("AI ANALYSIS RESULTS")
    print("=" * 60)
    
    print(f"\n[AI] Risk Score: {ai_analysis['risk_score']:.2f}/10.0")
    print(f"[AI] Risk Level: {ai_analysis['risk_level'].upper()}")
    
    # Display threat categories
    if ai_analysis['threat_categories']:
        print(f"\n[AI] Identified Threat Categories:")
        for category in ai_analysis['threat_categories']:
            print(f"     - {category.replace('_', ' ').title()}")
    
    # Display insights
    if ai_analysis['insights']:
        print(f"\n[AI] Security Insights:")
        for i, insight in enumerate(ai_analysis['insights'], 1):
            print(f"     {i}. {insight}")
    
    # Display recommendations
    if ai_analysis['recommendations']:
        print(f"\n[AI] Security Recommendations:")
        for i, rec in enumerate(ai_analysis['recommendations'], 1):
            print(f"\n     {i}. {rec['title']}")
            print(f"        Priority: {rec['priority'].upper()}")
            print(f"        {rec['description']}")
            if 'impact' in rec:
                print(f"        Impact: {rec['impact']}")
    
    # Display attack vectors (if available)
    if 'attack_vectors' in ai_analysis:
        print(f"\n[AI] Potential Attack Vectors:")
        for vector in ai_analysis['attack_vectors']:
            print(f"\n     - {vector['service']} on port {vector['port']}")
            print(f"       Attack types: {', '.join(vector['attack_types'])}")
    
    print("\n" + "=" * 60)
    print("[+] AI analysis completed!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
