#!/usr/bin/env python3
"""
WARP + NextDNS Workflow Health Check
Author: Tuhin Garai
Checks all GitHub Actions workflows for issues
"""

import os
import yaml
import sys
from pathlib import Path

def check_workflow_file(filepath):
    """Check a single workflow file for issues"""
    issues = []
    
    with open(filepath, 'r') as f:
        content = f.read()
        
    # Check for deprecated actions
    deprecated_actions = [
        ('actions/upload-artifact@v3', 'actions/upload-artifact@v4'),
        ('actions/download-artifact@v3', 'actions/download-artifact@v4'),
        ('actions/create-release@', 'softprops/action-gh-release@v2'),
        ('actions/upload-release-asset@', 'softprops/action-gh-release@v2'),
        ('actions/cache@v1', 'actions/cache@v4'),
        ('actions/cache@v2', 'actions/cache@v4'),
        ('ubuntu-20.04', 'ubuntu-22.04 or ubuntu-latest'),
    ]
    
    for deprecated, replacement in deprecated_actions:
        if deprecated in content:
            issues.append(f"❌ Uses deprecated: {deprecated} → Use {replacement}")
    
    # Check for bot references
    if 'github-actions[bot]' in content:
        issues.append("⚠️  Contains bot reference - should use 'Tuhin Garai'")
    
    # Parse YAML
    try:
        workflow = yaml.safe_load(content)
        
        # Check workflow name
        if 'name' in workflow:
            if 'WARP' not in workflow['name'] and 'NextDNS' not in workflow['name']:
                issues.append("💡 Workflow name could be more project-specific")
        
        # Check for proper permissions
        if 'permissions' not in workflow and 'release' in filepath.name:
            issues.append("⚠️  Release workflow should specify permissions")
            
    except yaml.YAMLError as e:
        issues.append(f"❌ YAML parsing error: {str(e)}")
    
    return issues

def main():
    """Check all workflows"""
    print("🔍 WARP + NextDNS Workflow Health Check")
    print("=" * 50)
    print("Author: Tuhin Garai")
    print("=" * 50 + "\n")
    
    workflows_dir = Path('.github/workflows')
    if not workflows_dir.exists():
        print("❌ No .github/workflows directory found!")
        return 1
    
    workflow_files = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))
    
    total_issues = 0
    healthy_workflows = []
    problematic_workflows = []
    
    for workflow_file in sorted(workflow_files):
        print(f"\n📄 Checking: {workflow_file.name}")
        issues = check_workflow_file(workflow_file)
        
        if issues:
            total_issues += len(issues)
            problematic_workflows.append(workflow_file.name)
            for issue in issues:
                print(f"   {issue}")
        else:
            healthy_workflows.append(workflow_file.name)
            print("   ✅ Healthy - No issues found")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary Report")
    print("=" * 50)
    print(f"Total workflows checked: {len(workflow_files)}")
    print(f"Healthy workflows: {len(healthy_workflows)}")
    print(f"Workflows with issues: {len(problematic_workflows)}")
    print(f"Total issues found: {total_issues}")
    
    if healthy_workflows:
        print("\n✅ Healthy Workflows:")
        for wf in healthy_workflows:
            print(f"   - {wf}")
    
    if problematic_workflows:
        print("\n⚠️  Workflows Needing Attention:")
        for wf in problematic_workflows:
            print(f"   - {wf}")
    
    print("\n" + "=" * 50)
    if total_issues == 0:
        print("🎉 All workflows are healthy and ready for GitHub Actions!")
        print("✅ No deprecated actions found")
        print("✅ All workflows are project-specific")
        print("✅ Authored by Tuhin Garai")
        return 0
    else:
        print("⚠️  Some workflows need attention")
        print("Run 'python3 scripts/fix-deprecated-actions.py' to fix issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())