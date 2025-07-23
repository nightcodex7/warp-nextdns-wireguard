<<<<<<< HEAD
#!/usr/bin/env python3
"""
CLI interface for WARP + NextDNS Manager
"""

import click
import json
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax

from core import EnhancedWARPManager

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """WARP + NextDNS Manager - Secure internet with Cloudflare WARP and NextDNS"""
    pass

@cli.command()
@click.option('--profile-id', '-p', help='NextDNS profile ID')
@click.option('--non-interactive', '-n', is_flag=True, help='Non-interactive mode')
@click.option('--auto-elevate', '-e', is_flag=True, help='Automatically elevate privileges')
def setup(profile_id, non_interactive, auto_elevate):
    """Setup WARP + NextDNS configuration"""
    manager = EnhancedWARPManager()
    
    with console.status("[bold green]Initializing setup..."):
        # Check elevation
        if not manager.ensure_elevation():
            console.print("[red]❌ Elevated privileges required[/red]")
            if auto_elevate:
                console.print("[yellow]Attempting auto-elevation...[/yellow]")
                if not manager.auto_elevate_if_needed():
                    console.print("[red]Auto-elevation failed. Please run with sudo/admin rights.[/red]")
                    sys.exit(1)
            else:
                console.print("[yellow]Please run with sudo/admin rights or use --auto-elevate[/yellow]")
                sys.exit(1)
    
    console.print("[green]✅ Elevated privileges confirmed[/green]")
    
    # Install dependencies
    with console.status("[bold blue]Installing dependencies..."):
        deps = manager.install_dependencies()
        
        if not all(deps.values()):
            console.print("[red]❌ Some dependencies failed to install:[/red]")
            for dep, success in deps.items():
                status = "✅" if success else "❌"
                console.print(f"   {dep}: {status}")
            sys.exit(1)
    
    console.print("[green]✅ All dependencies installed[/green]")
    
    # Setup WGCF
    with console.status("[bold blue]Setting up WGCF..."):
        wgcf_result = manager.setup_wgcf()
        
        if not wgcf_result['success']:
            console.print(f"[red]❌ WGCF setup failed: {wgcf_result['error']}[/red]")
            sys.exit(1)
    
    console.print("[green]✅ WGCF setup completed[/green]")
    
    # Setup NextDNS
    if not profile_id and not non_interactive:
        profile_id = Prompt.ask("Enter your NextDNS profile ID")
    
    if not profile_id:
        console.print("[red]❌ NextDNS profile ID is required[/red]")
        sys.exit(1)
    
    with console.status("[bold blue]Setting up NextDNS..."):
        nextdns_result = manager.setup_nextdns_config(profile_id)
        
        if not nextdns_result['success']:
            console.print(f"[red]❌ NextDNS setup failed: {nextdns_result['error']}[/red]")
            sys.exit(1)
    
    console.print("[green]✅ NextDNS setup completed[/green]")
    
    # Create system services
    if manager.platform.is_linux:
        with console.status("[bold blue]Creating system services..."):
            if manager.create_systemd_services():
                console.print("[green]✅ System services created[/green]")
            else:
                console.print("[yellow]⚠️  Failed to create system services[/yellow]")
    
    # Start services
    with console.status("[bold blue]Starting services..."):
        start_results = manager.start_services()
        
        if all(start_results.values()):
            console.print("[green]✅ All services started[/green]")
        else:
            console.print("[yellow]⚠️  Some services failed to start[/yellow]")
    
    # Test connection
    with console.status("[bold blue]Testing connectivity..."):
        test_results = manager.test_connection()
    
    # Display results
    table = Table(title="Connection Test Results")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="green")
    
    table.add_row("Internet", "✅" if test_results['internet'] else "❌")
    table.add_row("WARP", "✅" if test_results['warp'] else "❌")
    table.add_row("NextDNS", "✅" if test_results['nextdns'] else "❌")
    
    console.print(table)
    
    # Setup auto-start
    if not non_interactive or Confirm.ask("Setup auto-start?"):
        with console.status("[bold blue]Setting up auto-start..."):
            if manager.setup_auto_start():
                console.print("[green]✅ Auto-start configured[/green]")
            else:
                console.print("[yellow]⚠️  Auto-start configuration failed[/yellow]")
    
    console.print(Panel.fit(
        "[bold green]🎉 Setup completed successfully![/bold green]\n"
        "Your WARP + NextDNS configuration is now active.",
        title="Setup Complete"
    ))

@cli.command()
def start():
    """Start WARP + NextDNS services"""
    manager = EnhancedWARPManager()
    
    if not manager.ensure_elevation():
        console.print("[red]❌ Elevated privileges required[/red]")
        sys.exit(1)
    
    with console.status("[bold blue]Starting services..."):
        results = manager.start_services()
    
    table = Table(title="Service Start Results")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="green")
    
    for service, success in results.items():
        status = "✅ Started" if success else "❌ Failed"
        table.add_row(service, status)
    
    console.print(table)

@cli.command()
def stop():
    """Stop WARP + NextDNS services"""
    manager = EnhancedWARPManager()
    
    if not manager.ensure_elevation():
        console.print("[red]❌ Elevated privileges required[/red]")
        sys.exit(1)
    
    with console.status("[bold blue]Stopping services..."):
        results = manager.stop_services()
    
    table = Table(title="Service Stop Results")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="green")
    
    for service, success in results.items():
        status = "✅ Stopped" if success else "❌ Failed"
        table.add_row(service, status)
    
    console.print(table)

@cli.command()
def status():
    """Show status of WARP + NextDNS services"""
    manager = EnhancedWARPManager()
    
    with console.status("[bold blue]Checking status..."):
        status_data = manager.get_status()
    
    # Platform info
    platform_table = Table(title="Platform Information")
    platform_table.add_column("Property", style="cyan")
    platform_table.add_column("Value", style="green")
    
    for key, value in status_data['platform'].items():
        platform_table.add_row(key, str(value))
    
    console.print(platform_table)
    console.print()
    
    # Service status
    service_table = Table(title="Service Status")
    service_table.add_column("Service", style="cyan")
    service_table.add_column("Installed", style="green")
    service_table.add_column("Running", style="green")
    service_table.add_column("Configured", style="green")
    
    # WGCF status
    wgcf_status = status_data['wgcf']
    service_table.add_row(
        "WGCF",
        "✅" if wgcf_status.get('wgcf_binary') else "❌",
        "✅" if wgcf_status.get('running') else "❌",
        "✅" if wgcf_status.get('profile_installed') else "❌"
    )
    
    # NextDNS status
    nextdns_status = status_data['nextdns']
    service_table.add_row(
        "NextDNS",
        "✅" if nextdns_status.get('installed') else "❌",
        "✅" if nextdns_status.get('running') else "❌",
        "✅" if nextdns_status.get('configured') else "❌"
    )
    
    console.print(service_table)

@cli.command()
def test():
    """Test WARP + NextDNS connectivity"""
    manager = EnhancedWARPManager()
    
    with console.status("[bold blue]Testing connectivity..."):
        results = manager.test_connection()
    
    table = Table(title="Connectivity Test Results")
    table.add_column("Test", style="cyan")
    table.add_column("Result", style="green")
    table.add_column("Details", style="yellow")
    
    table.add_row(
        "Internet",
        "✅ Connected" if results['internet'] else "❌ Disconnected",
        "Basic internet connectivity"
    )
    
    table.add_row(
        "WARP",
        "✅ Active" if results['warp'] else "❌ Inactive",
        "Cloudflare WARP tunnel"
    )
    
    table.add_row(
        "NextDNS",
        "✅ Working" if results['nextdns'] else "❌ Failed",
        "DNS resolution through NextDNS"
    )
    
    console.print(table)

@cli.command()
def logs():
    """Show service logs"""
    manager = EnhancedWARPManager()
    
    console.print("[bold blue]NextDNS Logs:[/bold blue]")
    try:
        logs = manager.nextdns_manager.get_logs(50)
        syntax = Syntax(logs, "bash", theme="monokai")
        console.print(syntax)
    except Exception as e:
        console.print(f"[red]Failed to get NextDNS logs: {e}[/red]")

@cli.command()
def uninstall():
    """Uninstall WARP + NextDNS configuration"""
    if not Confirm.ask("Are you sure you want to uninstall?"):
        console.print("[yellow]Uninstall cancelled[/yellow]")
        return
    
    manager = EnhancedWARPManager()
    
    if not manager.ensure_elevation():
        console.print("[red]❌ Elevated privileges required[/red]")
        sys.exit(1)
    
    with console.status("[bold red]Uninstalling..."):
        # Stop services
        manager.stop_services()
        
        # Remove systemd services
        if manager.platform.is_linux:
            try:
                manager.platform.run_command(["systemctl", "disable", "wgcf"])
                manager.platform.run_command(["systemctl", "disable", "nextdns"])
                manager.platform.run_command(["systemctl", "daemon-reload"])
            except:
                pass
        
        # Remove configuration files
        try:
            import shutil
            if manager.config_dir.exists():
                shutil.rmtree(manager.config_dir)
        except:
            pass
    
    console.print("[green]✅ Uninstall completed[/green]")

if __name__ == "__main__":
    cli() 
=======
"""Command-line interface for WARP NextDNS WireGuard Manager."""
import click
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from core import WarpNextDNSManager
from utils.platform_utils import PlatformUtils


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
        if manager.verify_connection():
            console.print("\n[green]✓ All systems operational![/green]")
        else:
            console.print("\n[yellow]⚠ Some services are not working properly.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.pass_context
def logs(ctx):
    """Show service logs."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))
    
    try:
        manager.show_logs()
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
        output_path = Path(output) if output else None
        if manager.export_config(output_path):
            console.print("[green]✓ Configuration backed up successfully![/green]")
        else:
            console.print("[red]✗ Failed to backup configuration.[/red]")
            sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.pass_context
def uninstall(ctx):
    """Uninstall WARP NextDNS setup."""
    manager = WarpNextDNSManager(auto_mode=ctx.obj.get('auto', False))
    
    try:
        if manager.uninstall():
            console.print("[green]✓ Uninstalled successfully![/green]")
        else:
            console.print("[yellow]Uninstall cancelled.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
def version():
    """Show version information."""
    with open("VERSION", "r") as f:
        version = f.read().strip()
    
    platform = PlatformUtils()
    info = platform.get_system_info()
    
    console.print(Panel(f"WARP NextDNS Manager v{version}", style="bold blue"))
    console.print(f"\nSystem Information:")
    console.print(f"  OS: {info['os'].title()}")
    console.print(f"  Platform: {info['platform']}")
    console.print(f"  Python: {sys.version.split()[0]}")


if __name__ == "__main__":
    cli()
>>>>>>> 6f8763ed9c292fb062677073732ac3e864bb795d
