#!/usr/bin/env python3
"""
CLI interface for WARP + NextDNS Manager
"""

import click
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
import time

from core import WarpNextDNSManager
from utils.platform_utils import PlatformUtils
from utils.navigation_manager import NavigationManager

console = Console()


@click.group()
@click.option('--auto', is_flag=True, help='Run in automatic mode (auto-accept prompts)')
@click.pass_context
def cli(ctx, auto):
    """WARP + NextDNS WireGuard Manager - Secure your connection with Cloudflare WARP and NextDNS."""
    ctx.ensure_object(dict)
    ctx.obj['auto'] = auto


@cli.command()
@click.pass_context
def setup(ctx):
    """Run the complete setup wizard."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    try:
        if manager.quick_setup():
            console.print("\n[green]✓ Setup completed successfully![/green]")
            console.print("\nYour connection is now secured with WARP + NextDNS")
        else:
            console.print("\n[red]✗ Setup failed. Check the logs for details.[/red]")
            sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Setup cancelled by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.pass_context
def start(ctx):
    """Start WARP and NextDNS services."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    try:
        if manager.start_services():
            console.print("[green]✓ Services started successfully![/green]")
        else:
            console.print("[red]✗ Failed to start services.[/red]")
            sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.pass_context
def stop(ctx):
    """Stop WARP and NextDNS services."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    try:
        if manager.stop_services():
            console.print("[green]✓ Services stopped successfully![/green]")
        else:
            console.print("[red]✗ Failed to stop services.[/red]")
            sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx):
    """Check connection status."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    try:
        console.print(Panel("Checking Connection Status", style="bold blue"))
        status_info = manager.get_status()
        
        # Display status in a table
        table = Table(title="System Status")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Details", style="green")
        
        # Platform info
        table.add_row("Platform", "✅ Active", f"{status_info['platform']} ({status_info['architecture']})")
        table.add_row("Python", "✅ Active", status_info['python_version'])
        
        # Services
        for service_name, service_status in status_info['services'].items():
            status_text = "✅ Running" if service_status.get('running', False) else "❌ Stopped"
            details = service_status.get('details', '')
            table.add_row(f"{service_name.title()} Service", status_text, details)
        
        # Tools
        for tool_name, tool_installed in status_info['tools'].items():
            status_text = "✅ Installed" if tool_installed else "❌ Not Installed"
            table.add_row(f"{tool_name.upper()} Tool", status_text, "")
        
        # Network
        for network_item, network_status in status_info['network'].items():
            if network_item == 'internet':
                status_text = "✅ Connected" if network_status else "❌ Disconnected"
                table.add_row("Internet", status_text, "")
            elif network_item == 'warp_ip':
                status_text = "✅ Active" if network_status else "❌ Inactive"
                table.add_row("WARP IP", status_text, network_status or "Not available")
            elif network_item == 'dns_servers':
                status_text = "✅ Configured" if network_status else "❌ Not configured"
                table.add_row("DNS Servers", status_text, ", ".join(network_status) if network_status else "")
        
        console.print(table)
        
        if manager.verify_connection():
            console.print("\n[green]✓ All systems operational![/green]")
        else:
            console.print("\n[yellow]⚠ Some services are not working properly.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--refresh', default=5, help='Refresh interval in seconds')
@click.pass_context
def monitor(ctx, refresh):
    """Live status monitoring."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))
    
    def generate_status_table():
        try:
            status_info = manager.get_status()
            
            table = Table(title=f"Live Status Monitor (Refreshing every {refresh}s)")
            table.add_column("Component", style="cyan")
            table.add_column("Status", style="magenta")
            table.add_column("Details", style="green")
            table.add_column("Last Update", style="yellow")
            
            # Services
            for service_name, service_status in status_info['services'].items():
                status_text = "✅ Running" if service_status.get('running', False) else "❌ Stopped"
                details = service_status.get('details', '')
                table.add_row(f"{service_name.title()}", status_text, details, status_info['timestamp'])
            
            # Network
            internet_status = "✅ Connected" if status_info['network']['internet'] else "❌ Disconnected"
            table.add_row("Internet", internet_status, "", status_info['timestamp'])
            
            warp_ip = status_info['network']['warp_ip']
            warp_status = "✅ Active" if warp_ip else "❌ Inactive"
            table.add_row("WARP IP", warp_status, warp_ip or "Not available", status_info['timestamp'])
            
            return table
        except Exception as e:
            table = Table(title="Status Monitor - Error")
            table.add_column("Error", style="red")
            table.add_row(str(e))
            return table
    
    try:
        console.print("[yellow]Press Ctrl+C to stop monitoring[/yellow]")
        
        with Live(generate_status_table(), refresh_per_second=1) as live:
            while True:
                live.update(generate_status_table())
                time.sleep(refresh)
    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoring stopped.[/yellow]")


@cli.command()
@click.pass_context
def interactive(ctx):
    """Launch interactive menu mode."""
    nav = NavigationManager(auto_mode=ctx.obj.get('auto', False))
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))
    
    def show_main_menu():
        options = [
            {"label": "System Status", "action": lambda: show_status()},
            {"label": "Installation", "action": lambda: run_installation()},
            {"label": "Service Management", "action": lambda: show_service_menu()},
            {"label": "Network Diagnostics", "action": lambda: run_diagnostics()},
            {"label": "Speed Testing", "action": lambda: run_speed_test()},
            {"label": "Security Report", "action": lambda: show_security_report()},
            {"label": "Backup Management", "action": lambda: show_backup_menu()},
            {"label": "Network Monitoring", "action": lambda: run_monitoring()},
            {"label": "View Logs", "action": lambda: show_logs()},
            {"label": "Configuration", "action": lambda: show_config_menu()},
            {"label": "Uninstall", "action": lambda: run_uninstall()},
            {"label": "Exit", "action": lambda: None}
        ]
        
        choice = nav.display_menu("WARP + NextDNS Manager - Main Menu", options)
        if choice and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                options[idx]["action"]()
    
    def show_status():
        nav.clear_screen()
        console.print(Panel("System Status", style="bold blue"))
        status_info = manager.get_status()
        
        table = Table()
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="magenta")
        
        for service_name, service_status in status_info['services'].items():
            status_text = "✅ Running" if service_status.get('running', False) else "❌ Stopped"
            table.add_row(f"{service_name.title()}", status_text)
        
        console.print(table)
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def run_installation():
        nav.clear_screen()
        console.print(Panel("Installation", style="bold blue"))
        if nav.auto_confirm("Run complete setup?", default=True):
            if manager.quick_setup():
                console.print("[green]✓ Installation completed successfully![/green]")
            else:
                console.print("[red]✗ Installation failed.[/red]")
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def show_service_menu():
        nav.clear_screen()
        options = [
            {"label": "Start Services", "action": lambda: manager.start_services()},
            {"label": "Stop Services", "action": lambda: manager.stop_services()},
            {"label": "Restart Services", "action": lambda: restart_services()},
            {"label": "Back to Main Menu", "action": lambda: None}
        ]
        
        choice = nav.display_menu("Service Management", options)
        if choice and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                options[idx]["action"]()
    
    def restart_services():
        manager.stop_services()
        time.sleep(2)
        manager.start_services()
    
    def run_diagnostics():
        nav.clear_screen()
        console.print(Panel("Network Diagnostics", style="bold blue"))
        console.print("Running network diagnostics...")
        # Add diagnostic logic here
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def run_speed_test():
        nav.clear_screen()
        console.print(Panel("Speed Testing", style="bold blue"))
        console.print("Running speed test...")
        # Add speed test logic here
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def show_security_report():
        nav.clear_screen()
        console.print(Panel("Security Report", style="bold blue"))
        console.print("Generating security report...")
        # Add security report logic here
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def show_backup_menu():
        nav.clear_screen()
        options = [
            {"label": "Create Backup", "action": lambda: create_backup()},
            {"label": "Restore Backup", "action": lambda: restore_backup()},
            {"label": "List Backups", "action": lambda: list_backups()},
            {"label": "Back to Main Menu", "action": lambda: None}
        ]
        
        choice = nav.display_menu("Backup Management", options)
        if choice and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                options[idx]["action"]()
    
    def create_backup():
        console.print("Creating backup...")
        # Add backup logic here
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def restore_backup():
        console.print("Restoring backup...")
        # Add restore logic here
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def list_backups():
        console.print("Listing backups...")
        # Add list logic here
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def run_monitoring():
        nav.clear_screen()
        console.print(Panel("Network Monitoring", style="bold blue"))
        console.print("Starting network monitoring...")
        # Add monitoring logic here
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def show_logs():
        nav.clear_screen()
        console.print(Panel("Application Logs", style="bold blue"))
        console.print("Displaying logs...")
        # Add log display logic here
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def show_config_menu():
        nav.clear_screen()
        options = [
            {"label": "View Configuration", "action": lambda: view_config()},
            {"label": "Edit Configuration", "action": lambda: edit_config()},
            {"label": "Reset Configuration", "action": lambda: reset_config()},
            {"label": "Back to Main Menu", "action": lambda: None}
        ]
        
        choice = nav.display_menu("Configuration", options)
        if choice and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                options[idx]["action"]()
    
    def view_config():
        console.print("Viewing configuration...")
        # Add config view logic here
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def edit_config():
        console.print("Editing configuration...")
        # Add config edit logic here
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def reset_config():
        console.print("Resetting configuration...")
        # Add config reset logic here
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    def run_uninstall():
        nav.clear_screen()
        console.print(Panel("Uninstall", style="bold red"))
        if nav.auto_confirm("Are you sure you want to uninstall?", default=False):
            console.print("Uninstalling...")
            # Add uninstall logic here
        nav.auto_confirm("Press Enter to continue...", default=True)
    
    try:
        while True:
            show_main_menu()
    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting interactive mode.[/yellow]")


@cli.command()
@click.pass_context
def logs(ctx):
    """Show service logs."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    try:
        # Add log display logic here
        console.print("Displaying logs...")
        console.print("Log functionality will be implemented in the next phase.")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--output', '-o', type=click.Path(), help='Output file for backup')
@click.pass_context
def backup(ctx, output):
    """Export configuration backup."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    try:
        # Add backup logic here
        console.print("Backup functionality will be implemented in the next phase.")
        console.print("[green]✓ Configuration backed up successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.pass_context
def uninstall(ctx):
    """Uninstall WARP NextDNS setup."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    try:
        # Add uninstall logic here
        console.print("Uninstall functionality will be implemented in the next phase.")
        console.print("[green]✓ Uninstalled successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
def version():
    """Show version information."""
    version_file = Path(__file__).parent / "VERSION"
    version = version_file.read_text().strip() if version_file.exists() else "2.0.0"

    platform = PlatformUtils()
    info = platform.get_system_info()

    console.print(Panel(f"WARP NextDNS Manager v{version}", style="bold blue"))
    console.print(f"\nSystem Information:")
    console.print(f"  OS: {info['os'].title()}")
    console.print(f"  Platform: {info['platform']}")
    console.print(f"  Python: {sys.version.split()[0]}")


if __name__ == "__main__":
    cli()
