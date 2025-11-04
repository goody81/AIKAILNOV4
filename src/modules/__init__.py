"""
Modules package for AIKAILNOV4
Security testing modules
"""

from typing import Dict, Any, Type


class BaseModule:
    """Base class for all security modules."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def execute(self, target: str, **kwargs) -> Dict[str, Any]:
        """Execute the module."""
        raise NotImplementedError


# Module registry
AVAILABLE_MODULES: Dict[str, Type[BaseModule]] = {}


def register_module(name: str, module_class: Type[BaseModule]):
    """Register a security module."""
    AVAILABLE_MODULES[name] = module_class


def load_module(name: str) -> Type[BaseModule]:
    """Load a module by name."""
    if name not in AVAILABLE_MODULES:
        raise ValueError(f"Module '{name}' not found")
    return AVAILABLE_MODULES[name]


def list_modules() -> list:
    """List all available modules."""
    return list(AVAILABLE_MODULES.keys())
