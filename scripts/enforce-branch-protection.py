#!/usr/bin/env python3
"""
Branch Protection Rules Enforcement Script
Enforces strict branch protection rules before commits
"""

import os
import sys
import subprocess
from pathlib import Path

# Branch-specific rules
BRANCH_RULES = {
    'main': {
        'allowed_folders': ['src', 'utils', 'tests', '.cursor'],
        'required_files': ['README.md', 'CHANGELOG.md', 'LICENSE', 'setup.py', 'pyproject.toml', 'requirements.txt', 'VERSION'],
        'forbidden_folders': ['docs', 'scripts'],
        'forbidden_patterns': ['*_guide.md', '*_summary.md', '*_rules.md', 'BRANCH_*.md', 'WORKFLOW_*.md', 'SETUP_*.md']
    },
    'testing': {
        'allowed_folders': ['src', 'utils', 'tests', '.cursor', 'docs', 'scripts'],
        'required_files': ['README.md', 'CHANGELOG.md', 'LICENSE', 'setup.py', 'pyproject.toml', 'requirements.txt', 'VERSION'],
        'forbidden_folders': [],
        'forbidden_patterns': ['*_guide.md', '*_summary.md', '*_rules.md', 'BRANCH_*.md', 'WORKFLOW_*.md', 'SETUP_*.md']
    },
    'master': {
        'allowed_folders': ['src', 'utils', 'tests', '.cursor', 'docs', 'scripts'],
        'required_files': ['README.md', 'CHANGELOG.md', 'LICENSE', 'setup.py', 'pyproject.toml', 'requirements.txt', 'VERSION'],
        'forbidden_folders': [],
        'forbidden_patterns': ['*_guide.md', '*_summary.md', '*_rules.md', 'BRANCH_*.md', 'WORKFLOW_*.md', 'SETUP_*.md']
    }
}

def get_current_branch():
    """Get the current git branch"""
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def check_forbidden_folders(branch_rules):
    """Check for forbidden folders"""
    violations = []
    for folder in branch_rules['forbidden_folders']:
        if Path(folder).exists():
            violations.append(f"❌ Forbidden folder found: {folder}")
    return violations

def check_forbidden_patterns(branch_rules):
    """Check for forbidden file patterns"""
    violations = []
    for pattern in branch_rules['forbidden_patterns']:
        for file_path in Path('.').glob(pattern):
            if file_path.is_file():
                violations.append(f"❌ Forbidden file pattern found: {file_path}")
    return violations

def check_required_files(branch_rules):
    """Check for required files"""
    missing = []
    for file in branch_rules['required_files']:
        if not Path(file).exists():
            missing.append(f"❌ Required file missing: {file}")
    return missing

def validate_branch_structure():
    """Validate the current branch structure"""
    current_branch = get_current_branch()
    if not current_branch:
        print("❌ Error: Could not determine current branch")
        return False
    
    if current_branch not in BRANCH_RULES:
        print(f"❌ Error: No rules defined for branch '{current_branch}'")
        return False
    
    print(f"🔍 Validating branch: {current_branch}")
    print("=" * 50)
    
    branch_rules = BRANCH_RULES[current_branch]
    violations = []
    
    # Check forbidden folders
    folder_violations = check_forbidden_folders(branch_rules)
    violations.extend(folder_violations)
    
    # Check forbidden patterns
    pattern_violations = check_forbidden_patterns(branch_rules)
    violations.extend(pattern_violations)
    
    # Check required files
    missing_files = check_required_files(branch_rules)
    violations.extend(missing_files)
    
    if violations:
        print("❌ Branch protection violations found:")
        for violation in violations:
            print(f"   {violation}")
        print("\n🚫 Commit blocked due to branch protection violations")
        return False
    else:
        print("✅ Branch structure validation passed")
        return True

def main():
    """Main function"""
    print("🔒 Branch Protection Rules Enforcement")
    print("=" * 50)
    
    if not validate_branch_structure():
        sys.exit(1)
    
    print("\n✅ All branch protection rules satisfied")
    print("✅ Proceeding with commit...")

if __name__ == "__main__":
    main() 