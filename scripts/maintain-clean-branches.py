#!/usr/bin/env python3
"""
Maintain Clean Branches - Ensures each branch only has appropriate files
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

def clean_common_unwanted_files():
    """Remove common unwanted files from any branch"""
    unwanted_patterns = [
        "*_SUMMARY.md",
        "*_summary.md",
        "*.tmp",
        "*.temp",
        "*.bak",
        "*~",
        ".DS_Store",
        "Thumbs.db",
        "desktop.ini",
        "*.swp",
        "*.swo",
        "*.log",
        "test-minimal.yml",
        "simple-test.yml",
        "ci-simple.yml"
    ]
    
    removed_count = 0
    for pattern in unwanted_patterns:
        success, files, _ = run_command(f'find . -name "{pattern}" -type f | grep -v ".git"', check=False)
        if success and files:
            for file in files.split('\n'):
                if file.strip():
                    os.remove(file.strip())
                    print_status(f"Removed: {file.strip()}", "warning")
                    removed_count += 1
    
    return removed_count

def clean_main_branch():
    """Clean main branch - remove development files"""
    print_status("Cleaning main branch...")
    
    # Files/directories that should NOT be on main
    remove_items = [
        "docs/",  # Documentation website
        ".github/workflows/ci.yml",
        ".github/workflows/ci-simple.yml",
        ".github/workflows/simple-test.yml",
        ".github/workflows/test-simple.yml",
        ".github/workflows/docs-deploy.yml",
        ".github/workflows/pages.yml",
        ".github/workflows/release.yml",
        ".github/pre-commit-config.yml",
        ".github/branch-protection.yml",
        "setup-branch-protection.py",
        "cleanup-branch-files.py",
        "cleanup-branches.sh",
        "remove-unwanted-branches.sh",
        "remove-unwanted-branches.ps1"
    ]
    
    removed_count = 0
    for item in remove_items:
        if os.path.exists(item):
            if os.path.isdir(item):
                run_command(f"rm -rf {item}")
                print_status(f"Removed directory: {item}", "warning")
            else:
                os.remove(item)
                print_status(f"Removed file: {item}", "warning")
            removed_count += 1
    
    # Ensure only allowed workflows exist
    allowed_workflows = [
        "main-release.yml",
        "promote-to-main.yml",
        "branch-protection-check.yml",
        "branch-sync.yml"
    ]
    
    workflow_dir = Path(".github/workflows")
    if workflow_dir.exists():
        for workflow in workflow_dir.glob("*.yml"):
            if workflow.name not in allowed_workflows:
                workflow.unlink()
                print_status(f"Removed workflow: {workflow.name}", "warning")
                removed_count += 1
    
    return removed_count

def clean_testing_branch():
    """Clean testing branch - it can have most files but not temporary ones"""
    print_status("Cleaning testing branch...")
    
    # Testing branch should NOT have
    remove_items = [
        "setup-branch-protection.py",
        "cleanup-branch-files.py",
        "cleanup-branches.sh",
        "remove-unwanted-branches.sh",
        "remove-unwanted-branches.ps1"
    ]
    
    removed_count = 0
    for item in remove_items:
        if os.path.exists(item):
            os.remove(item)
            print_status(f"Removed: {item}", "warning")
            removed_count += 1
    
    return removed_count

def verify_branch_structure():
    """Verify proper directory structure exists"""
    required_dirs = ["src", "scripts", "utils", "tests"]
    missing_dirs = []
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print_status(f"Missing required directories: {', '.join(missing_dirs)}", "error")
        return False
    
    # Check core files in src/
    core_files = ["src/main.py", "src/cli.py", "src/core.py"]
    missing_files = []
    
    for file_path in core_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print_status(f"Missing core files: {', '.join(missing_files)}", "error")
        return False
    
    return True

def commit_changes(message):
    """Commit changes if any"""
    success, status, _ = run_command("git status --porcelain")
    if success and status:
        run_command("git add -A")
        run_command(f'git commit -m "{message}"')
        return True
    return False

def main():
    """Main function"""
    print(f"{Colors.BLUE}🧹 Branch Cleanup Tool{Colors.END}")
    print("=" * 50)
    
    current_branch = get_current_branch()
    if not current_branch:
        print_status("Failed to get current branch", "error")
        return 1
    
    print_status(f"Current branch: {current_branch}")
    
    # Clean common unwanted files
    print_status("Removing common unwanted files...")
    removed = clean_common_unwanted_files()
    
    # Branch-specific cleanup
    if current_branch == "main":
        removed += clean_main_branch()
    elif current_branch == "testing":
        removed += clean_testing_branch()
    elif current_branch == "master":
        # Master can have everything, just clean common unwanted
        print_status("Master branch - keeping all files from both branches")
    
    # Verify structure
    if not verify_branch_structure():
        print_status("Branch structure verification failed", "error")
    else:
        print_status("Branch structure verified", "success")
    
    # Commit if changes were made
    if removed > 0:
        print_status(f"Removed {removed} unwanted files/directories", "success")
        if commit_changes(f"cleanup: remove unwanted files from {current_branch} branch"):
            print_status("Changes committed", "success")
            print_status("Run 'git push' to push changes", "info")
    else:
        print_status("No unwanted files found - branch is clean!", "success")
    
    # Show summary
    print("\n" + "=" * 50)
    print("📋 Branch Rules Summary:")
    print("  main: Production only (no docs/, minimal workflows)")
    print("  testing: Development (all files except temp/setup)")
    print("  master: Complete mirror (everything)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())