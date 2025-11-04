#!/usr/bin/env python3
"""
AIKAILNOV4 - AI-Powered Kali Linux Security System
Main Entry Point

This is the primary command-line interface for the AIKAILNOV4 security system.
"""

import sys
import click
from pathlib import Path
from typing import Optional
import yaml
from rich.console import Console
from rich.table import Table

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.scanner import SecurityScanner
from src.core.ai_engine import AIEngine
from src.core.reporter import ReportGenerator
from src.utils.logger import setup_logger
from src.utils.config import load_config

console = Console()
logger = setup_logger(__name__)

__version__ = "1.0.0"


@click.group()
@click.version_option(version=__version__)
@click.option('--config', '-c', type=click.Path(), help='Path to configuration file')
@click.option('--debug', '-d', is_flag=True, help='Enable debug mode')
@click.pass_context
def cli(ctx, config, debug):
    """
    AIKAILNOV4 - AI-Powered Kali Linux Security System
    
    An advanced security automation framework combining AI with powerful
    penetration testing tools for intelligent security assessment.
    """
    ctx.ensure_object(dict)
    
    # Load configuration
    config_path = config or 'config/config.yaml'
    try:
        ctx.obj['config'] = load_config(config_path)
    except FileNotFoundError:
        console.print(f"[yellow]Warning: Config file not found at {config_path}[/yellow]")
        console.print("[yellow]Using default configuration[/yellow]")
        ctx.obj['config'] = {}
    
    ctx.obj['debug'] = debug
    
    if debug:
        logger.setLevel('DEBUG')
        console.print("[yellow]Debug mode enabled[/yellow]")


@cli.command()
@click.option('--target', '-t', required=True, help='Target IP address or hostname')
@click.option('--ports', '-p', default='1-1000', help='Port range to scan')
@click.option('--ai-mode', type=click.Choice(['basic', 'advanced', 'full']), default='basic',
              help='AI analysis mode')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--report-format', type=click.Choice(['html', 'pdf', 'json', 'xml']), 
              default='html', help='Report format')
@click.pass_context
def scan(ctx, target, ports, ai_mode, output, report_format):
    """
    Perform a security scan on the specified target.
    
    Examples:
        aikail scan -t 192.168.1.100
        aikail scan -t example.com --ai-mode advanced
        aikail scan -t 10.0.0.0/24 -o report.html
    """
    console.print(f"[bold blue]Starting security scan on {target}[/bold blue]")
    console.print(f"Port range: {ports}")
    console.print(f"AI mode: {ai_mode}")
    
    try:
        # Initialize scanner
        scanner = SecurityScanner(ctx.obj['config'])
        
        # Perform scan
        with console.status("[bold green]Scanning..."):
            scan_results = scanner.scan(target, ports)
        
        console.print(f"[green]✓[/green] Scan completed. Found {len(scan_results.get('hosts', []))} hosts")
        
        # AI Analysis
        if ai_mode != 'basic':
            with console.status("[bold green]Performing AI analysis..."):
                ai_engine = AIEngine(ctx.obj['config'])
                analysis = ai_engine.analyze(scan_results, mode=ai_mode)
                scan_results['ai_analysis'] = analysis
            
            console.print("[green]✓[/green] AI analysis completed")
        
        # Generate report
        if output:
            reporter = ReportGenerator(ctx.obj['config'])
            reporter.generate(scan_results, output, format=report_format)
            console.print(f"[green]✓[/green] Report saved to {output}")
        
        # Display summary
        _display_scan_summary(scan_results)
        
    except Exception as e:
        console.print(f"[red]Error during scan: {str(e)}[/red]")
        if ctx.obj['debug']:
            raise
        sys.exit(1)


@cli.command()
@click.pass_context
def interactive(ctx):
    """
    Launch interactive AI security assistant mode.
    """
    console.print("[bold blue]AIKAILNOV4 Interactive Mode[/bold blue]")
    console.print("Type 'help' for available commands or 'exit' to quit\n")
    
    from src.core.interactive import InteractiveShell
    shell = InteractiveShell(ctx.obj['config'])
    shell.run()


@cli.command()
@click.option('--name', '-n', required=True, help='Module name')
@click.option('--target', '-t', required=True, help='Target IP address or hostname')
@click.option('--params', '-p', help='Module parameters (JSON format)')
@click.pass_context
def module(ctx, name, target, params):
    """
    Run a specific security module.
    
    Examples:
        aikail module -n port_scanner -t 192.168.1.100
        aikail module -n web_scanner -t example.com -p '{"depth": 3}'
    """
    console.print(f"[bold blue]Running module: {name}[/bold blue]")
    console.print(f"Target: {target}")
    
    try:
        from src.modules import load_module
        
        # Load and execute module
        mod = load_module(name)
        
        import json
        module_params = json.loads(params) if params else {}
        
        with console.status(f"[bold green]Executing {name}..."):
            results = mod.execute(target, **module_params)
        
        console.print("[green]✓[/green] Module execution completed")
        console.print("\nResults:")
        console.print(results)
        
    except Exception as e:
        console.print(f"[red]Error executing module: {str(e)}[/red]")
        if ctx.obj['debug']:
            raise
        sys.exit(1)


@cli.command()
@click.option('--list', '-l', 'list_modules', is_flag=True, help='List available modules')
@click.pass_context
def modules(ctx, list_modules):
    """
    Manage security modules.
    """
    if list_modules:
        _display_available_modules()


@cli.command()
@click.option('--threats', is_flag=True, help='Update threat intelligence database')
@click.option('--signatures', is_flag=True, help='Update vulnerability signatures')
@click.option('--all', 'update_all', is_flag=True, help='Update everything')
@click.pass_context
def update(ctx, threats, signatures, update_all):
    """
    Update threat intelligence and vulnerability databases.
    """
    console.print("[bold blue]Updating AIKAILNOV4 databases...[/bold blue]")
    
    try:
        from src.core.updater import DatabaseUpdater
        
        updater = DatabaseUpdater(ctx.obj['config'])
        
        if update_all or threats:
            with console.status("[bold green]Updating threat intelligence..."):
                updater.update_threats()
            console.print("[green]✓[/green] Threat intelligence updated")
        
        if update_all or signatures:
            with console.status("[bold green]Updating vulnerability signatures..."):
                updater.update_signatures()
            console.print("[green]✓[/green] Vulnerability signatures updated")
        
    except Exception as e:
        console.print(f"[red]Error during update: {str(e)}[/red]")
        if ctx.obj['debug']:
            raise
        sys.exit(1)


@cli.command()
@click.option('--scan-id', required=True, help='Scan ID to generate report from')
@click.option('--format', 'report_format', type=click.Choice(['html', 'pdf', 'json', 'xml']),
              default='html', help='Report format')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.pass_context
def report(ctx, scan_id, report_format, output):
    """
    Generate a report from a previous scan.
    """
    console.print(f"[bold blue]Generating report for scan {scan_id}[/bold blue]")
    
    try:
        from src.core.reporter import ReportGenerator
        from src.core.database import Database
        
        # Load scan data
        db = Database(ctx.obj['config'])
        scan_data = db.get_scan(scan_id)
        
        if not scan_data:
            console.print(f"[red]Error: Scan {scan_id} not found[/red]")
            sys.exit(1)
        
        # Generate report
        reporter = ReportGenerator(ctx.obj['config'])
        output_path = output or f"report_{scan_id}.{report_format}"
        
        with console.status("[bold green]Generating report..."):
            reporter.generate(scan_data, output_path, format=report_format)
        
        console.print(f"[green]✓[/green] Report saved to {output_path}")
        
    except Exception as e:
        console.print(f"[red]Error generating report: {str(e)}[/red]")
        if ctx.obj['debug']:
            raise
        sys.exit(1)


def _display_scan_summary(results):
    """Display a summary table of scan results."""
    table = Table(title="Scan Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total Hosts", str(len(results.get('hosts', []))))
    table.add_row("Open Ports", str(results.get('total_open_ports', 0)))
    table.add_row("Vulnerabilities", str(len(results.get('vulnerabilities', []))))
    
    if 'ai_analysis' in results:
        table.add_row("Risk Level", results['ai_analysis'].get('risk_level', 'Unknown'))
    
    console.print(table)


def _display_available_modules():
    """Display available security modules."""
    table = Table(title="Available Security Modules")
    table.add_column("Module", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Status", style="green")
    
    modules_info = [
        ("port_scanner", "Advanced port scanning with service detection", "Active"),
        ("vulnerability_scanner", "Automated vulnerability assessment", "Active"),
        ("web_scanner", "Web application security testing", "Active"),
        ("network_analyzer", "Network traffic analysis", "Active"),
        ("exploit_framework", "Automated exploitation capabilities", "Inactive"),
        ("password_cracker", "Password security analysis", "Active"),
        ("threat_intelligence", "AI-powered threat detection", "Active"),
    ]
    
    for name, desc, status in modules_info:
        table.add_row(name, desc, status)
    
    console.print(table)


def main():
    """Main entry point."""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()
