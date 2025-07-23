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