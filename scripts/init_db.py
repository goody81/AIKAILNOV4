#!/usr/bin/env python3
"""
Database initialization script for AIKAILNOV4
"""

import sys
import sqlite3
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def create_database():
    """Create and initialize the AIKAILNOV4 database."""
    
    print("Initializing AIKAILNOV4 database...")
    
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Connect to database
    db_path = data_dir / "aikail.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    print("Creating tables...")
    
    # Scans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id TEXT UNIQUE NOT NULL,
            target TEXT NOT NULL,
            scan_type TEXT NOT NULL,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            status TEXT NOT NULL,
            results TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Hosts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hosts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            hostname TEXT,
            os TEXT,
            state TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (scan_id) REFERENCES scans(scan_id)
        )
    """)
    
    # Ports table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host_id INTEGER NOT NULL,
            port_number INTEGER NOT NULL,
            protocol TEXT NOT NULL,
            state TEXT NOT NULL,
            service TEXT,
            version TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (host_id) REFERENCES hosts(id)
        )
    """)
    
    # Vulnerabilities table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id TEXT NOT NULL,
            host_id INTEGER NOT NULL,
            vuln_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT,
            cvss_score REAL,
            cve_id TEXT,
            remediation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (scan_id) REFERENCES scans(scan_id),
            FOREIGN KEY (host_id) REFERENCES hosts(id)
        )
    """)
    
    # AI Analysis table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id TEXT NOT NULL,
            risk_score REAL NOT NULL,
            risk_level TEXT NOT NULL,
            analysis_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (scan_id) REFERENCES scans(scan_id)
        )
    """)
    
    # Reports table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id TEXT NOT NULL,
            report_type TEXT NOT NULL,
            file_path TEXT NOT NULL,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (scan_id) REFERENCES scans(scan_id)
        )
    """)
    
    # Create indexes
    print("Creating indexes...")
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_scans_scan_id ON scans(scan_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_hosts_scan_id ON hosts(scan_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_hosts_ip ON hosts(ip_address)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ports_host_id ON ports(host_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_vulns_scan_id ON vulnerabilities(scan_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_vulns_severity ON vulnerabilities(severity)")
    
    # Commit changes
    conn.commit()
    
    print(f"✓ Database created successfully at: {db_path}")
    print("✓ Tables created: scans, hosts, ports, vulnerabilities, ai_analysis, reports")
    print("✓ Indexes created")
    
    # Close connection
    conn.close()
    
    return True


if __name__ == '__main__':
    try:
        create_database()
        print("\n[SUCCESS] Database initialization completed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Database initialization failed: {str(e)}")
        sys.exit(1)
