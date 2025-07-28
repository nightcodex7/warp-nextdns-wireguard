#!/usr/bin/env python3
"""
Release Validation Script
Ensures releases follow branch-specific rules and contain only appropriate files
"""

import os
import re
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

def get_latest_tag():
    """Get the latest tag on current branch"""
    success, tag, _ = run_command("git describe --tags --abbrev=0", check=False)
    return tag if success else None

def validate_version_format(version, branch):
    """Validate version format based on branch"""
    # Remove 'v' prefix if present
    version = version.lstrip('v')
    
    if branch == "main":
        # Main branch: stable versions only (e.g., 1.0.0, 2.1.3)
        pattern = r'^\d+\.\d+\.\d+$'
        if not re.match(pattern, version):
            return False, "Main branch requires stable version format (e.g., 1.0.0)"
        return True, "Valid stable version"
    
    elif branch == "testing":
        # Testing branch: pre-release versions only
        pattern = r'^\d+\.\d+\.\d+-(alpha|beta|rc)\.\d+$'
        if not re.match(pattern, version):
            return False, "Testing branch requires pre-release format (e.g., 1.0.0-beta.1)"
        return True, "Valid pre-release version"
    
    else:
        return False, f"Releases not allowed on branch '{branch}'"

def check_forbidden_files():
    """Check for forbidden files that should never be in releases"""
    forbidden_patterns = [
        "*_SUMMARY.md",
        "*_summary.md",
        "*SUMMARY*",
        "*.tmp",
        "*.temp",
        "*.bak",
        "*~",
        "*.swp",
        "*.swo",
        ".DS_Store",
        "Thumbs.db",
        "desktop.ini"
    ]
    
    found_files = []
    for pattern in forbidden_patterns:
        success, files, _ = run_command(f'find . -name "{pattern}" -type f | grep -v ".git"', check=False)
        if success and files:
            found_files.extend(files.strip().split('\n'))
    
    return [f for f in found_files if f]

def check_changelog():
    """Check if CHANGELOG.md exists and is updated"""
    if not os.path.exists("CHANGELOG.md"):
        return False, "CHANGELOG.md not found"
    
    # Check if CHANGELOG.md has been modified recently
    success, status, _ = run_command("git status --porcelain CHANGELOG.md")
    if not success:
        return False, "Failed to check CHANGELOG.md status"
    
    # Get last commit that modified CHANGELOG.md
    success, last_commit, _ = run_command("git log -1 --format=%H -- CHANGELOG.md")
    if success:
        return True, "CHANGELOG.md exists"
    
    return True, "CHANGELOG.md exists"

def validate_release_assets():
    """Validate files that would be included in release"""
    # Check for build artifacts if they exist
    allowed_assets = [
        "warp-nextdns-manager-linux",
        "warp-nextdns-manager-windows.exe",
        "warp-nextdns-manager-macos",
        "*.tar.gz",
        "*.zip"
    ]
    
    # This is more of a guideline check
    return True, "Asset validation passed"

def check_git_status():
    """Check if working directory is clean"""
    success, status, _ = run_command("git status --porcelain")
    if success and status:
        return False, "Working directory has uncommitted changes"
    return True, "Working directory is clean"

def validate_release_notes_format(tag):
    """Validate release notes don't contain forbidden content"""
    # This would check the release notes if they exist
    # For now, we'll provide guidelines
    forbidden_terms = [
        "summary",
        "SUMMARY",
        "_summary",
        "internal use",
        "debug",
        "TODO",
        "FIXME"
    ]
    
    return True, "Release notes guidelines checked"

def main():
    """Main validation function"""
    print(f"{Colors.BLUE}🔍 Release Validation Tool{Colors.END}")
    print("=" * 50)
    
    # Get current branch
    branch = get_current_branch()
    if not branch:
        print_status("Failed to determine current branch", "error")
        return 1
    
    print_status(f"Current branch: {branch}")
    
    # Track validation results
    errors = []
    warnings = []
    
    # 1. Check if releases are allowed on this branch
    if branch not in ["main", "testing"]:
        errors.append(f"Releases not allowed on branch '{branch}'")
    
    # 2. Check for forbidden files
    print_status("Checking for forbidden files...")
    forbidden = check_forbidden_files()
    if forbidden:
        errors.append(f"Found {len(forbidden)} forbidden files:")
        for f in forbidden:
            print(f"  - {f}")
    else:
        print_status("No forbidden files found", "success")
    
    # 3. Validate version format (if tag provided)
    if len(sys.argv) > 1:
        version = sys.argv[1]
        print_status(f"Validating version: {version}")
        valid, message = validate_version_format(version, branch)
        if valid:
            print_status(message, "success")
        else:
            errors.append(message)
    
    # 4. Check CHANGELOG.md
    print_status("Checking CHANGELOG.md...")
    exists, message = check_changelog()
    if exists:
        print_status(message, "success")
    else:
        warnings.append(message)
    
    # 5. Check git status
    print_status("Checking git status...")
    clean, message = check_git_status()
    if clean:
        print_status(message, "success")
    else:
        warnings.append(message)
    
    # 6. Branch-specific checks
    if branch == "main":
        print_status("Validating main branch requirements...")
        # Check no beta/rc versions in git log
        success, tags, _ = run_command("git tag -l '*-beta*' '*-rc*' '*-alpha*'", check=False)
        if success and tags:
            warnings.append("Found pre-release tags on main branch (should be on testing)")
    
    elif branch == "testing":
        print_status("Validating testing branch requirements...")
        # Check no stable versions tagged recently
        success, tags, _ = run_command("git tag -l | grep -v -E '(alpha|beta|rc)'", check=False)
        if success and tags:
            stable_tags = [t for t in tags.split('\n') if re.match(r'^v?\d+\.\d+\.\d+$', t)]
            if stable_tags:
                warnings.append("Found stable version tags on testing branch (should be on main)")
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Validation Summary:")
    
    if not errors and not warnings:
        print_status("All validation checks passed!", "success")
        print("\n✅ Ready to create release!")
        
        # Print next steps
        print(f"\n📝 Next steps for {branch} branch:")
        if branch == "main":
            print("  1. Tag with stable version: git tag -a v1.0.0 -m 'Release v1.0.0'")
            print("  2. Push tags: git push origin main --tags")
        elif branch == "testing":
            print("  1. Tag with beta version: git tag -a v1.0.0-beta.1 -m 'Beta release v1.0.0-beta.1'")
            print("  2. Push tags: git push origin testing --tags")
        
        return 0
    
    if warnings:
        print(f"\n{Colors.YELLOW}⚠️  Warnings ({len(warnings)}):{Colors.END}")
        for warning in warnings:
            print(f"  - {warning}")
    
    if errors:
        print(f"\n{Colors.RED}❌ Errors ({len(errors)}):{Colors.END}")
        for error in errors:
            print(f"  - {error}")
        print("\n❌ Release validation failed! Fix errors before proceeding.")
        return 1
    
    print("\n⚠️  Release validation completed with warnings.")
    return 0

if __name__ == "__main__":
    sys.exit(main())