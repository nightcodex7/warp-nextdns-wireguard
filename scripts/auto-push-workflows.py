#!/usr/bin/env python3
"""
Automated Workflow Push Script
Author: Tuhin Garai
Email: 64925748+nightcodex7@users.noreply.github.com

This script automatically attempts multiple methods to push workflow files.
"""

import subprocess
import os
import sys
import json
import base64
from pathlib import Path

def run_command(cmd, shell=True):
    """Run a command and return success, stdout, stderr"""
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_gh_cli():
    """Check if GitHub CLI is available"""
    success, _, _ = run_command("gh --version")
    return success

def try_gh_push():
    """Try pushing with GitHub CLI"""
    print("\n🔧 Method 1: Trying GitHub CLI push...")
    
    if not check_gh_cli():
        print("  ❌ GitHub CLI not available")
        return False
    
    # Check auth
    success, _, _ = run_command("gh auth status")
    if not success:
        print("  ❌ GitHub CLI not authenticated")
        return False
    
    # Get current branch
    success, branch, _ = run_command("git branch --show-current")
    if not success:
        print("  ❌ Could not determine current branch")
        return False
    
    print(f"  📤 Pushing {branch} branch with gh...")
    success, output, error = run_command(f"gh repo sync --branch {branch}")
    
    if success:
        print("  ✅ Successfully pushed with GitHub CLI!")
        return True
    else:
        print(f"  ❌ GitHub CLI push failed: {error}")
        return False

def try_api_push():
    """Try pushing workflows via GitHub API"""
    print("\n🔧 Method 2: Trying GitHub API push...")
    
    # Check for gh auth token
    success, token, _ = run_command("gh auth token")
    if not success or not token:
        print("  ❌ Could not get GitHub token")
        return False
    
    print("  🔑 Got authentication token")
    
    # Get repository info
    success, remote_url, _ = run_command("git remote get-url origin")
    if not success:
        print("  ❌ Could not get remote URL")
        return False
    
    # Parse owner and repo
    if "github.com" in remote_url:
        parts = remote_url.split("github.com")[-1].strip(":/").replace(".git", "").split("/")
        owner, repo = parts[-2], parts[-1]
    else:
        print("  ❌ Could not parse repository info")
        return False
    
    print(f"  📦 Repository: {owner}/{repo}")
    
    # Get current branch
    success, branch, _ = run_command("git branch --show-current")
    if not success:
        branch = "testing"
    
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("  ❌ No workflows directory found")
        return False
    
    success_count = 0
    for workflow_file in workflow_dir.glob("*.yml"):
        print(f"  📄 Uploading {workflow_file.name}...")
        
        # Read file content
        with open(workflow_file, 'rb') as f:
            content = base64.b64encode(f.read()).decode()
        
        # Create API request
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/.github/workflows/{workflow_file.name}"
        
        # Check if file exists
        check_cmd = f'curl -s -H "Authorization: token {token}" {api_url}'
        success, response, _ = run_command(check_cmd)
        
        sha = None
        if success and response:
            try:
                data = json.loads(response)
                sha = data.get('sha')
            except:
                pass
        
        # Prepare the request
        json_data = {
            "message": f"Add workflow: {workflow_file.name}\n\nAuthor: Tuhin Garai <64925748+nightcodex7@users.noreply.github.com>",
            "content": content,
            "branch": branch
        }
        
        if sha:
            json_data["sha"] = sha
        
        # Make the API request
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tf:
            json.dump(json_data, tf)
            temp_file = tf.name
        
        curl_cmd = f'curl -X PUT -H "Authorization: token {token}" -H "Accept: application/vnd.github.v3+json" -d @{temp_file} {api_url}'
        success, response, error = run_command(curl_cmd)
        
        os.unlink(temp_file)
        
        if success and "content" in response:
            print(f"    ✅ Uploaded successfully")
            success_count += 1
        else:
            print(f"    ❌ Failed to upload")
    
    if success_count > 0:
        print(f"  ✅ Successfully uploaded {success_count} workflow files!")
        return True
    else:
        print("  ❌ API upload failed")
        return False

def try_ssh_push():
    """Try converting to SSH and pushing"""
    print("\n🔧 Method 3: Trying SSH push...")
    
    # Check current remote
    success, remote_url, _ = run_command("git remote get-url origin")
    if not success:
        print("  ❌ Could not get remote URL")
        return False
    
    # If already SSH, just try pushing
    if remote_url.startswith("git@"):
        print("  📤 Already using SSH, attempting push...")
        success, _, error = run_command("git push origin HEAD")
        if success:
            print("  ✅ Successfully pushed via SSH!")
            return True
        else:
            print(f"  ❌ SSH push failed: {error}")
            return False
    
    # Convert to SSH URL
    if "github.com" in remote_url:
        parts = remote_url.split("github.com")[-1].strip(":/").replace(".git", "")
        ssh_url = f"git@github.com:{parts}.git"
        
        print(f"  🔄 Converting to SSH URL: {ssh_url}")
        
        # Temporarily change remote
        run_command(f"git remote set-url origin {ssh_url}")
        
        # Try push
        success, _, error = run_command("git push origin HEAD")
        
        # Restore original URL
        run_command(f"git remote set-url origin {remote_url}")
        
        if success:
            print("  ✅ Successfully pushed via SSH!")
            return True
        else:
            print(f"  ❌ SSH push failed: {error}")
            return False
    
    return False

def create_workflow_bundle():
    """Create a bundle of workflow files for manual upload"""
    print("\n📦 Creating workflow bundle for manual upload...")
    
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("  ❌ No workflows directory found")
        return
    
    # Create a zip file
    import zipfile
    
    bundle_name = "workflow-files.zip"
    with zipfile.ZipFile(bundle_name, 'w') as zf:
        for workflow_file in workflow_dir.glob("*.yml"):
            zf.write(workflow_file, f"workflows/{workflow_file.name}")
    
    print(f"  ✅ Created {bundle_name}")
    print("\n  📋 Manual upload instructions:")
    print("  1. Download workflow-files.zip")
    print("  2. Go to: https://github.com/nightcodex7/warp-nextdns-wireguard")
    print("  3. Navigate to .github/ directory")
    print("  4. Upload the workflows folder")

def main():
    """Main function"""
    print("🚀 Automated Workflow Push")
    print("="*60)
    print("Author: Tuhin Garai")
    print("Email: 64925748+nightcodex7@users.noreply.github.com")
    print("="*60)
    
    # Change to repository root
    repo_root = subprocess.run(["git", "rev-parse", "--show-toplevel"], 
                              capture_output=True, text=True).stdout.strip()
    if repo_root:
        os.chdir(repo_root)
    
    # Try different methods
    methods = [
        ("GitHub CLI", try_gh_push),
        ("GitHub API", try_api_push),
        ("SSH Push", try_ssh_push)
    ]
    
    for method_name, method_func in methods:
        try:
            if method_func():
                print(f"\n✅ Success! Workflows pushed using {method_name}")
                print("\n📊 Verify at: https://github.com/nightcodex7/warp-nextdns-wireguard/actions")
                return 0
        except Exception as e:
            print(f"  ❌ {method_name} error: {str(e)}")
    
    # If all methods fail, create bundle
    print("\n❌ All automated methods failed")
    create_workflow_bundle()
    
    print("\n💡 Alternative solutions:")
    print("1. Use Personal Access Token:")
    print("   git remote set-url origin https://YOUR_TOKEN@github.com/nightcodex7/warp-nextdns-wireguard.git")
    print("2. Use GitHub CLI from Windows:")
    print("   gh repo sync --branch testing")
    print("3. Upload workflow-files.zip manually via GitHub web interface")
    
    return 1

if __name__ == "__main__":
    sys.exit(main())