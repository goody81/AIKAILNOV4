# Examples

This directory contains example scripts demonstrating how to use AIKAILNOV4.

## Available Examples

### 1. basic_scan.py
Basic network scanning example showing how to:
- Initialize the scanner
- Perform a simple scan
- Display results

**Usage:**
```bash
python3 examples/basic_scan.py
```

### 2. ai_analysis.py
AI-enhanced security analysis example showing how to:
- Perform a scan
- Run AI analysis
- Get recommendations

**Usage:**
```bash
python3 examples/ai_analysis.py
```

## Running Examples

Make sure you have AIKAILNOV4 installed and configured:

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp config/config.example.yaml config/config.yaml

# Run an example
python3 examples/basic_scan.py
```

## Creating Your Own Examples

Feel free to create your own examples and submit them via pull request!

Basic template:
```python
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.aikail import AIKail

# Your code here
```
