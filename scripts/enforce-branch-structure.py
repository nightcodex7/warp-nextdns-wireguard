#!/usr/bin/env python3
"""
Enforce Branch Structure Script
Ensures only main, testing, and master branches exist with proper file organization
"""

import subprocess
import os
import sys
from pathlib import Path

# Allowed branches
ALLOWED_BRANCHES = {'main', 'testing', 'master'}

# Branch-specific file rules
BRANCH_RULES = {
    'main': {
        'allowed_dirs': ['src', 'scripts', 'utils', 'tests', '.github'],
        'forbidden_dirs': ['docs'],
        'allowed_workflows': ['main-release.yml', 'promote-to-main.yml', 'branch-protection-check.yml', 'branch-sync.yml'],
        'forbidden_patterns': ['*_SUMMARY.md', '*_summary.md', '*.tmp', '*.temp', 'implement_*.py', 'create_*.py', 'test-*.html']
    },
    'testing': {
        'allowed_dirs': ['src', 'scripts', 'utils', 'tests', '.github', 'docs'],
        'forbidden_dirs': [],
        'allowed_workflows': None,  # All workflows allowed
        'forbidden_patterns': ['*_SUMMARY.md', '*_summary.md', '*.tmp', '*.temp']
    },
    'master': {
        'allowed_dirs': ['src', 'scripts', 'utils', 'tests', '.github', 'docs'],
        'forbidden_dirs': [],
        'allowed_workflows': None,  # All workflows allowed
        'forbidden_patterns': ['*_SUMMARY.md', '*_summary.md', '*.tmp', '*.temp']
    }
}

def run_command(cmd, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stdout if hasattr(e, 'stdout') else "", e.stderr if hasattr(e, 'stderr') else str(e)

def get_all_branches():
    """Get all local and remote branches"""
    success, output, _ = run_command("git branch -a")
    if not success:
        return []
    
    branches = []
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('*'):
            line = line[2:]
        if 'remotes/origin/' in line:
            line = line.replace('remotes/origin/', '')
        if '->' not in line and line and line != 'HEAD':
            branches.append(line)
    
    return list(set(branches))

def delete_unauthorized_branches():
    """Delete any branches not in the allowed list"""
    all_branches = get_all_branches()
    unauthorized = [b for b in all_branches if b not in ALLOWED_BRANCHES]
    
    if not unauthorized:
        print("✅ No unauthorized branches found")
        return
    
    print(f"🗑️  Found {len(unauthorized)} unauthorized branches:")
    for branch in unauthorized:
        print(f"  - {branch}")
    
    # Delete local branches
    for branch in unauthorized:
        success, _, _ = run_command(f"git show-ref --verify --quiet refs/heads/{branch}")
        if success:
            print(f"  Deleting local branch: {branch}")
            run_command(f"git branch -D {branch}")
    
    # Delete remote branches
    for branch in unauthorized:
        success, _, _ = run_command(f"git ls-remote --heads origin {branch}")
        if success:
            print(f"  Deleting remote branch: {branch}")
            run_command(f"git push origin --delete {branch}")

def check_branch_files(branch):
    """Check if files on a branch comply with rules"""
    print(f"\n🔍 Checking {branch} branch...")
    
    # Stash current changes
    run_command("git stash push -m 'temp stash for branch check'", check=False)
    
    # Checkout branch
    success, _, error = run_command(f"git checkout {branch}")
    if not success:
        print(f"❌ Failed to checkout {branch}: {error}")
        return False
    
    rules = BRANCH_RULES.get(branch, {})
    violations = []
    
    # Check forbidden directories
    for forbidden_dir in rules.get('forbidden_dirs', []):
        if os.path.exists(forbidden_dir):
            violations.append(f"Forbidden directory exists: {forbidden_dir}/")
    
    # Check workflows if branch is main
    if branch == 'main' and rules.get('allowed_workflows'):
        workflow_dir = '.github/workflows'
        if os.path.exists(workflow_dir):
            workflows = os.listdir(workflow_dir)
            for workflow in workflows:
                if workflow not in rules['allowed_workflows']:
                    violations.append(f"Unauthorized workflow: {workflow}")
    
    # Check forbidden patterns
    for pattern in rules.get('forbidden_patterns', []):
        cmd = f'find . -name "{pattern}" -type f | grep -v ".git"'
        success, output, _ = run_command(cmd, check=False)
        if output:
            for file in output.split('\n'):
                if file:
                    violations.append(f"Forbidden file: {file}")
    
    # Report violations
    if violations:
        print(f"❌ Found {len(violations)} violations on {branch}:")
        for v in violations:
            print(f"   - {v}")
        return False
    else:
        print(f"✅ {branch} branch is compliant")
        return True

def fix_branch_violations(branch):
    """Fix violations on a branch"""
    print(f"\n🔧 Fixing violations on {branch}...")
    
    rules = BRANCH_RULES.get(branch, {})
    
    # Remove forbidden directories
    for forbidden_dir in rules.get('forbidden_dirs', []):
        if os.path.exists(forbidden_dir):
            print(f"  Removing {forbidden_dir}/")
            run_command(f"git rm -rf {forbidden_dir}")
    
    # Remove unauthorized workflows
    if branch == 'main' and rules.get('allowed_workflows'):
        workflow_dir = '.github/workflows'
        if os.path.exists(workflow_dir):
            workflows = os.listdir(workflow_dir)
            for workflow in workflows:
                if workflow not in rules['allowed_workflows']:
                    print(f"  Removing workflow: {workflow}")
                    run_command(f"git rm {workflow_dir}/{workflow}")
    
    # Remove forbidden files
    for pattern in rules.get('forbidden_patterns', []):
        cmd = f'find . -name "{pattern}" -type f | grep -v ".git"'
        success, output, _ = run_command(cmd, check=False)
        if output:
            for file in output.split('\n'):
                if file:
                    print(f"  Removing: {file}")
                    run_command(f'git rm -f "{file}"', check=False)
                    run_command(f'rm -f "{file}"', check=False)
    
    # Commit changes if any
    success, output, _ = run_command("git status --porcelain")
    if output:
        run_command('git commit -m "chore: enforce branch file structure rules"')
        print("✅ Fixed violations and committed changes")

def create_git_config():
    """Create git config to prevent branch creation"""
    config_content = """# Git hooks configuration
[branch]
    # Prevent creation of new branches
    autosetupmerge = false
    autosetuprebase = never

[advice]
    # Show warnings about branch creation
    detachedHead = true
"""
    
    with open('.git/config.local', 'w') as f:
        f.write(config_content)
    
    # Include local config
    run_command('git config --local include.path config.local')
    print("✅ Created git config to discourage branch creation")

def main():
    """Main enforcement function"""
    print("🛡️  Branch Structure Enforcement Tool")
    print("=" * 50)
    
    # Get current branch
    success, current_branch, _ = run_command("git branch --show-current")
    if not success:
        print("❌ Failed to get current branch")
        return 1
    
    print(f"Current branch: {current_branch}")
    
    # Step 1: Delete unauthorized branches
    print("\n📋 Step 1: Checking for unauthorized branches...")
    delete_unauthorized_branches()
    
    # Step 2: Check each allowed branch
    print("\n📋 Step 2: Checking branch compliance...")
    all_compliant = True
    for branch in ALLOWED_BRANCHES:
        # Skip if branch doesn't exist
        success, _, _ = run_command(f"git show-ref --verify --quiet refs/heads/{branch}")
        if not success:
            continue
        
        if not check_branch_files(branch):
            all_compliant = False
            if '--fix' in sys.argv:
                fix_branch_violations(branch)
    
    # Step 3: Create git config
    print("\n📋 Step 3: Setting up git configuration...")
    create_git_config()
    
    # Return to original branch
    run_command(f"git checkout {current_branch}")
    run_command("git stash pop", check=False)
    
    print("\n" + "=" * 50)
    if all_compliant:
        print("✅ All branches are compliant!")
    else:
        print("⚠️  Some branches have violations")
        print("Run with --fix flag to automatically fix violations:")
        print(f"  python {sys.argv[0]} --fix")
    
    print("\n📌 Remember:")
    print("- Only use main, testing, and master branches")
    print("- main: production code only (no docs/)")
    print("- testing: development + documentation")
    print("- master: complete mirror (auto-synced)")

if __name__ == "__main__":
    main()