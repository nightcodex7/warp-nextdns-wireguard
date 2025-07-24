#!/usr/bin/env python3
"""
Script to remove unwanted GitHub Actions workflows
"""

import os
import sys
from pathlib import Path

# Workflows to remove (based on the GitHub Actions interface)
WORKFLOWS_TO_REMOVE = [
    "Build and Release",
    "CI/CD Pipeline",
    "CI/CD Pipeline (Simplified)",
    "Debug GitHub Pages",
    "Deploy Documentation to GitHub Pages",
    "Deploy to GitHub Pages (DEPRECATED)",
    "Main Branch Release Management",
    "pages-build-deployment",
    "Promote Testing to Main",
    "Simple Test"
]

def remove_workflow_files():
    """Remove workflow files from .github/workflows directory"""
    workflows_dir = Path(".github/workflows")
    
    if not workflows_dir.exists():
        print("✅ No .github/workflows directory found - already clean!")
        return
    
    print(f"🗑️  Removing workflow files from {workflows_dir}...")
    
    for workflow_file in workflows_dir.glob("*.yml"):
        print(f"   Removing: {workflow_file}")
        workflow_file.unlink()
    
    for workflow_file in workflows_dir.glob("*.yaml"):
        print(f"   Removing: {workflow_file}")
        workflow_file.unlink()
    
    # Remove the workflows directory if empty
    try:
        workflows_dir.rmdir()
        print(f"   Removed empty directory: {workflows_dir}")
    except OSError:
        print(f"   Directory {workflows_dir} not empty or already removed")
    
    # Remove .github directory if empty
    github_dir = Path(".github")
    try:
        github_dir.rmdir()
        print(f"   Removed empty directory: {github_dir}")
    except OSError:
        print(f"   Directory {github_dir} not empty or already removed")

def main():
    """Main function"""
    print("🧹 GitHub Actions Workflow Cleanup")
    print("=" * 40)
    
    print(f"📋 Workflows to remove: {len(WORKFLOWS_TO_REMOVE)}")
    for workflow in WORKFLOWS_TO_REMOVE:
        print(f"   - {workflow}")
    
    print("\n🗑️  Removing workflow files...")
    remove_workflow_files()
    
    print("\n✅ Workflow cleanup completed!")
    print("\n📝 Next steps:")
    print("   1. Commit these changes: git add -A && git commit -m 'remove: unwanted GitHub Actions workflows'")
    print("   2. Push to remote: git push origin testing")
    print("   3. The workflows will be automatically removed from GitHub Actions")

if __name__ == "__main__":
    main() 