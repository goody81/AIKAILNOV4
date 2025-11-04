# Contributing to AIKAILNOV4

Thank you for your interest in contributing to AIKAILNOV4! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Community](#community)

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior
- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discriminatory language
- Personal attacks or trolling
- Publishing private information
- Any conduct that could be considered inappropriate

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- GitHub account
- Basic understanding of security concepts

### Setting Up Development Environment

1. **Fork the Repository**
   ```bash
   # Fork via GitHub UI, then clone your fork
   git clone https://github.com/YOUR_USERNAME/AIKAILNOV4.git
   cd AIKAILNOV4
   ```

2. **Add Upstream Remote**
   ```bash
   git remote add upstream https://github.com/goody81/AIKAILNOV4.git
   ```

3. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Development Dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## Development Process

### Finding Something to Work On

1. Check [GitHub Issues](https://github.com/goody81/AIKAILNOV4/issues)
2. Look for issues labeled `good first issue` or `help wanted`
3. Comment on the issue to claim it
4. Wait for maintainer approval before starting work

### Creating a New Issue

Before creating an issue:
- Search existing issues to avoid duplicates
- Use the appropriate issue template
- Provide clear, detailed information
- Include steps to reproduce (for bugs)

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Good
def scan_target(target: str, ports: str = "1-1000") -> Dict[str, Any]:
    """
    Scan a target for open ports.
    
    Args:
        target: IP address or hostname
        ports: Port range to scan
    
    Returns:
        Dictionary containing scan results
    """
    pass

# Bad
def ScanTarget(target,ports="1-1000"):
    pass
```

### Documentation

- All functions must have docstrings
- Use Google-style docstrings
- Include type hints
- Document complex algorithms

Example:
```python
def calculate_risk_score(vulnerabilities: List[Dict]) -> float:
    """
    Calculate overall risk score based on vulnerabilities.
    
    The risk score is calculated using a weighted average of
    vulnerability severities and their CVSS scores.
    
    Args:
        vulnerabilities: List of vulnerability dictionaries
    
    Returns:
        Risk score between 0.0 and 10.0
    
    Raises:
        ValueError: If vulnerabilities list is empty
    
    Example:
        >>> vulns = [{'severity': 'high', 'cvss': 8.5}]
        >>> calculate_risk_score(vulns)
        8.5
    """
    pass
```

### Code Organization

```
src/
├── core/           # Core functionality
├── modules/        # Security modules
├── utils/          # Utility functions
└── api/            # API implementation
```

### Import Organization

```python
# Standard library imports
import os
import sys
from typing import Dict, List

# Third-party imports
import nmap
import yaml

# Local imports
from src.core.scanner import SecurityScanner
from src.utils.logger import setup_logger
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_scanner.py

# Run with coverage
pytest --cov=src tests/

# Run integration tests
pytest tests/integration/
```

### Writing Tests

```python
import pytest
from src.core.scanner import SecurityScanner

class TestSecurityScanner:
    """Test suite for SecurityScanner class."""
    
    @pytest.fixture
    def scanner(self):
        """Create a scanner instance for testing."""
        config = {'scanning': {'timeout': 30}}
        return SecurityScanner(config)
    
    def test_scan_valid_target(self, scanner):
        """Test scanning a valid target."""
        result = scanner.scan('127.0.0.1', '80')
        assert 'hosts' in result
        assert result['target'] == '127.0.0.1'
    
    def test_scan_invalid_target(self, scanner):
        """Test scanning an invalid target."""
        with pytest.raises(ValueError):
            scanner.scan('invalid_target', '80')
```

### Test Coverage

- Aim for >80% code coverage
- Test edge cases and error conditions
- Include integration tests for critical paths

## Submitting Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-web-scanner`
- `bugfix/fix-port-scan-timeout`
- `docs/update-installation-guide`
- `refactor/improve-ai-engine`

### Commit Messages

Write clear, descriptive commit messages:

```
Good:
✓ Add SQL injection detection module
✓ Fix timeout issue in port scanner
✓ Update installation documentation

Bad:
✗ Update code
✗ Fix bug
✗ Changes
```

Format:
```
<type>: <short summary>

<detailed description>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Request Process

1. **Update Your Branch**
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Run Tests**
   ```bash
   pytest
   flake8 src/
   black src/
   mypy src/
   ```

3. **Push Changes**
   ```bash
   git push origin your-branch
   ```

4. **Create Pull Request**
   - Use the PR template
   - Link related issues
   - Provide clear description
   - Add screenshots (if UI changes)

5. **Code Review**
   - Address review comments
   - Keep discussion professional
   - Be open to feedback

6. **Merge**
   - Maintainer will merge when approved
   - Delete branch after merge

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No merge conflicts
- [ ] Commit messages are clear

## Development Guidelines

### Security Considerations

- Never commit API keys or credentials
- Use environment variables for sensitive data
- Validate all user input
- Follow secure coding practices
- Report security issues privately

### Performance

- Profile code before optimization
- Use appropriate data structures
- Avoid premature optimization
- Document performance-critical code

### Adding New Modules

1. Create module in `src/modules/`
2. Implement required interface
3. Add tests
4. Update documentation
5. Add example usage

Example module structure:
```python
"""
New Security Module
"""

from typing import Dict, Any

class NewModule:
    """New security module implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def execute(self, target: str, **kwargs) -> Dict[str, Any]:
        """
        Execute the module.
        
        Args:
            target: Target to scan
            **kwargs: Additional parameters
        
        Returns:
            Module results
        """
        pass
```

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and features
- **GitHub Discussions**: General questions
- **Discord**: Real-time chat
- **Email**: security@aikailnov4.com

### Getting Help

- Read the documentation first
- Search existing issues
- Ask in discussions or Discord
- Be patient and respectful

### Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project README
- Annual contributor highlight

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to reach out:
- Open a discussion on GitHub
- Join our Discord server
- Email: support@aikailnov4.com

---

**Thank you for contributing to AIKAILNOV4!** 🎉
