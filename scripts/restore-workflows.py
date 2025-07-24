#!/usr/bin/env python3
"""
Restore GitHub Actions Workflows
This script helps restore workflows after permission issues are resolved
"""

import os
import subprocess
import sys
from pathlib import Path

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

def check_workflow_files():
    """Check if workflow files exist locally"""
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        return False, []
    
    workflows = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    return len(workflows) > 0, workflows

def restore_workflows_from_backup():
    """Restore workflows from backup if they exist"""
    backup_dir = Path("/tmp/workflows-backup")
    if backup_dir.exists():
        print_status("Found workflow backup, restoring...")
        os.makedirs(".github/workflows", exist_ok=True)
        success, _, _ = run_command(f"cp -r {backup_dir}/* .github/workflows/")
        if success:
            print_status("Workflows restored from backup", "success")
            return True
    return False

def create_essential_workflows():
    """Create essential workflow files if they don't exist"""
    print_status("Creating essential workflows...")
    
    workflow_dir = Path(".github/workflows")
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    # Branch protection workflow
    branch_protection = workflow_dir / "branch-protection-check.yml"
    if not branch_protection.exists():
        with open(branch_protection, 'w') as f:
            f.write("""name: Branch Protection Check

on:
  pull_request:
    branches: [ main, testing, master ]
  push:
    branches: [ main, testing, master ]
  create:

jobs:
  check-files:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Check branch compliance
      run: |
        echo "Branch protection check would run here"
        # Actual checks implemented in the full version
""")
        print_status(f"Created {branch_protection.name}", "success")
    
    # Branch sync workflow
    branch_sync = workflow_dir / "branch-sync.yml"
    if not branch_sync.exists():
        with open(branch_sync, 'w') as f:
            f.write("""name: Branch Sync Workflow

permissions:
  contents: write
  pull-requests: write

on:
  push:
    branches: [ main, testing ]
  workflow_dispatch:

jobs:
  sync-master:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Sync to master
      run: |
        echo "Master sync would run here"
        # Actual sync implemented in the full version
""")
        print_status(f"Created {branch_sync.name}", "success")

def main():
    """Main function to restore workflows"""
    print(f"{Colors.BLUE}🔧 Workflow Restoration Tool{Colors.END}")
    print("=" * 50)
    
    # Check current branch
    current_branch = get_current_branch()
    if not current_branch:
        print_status("Failed to get current branch", "error")
        return 1
    
    print_status(f"Current branch: {current_branch}")
    
    # Check if workflows exist
    has_workflows, workflow_files = check_workflow_files()
    
    if has_workflows:
        print_status(f"Found {len(workflow_files)} workflow files")
        for wf in workflow_files:
            print(f"  - {wf.name}")
    else:
        print_status("No workflow files found", "warning")
        
        # Try to restore from backup
        if not restore_workflows_from_backup():
            # Create essential workflows
            create_essential_workflows()
    
    # Commit and push options
    print("\n" + "=" * 50)
    print("Options:")
    print("1. Commit and push workflows to current branch")
    print("2. Push to all branches (testing, master)")
    print("3. Just commit locally (no push)")
    print("4. Exit without changes")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        # Commit and push to current branch
        print_status(f"Committing and pushing to {current_branch}...")
        run_command("git add .github/workflows/")
        success, _, _ = run_command('git commit -m "restore: add GitHub Actions workflows"')
        if success:
            print_status("Committed successfully", "success")
            success, _, error = run_command(f"git push origin {current_branch}")
            if success:
                print_status(f"Pushed to {current_branch}", "success")
            else:
                print_status(f"Push failed: {error}", "error")
                print_status("This might be due to workflow permissions. Please check GitHub App settings.", "warning")
        else:
            print_status("No changes to commit", "warning")
    
    elif choice == "2":
        # Push to multiple branches
        for branch in ["testing", "master"]:
            print_status(f"\nProcessing {branch} branch...")
            success, _, _ = run_command(f"git checkout {branch}")
            if success:
                run_command("git add .github/workflows/")
                run_command('git commit -m "restore: add GitHub Actions workflows"')
                success, _, error = run_command(f"git push origin {branch}")
                if success:
                    print_status(f"Pushed to {branch}", "success")
                else:
                    print_status(f"Push to {branch} failed: {error}", "error")
        
        # Return to original branch
        run_command(f"git checkout {current_branch}")
    
    elif choice == "3":
        # Just commit locally
        run_command("git add .github/workflows/")
        success, _, _ = run_command('git commit -m "restore: add GitHub Actions workflows"')
        if success:
            print_status("Committed locally", "success")
        else:
            print_status("No changes to commit", "warning")
    
    print("\n" + "=" * 50)
    print_status("Workflow restoration complete!", "success")
    
    # Final recommendations
    print("\n📝 Recommendations:")
    print("1. If push failed, check GitHub App permissions")
    print("2. Grant 'workflows' permission in repository settings")
    print("3. Or use a Personal Access Token with workflow scope")
    print("4. Run 'git push origin <branch>' after fixing permissions")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())