"""
Navigation Manager
Handles menu navigation and ensures proper flow throughout the application
"""

import sys
import time
import threading
from typing import Dict, List, Optional, Callable, Any
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
import logging

logger = logging.getLogger(__name__)

class NavigationManager:
    """Manages navigation between different sections of the application"""
    
    def __init__(self, auto_mode: bool = False):
        self.console = Console()
        self.auto_mode = auto_mode
        self.menu_stack = []
        self.current_menu = "main"
        self.menu_history = []
        self.auto_continue = auto_mode
        
    def clear_screen(self):
        """Clear the terminal screen"""
        self.console.clear()
    
    def display_menu(self, title: str, options: List[Dict[str, Any]], back_option: bool = True) -> Optional[str]:
        """Display a menu with options and handle navigation"""
        try:
            self.console.print(f"\n[bold blue]{title}[/bold blue]")
            self.console.print("=" * len(title))
            
            # Display options
            for i, option in enumerate(options, 1):
                self.console.print(f"{i}. {option['label']}")
            
            # Add navigation options
            if back_option and self.menu_stack:
                self.console.print(f"{len(options) + 1}. Back to previous menu")
            self.console.print(f"{len(options) + 2}. Exit")
            
            # Get user choice
            if self.auto_mode:
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
            if choice == str(len(options) + 1) and back_option and self.menu_stack:
                return "back"
            elif choice == str(len(options) + 2):
                return "exit"
            else:
                return choice
                
        except Exception as e:
            logger.error(f"Menu display error: {e}")
            return "exit"
    
    def auto_confirm(self, message: str, default: bool = True) -> bool:
        """Auto-confirm or prompt user for confirmation"""
        if self.auto_mode:
            return default
        
        try:
            return Confirm.ask(message, default=default)
        except (KeyboardInterrupt, EOFError):
            return False
    
    def auto_prompt(self, message: str, default: str = "", password: bool = False) -> str:
        """Auto-fill or prompt user for input"""
        if self.auto_mode:
            return default
        
        try:
            if password:
                return Prompt.ask(message, password=True, default=default)
            else:
                return Prompt.ask(message, default=default)
        except (KeyboardInterrupt, EOFError):
            return default
    
    def handle_stuck_terminal(self, timeout: int = 5) -> bool:
        """Handle stuck terminal by implementing timeout"""
        def check_input():
            try:
                input()
                return True
            except (KeyboardInterrupt, EOFError):
                return False
        
        # Start input thread
        input_thread = threading.Thread(target=check_input)
        input_thread.daemon = True
        input_thread.start()
        
        # Wait for timeout or input
        input_thread.join(timeout)
        
        if input_thread.is_alive():
            # Timeout occurred, continue automatically
            return True
        else:
            # User provided input
            return False
    
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
    
    def display_progress(self, message: str, steps: List[Dict[str, Callable]], auto_continue: bool = True):
        """Display progress for a series of steps"""
        self.console.print(f"\n[bold cyan]{message}[/bold cyan]")
        
        for i, step in enumerate(steps, 1):
            step_name = step.get('name', f'Step {i}')
            step_action = step.get('action')
            
            self.console.print(f"\n{i}. {step_name}")
            
            if step_action and callable(step_action):
                try:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=self.console
                    ) as progress:
                        task = progress.add_task(f"Executing {step_name}...", total=None)
                        result = step_action()
                        progress.update(task, description=f"Completed {step_name}")
                    
                    if result:
                        self.console.print(f"[green]✓ {step_name} completed[/green]")
                    else:
                        self.console.print(f"[red]✗ {step_name} failed[/red]")
                        if not auto_continue:
                            if not self.auto_confirm("Continue with remaining steps?", default=False):
                                return False
                
                except Exception as e:
                    self.console.print(f"[red]✗ {step_name} failed: {e}[/red]")
                    if not auto_continue:
                        if not self.auto_confirm("Continue with remaining steps?", default=False):
                            return False
        
        return True
    
    def display_status(self, title: str, status_items: Dict[str, Any]):
        """Display status information in a formatted table"""
        table = Table(title=title)
        table.add_column("Item", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Details", style="green")
        
        for item, value in status_items.items():
            if isinstance(value, bool):
                status = "✅ Active" if value else "❌ Inactive"
                details = "Working" if value else "Not working"
            elif isinstance(value, dict):
                status = "✅ Active" if value.get('running', False) else "❌ Inactive"
                details = str(value.get('details', ''))
            else:
                status = "✅ Active" if value else "❌ Inactive"
                details = str(value)
            
            table.add_row(item, status, details)
        
        self.console.print(table)
    
    def wait_with_spinner(self, message: str, duration: int = 3):
        """Show a spinner with message for specified duration"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task(message, total=duration)
            
            for i in range(duration):
                time.sleep(1)
                progress.update(task, completed=i + 1)
    
    def error_recovery(self, error: Exception, recovery_actions: List[Dict[str, Callable]]) -> bool:
        """Handle errors with recovery actions"""
        self.console.print(f"\n[red]Error occurred: {error}[/red]")
        
        if not recovery_actions:
            return False
        
        self.console.print("\n[yellow]Attempting recovery...[/yellow]")
        
        for action in recovery_actions:
            action_name = action.get('name', 'Recovery action')
            action_func = action.get('action')
            
            if action_func and callable(action_func):
                try:
                    self.console.print(f"Trying: {action_name}")
                    if action_func():
                        self.console.print(f"[green]✓ {action_name} successful[/green]")
                        return True
                    else:
                        self.console.print(f"[yellow]⚠ {action_name} failed[/yellow]")
                except Exception as e:
                    self.console.print(f"[red]✗ {action_name} failed: {e}[/red]")
        
        return False
    
    def show_menu(self, title: str, options: List[Dict], auto_continue: bool = False) -> str:
        """Show menu with proper navigation (legacy method for compatibility)"""
        return self.display_menu(title, options, back_option=True) or "exit"
    
    def execute_menu_option(self, options: List[Dict], choice: str) -> bool:
        """Execute selected menu option (legacy method for compatibility)"""
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
            return False
    
    def run_menu_loop(self, title: str, options: List[Dict], auto_continue: bool = False):
        """Run menu loop (legacy method for compatibility)"""
        while True:
            choice = self.show_menu(title, options, auto_continue)
            if not self.execute_menu_option(options, choice):
                break
    
    def confirm_action(self, message: str, auto_accept: bool = False) -> bool:
        """Confirm action (legacy method for compatibility)"""
        return self.auto_confirm(message, default=auto_accept)
    
    def prompt_input(self, message: str, default: str = "", auto_fill: bool = False) -> str:
        """Prompt for input (legacy method for compatibility)"""
        return self.auto_prompt(message, default=default)
    
    def handle_error(self, error: Exception, auto_continue: bool = False):
        """Handle error (legacy method for compatibility)"""
        self.console.print(f"[red]Error: {error}[/red]")
        if not auto_continue:
            self.auto_confirm("Press Enter to continue...", default=True)
    
    def show_progress(self, message: str, auto_continue: bool = False):
        """Show progress (legacy method for compatibility)"""
        self.console.print(f"[cyan]{message}[/cyan]")
        if not auto_continue:
            self.auto_confirm("Press Enter to continue...", default=True)
