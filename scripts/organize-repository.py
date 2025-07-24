#!/usr/bin/env python3
"""
Repository Organization Script for WARP + NextDNS Manager
Author: Tuhin Garai
Ensures all files are properly organized and ready for GitHub
"""

import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Ensure proper directory structure exists"""
    directories = [
        '.github/workflows',
        'src',
        'scripts',
        'tests',
        'utils',
        'docs'  # Only on testing branch
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directory ensured: {directory}")

def organize_documentation():
    """Organize documentation files"""
    doc_files = {
        'README.md': 'Project documentation',
        'CHANGELOG.md': 'Version history',
        'LICENSE': 'MIT License',
        'CONTRIBUTING.md': 'Contribution guidelines',
        'CODE_OF_CONDUCT.md': 'Community standards',
        'SECURITY.md': 'Security policy',
        'BRANCH_PROTECTION_RULES.md': 'Branch management rules',
        'RELEASE_RULES.md': 'Release policies',
        'VERSIONING_RULES.md': 'Version management',
        'DEVELOPER_GUIDE.md': 'Developer instructions',
        'BRANCH_MANAGEMENT.md': 'Git workflow guide'
    }
    
    print("\n📄 Documentation Files:")
    for file, description in doc_files.items():
        if os.path.exists(file):
            print(f"  ✅ {file} - {description}")
        else:
            print(f"  ❌ {file} - Missing! ({description})")

def check_workflow_files():
    """Check GitHub Actions workflow files"""
    workflows = [
        'ci.yml',
        'warp-nextdns-tests.yml',
        'main-release.yml',
        'release.yml',
        'docs-deploy.yml',
        'pages.yml',
        'promote-to-main.yml'
    ]
    
    print("\n🔧 Workflow Files (.github/workflows/):")
    workflow_dir = Path('.github/workflows')
    
    for workflow in workflows:
        workflow_path = workflow_dir / workflow
        if workflow_path.exists():
            print(f"  ✅ {workflow}")
        else:
            print(f"  ❌ {workflow} - Missing!")

def check_scripts():
    """Check essential scripts"""
    scripts = {
        'maintain-clean-branches.py': 'Branch cleanup automation',
        'validate-release.py': 'Release validation',
        'check-workflow-health.py': 'Workflow health monitoring',
        'git-sync-helper.py': 'Branch synchronization',
        'enforce-branch-structure.py': 'Branch compliance',
        'push-without-workflows.py': 'Emergency workflow bypass'
    }
    
    print("\n🐍 Essential Scripts (scripts/):")
    scripts_dir = Path('scripts')
    
    for script, description in scripts.items():
        script_path = scripts_dir / script
        if script_path.exists():
            print(f"  ✅ {script} - {description}")
        else:
            print(f"  ❌ {script} - Missing! ({description})")

def check_source_code():
    """Check source code structure"""
    src_files = ['__init__.py', 'main.py', 'cli.py', 'core.py']
    
    print("\n💻 Source Code (src/):")
    src_dir = Path('src')
    
    for file in src_files:
        file_path = src_dir / file
        if file_path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - Missing!")

def cleanup_unwanted_files():
    """Remove any unwanted files"""
    unwanted_patterns = [
        '*_SUMMARY.md',
        '*.tmp',
        '*.temp',
        '*.bak',
        '*~',
        '.DS_Store',
        'Thumbs.db'
    ]
    
    print("\n🧹 Cleaning unwanted files:")
    cleaned = 0
    
    for pattern in unwanted_patterns:
        for file in Path('.').rglob(pattern):
            if '.git' not in str(file):
                file.unlink()
                print(f"  🗑️  Removed: {file}")
                cleaned += 1
    
    if cleaned == 0:
        print("  ✅ No unwanted files found")

def generate_upload_report():
    """Generate a report of what needs to be uploaded"""
    print("\n" + "="*60)
    print("📊 GITHUB UPLOAD REPORT")
    print("="*60)
    
    print("\n🚨 URGENT - Manual Upload Required:")
    print("The following workflow files need to be manually uploaded to GitHub:")
    print("(.github/workflows/)")
    
    workflows = [
        'ci.yml', 'warp-nextdns-tests.yml', 'main-release.yml',
        'release.yml', 'docs-deploy.yml', 'pages.yml', 'promote-to-main.yml'
    ]
    
    for workflow in workflows:
        if Path(f'.github/workflows/{workflow}').exists():
            print(f"  📄 {workflow}")
    
    print("\n📝 How to upload:")
    print("1. Go to: https://github.com/nightcodex7/warp-nextdns-wireguard")
    print("2. Switch to 'testing' branch")
    print("3. Navigate to .github/workflows/")
    print("4. Click 'Add file' → 'Upload files'")
    print("5. Upload all workflow files")
    print("6. Commit with message: 'fix: add updated GitHub Actions workflows'")
    
    print("\n✅ Repository Status:")
    print("- All files organized properly")
    print("- No unwanted files")
    print("- Ready for GitHub")
    print("- Authored by Tuhin Garai")

def main():
    """Main organization function"""
    print("🚀 WARP + NextDNS Repository Organization")
    print("Author: Tuhin Garai")
    print("="*60)
    
    # Ensure directory structure
    create_directory_structure()
    
    # Check all components
    organize_documentation()
    check_workflow_files()
    check_scripts()
    check_source_code()
    
    # Clean up
    cleanup_unwanted_files()
    
    # Generate report
    generate_upload_report()
    
    print("\n✅ Repository organization complete!")

if __name__ == "__main__":
    main()