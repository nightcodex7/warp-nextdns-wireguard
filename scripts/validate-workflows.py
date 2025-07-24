#!/usr/bin/env python3
"""
Validate GitHub Actions Workflows
Checks for common errors and fixes them
"""

import os
import yaml
import re
from pathlib import Path

def check_workflow_syntax(filepath):
    """Check a workflow file for common issues"""
    issues = []
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check for YAML syntax
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        issues.append(f"YAML syntax error: {e}")
        return issues
    
    # Check required fields
    if not data:
        issues.append("Empty workflow file")
        return issues
    
    if 'name' not in data:
        issues.append("Missing 'name' field")
    
    if 'on' not in data:
        issues.append("Missing 'on' trigger field")
    
    if 'jobs' not in data:
        issues.append("Missing 'jobs' field")
    
    # Check for common issues in jobs
    if 'jobs' in data:
        for job_name, job in data['jobs'].items():
            if not isinstance(job, dict):
                issues.append(f"Job '{job_name}' is not properly formatted")
                continue
                
            if 'runs-on' not in job:
                issues.append(f"Job '{job_name}' missing 'runs-on'")
            
            if 'steps' not in job:
                issues.append(f"Job '{job_name}' missing 'steps'")
            
            # Check steps
            if 'steps' in job and isinstance(job['steps'], list):
                for i, step in enumerate(job['steps']):
                    if 'uses' not in step and 'run' not in step:
                        issues.append(f"Job '{job_name}' step {i+1} missing 'uses' or 'run'")
    
    # Check for deprecated actions
    deprecated_patterns = [
        (r'actions/checkout@v[12]', 'Use actions/checkout@v3 or v4'),
        (r'actions/setup-python@v[12]', 'Use actions/setup-python@v4'),
        (r'actions/upload-artifact@v[12]', 'Use actions/upload-artifact@v3'),
    ]
    
    for pattern, suggestion in deprecated_patterns:
        if re.search(pattern, content):
            issues.append(f"Deprecated action found: {suggestion}")
    
    # Check for shell issues in run commands
    run_blocks = re.findall(r'run:\s*\|([^-]+?)(?=\n\s*[-\w]|\Z)', content, re.DOTALL)
    for block in run_blocks:
        # Check for common shell issues
        if '&>' in block and 'bash' not in block:
            issues.append("Using '&>' redirection without bash shell")
        
        if re.search(r'\$\{[^}]+\}', block) and 'bash' not in content:
            issues.append("Using bash-style variable expansion without bash shell")
    
    return issues

def fix_common_issues(filepath):
    """Fix common workflow issues"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Update deprecated actions
    content = re.sub(r'actions/checkout@v[12]', 'actions/checkout@v3', content)
    content = re.sub(r'actions/setup-python@v[12]', 'actions/setup-python@v4', content)
    content = re.sub(r'actions/upload-artifact@v[12]', 'actions/upload-artifact@v3', content)
    
    # Fix permission issues for GITHUB_TOKEN
    if 'GITHUB_TOKEN' in content and 'permissions:' not in content:
        # Add permissions after name
        content = re.sub(
            r'(name:.*\n)',
            r'\1\npermissions:\n  contents: write\n  pull-requests: write\n',
            content,
            count=1
        )
    
    # Fix branch protection for master branch
    if 'branches: [ main, testing ]' in content:
        content = content.replace(
            'branches: [ main, testing ]',
            'branches: [ main, testing, master ]'
        )
    
    # Ensure shell is specified for complex commands
    if '${' in content or '&>' in content:
        # Add shell: bash to run steps that need it
        content = re.sub(
            r'(\n\s*-\s+run:.*\n)(\s+)(?!shell:)',
            r'\1\2shell: bash\n\2',
            content
        )
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def validate_all_workflows():
    """Validate all workflow files"""
    workflow_dir = '.github/workflows'
    if not os.path.exists(workflow_dir):
        print("❌ No .github/workflows directory found")
        return
    
    print("🔍 Validating GitHub Actions workflows...\n")
    
    all_issues = {}
    workflow_files = list(Path(workflow_dir).glob('*.yml')) + list(Path(workflow_dir).glob('*.yaml'))
    
    for workflow_file in workflow_files:
        print(f"Checking {workflow_file.name}...")
        issues = check_workflow_syntax(workflow_file)
        
        if issues:
            all_issues[workflow_file.name] = issues
            print(f"  ❌ Found {len(issues)} issues")
            for issue in issues:
                print(f"     - {issue}")
        else:
            print(f"  ✅ No issues found")
    
    # Attempt to fix issues
    if all_issues:
        print("\n🔧 Attempting to fix common issues...")
        fixed_count = 0
        
        for workflow_file in workflow_files:
            if fix_common_issues(workflow_file):
                print(f"  ✅ Fixed issues in {workflow_file.name}")
                fixed_count += 1
        
        if fixed_count > 0:
            print(f"\n✅ Fixed issues in {fixed_count} workflow files")
            print("Re-validating...")
            
            # Re-validate
            remaining_issues = {}
            for workflow_file in workflow_files:
                issues = check_workflow_syntax(workflow_file)
                if issues:
                    remaining_issues[workflow_file.name] = issues
            
            if remaining_issues:
                print(f"\n⚠️  {len(remaining_issues)} workflows still have issues:")
                for workflow, issues in remaining_issues.items():
                    print(f"\n{workflow}:")
                    for issue in issues:
                        print(f"  - {issue}")
            else:
                print("\n✅ All workflows are now valid!")
    else:
        print("\n✅ All workflows are valid!")

def check_workflow_permissions():
    """Check if workflows have necessary permissions"""
    print("\n🔐 Checking workflow permissions...")
    
    workflows_needing_permissions = {
        'branch-sync.yml': ['contents: write', 'pull-requests: write'],
        'main-release.yml': ['contents: write', 'packages: write'],
        'promote-to-main.yml': ['contents: write', 'actions: write'],
        'docs-deploy.yml': ['contents: write', 'pages: write'],
    }
    
    for workflow, needed_perms in workflows_needing_permissions.items():
        filepath = f'.github/workflows/{workflow}'
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
            
            missing_perms = []
            for perm in needed_perms:
                if perm not in content:
                    missing_perms.append(perm)
            
            if missing_perms:
                print(f"  ⚠️  {workflow} may need permissions: {', '.join(missing_perms)}")
            else:
                print(f"  ✅ {workflow} has necessary permissions")

if __name__ == "__main__":
    validate_all_workflows()
    check_workflow_permissions()