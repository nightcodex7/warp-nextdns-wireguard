#!/usr/bin/env python3
"""
Branch Protection Rules Enforcement Script (Final, Strict Version)
Enforces strict branch protection rules before commits
"""

import os
import sys
import subprocess
from pathlib import Path

# Branch-specific rules (Final, Strict Version)
BRANCH_RULES = {
    'main': {
        'allowed_folders': ['src', 'utils', 'tests', '.cursor'],
        'required_files': ['README.md', 'CHANGELOG.md', 'LICENSE', 'setup.py', 'pyproject.toml', 'requirements.txt', 'VERSION'],
        'forbidden_folders': ['docs', 'scripts'],
        'forbidden_patterns': [
            '*_summary.md', '*_rules.md', 'BRANCH_*.md', 'WORKFLOW_*.md', 'SETUP_*.md',
            'release-notes.md', 'updates.txt', '*.log', '*.tmp', '*.bak', '*.cache',
            'experimental_*', 'local_*', 'temp_*', 'debug_*', 'staging_*'
        ],
        'allowed_root_scripts': ['build.py', 'release.py', 'build.sh', 'release.sh'],
        'description': 'Primary branch for stable production releases and changelog management'
    },
    'testing': {
        'allowed_folders': ['src', 'utils', 'tests', '.cursor', 'docs', 'scripts'],
        'required_files': ['README.md', 'LICENSE', 'setup.py', 'pyproject.toml', 'requirements.txt', 'VERSION'],
        'forbidden_folders': [],
        'forbidden_patterns': [
            '*_summary.md', '*_rules.md', 'BRANCH_*.md', 'WORKFLOW_*.md', 'SETUP_*.md',
            'release-notes.md', 'updates.txt', 'personal_*', 'temp_*', 'irrelevant_*'
        ],
        'allowed_root_scripts': ['*'],  # All scripts allowed in testing
        'description': 'Beta release environment and GitHub Pages deployment'
    },
    'master': {
        'allowed_folders': ['src', 'utils', 'tests', '.cursor', 'scripts'],
        'required_files': ['README.md', 'LICENSE', 'setup.py', 'pyproject.toml', 'requirements.txt', 'VERSION'],
        'forbidden_folders': ['docs'],  # No docs in master
        'forbidden_patterns': [
            '*_summary.md', '*_rules.md', 'BRANCH_*.md', 'WORKFLOW_*.md', 'SETUP_*.md',
            'release-notes.md', 'updates.txt', 'redundant_*', 'outdated_*'
        ],
        'allowed_root_scripts': ['*'],  # All scripts allowed in master for development
        'description': 'Central development branch with latest changes'
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

def check_root_scripts(branch_rules):
    """Check root directory scripts according to branch rules"""
    violations = []
    current_branch = get_current_branch()
    
    if current_branch == 'main':
        # In main branch, only critical release-related scripts are allowed
        allowed_scripts = branch_rules['allowed_root_scripts']
        for script_file in Path('.').glob('*.py'):
            if script_file.name not in allowed_scripts:
                violations.append(f"❌ Unauthorized root script in main branch: {script_file.name}")
        for script_file in Path('.').glob('*.sh'):
            if script_file.name not in allowed_scripts:
                violations.append(f"❌ Unauthorized root script in main branch: {script_file.name}")
    
    return violations

def check_changelog_rules():
    """Check changelog management rules"""
    violations = []
    current_branch = get_current_branch()
    
    # Check for duplicate changelogs
    changelog_files = list(Path('.').glob('*changelog*'))
    if len(changelog_files) > 1:
        violations.append(f"❌ Multiple changelog files found: {[f.name for f in changelog_files]}")
    
    # Check for additional release notes
    release_note_files = list(Path('.').glob('*release*note*')) + list(Path('.').glob('*update*.txt'))
    if release_note_files:
        violations.append(f"❌ Additional release notes found: {[f.name for f in release_note_files]}")
    
    # Master branch should not have CHANGELOG.md (must be edited only in main)
    if current_branch == 'master' and Path('CHANGELOG.md').exists():
        violations.append("❌ CHANGELOG.md should not be in master branch (edit only in main)")
    
    return violations

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
    print(f"📋 Purpose: {BRANCH_RULES[current_branch]['description']}")
    print("=" * 60)
    
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
    
    # Check root scripts
    script_violations = check_root_scripts(branch_rules)
    violations.extend(script_violations)
    
    # Check changelog rules
    changelog_violations = check_changelog_rules()
    violations.extend(changelog_violations)
    
    if violations:
        print("❌ Branch protection violations found:")
        for violation in violations:
            print(f"   {violation}")
        print("\n🚫 Commit blocked due to branch protection violations")
        print("\n💡 Fix these issues before committing:")
        print("   - Remove forbidden files/folders")
        print("   - Ensure required files are present")
        print("   - Follow branch-specific script policies")
        print("   - Maintain single changelog in main branch only")
        return False
    else:
        print("✅ Branch structure validation passed")
        print("✅ All branch protection rules satisfied")
        return True

def main():
    """Main function"""
    print("🔒 Branch Protection Rules Enforcement (Final, Strict Version)")
    print("=" * 60)
    
    if not validate_branch_structure():
        sys.exit(1)
    
    print("\n✅ All branch protection rules satisfied")
    print("✅ Proceeding with commit...")

if __name__ == "__main__":
    main() 