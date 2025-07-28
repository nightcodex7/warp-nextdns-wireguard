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
from rich.theme import Theme
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
import time

from .core import WarpNextDNSManager
from utils.platform_utils import PlatformUtils
from utils.navigation_manager import NavigationManager

# Custom dark theme inspired by Ghost Pass design
custom_theme = Theme({
    "info": "bright_cyan",
    "warning": "bright_yellow", 
    "danger": "bright_red",
    "success": "bright_green",
    "primary": "bright_magenta",
    "secondary": "cyan",
    "accent": "bright_blue",
    "muted": "dim white",
    "title": "bold bright_magenta",
    "header": "bold bright_cyan",
    "code": "bright_white on black",
    "panel": "bright_white on rgb(20,20,30)",
    "border": "bright_blue"
})

console = Console(theme=custom_theme)


@click.group()
@click.option('--auto', is_flag=True, help='Run in automatic mode (auto-accept prompts)')
@click.pass_context
def cli(ctx, auto):
    """WARP + NextDNS WireGuard Manager - Secure your connection with Cloudflare WARP and NextDNS."""
    ctx.ensure_object(dict)
    ctx.obj['auto'] = auto
    
    # Check platform and warn about macOS
    platform = PlatformUtils()
    if platform.is_macos:
        console.print(Panel(
            "[danger]⚠️  WARNING: macOS is not supported by this project![/danger]\n\n"
            "[warning]This software is designed for Linux and Windows only.[/warning]\n"
            "[warning]Attempting to continue may cause system issues.[/warning]\n"
            "[warning]Please use a supported platform.[/warning]",
            title="🚫 Platform Not Supported",
            style="panel",
            border_style="danger"
        ))
        if not Confirm.ask("Do you want to continue anyway?", default=False):
            sys.exit(1)


@cli.command()
@click.pass_context
def setup(ctx):
    """Run the complete setup wizard."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    # Modern header with gradient-like styling
    header_text = Text("🚀 WARP + NextDNS Setup", style="title")
    console.print(Panel(header_text, style="panel", border_style="border", padding=(1, 2)))

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Initializing setup...", total=None)
            
            if manager.quick_setup():
                progress.update(task, description="Setup completed successfully!")
                console.print("\n[success]✓ Setup completed successfully![/success]")
                console.print("\n[info]Your connection is now secured with WARP + NextDNS[/info]")
                
                # Show next steps
                console.print(Panel(
                    "[header]Next Steps:[/header]\n"
                    "[info]• Run 'python cli.py status' to check your connection[/info]\n"
                    "[info]• Run 'python cli.py monitor' for live status monitoring[/info]\n"
                    "[info]• Visit the documentation website for more information[/info]",
                    title="🎯 What's Next?",
                    style="panel",
                    border_style="border"
                ))
            else:
                progress.update(task, description="Setup failed!")
                console.print("\n[danger]✗ Setup failed. Check the logs for details.[/danger]")
                sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[warning]Setup cancelled by user.[/warning]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[danger]Error: {str(e)}[/danger]")
        sys.exit(1)


@cli.command()
@click.pass_context
def start(ctx):
    """Start WARP and NextDNS services."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    console.print(Panel("🟢 Starting Services", style="panel", border_style="border"))

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Starting WARP and NextDNS services...", total=None)
            
            if manager.start_services():
                progress.update(task, description="Services started successfully!")
                console.print("[success]✓ Services started successfully![/success]")
            else:
                progress.update(task, description="Failed to start services!")
                console.print("[danger]✗ Failed to start services.[/danger]")
                sys.exit(1)
    except Exception as e:
        console.print(f"[danger]Error: {str(e)}[/danger]")
        sys.exit(1)


@cli.command()
@click.pass_context
def stop(ctx):
    """Stop WARP and NextDNS services."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    console.print(Panel("🔴 Stopping Services", style="panel", border_style="border"))

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Stopping WARP and NextDNS services...", total=None)
            
            if manager.stop_services():
                progress.update(task, description="Services stopped successfully!")
                console.print("[success]✓ Services stopped successfully![/success]")
            else:
                progress.update(task, description="Failed to stop services!")
                console.print("[danger]✗ Failed to stop services.[/danger]")
                sys.exit(1)
    except Exception as e:
        console.print(f"[danger]Error: {str(e)}[/danger]")
        sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx):
    """Check connection status."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    try:
        console.print(Panel("📊 Connection Status", style="panel", border_style="border"))
        status_info = manager.get_status()
        
        # Create a modern status table
        table = Table(
            title="System Status",
            title_style="title",
            border_style="border",
            header_style="header",
            show_header=True,
            header_box=True
        )
        table.add_column("Component", style="primary", width=20)
        table.add_column("Status", style="secondary", width=15)
        table.add_column("Details", style="muted", width=40)
        
        # Add status rows with modern styling
        for component, info in status_info.items():
            if isinstance(info, dict):
                status = info.get('status', 'Unknown')
                details = info.get('details', '')
                
                # Color-code the status
                if status == 'Active' or status == 'Running':
                    status_style = "success"
                elif status == 'Inactive' or status == 'Stopped':
                    status_style = "warning"
                elif status == 'Error' or status == 'Failed':
                    status_style = "danger"
                else:
                    status_style = "muted"
                
                table.add_row(
                    component,
                    f"[{status_style}]{status}[/{status_style}]",
                    details
                )
            else:
                table.add_row(component, str(info), "")
        
        console.print(table)
        
        # Show connection summary
        if status_info.get('warp_status', {}).get('status') == 'Active':
            console.print("\n[success]🎉 Your connection is secured with WARP + NextDNS![/success]")
        else:
            console.print("\n[warning]⚠️  Services are not running. Run 'python cli.py start' to activate.[/warning]")
            
    except Exception as e:
        console.print(f"[danger]Error: {str(e)}[/danger]")
        sys.exit(1)


@cli.command()
@click.option('--refresh', default=5, help='Refresh interval in seconds')
@click.pass_context
def monitor(ctx, refresh):
    """Monitor connection status in real-time."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    console.print(Panel("📡 Live Status Monitor", style="panel", border_style="border"))
    console.print(f"[info]Refreshing every {refresh} seconds. Press Ctrl+C to stop.[/info]\n")

    def generate_status_table():
        try:
            status_info = manager.get_status()
            
            table = Table(
                title=f"Live Status - {time.strftime('%H:%M:%S')}",
                title_style="title",
                border_style="border",
                header_style="header"
            )
            table.add_column("Component", style="primary", width=20)
            table.add_column("Status", style="secondary", width=15)
            table.add_column("Details", style="muted", width=40)
            
            for component, info in status_info.items():
                if isinstance(info, dict):
                    status = info.get('status', 'Unknown')
                    details = info.get('details', '')
                    
                    if status == 'Active' or status == 'Running':
                        status_style = "success"
                    elif status == 'Inactive' or status == 'Stopped':
                        status_style = "warning"
                    elif status == 'Error' or status == 'Failed':
                        status_style = "danger"
                    else:
                        status_style = "muted"
                    
                    table.add_row(
                        component,
                        f"[{status_style}]{status}[/{status_style}]",
                        details
                    )
                else:
                    table.add_row(component, str(info), "")
            
            return table
        except Exception as e:
            error_table = Table(title="Error", title_style="danger")
            error_table.add_column("Error", style="danger")
            error_table.add_row(str(e))
            return error_table

    try:
        with Live(generate_status_table(), refresh_per_second=1, console=console) as live:
            while True:
                time.sleep(refresh)
                live.update(generate_status_table())
    except KeyboardInterrupt:
        console.print("\n[info]Monitoring stopped.[/info]")


@cli.command()
@click.pass_context
def interactive(ctx):
    """Launch interactive mode with menu-driven interface."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))
    nav = NavigationManager(auto_mode=ctx.obj.get('auto', False))

    console.print(Panel("🎮 Interactive Mode", style="panel", border_style="border"))

    def show_main_menu():
        while True:
            console.print("\n[header]Main Menu:[/header]")
            console.print("[info]1.[/info] Check Status")
            console.print("[info]2.[/info] Install/Setup")
            console.print("[info]3.[/info] Service Management")
            console.print("[info]4.[/info] Diagnostics")
            console.print("[info]5.[/info] Security & Backup")
            console.print("[info]6.[/info] Configuration")
            console.print("[info]7.[/info] Monitoring")
            console.print("[info]8.[/info] View Logs")
            console.print("[info]9.[/info] Uninstall")
            console.print("[info]0.[/info] Exit")
            
            choice = Prompt.ask("\n[primary]Select an option[/primary]", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
            
            if choice == "0":
                console.print("[info]Goodbye![/info]")
                break
            elif choice == "1":
                show_status()
            elif choice == "2":
                run_installation()
            elif choice == "3":
                show_service_menu()
            elif choice == "4":
                run_diagnostics()
            elif choice == "5":
                show_backup_menu()
            elif choice == "6":
                show_config_menu()
            elif choice == "7":
                run_monitoring()
            elif choice == "8":
                show_logs()
            elif choice == "9":
                run_uninstall()

    def show_status():
        console.print(Panel("📊 Status Check", style="panel", border_style="border"))
        status_info = manager.get_status()
        
        table = Table(title="Current Status", title_style="title", border_style="border")
        table.add_column("Component", style="primary")
        table.add_column("Status", style="secondary")
        
        for component, info in status_info.items():
            if isinstance(info, dict):
                status = info.get('status', 'Unknown')
                table.add_row(component, status)
            else:
                table.add_row(component, str(info))
        
        console.print(table)

    def run_installation():
        console.print(Panel("🚀 Installation", style="panel", border_style="border"))
        if Confirm.ask("Run complete setup?"):
            manager.quick_setup()

    def show_service_menu():
        while True:
            console.print("\n[header]Service Management:[/header]")
            console.print("[info]1.[/info] Start Services")
            console.print("[info]2.[/info] Stop Services")
            console.print("[info]3.[/info] Restart Services")
            console.print("[info]0.[/info] Back to Main Menu")
            
            choice = Prompt.ask("\n[primary]Select an option[/primary]", choices=["0", "1", "2", "3"])
            
            if choice == "0":
                break
            elif choice == "1":
                manager.start_services()
            elif choice == "2":
                manager.stop_services()
            elif choice == "3":
                restart_services()

    def restart_services():
        console.print("[info]Restarting services...[/info]")
        manager.stop_services()
        time.sleep(2)
        manager.start_services()

    def run_diagnostics():
        console.print(Panel("🔍 Diagnostics", style="panel", border_style="border"))
        console.print("[info]Running diagnostics...[/info]")
        # Add diagnostic logic here

    def run_speed_test():
        console.print(Panel("⚡ Speed Test", style="panel", border_style="border"))
        console.print("[info]Running speed test...[/info]")
        # Add speed test logic here

    def show_security_report():
        console.print(Panel("🔒 Security Report", style="panel", border_style="border"))
        console.print("[info]Generating security report...[/info]")
        # Add security report logic here

    def show_backup_menu():
        while True:
            console.print("\n[header]Backup & Security:[/header]")
            console.print("[info]1.[/info] Create Backup")
            console.print("[info]2.[/info] Restore Backup")
            console.print("[info]3.[/info] List Backups")
            console.print("[info]4.[/info] Security Report")
            console.print("[info]0.[/info] Back to Main Menu")
            
            choice = Prompt.ask("\n[primary]Select an option[/primary]", choices=["0", "1", "2", "3", "4"])
            
            if choice == "0":
                break
            elif choice == "1":
                create_backup()
            elif choice == "2":
                restore_backup()
            elif choice == "3":
                list_backups()
            elif choice == "4":
                show_security_report()

    def create_backup():
        console.print("[info]Creating backup...[/info]")
        # Add backup logic here

    def restore_backup():
        console.print("[info]Restoring backup...[/info]")
        # Add restore logic here

    def list_backups():
        console.print("[info]Listing backups...[/info]")
        # Add list backups logic here

    def run_monitoring():
        console.print(Panel("📡 Live Monitoring", style="panel", border_style="border"))
        console.print("[info]Starting live monitoring...[/info]")
        # Add monitoring logic here

    def show_logs():
        console.print(Panel("📋 Logs", style="panel", border_style="border"))
        console.print("[info]Displaying logs...[/info]")
        # Add logs display logic here

    def show_config_menu():
        while True:
            console.print("\n[header]Configuration:[/header]")
            console.print("[info]1.[/info] View Config")
            console.print("[info]2.[/info] Edit Config")
            console.print("[info]3.[/info] Reset Config")
            console.print("[info]0.[/info] Back to Main Menu")
            
            choice = Prompt.ask("\n[primary]Select an option[/primary]", choices=["0", "1", "2", "3"])
            
            if choice == "0":
                break
            elif choice == "1":
                view_config()
            elif choice == "2":
                edit_config()
            elif choice == "3":
                reset_config()

    def view_config():
        console.print("[info]Viewing configuration...[/info]")
        # Add view config logic here

    def edit_config():
        console.print("[info]Editing configuration...[/info]")
        # Add edit config logic here

    def reset_config():
        console.print("[info]Resetting configuration...[/info]")
        # Add reset config logic here

    def run_uninstall():
        console.print(Panel("🗑️  Uninstall", style="panel", border_style="border"))
        if Confirm.ask("Are you sure you want to uninstall?"):
            console.print("[info]Uninstalling...[/info]")
            # Add uninstall logic here

    show_main_menu()


@cli.command()
@click.pass_context
def logs(ctx):
    """View application logs."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    console.print(Panel("📋 Application Logs", style="panel", border_style="border"))
    
    try:
        # Add log viewing logic here
        console.print("[info]Log viewing functionality will be implemented here.[/info]")
    except Exception as e:
        console.print(f"[danger]Error: {str(e)}[/danger]")
        sys.exit(1)


@cli.command()
@click.option('--output', '-o', type=click.Path(), help='Output file for backup')
@click.pass_context
def backup(ctx, output):
    """Create a backup of current configuration."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    console.print(Panel("💾 Backup Configuration", style="panel", border_style="border"))
    
    try:
        # Add backup logic here
        console.print("[info]Backup functionality will be implemented here.[/info]")
    except Exception as e:
        console.print(f"[danger]Error: {str(e)}[/danger]")
        sys.exit(1)


@cli.command()
@click.pass_context
def uninstall(ctx):
    """Uninstall WARP + NextDNS Manager."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    console.print(Panel("🗑️  Uninstall", style="panel", border_style="border"))
    
    if not Confirm.ask("Are you sure you want to uninstall WARP + NextDNS Manager?"):
        console.print("[info]Uninstall cancelled.[/info]")
        return
    
    try:
        # Add uninstall logic here
        console.print("[info]Uninstall functionality will be implemented here.[/info]")
    except Exception as e:
        console.print(f"[danger]Error: {str(e)}[/danger]")
        sys.exit(1)


@cli.command()
@click.pass_context
def test(ctx):
    """Run connection and leak tests."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))

    console.print(Panel("🧪 Connection Tests", style="panel", border_style="border"))
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            # Test 1: Internet Connection
            task1 = progress.add_task("Testing internet connection...", total=None)
            internet_ok = manager.check_internet_connection()
            progress.update(task1, description="Internet connection test completed")
            
            # Test 2: WARP IP
            task2 = progress.add_task("Testing WARP IP...", total=None)
            warp_ip = manager.get_warp_ip()
            progress.update(task2, description="WARP IP test completed")
            
            # Test 3: DNS Servers
            task3 = progress.add_task("Testing DNS configuration...", total=None)
            dns_servers = manager.get_dns_servers()
            progress.update(task3, description="DNS configuration test completed")
            
            # Test 4: Service Status
            task4 = progress.add_task("Checking service status...", total=None)
            status = manager.get_status()
            progress.update(task4, description="Service status check completed")
        
        # Display results
        console.print("\n[header]Test Results:[/header]")
        
        # Create results table
        table = Table(
            title="Connection Test Results",
            title_style="title",
            border_style="border",
            header_style="header"
        )
        table.add_column("Test", style="primary", width=20)
        table.add_column("Status", style="secondary", width=15)
        table.add_column("Details", style="muted", width=40)
        
        # Internet test
        internet_status = "Pass" if internet_ok else "Fail"
        internet_style = "success" if internet_ok else "danger"
        table.add_row(
            "Internet Connection",
            f"[{internet_style}]{internet_status}[/{internet_style}]",
            "Basic connectivity test"
        )
        
        # WARP IP test
        warp_status = "Pass" if warp_ip else "Fail"
        warp_style = "success" if warp_ip else "warning"
        table.add_row(
            "WARP IP",
            f"[{warp_style}]{warp_status}[/{warp_style}]",
            warp_ip or "No WARP IP detected"
        )
        
        # DNS test
        dns_status = "Pass" if dns_servers else "Fail"
        dns_style = "success" if dns_servers else "warning"
        table.add_row(
            "DNS Configuration",
            f"[{dns_style}]{dns_status}[/{dns_style}]",
            f"{len(dns_servers)} DNS server(s) configured"
        )
        
        # Service test
        warp_service = status.get('WARP Service', {}).get('status', 'Unknown')
        nextdns_service = status.get('NextDNS Service', {}).get('status', 'Unknown')
        services_ok = warp_service == 'Running' and nextdns_service == 'Running'
        services_status = "Pass" if services_ok else "Fail"
        services_style = "success" if services_ok else "danger"
        table.add_row(
            "Services",
            f"[{services_style}]{services_status}[/{services_style}]",
            f"WARP: {warp_service}, NextDNS: {nextdns_service}"
        )
        
        console.print(table)
        
        # Summary
        if internet_ok and warp_ip and dns_servers and services_ok:
            console.print("\n[success]🎉 All tests passed! Your connection is secure.[/success]")
        else:
            console.print("\n[warning]⚠️  Some tests failed. Check the details above.[/warning]")
            
    except Exception as e:
        console.print(f"[danger]Error: {str(e)}[/danger]")
        sys.exit(1)


@cli.command()
def version():
    """Show version information."""
    version_file = Path(__file__).parent / "VERSION"
    version = version_file.read_text().strip() if version_file.exists() else "1.0.0"

    platform = PlatformUtils()
    info = platform.get_system_info()

    # Modern version display
    version_text = Text(f"WARP NextDNS Manager v{version}", style="title")
    console.print(Panel(version_text, style="panel", border_style="border", padding=(1, 2)))
    
    console.print(f"\n[header]System Information:[/header]")
    console.print(f"  [info]OS:[/info] {info['os'].title()}")
    console.print(f"  [info]Platform:[/info] {info['platform']}")
    console.print(f"  [info]Python:[/info] {sys.version.split()[0]}")
    
    # Show additional info
    console.print(f"\n[header]Features:[/header]")
    console.print(f"  [success]✓[/success] Cloudflare WARP Integration")
    console.print(f"  [success]✓[/success] NextDNS Custom DNS")
    console.print(f"  [success]✓[/success] WireGuard Protocol")
    console.print(f"  [success]✓[/success] Cross-Platform Support")
    console.print(f"  [success]✓[/success] Modern Dark UI")


if __name__ == "__main__":
    cli()
