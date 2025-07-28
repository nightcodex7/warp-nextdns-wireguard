#!/usr/bin/env python3
"""
Verify Author Compliance
Author: Tuhin Garai
Email: 64925748+nightcodex7@users.noreply.github.com

This script ensures all author information is correct throughout the repository.
"""

import subprocess
import os
from pathlib import Path

CORRECT_NAME = "Tuhin Garai"
CORRECT_EMAIL = "64925748+nightcodex7@users.noreply.github.com"
OLD_EMAIL = "nightcodex7@gmail.com"  # This should not be used anymore

def run_command(cmd):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_git_config():
    """Check Git configuration"""
    print("🔍 Checking Git Configuration...")
    
    # Local config
    success, local_name, _ = run_command('git config user.name')
    success2, local_email, _ = run_command('git config user.email')
    
    # Global config
    success3, global_name, _ = run_command('git config --global user.name')
    success4, global_email, _ = run_command('git config --global user.email')
    
    issues = []
    
    if local_name != CORRECT_NAME:
        issues.append(f"Local git user.name is '{local_name}', should be '{CORRECT_NAME}'")
    if local_email != CORRECT_EMAIL:
        issues.append(f"Local git user.email is '{local_email}', should be '{CORRECT_EMAIL}'")
    if global_name != CORRECT_NAME:
        issues.append(f"Global git user.name is '{global_name}', should be '{CORRECT_NAME}'")
    if global_email != CORRECT_EMAIL:
        issues.append(f"Global git user.email is '{global_email}', should be '{CORRECT_EMAIL}'")
    
    if not issues:
        print("  ✅ Git configuration is correct!")
        print(f"     Name: {CORRECT_NAME}")
        print(f"     Email: {CORRECT_EMAIL}")
    else:
        print("  ❌ Git configuration issues found:")
        for issue in issues:
            print(f"     - {issue}")
    
    return len(issues) == 0

def check_files_for_old_email():
    """Check all files for old email"""
    print("\n🔍 Checking for old email addresses...")
    
    # Skip binary files and git directory
    skip_patterns = ['.git', '.pyc', '.png', '.jpg', '.ico', '.svg']
    
    files_with_old_email = []
    
    for file_path in Path('.').rglob('*'):
        if any(pattern in str(file_path) for pattern in skip_patterns):
            continue
        
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if OLD_EMAIL in content:
                        files_with_old_email.append(str(file_path))
            except:
                pass
    
    if files_with_old_email:
        print(f"  ❌ Found {len(files_with_old_email)} files with old email:")
        for file in files_with_old_email[:10]:  # Show first 10
            print(f"     - {file}")
        if len(files_with_old_email) > 10:
            print(f"     ... and {len(files_with_old_email) - 10} more")
    else:
        print("  ✅ No files contain the old email address!")
    
    return len(files_with_old_email) == 0

def check_workflow_files():
    """Check workflow files for correct author info"""
    print("\n🔍 Checking workflow files...")
    
    workflow_dir = Path('.github/workflows')
    if not workflow_dir.exists():
        print("  ❌ No workflow directory found")
        return False
    
    issues = []
    
    for workflow_file in workflow_dir.glob('*.yml'):
        with open(workflow_file, 'r') as f:
            content = f.read()
            
        if 'github-actions[bot]' in content:
            issues.append(f"{workflow_file.name} contains bot reference")
        if OLD_EMAIL in content:
            issues.append(f"{workflow_file.name} contains old email")
    
    if not issues:
        print("  ✅ All workflow files have correct author information!")
    else:
        print("  ❌ Workflow issues found:")
        for issue in issues:
            print(f"     - {issue}")
    
    return len(issues) == 0

def check_recent_commits():
    """Check recent commits for correct author"""
    print("\n🔍 Checking recent commits...")
    
    success, log_output, _ = run_command('git log --format="%an <%ae>" -5')
    
    if success and log_output:
        commits = log_output.split('\n')
        correct_format = f"{CORRECT_NAME} <{CORRECT_EMAIL}>"
        
        all_correct = all(commit == correct_format for commit in commits)
        
        if all_correct:
            print("  ✅ Last 5 commits have correct author information!")
        else:
            print("  ⚠️  Some recent commits have different author info:")
            for i, commit in enumerate(commits):
                if commit != correct_format:
                    print(f"     Commit {i+1}: {commit}")
    
    return True  # Don't fail on this, just warn

def generate_report():
    """Generate compliance report"""
    print("\n" + "="*60)
    print("📊 AUTHOR COMPLIANCE REPORT")
    print("="*60)
    
    all_checks = []
    
    # Run all checks
    all_checks.append(("Git Configuration", check_git_config()))
    all_checks.append(("Old Email Check", check_files_for_old_email()))
    all_checks.append(("Workflow Files", check_workflow_files()))
    all_checks.append(("Recent Commits", check_recent_commits()))
    
    # Summary
    passed = sum(1 for _, result in all_checks if result)
    total = len(all_checks)
    
    print(f"\n✅ Passed: {passed}/{total} checks")
    
    if passed == total:
        print("\n🎉 FULL COMPLIANCE ACHIEVED!")
        print(f"   Author: {CORRECT_NAME}")
        print(f"   Email: {CORRECT_EMAIL}")
        print("   All files and configurations are correct!")
    else:
        print("\n⚠️  Some issues need attention")
        print("   Run: python3 scripts/fix-author-info.py")
    
    return passed == total

def main():
    """Main function"""
    print("🚀 Author Compliance Verification")
    print("="*60)
    print(f"Correct Author: {CORRECT_NAME}")
    print(f"Correct Email: {CORRECT_EMAIL}")
    print("="*60)
    
    # Generate report
    compliant = generate_report()
    
    # Exit code
    return 0 if compliant else 1

if __name__ == "__main__":
    exit(main())