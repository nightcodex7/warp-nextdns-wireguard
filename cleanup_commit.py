#!/usr/bin/env python3
"""
Script to commit and push cleanup changes
"""

import subprocess
import sys

def run_command(cmd):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"Command: {cmd}")
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Exception: {e}")
        return False

def main():
    print("🧹 Committing cleanup changes...")
    
    # Add all changes
    success = run_command("git add -A")
    if not success:
        print("❌ Failed to add files")
        return 1
    
    # Commit the changes
    success = run_command('git commit -m "cleanup: remove unnecessary scripts and redundant setup.py file"')
    if not success:
        print("❌ Failed to commit changes")
        return 1
    
    # Push to testing branch
    success = run_command("git push origin testing")
    if not success:
        print("❌ Failed to push changes")
        return 1
    
    print("✅ Successfully pushed cleanup changes!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 