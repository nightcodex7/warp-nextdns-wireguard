"""
Navigation Manager
Handles menu navigation and ensures proper flow throughout the application
"""

import sys
from typing import Dict, List, Optional, Callable
from rich.console import Console
from rich.prompt import Prompt, Confirm
import logging

logger = logging.getLogger(__name__)

class NavigationManager:
    """Manages navigation between different sections of the application"""
    
    def __init__(self):
        self.console = Console()
        self.menu_stack = []
        self.current_menu = "main"
        self.menu_history = []
        self.auto_continue = False
        
    def push_menu(self, menu_name: str):
        """Push menu to stack"""
        self.menu_stack.append(self.current_menu)
        self.current_menu = menu_name
        self.menu_history.append(menu_name)
    
    def pop_menu(self) -> Optional[str]:
        """Pop menu from stack"""
        if self.menu_stack:
            previous_menu = self.menu_stack.pop()
            self.current_menu = previous_menu
            return previous_menu
        return None
    
    def get_current_menu(self) -> str:
        """Get current menu name"""
        return self.current_menu
    
    def show_menu(self, title: str, options: List[Dict], auto_continue: bool = False) -> str:
        """Show menu with proper navigation"""
        try:
            self.console.print(f"\n[bold blue]{title}[/bold blue]")
            self.console.print("=" * len(title))
            
            # Display options
            for i, option in enumerate(options, 1):
                self.console.print(f"{i}. {option['label']}")
            
            # Add navigation options
            if self.menu_stack:
                self.console.print(f"{len(options) + 1}. Back to previous menu")
            self.console.print(f"{len(options) + 2}. Exit")
            
            # Get user choice
            if auto_continue:
                choice = "1"  # Auto-select first option
            else:
                try:
                    choice = Prompt.ask(
                        "\nEnter your choice", 
                        choices=[str(i) for i in range(1, len(options) + 3)],
                        default="1"
                    )
                except (KeyboardInterrupt, EOFError):
                    return "exit"
            
            # Handle navigation
            if choice == str(len(options) + 1) and self.menu_stack:
                return "back"
            elif choice == str(len(options) + 2):
                return "exit"
            else:
                return choice
                
        except Exception as e:
            logger.error(f"Menu display error: {e}")
            return "exit"
    
    def execute_menu_option(self, options: List[Dict], choice: str) -> bool:
        """Execute selected menu option"""
        try:
            if choice == "back":
                self.pop_menu()
                return True
            elif choice == "exit":
                return False
            else:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(options):
                    option = options[choice_index]
                    if 'action' in option and callable(option['action']):
                        option['action']()
                    return True
                else:
                    self.console.print("[red]Invalid choice[/red]")
                    return True
        except Exception as e:
            logger.error(f"Menu execution error: {e}")
            return True
    
    def run_menu_loop(self, title: str, options: List[Dict], auto_continue: bool = False):
        """Run menu loop with proper navigation"""
        while True:
            choice = self.show_menu(title, options, auto_continue)
            if not self.execute_menu_option(options, choice):
                break
            
            if auto_continue:
                break
    
    def confirm_action(self, message: str, auto_accept: bool = False) -> bool:
        """Confirm action with auto-accept option"""
        if auto_accept:
            return True
        
        try:
            return Confirm.ask(message)
        except (KeyboardInterrupt, EOFError):
            return False
    
    def prompt_input(self, message: str, default: str = "", auto_fill: bool = False) -> str:
        """Prompt for input with auto-fill option"""
        if auto_fill and default:
            return default
        
        try:
            return Prompt.ask(message, default=default)
        except (KeyboardInterrupt, EOFError):
            return default
    
    def handle_error(self, error: Exception, auto_continue: bool = False):
        """Handle errors with auto-continue option"""
        self.console.print(f"[red]Error: {error}[/red]")
        
        if not auto_continue:
            try:
                Prompt.ask("Press Enter to continue")
            except (KeyboardInterrupt, EOFError):
                pass
    
    def clear_screen(self):
        """Clear the screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_progress(self, message: str, auto_continue: bool = False):
        """Show progress message"""
        self.console.print(f"[yellow]{message}[/yellow]")
        if not auto_continue:
            try:
                Prompt.ask("Press Enter to continue")
            except (KeyboardInterrupt, EOFError):
                pass

# Global instance
navigation_manager = NavigationManager() 