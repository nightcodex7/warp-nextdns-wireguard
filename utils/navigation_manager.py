<<<<<<< HEAD
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
=======
"""Navigation manager for improved menu navigation and auto-response handling."""
import os
import sys
import time
from typing import List, Optional, Dict, Callable
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import print as rprint

# Platform-specific imports
if os.name != 'nt':
    import select
    import termios
    import tty


class NavigationManager:
    """Handle menu navigation with auto-response capabilities."""
    
    def __init__(self, auto_mode: bool = False):
        self.console = Console()
        self.auto_mode = auto_mode
        self.auto_responses = {
            "yes": ["y", "yes", "continue", "proceed", "accept", "ok"],
            "no": ["n", "no", "cancel", "abort", "decline"],
            "all": ["all", "a", "always"],
        }
        self.navigation_stack = []
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_menu(self, title: str, options: List[Dict[str, any]], back_option: bool = True) -> Optional[str]:
        """Display a menu with options and handle navigation."""
        self.clear_screen()
        self.console.print(Panel(title, style="bold blue"))
        
        # Create table for options
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", style="cyan", width=12)
        table.add_column("Description", style="white")
        
        # Add options to table
        for i, option in enumerate(options, 1):
            table.add_row(str(i), option["description"])
        
        if back_option and self.navigation_stack:
            table.add_row("0", "Back to previous menu")
        
        table.add_row("q", "Quit")
        
        self.console.print(table)
        
        # Handle input
        if self.auto_mode:
            # In auto mode, select first option
            time.sleep(0.5)  # Brief pause for visibility
            choice = "1"
            self.console.print(f"\n[yellow]Auto-selecting: {choice}[/yellow]")
        else:
            choice = Prompt.ask("\nSelect an option", default="")
        
        # Process choice
        if choice.lower() == 'q':
            return None
        elif choice == '0' and back_option and self.navigation_stack:
            return 'back'
        elif choice.isdigit() and 1 <= int(choice) <= len(options):
            selected_option = options[int(choice) - 1]
            return selected_option["value"]
        else:
            self.console.print("[red]Invalid choice. Please try again.[/red]")
            time.sleep(1)
            return self.display_menu(title, options, back_option)
    
    def auto_confirm(self, message: str, default: bool = True) -> bool:
        """Auto-confirm prompts in auto mode."""
        if self.auto_mode:
            self.console.print(f"\n[yellow]{message} Auto-responding: {'Yes' if default else 'No'}[/yellow]")
            time.sleep(0.5)
            return default
        else:
            return Confirm.ask(message, default=default)
    
    def auto_prompt(self, message: str, default: str = "", password: bool = False) -> str:
        """Auto-prompt with default values in auto mode."""
        if self.auto_mode and default:
            self.console.print(f"\n[yellow]{message} Auto-responding: {default if not password else '***'}[/yellow]")
            time.sleep(0.5)
            return default
        else:
            return Prompt.ask(message, default=default, password=password)
    
    def handle_stuck_terminal(self, timeout: int = 5) -> bool:
        """Handle stuck terminal by sending Enter keys."""
        if os.name == 'nt':  # Windows
            # Windows implementation
            import msvcrt
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                if msvcrt.kbhit():
                    return False
                time.sleep(0.1)
            
            # Send Enter key
            os.system('echo.')
            return True
            
        else:  # Unix-like systems
            # Save terminal settings
            old_settings = termios.tcgetattr(sys.stdin)
            
            try:
                # Set terminal to raw mode
                tty.setraw(sys.stdin.fileno())
                
                # Check if input is available
                start_time = time.time()
                while time.time() - start_time < timeout:
                    if select.select([sys.stdin], [], [], 0)[0]:
                        return False
                    time.sleep(0.1)
                
                # Send Enter key
                sys.stdin.write('\n')
                sys.stdin.flush()
                return True
                
            finally:
                # Restore terminal settings
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    
    def push_menu(self, menu_name: str):
        """Push current menu to navigation stack."""
        self.navigation_stack.append(menu_name)
    
    def pop_menu(self) -> Optional[str]:
        """Pop menu from navigation stack."""
        if self.navigation_stack:
            return self.navigation_stack.pop()
        return None
    
    def display_progress(self, message: str, steps: List[Dict[str, Callable]], auto_continue: bool = True):
        """Display progress for multi-step operations."""
        total_steps = len(steps)
        
        for i, step in enumerate(steps, 1):
            self.console.print(f"\n[cyan]Step {i}/{total_steps}:[/cyan] {step['name']}")
            
            try:
                # Execute step
                result = step['action']()
                
                if result:
                    self.console.print(f"[green]✓ {step['name']} completed successfully[/green]")
                else:
                    self.console.print(f"[red]✗ {step['name']} failed[/red]")
                    
                    if not auto_continue and not self.auto_confirm("Continue with next step?", default=False):
                        return False
                        
            except Exception as e:
                self.console.print(f"[red]✗ {step['name']} failed: {str(e)}[/red]")
                
                if not auto_continue and not self.auto_confirm("Continue with next step?", default=False):
                    return False
        
        return True
    
    def display_status(self, title: str, status_items: Dict[str, any]):
        """Display status information in a formatted table."""
        self.console.print(Panel(title, style="bold green"))
        
        table = Table(show_header=False)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        for key, value in status_items.items():
            # Format boolean values
            if isinstance(value, bool):
                value_str = "[green]Yes[/green]" if value else "[red]No[/red]"
            else:
                value_str = str(value)
            
            table.add_row(key.replace("_", " ").title(), value_str)
        
        self.console.print(table)
    
    def wait_with_spinner(self, message: str, duration: int = 3):
        """Display a spinner while waiting."""
        spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        
        if self.auto_mode:
            # In auto mode, just wait without animation
            self.console.print(f"[yellow]{message}...[/yellow]")
            time.sleep(duration)
        else:
            with self.console.status(message) as status:
                for _ in range(duration * 10):
                    time.sleep(0.1)
    
    def error_recovery(self, error: Exception, recovery_actions: List[Dict[str, Callable]]) -> bool:
        """Handle errors with recovery actions."""
        self.console.print(f"\n[red]Error occurred: {str(error)}[/red]")
        
        if not recovery_actions:
            return False
        
        self.console.print("\n[yellow]Attempting recovery actions...[/yellow]")
        
        for action in recovery_actions:
            try:
                self.console.print(f"Trying: {action['name']}")
                if action['action']():
                    self.console.print(f"[green]✓ Recovery successful with: {action['name']}[/green]")
                    return True
            except:
                continue
        
        self.console.print("[red]All recovery attempts failed.[/red]")
        return False
>>>>>>> 6f8763ed9c292fb062677073732ac3e864bb795d
