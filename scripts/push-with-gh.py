#!/usr/bin/env python3
"""
Push to GitHub using GitHub CLI (gh)
Author: Tuhin Garai
Email: 64925748+nightcodex7@users.noreply.github.com

This script uses GitHub CLI to push changes, avoiding workflow permission issues.
Works with gh configured on Windows PowerShell.
"""

import subprocess
import os
import sys
from pathlib import Path

def run_command(cmd, shell=True):
    """Run a command and return success, stdout, stderr"""
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_gh_auth():
    """Check if gh is authenticated"""
    print("🔍 Checking GitHub CLI authentication...")
    
    success, output, error = run_command("gh auth status")
    
    if success:
        print("  ✅ GitHub CLI is authenticated!")
        return True
    else:
        print("  ❌ GitHub CLI not authenticated")
        print("  Please run: gh auth login")
        return False

def get_current_branch():
    """Get current Git branch"""
    success, branch, _ = run_command("git branch --show-current")
    return branch if success else None

def push_with_gh():
    """Push using GitHub CLI"""
    branch = get_current_branch()
    if not branch:
        print("❌ Could not determine current branch")
        return False
    
    print(f"\n🚀 Pushing to origin/{branch} using GitHub CLI...")
    
    # First, ensure we're up to date
    print("  📥 Fetching latest changes...")
    run_command("git fetch origin")
    
    # Push using gh
    print("  📤 Pushing with gh...")
    success, output, error = run_command(f"gh repo sync --branch {branch}")
    
    if success:
        print("  ✅ Push successful using GitHub CLI!")
        print("  All files including workflows have been pushed!")
        return True
    else:
        print(f"  ❌ Push failed: {error}")
        
        # Try alternative gh command
        print("\n  🔄 Trying alternative method...")
        success2, output2, error2 = run_command(f"git push origin {branch}")
        
        if success2:
            print("  ✅ Push successful!")
            return True
        else:
            print(f"  ❌ Alternative push also failed: {error2}")
            return False

def create_windows_batch_script():
    """Create a Windows batch script for easy execution"""
    batch_content = """@echo off
REM Push to GitHub using GitHub CLI
REM Author: Tuhin Garai
REM Email: 64925748+nightcodex7@users.noreply.github.com

echo ========================================
echo GitHub CLI Push Tool
echo ========================================

REM Check if gh is available
where gh >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: GitHub CLI (gh) not found!
    echo Please install from: https://cli.github.com/
    pause
    exit /b 1
)

REM Check authentication
gh auth status >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Not authenticated with GitHub CLI
    echo Running: gh auth login
    gh auth login
)

REM Get current branch
for /f "tokens=*" %%i in ('git branch --show-current') do set BRANCH=%%i
echo Current branch: %BRANCH%

REM Push using gh
echo Pushing to GitHub...
gh repo sync --branch %BRANCH%

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! All files pushed including workflows!
) else (
    echo.
    echo Trying alternative push method...
    git push origin %BRANCH%
)

echo.
echo ========================================
echo Push complete!
echo ========================================
pause
"""
    
    with open('push-with-gh.bat', 'w') as f:
        f.write(batch_content)
    
    print("\n📄 Created Windows batch script: push-with-gh.bat")
    print("   You can double-click this file in Windows to push!")

def create_powershell_script():
    """Create a PowerShell script for Windows"""
    ps1_content = """# Push to GitHub using GitHub CLI
# Author: Tuhin Garai
# Email: 64925748+nightcodex7@users.noreply.github.com

Write-Host "========================================"
Write-Host "GitHub CLI Push Tool" -ForegroundColor Cyan
Write-Host "========================================"

# Check if gh is available
if (!(Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: GitHub CLI (gh) not found!" -ForegroundColor Red
    Write-Host "Please install from: https://cli.github.com/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check authentication
$authCheck = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Not authenticated with GitHub CLI" -ForegroundColor Red
    Write-Host "Running: gh auth login"
    gh auth login
}

# Get current branch
$branch = git branch --show-current
Write-Host "Current branch: $branch" -ForegroundColor Green

# Push using gh
Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
gh repo sync --branch $branch

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSUCCESS! All files pushed including workflows!" -ForegroundColor Green
} else {
    Write-Host "`nTrying alternative push method..." -ForegroundColor Yellow
    git push origin $branch
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nSUCCESS! Push completed!" -ForegroundColor Green
    }
}

Write-Host "`n========================================"
Write-Host "Push complete!" -ForegroundColor Cyan
Write-Host "========================================"
Read-Host "`nPress Enter to exit"
"""
    
    with open('push-with-gh.ps1', 'w') as f:
        f.write(ps1_content)
    
    print("\n📄 Created PowerShell script: push-with-gh.ps1")
    print("   Run in PowerShell: .\\push-with-gh.ps1")

def main():
    """Main function"""
    print("🚀 GitHub CLI Push Tool")
    print("="*60)
    print("Author: Tuhin Garai")
    print("Email: 64925748+nightcodex7@users.noreply.github.com")
    print("="*60)
    
    # Check if running on Windows
    is_windows = sys.platform.startswith('win')
    
    if is_windows:
        print("\n🪟 Detected Windows environment")
        create_windows_batch_script()
        create_powershell_script()
        print("\n✅ Windows scripts created!")
        print("\nYou can now:")
        print("1. Double-click 'push-with-gh.bat'")
        print("2. Or run '.\\push-with-gh.ps1' in PowerShell")
        print("3. Or continue with this Python script")
        
        response = input("\nContinue with push? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Check gh authentication
    if not check_gh_auth():
        print("\n❌ Please authenticate with GitHub CLI first:")
        print("   Run: gh auth login")
        print("   - Choose GitHub.com")
        print("   - Choose HTTPS")
        print("   - Authenticate with browser")
        return
    
    # Get current status
    success, status, _ = run_command("git status --porcelain")
    if success and status:
        print(f"\n⚠️  You have uncommitted changes:")
        print(status[:200] + "..." if len(status) > 200 else status)
        response = input("\nCommit and push? (y/n): ")
        
        if response.lower() == 'y':
            message = input("Commit message: ")
            run_command(f'git add -A && git commit -m "{message}" --author="Tuhin Garai <64925748+nightcodex7@users.noreply.github.com>"')
    
    # Push with gh
    if push_with_gh():
        print("\n✅ Success! All files including workflows have been pushed!")
        print("\n📊 Verify at: https://github.com/nightcodex7/warp-nextdns-wireguard/actions")
    else:
        print("\n❌ Push failed. Please check your GitHub CLI configuration.")
        print("\nTroubleshooting:")
        print("1. Run: gh auth status")
        print("2. Run: gh auth refresh")
        print("3. Or re-authenticate: gh auth login")

if __name__ == "__main__":
    main()