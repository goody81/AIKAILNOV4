# Scripts

Utility scripts for AIKAILNOV4 installation, maintenance, and operations.

## Available Scripts

### install.sh
Automated installation script for AIKAILNOV4.

**Usage:**
```bash
sudo bash scripts/install.sh
```

**What it does:**
- Checks system requirements
- Installs system dependencies
- Creates virtual environment
- Installs Python packages
- Initializes database
- Sets up configuration
- Verifies installation

**Supported Systems:**
- Kali Linux
- Ubuntu/Debian
- Arch Linux
- macOS

---

### init_db.py
Database initialization script.

**Usage:**
```bash
python3 scripts/init_db.py
```

**What it does:**
- Creates database schema
- Creates necessary tables
- Sets up indexes
- Initializes with default data

---

### verify_installation.py
System verification and health check script.

**Usage:**
```bash
python3 scripts/verify_installation.py
```

**What it checks:**
- Python version
- System dependencies
- Python packages
- Directory structure
- Configuration files
- Database status

---

## Creating Custom Scripts

You can create additional scripts for automation. Place them in this directory and follow these guidelines:

### Python Scripts

```python
#!/usr/bin/env python3
"""
Script description
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Your code here

if __name__ == '__main__':
    main()
```

### Shell Scripts

```bash
#!/bin/bash
# Script description

set -e  # Exit on error

# Your code here
```

## Best Practices

1. **Make scripts executable**: `chmod +x script.sh`
2. **Add shebang**: `#!/usr/bin/env python3` or `#!/bin/bash`
3. **Handle errors**: Use proper error handling
4. **Provide feedback**: Print status messages
5. **Document usage**: Add help text and examples
6. **Test thoroughly**: Test on clean systems

## Maintenance Scripts

Consider creating scripts for:

- Database backups
- Log rotation
- Threat database updates
- Report generation
- System cleanup
- Performance monitoring
- Automated testing

---

For more information, see the [main documentation](../docs/README.md).
