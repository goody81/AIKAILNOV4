"""
Interactive shell module for AIKAILNOV4
"""

from typing import Dict, Any
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class InteractiveShell:
    """Interactive command shell for AIKAILNOV4."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize interactive shell."""
        self.config = config
        self.running = True
    
    def run(self):
        """Run the interactive shell."""
        logger.info("Starting interactive shell")
        
        print("\nAIKAILNOV4 Interactive Mode")
        print("Type 'help' for commands or 'exit' to quit\n")
        
        while self.running:
            try:
                command = input("aikail> ").strip()
                
                if not command:
                    continue
                
                self._execute_command(command)
                
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def _execute_command(self, command: str):
        """Execute a command."""
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd == 'exit' or cmd == 'quit':
            self.running = False
            print("Goodbye!")
        elif cmd == 'help':
            self._show_help()
        else:
            print(f"Unknown command: {cmd}")
            print("Type 'help' for available commands")
    
    def _show_help(self):
        """Show help message."""
        print("""
Available Commands:
  help              Show this help message
  scan <target>     Scan a target
  analyze <id>      Analyze scan results
  report <id>       Generate report
  exit              Exit interactive mode
""")
