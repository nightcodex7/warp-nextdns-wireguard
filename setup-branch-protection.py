#!/usr/bin/env python3
"""
Branch Protection Setup Script
This script sets up permanent rules to prevent docs/ from being pushed to main branch
and ensures branch-specific file management.
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def get_current_branch():
    """Get the current git branch name."""
    success, branch, _ = run_command("git branch --show-current")
    return branch if success else None

def create_branch_gitignore():
    """Create branch-specific .gitignore rules."""
    main_gitignore = """.gitignore.branch-main
# Main branch specific ignores
docs/
*.md
!README.md
!LICENSE
!CHANGELOG.md
!SECURITY.md
!CODE_OF_CONDUCT.md
!CONTRIBUTING.md
!BRANCHING_STRATEGY.md
!SETUP_SUMMARY.md
"""

    testing_gitignore = """.gitignore.branch-testing
# Testing branch specific ignores
# All files allowed on testing branch
"""

    # Write branch-specific gitignore files
    with open('.gitignore.branch-main', 'w') as f:
        f.write(main_gitignore)
    
    with open('.gitignore.branch-testing', 'w') as f:
        f.write(testing_gitignore)
    
    print("✅ Created branch-specific .gitignore files")

def create_pre_commit_hook():
    """Create a pre-commit hook to enforce branch-specific rules."""
    hook_content = '''#!/bin/bash
# Pre-commit hook to enforce branch-specific file rules

# Get current branch
BRANCH=$(git symbolic-ref --short HEAD)

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

echo -e "${GREEN}Running branch protection checks...${NC}"

# Function to check if file should be blocked
check_blocked_files() {
    local branch=$1
    local blocked_files=()
    
    if [ "$branch" = "main" ]; then
        # Check for docs folder
        if git diff --cached --name-only | grep -q "^docs/"; then
            blocked_files+=("docs/*")
        fi
        
        # Check for test files
        if git diff --cached --name-only | grep -q "^tests/"; then
            blocked_files+=("tests/*")
        fi
        
        # Check for GitHub workflows except essential ones
        if git diff --cached --name-only | grep -E "^.github/workflows/" | grep -vE "(main-release|promote-to-main).yml"; then
            blocked_files+=(".github/workflows/* (except main-release.yml and promote-to-main.yml)")
        fi
        
        # Check for development-only files
        if git diff --cached --name-only | grep -E "(pre-commit-config|branch-protection).yml"; then
            blocked_files+=("development configuration files")
        fi
    fi
    
    if [ ${#blocked_files[@]} -gt 0 ]; then
        echo -e "${RED}❌ ERROR: The following files/patterns are not allowed on branch '$branch':${NC}"
        for file in "${blocked_files[@]}"; do
            echo -e "${RED}   - $file${NC}"
        done
        echo -e "${YELLOW}These files should only exist on the 'testing' branch.${NC}"
        echo -e "${YELLOW}Please remove them from your commit or switch to the 'testing' branch.${NC}"
        return 1
    fi
    
    return 0
}

# Run the check
if ! check_blocked_files "$BRANCH"; then
    echo -e "${RED}Commit aborted due to branch protection rules.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All branch protection checks passed!${NC}"
exit 0
'''
    
    # Create .git/hooks directory if it doesn't exist
    hooks_dir = os.path.join('.git', 'hooks')
    os.makedirs(hooks_dir, exist_ok=True)
    
    # Write the pre-commit hook
    hook_path = os.path.join(hooks_dir, 'pre-commit')
    with open(hook_path, 'w') as f:
        f.write(hook_content)
    
    # Make the hook executable
    if platform.system() != 'Windows':
        os.chmod(hook_path, 0o755)
    
    print("✅ Created pre-commit hook for branch protection")

def create_branch_cleanup_script():
    """Create a script to clean up branch-specific files."""
    cleanup_script = '''#!/usr/bin/env python3
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
'''
    
    with open('cleanup-branch-files.py', 'w') as f:
        f.write(cleanup_script)
    
    if platform.system() != 'Windows':
        os.chmod('cleanup-branch-files.py', 0o755)
    
    print("✅ Created branch cleanup script")

def create_github_workflow():
    """Create a GitHub workflow to enforce branch protection."""
    workflow_content = '''name: Branch Protection Check

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  check-files:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Check for prohibited files on main branch
      run: |
        # Check if docs directory exists
        if [ -d "docs" ]; then
          echo "❌ ERROR: 'docs/' directory found on main branch!"
          echo "The docs/ directory should only exist on the testing branch."
          exit 1
        fi
        
        # Check for development-only workflow files
        PROHIBITED_WORKFLOWS=$(find .github/workflows -type f -name "*.yml" | grep -vE "(main-release|promote-to-main).yml" || true)
        if [ -n "$PROHIBITED_WORKFLOWS" ]; then
          echo "❌ ERROR: Development workflow files found on main branch:"
          echo "$PROHIBITED_WORKFLOWS"
          echo "Only main-release.yml and promote-to-main.yml are allowed on main."
          exit 1
        fi
        
        # Check for development config files
        if [ -f ".github/pre-commit-config.yml" ] || [ -f ".github/branch-protection.yml" ]; then
          echo "❌ ERROR: Development configuration files found on main branch!"
          exit 1
        fi
        
        echo "✅ Branch protection check passed!"
'''
    
    # Create workflow directory
    workflow_dir = os.path.join('.github', 'workflows')
    os.makedirs(workflow_dir, exist_ok=True)
    
    # Write the workflow file
    with open(os.path.join(workflow_dir, 'branch-protection-check.yml'), 'w') as f:
        f.write(workflow_content)
    
    print("✅ Created GitHub workflow for branch protection")

def main():
    print("🔧 Setting up branch protection rules...")
    
    current_branch = get_current_branch()
    print(f"Current branch: {current_branch}")
    
    # Create branch-specific gitignore files
    create_branch_gitignore()
    
    # Create pre-commit hook
    create_pre_commit_hook()
    
    # Create cleanup script
    create_branch_cleanup_script()
    
    # Create GitHub workflow (only on testing branch)
    if current_branch == 'testing':
        create_github_workflow()
    
    print("\n✅ Branch protection setup complete!")
    print("\n📋 Next steps:")
    print("1. Run 'python cleanup-branch-files.py' to clean up the current branch")
    print("2. The pre-commit hook will automatically prevent docs/ from being committed to main")
    print("3. Use the testing branch for all documentation and development work")
    print("\n💡 Tips:")
    print("- The pre-commit hook is now active and will block prohibited files")
    print("- To bypass the hook temporarily (not recommended): git commit --no-verify")
    print("- To disable the hook: rm .git/hooks/pre-commit")

if __name__ == "__main__":
    main()