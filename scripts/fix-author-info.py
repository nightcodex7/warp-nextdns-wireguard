#!/usr/bin/env python3
"""
Fix Author Information Throughout Repository
Author: Tuhin Garai
Email: 64925748+nightcodex7@users.noreply.github.com
"""

import subprocess
import os
from pathlib import Path

def run_command(cmd):
    """Run a shell command"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def fix_git_config():
    """Set correct Git configuration"""
    print("🔧 Setting Git Configuration...")
    
    commands = [
        'git config user.name "Tuhin Garai"',
        'git config user.email "64925748+nightcodex7@users.noreply.github.com"',
        'git config --global user.name "Tuhin Garai"',
        'git config --global user.email "64925748+nightcodex7@users.noreply.github.com"'
    ]
    
    for cmd in commands:
        success, _, _ = run_command(cmd)
        if success:
            print(f"  ✅ {cmd}")
        else:
            print(f"  ❌ Failed: {cmd}")

def update_workflow_files():
    """Update all workflow files with correct author info"""
    print("\n🔧 Updating Workflow Files...")
    
    workflow_dir = Path('.github/workflows')
    if not workflow_dir.exists():
        print("  ❌ No .github/workflows directory found")
        return
    
    # Replace any incorrect email addresses
    replacements = [
        ('64925748+nightcodex7@users.noreply.github.com', '64925748+nightcodex7@users.noreply.github.com'),
        ('github-actions\\[bot\\]@users.noreply.github.com', '64925748+nightcodex7@users.noreply.github.com'),
        ('github-actions\\[bot\\]', 'Tuhin Garai')
    ]
    
    for workflow_file in workflow_dir.glob('*.yml'):
        print(f"  📄 Updating {workflow_file.name}")
        
        content = workflow_file.read_text()
        original_content = content
        
        for old, new in replacements:
            import re
            content = re.sub(old, new, content)
        
        if content != original_content:
            workflow_file.write_text(content)
            print(f"    ✅ Updated")
        else:
            print(f"    ✓ Already correct")

def update_python_scripts():
    """Update all Python scripts with correct author info"""
    print("\n🔧 Updating Python Scripts...")
    
    for script_file in Path('.').rglob('*.py'):
        if '.git' in str(script_file):
            continue
            
        try:
            content = script_file.read_text()
            original_content = content
            
            # Update email addresses
            content = content.replace('64925748+nightcodex7@users.noreply.github.com', '64925748+nightcodex7@users.noreply.github.com')
            
            # Update any hardcoded author info
            if 'Author:' in content and 'Tuhin' not in content:
                content = content.replace('Author:', 'Author: Tuhin Garai')
            
            if content != original_content:
                script_file.write_text(content)
                print(f"  ✅ Updated: {script_file}")
                
        except Exception as e:
            print(f"  ❌ Error updating {script_file}: {e}")

def create_authors_file():
    """Create an AUTHORS file"""
    print("\n🔧 Creating AUTHORS File...")
    
    authors_content = """# Authors

## Primary Author
- **Tuhin Garai** <64925748+nightcodex7@users.noreply.github.com>
  - GitHub: [@nightcodex7](https://github.com/nightcodex7)
  - Project Lead and Main Developer
  - WARP + NextDNS Manager Creator

## Contributors
Contributors are listed in the order of their first contribution.

---
*This file lists all individuals who have contributed to this project.*
"""
    
    with open('AUTHORS', 'w') as f:
        f.write(authors_content)
    
    print("  ✅ AUTHORS file created")

def update_documentation():
    """Update documentation files with correct author info"""
    print("\n🔧 Updating Documentation...")
    
    doc_files = [
        'README.md',
        'CONTRIBUTING.md',
        'CODE_OF_CONDUCT.md',
        'SECURITY.md'
    ]
    
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            try:
                with open(doc_file, 'r') as f:
                    content = f.read()
                
                original_content = content
                
                # Update email
                content = content.replace('64925748+nightcodex7@users.noreply.github.com', '64925748+nightcodex7@users.noreply.github.com')
                
                if content != original_content:
                    with open(doc_file, 'w') as f:
                        f.write(content)
                    print(f"  ✅ Updated: {doc_file}")
                else:
                    print(f"  ✓ {doc_file} already correct")
                    
            except Exception as e:
                print(f"  ❌ Error updating {doc_file}: {e}")

def verify_author_info():
    """Verify author information is correct"""
    print("\n🔍 Verifying Author Information...")
    
    # Check current git config
    success, name, _ = run_command('git config user.name')
    success2, email, _ = run_command('git config user.email')
    
    if success and success2:
        print(f"  Current Git User: {name.strip()}")
        print(f"  Current Git Email: {email.strip()}")
        
        if name.strip() == "Tuhin Garai" and email.strip() == "64925748+nightcodex7@users.noreply.github.com":
            print("  ✅ Git configuration is correct!")
        else:
            print("  ❌ Git configuration needs updating")
    
    # Check for any remaining incorrect emails
    print("\n  Checking for incorrect emails...")
    success, results, _ = run_command('grep -r "64925748+nightcodex7@users.noreply.github.com" . --exclude-dir=.git || true')
    
    if results:
        print("  ⚠️  Found files with old email:")
        for line in results.split('\n')[:5]:  # Show first 5
            if line:
                print(f"    - {line}")
    else:
        print("  ✅ No incorrect emails found")

def main():
    """Main function"""
    print("🚀 Fixing Author Information")
    print("=" * 60)
    print("Author: Tuhin Garai")
    print("Email: 64925748+nightcodex7@users.noreply.github.com")
    print("=" * 60)
    
    # Fix everything
    fix_git_config()
    update_workflow_files()
    update_python_scripts()
    update_documentation()
    create_authors_file()
    
    # Verify
    verify_author_info()
    
    print("\n" + "=" * 60)
    print("✅ Author information fix complete!")
    print("\nIMPORTANT:")
    print("- Always use: 64925748+nightcodex7@users.noreply.github.com")
    print("- This ensures commits are linked to your GitHub account")
    print("- Use 'Tuhin Garai' as the author name")

if __name__ == "__main__":
    main()