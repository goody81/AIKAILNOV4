"""
AIKAILNOV4 Core Package
AI-Powered Kali Linux Security System
"""

__version__ = "1.0.0"
__author__ = "AIKAILNOV4 Team"
__license__ = "MIT"

from src.core.scanner import SecurityScanner
from src.core.ai_engine import AIEngine

__all__ = ['SecurityScanner', 'AIEngine']
