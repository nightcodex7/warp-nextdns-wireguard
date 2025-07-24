#!/usr/bin/env python3
"""
Push changes to GitHub without workflow files
This script helps bypass the workflow permission issue by:
1. Temporarily stashing workflow files
2. Pushing other changes
3. Providing instructions for manual workflow addition
"""

import os
import subprocess
import sys
from pathlib import Path
import shutil

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

def get_current_branch():
    """Get the current Git branch"""
    success, branch, _ = run_command("git branch --show-current")
    return branch if success else None

def stash_workflow_files():
    """Temporarily move workflow files"""
    workflow_dir = Path(".github/workflows")
    backup_dir = Path("/tmp/github-workflows-backup")
    
    if not workflow_dir.exists():
        return False, []
    
    # Create backup directory
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all workflow files
    workflow_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
    if not workflow_files:
        return False, []
    
    # Move files to backup
    moved_files = []
    for wf in workflow_files:
        backup_path = backup_dir / wf.name
        shutil.copy2(wf, backup_path)
        moved_files.append((wf, backup_path))
        os.remove(wf)
    
    return True, moved_files

def restore_workflow_files(moved_files):
    """Restore workflow files from backup"""
    workflow_dir = Path(".github/workflows")
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    for original, backup in moved_files:
        shutil.copy2(backup, original)
        os.remove(backup)

def main():
    """Main function"""
    print(f"{Colors.BLUE}🚀 Push Without Workflows Tool{Colors.END}")
    print("=" * 50)
    
    # Check current branch
    current_branch = get_current_branch()
    if not current_branch:
        print_status("Failed to get current branch", "error")
        return 1
    
    print_status(f"Current branch: {current_branch}")
    
    # Check for uncommitted changes
    success, status, _ = run_command("git status --porcelain")
    if status:
        print_status("You have uncommitted changes. Please commit or stash them first.", "error")
        return 1
    
    # Check if we're ahead of remote
    success, ahead, _ = run_command(f"git rev-list --count origin/{current_branch}..HEAD", check=False)
    if not success or ahead == "0":
        print_status("No commits to push", "warning")
        return 0
    
    print_status(f"Found {ahead} commits to push")
    
    # Stash workflow files
    print_status("Temporarily removing workflow files...")
    has_workflows, moved_files = stash_workflow_files()
    
    if has_workflows:
        print_status(f"Moved {len(moved_files)} workflow files", "success")
        
        # Commit the removal
        run_command("git add -A")
        success, _, _ = run_command('git commit -m "temp: remove workflows for push"')
        
        if success:
            print_status("Created temporary commit", "success")
    
    # Push changes
    print_status(f"Pushing to origin/{current_branch}...")
    success, output, error = run_command(f"git push origin {current_branch}")
    
    if success:
        print_status("Push successful!", "success")
    else:
        print_status(f"Push failed: {error}", "error")
        
        # Restore workflows if push failed
        if has_workflows:
            print_status("Restoring workflow files...")
            run_command("git reset --hard HEAD~1")
            restore_workflow_files(moved_files)
        return 1
    
    # Restore workflows locally
    if has_workflows:
        print_status("Restoring workflow files locally...")
        restore_workflow_files(moved_files)
        run_command("git add .github/workflows/")
        run_command('git commit -m "restore: add back workflows"')
        print_status("Workflows restored locally", "success")
    
    # Print instructions
    print("\n" + "=" * 50)
    print_status("Next Steps:", "warning")
    print("\n📝 To add workflows to GitHub:")
    print("1. Go to https://github.com/nightcodex7/warp-nextdns-wireguard")
    print(f"2. Switch to the '{current_branch}' branch")
    print("3. Navigate to .github/workflows/")
    print("4. Click 'Create new file' or 'Upload files'")
    print("5. Add each workflow file manually")
    print("\nOr, if you have a Personal Access Token with workflow scope:")
    print(f"git push https://<PAT>@github.com/nightcodex7/warp-nextdns-wireguard.git {current_branch}")
    
    if has_workflows:
        print("\n📁 Workflow files to add:")
        for wf, _ in moved_files:
            print(f"  - {wf.name}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())