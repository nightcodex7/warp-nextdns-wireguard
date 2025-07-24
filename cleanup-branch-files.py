#!/usr/bin/env python3
"""
Branch Cleanup Script
Ensures each branch only contains appropriate files
"""

import os
import subprocess
import sys

def run_git_command(cmd):
    """Run a git command."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def get_current_branch():
    """Get current branch name."""
    result = run_git_command("git branch --show-current")
    return result.stdout.strip()

def cleanup_main_branch():
    """Remove files that shouldn't be on main branch."""
    print("🧹 Cleaning up main branch...")
    
    files_to_remove = []
    
    # Check for docs directory
    if os.path.exists('docs'):
        files_to_remove.append('docs/')
    
    # Check for test directory (optional - uncomment if needed)
    # if os.path.exists('tests'):
    #     files_to_remove.append('tests/')
    
    # Check for GitHub workflow files (keep only essential ones)
    workflow_dir = '.github/workflows'
    if os.path.exists(workflow_dir):
        for file in os.listdir(workflow_dir):
            if file not in ['main-release.yml', 'promote-to-main.yml']:
                files_to_remove.append(f'{workflow_dir}/{file}')
    
    # Check for development config files
    dev_files = ['.github/pre-commit-config.yml', '.github/branch-protection.yml']
    for file in dev_files:
        if os.path.exists(file):
            files_to_remove.append(file)
    
    # Remove the files
    if files_to_remove:
        print(f"Found {len(files_to_remove)} files/directories to remove:")
        for file in files_to_remove:
            print(f"  - {file}")
            run_git_command(f'git rm -rf "{file}"')
        
        # Commit the changes
        run_git_command('git commit -m "cleanup: remove testing-only files from main branch"')
        print("✅ Cleanup complete! Files removed and committed.")
    else:
        print("✅ Main branch is already clean!")

def main():
    branch = get_current_branch()
    
    if branch == 'main':
        cleanup_main_branch()
    elif branch == 'testing':
        print("ℹ️  Testing branch can contain all files.")
    else:
        print(f"ℹ️  Current branch: {branch}")
        print("This script only cleans up the 'main' branch.")

if __name__ == "__main__":
    main()
