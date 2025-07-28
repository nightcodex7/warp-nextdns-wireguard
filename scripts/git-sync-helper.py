#!/usr/bin/env python3
"""
Git Sync Helper - Prevents and resolves divergent branch issues
"""

import subprocess
import sys
import os

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def run_command(cmd, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def print_status(message, status="info"):
    """Print colored status messages"""
    if status == "success":
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
    elif status == "error":
        print(f"{Colors.RED}❌ {message}{Colors.END}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
    else:
        print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def setup_git_config():
    """Configure Git to handle pulls properly"""
    configs = [
        ("pull.rebase", "false", "Use merge strategy for pulls"),
        ("pull.ff", "true", "Allow fast-forward when possible"),
        ("merge.conflictstyle", "diff3", "Better conflict markers"),
        ("core.autocrlf", "input", "Handle line endings properly"),
        ("push.default", "current", "Push current branch by default")
    ]
    
    print_status("Configuring Git settings...")
    for key, value, desc in configs:
        success, _, _ = run_command(f'git config {key} "{value}"')
        if success:
            print_status(f"{desc}: {key}={value}", "success")
        else:
            print_status(f"Failed to set {key}", "error")

def check_divergence():
    """Check if branches have diverged"""
    success, ahead, _ = run_command("git rev-list --count @{u}..HEAD", check=False)
    if not success:
        return False, 0, 0
    
    success, behind, _ = run_command("git rev-list --count HEAD..@{u}", check=False)
    if not success:
        return False, 0, 0
    
    return True, int(ahead) if ahead else 0, int(behind) if behind else 0

def safe_pull(branch=None):
    """Safely pull changes handling divergence"""
    current_branch = None
    if not branch:
        success, current_branch, _ = run_command("git branch --show-current")
        if not success:
            print_status("Failed to get current branch", "error")
            return False
        branch = current_branch
    
    print_status(f"Safely syncing {branch} branch...")
    
    # Fetch latest changes
    success, _, _ = run_command("git fetch origin")
    if not success:
        print_status("Failed to fetch from origin", "error")
        return False
    
    # Check for divergence
    has_info, ahead, behind = check_divergence()
    
    if has_info:
        if ahead > 0 and behind > 0:
            print_status(f"Branch has diverged: {ahead} ahead, {behind} behind", "warning")
            
            # Stash any uncommitted changes
            success, stash_output, _ = run_command("git stash")
            has_stash = "No local changes" not in stash_output
            
            # Try to pull with merge
            success, output, error = run_command(f"git pull origin {branch} --no-rebase", check=False)
            
            if not success and "CONFLICT" in error + output:
                print_status("Merge conflicts detected", "warning")
                print_status("Resolving by keeping remote version...")
                
                # Reset to remote state
                run_command(f"git reset --hard origin/{branch}")
                print_status("Reset to remote version", "success")
            
            # Restore stash if we had one
            if has_stash:
                run_command("git stash pop", check=False)
                
        elif behind > 0:
            print_status(f"Branch is {behind} commits behind", "info")
            run_command(f"git pull origin {branch}")
        elif ahead > 0:
            print_status(f"Branch is {ahead} commits ahead", "info")
        else:
            print_status("Branch is up to date", "success")
    else:
        # Just try to pull
        run_command(f"git pull origin {branch}")
    
    return True

def sync_all_branches():
    """Sync all three branches"""
    branches = ["main", "testing", "master"]
    
    # Save current branch
    success, current_branch, _ = run_command("git branch --show-current")
    
    for branch in branches:
        print(f"\n{Colors.BLUE}Syncing {branch} branch...{Colors.END}")
        
        # Check if branch exists locally
        success, _, _ = run_command(f"git show-ref --verify --quiet refs/heads/{branch}", check=False)
        
        if success:
            # Checkout and sync
            run_command(f"git checkout {branch}")
            safe_pull(branch)
        else:
            # Create branch from remote
            success, _, _ = run_command(f"git checkout -b {branch} origin/{branch}", check=False)
            if success:
                print_status(f"Created {branch} branch from remote", "success")
    
    # Return to original branch
    if current_branch:
        run_command(f"git checkout {current_branch}")

def main():
    """Main function"""
    print(f"{Colors.BLUE}🔧 Git Sync Helper{Colors.END}")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_git_config()
        print_status("Git configuration complete!", "success")
        return 0
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        sync_all_branches()
        return 0
    
    # Default: sync current branch
    if safe_pull():
        print_status("Sync completed successfully!", "success")
    else:
        print_status("Sync failed", "error")
        return 1
    
    print("\n" + "=" * 50)
    print("💡 Tips:")
    print("  --setup : Configure Git settings")
    print("  --all   : Sync all branches")
    print("  (none)  : Sync current branch")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())