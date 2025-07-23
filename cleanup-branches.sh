#!/bin/bash

# Branch Cleanup Script for WARP + NextDNS Manager
# This script removes unwanted files from all branches and ensures proper structure

set -e

echo "🧹 Starting branch cleanup process..."

# Files to remove from all branches
UNWANTED_FILES=(
    "warp-nextdns-manager.spec"
    "MODERN_UI_IMPLEMENTATION_SUMMARY.md"
    ".github/workflows/pages-debug.yml"
    ".github/workflows/test-trigger.yml"
)

# Files that should only be on testing branch
TESTING_ONLY_FILES=(
    ".github/pre-commit-config.yml"
    ".github/branch-protection.yml"
)

# Files that should be on both branches
COMMON_FILES=(
    "README.md"
    "LICENSE"
    "CHANGELOG.md"
    "SECURITY.md"
    "CODE_OF_CONDUCT.md"
    "CONTRIBUTING.md"
    "requirements.txt"
    "setup.py"
    "VERSION"
    "main.py"
    "cli.py"
    "core.py"
    "build.py"
    "deploy.py"
    "utils/"
    "tests/"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to clean unwanted files from a branch
clean_branch() {
    local branch=$1
    print_status "Cleaning branch: $branch"
    
    # Checkout branch
    git checkout "$branch" 2>/dev/null || {
        print_warning "Branch $branch does not exist locally, skipping..."
        return 0
    }
    
    # Remove unwanted files
    local removed_files=()
    for file in "${UNWANTED_FILES[@]}"; do
        if [ -f "$file" ]; then
            print_status "Removing $file from $branch"
            git rm "$file" 2>/dev/null && removed_files+=("$file") || print_warning "Could not remove $file"
        fi
    done
    
    # Commit changes if any files were removed
    if [ ${#removed_files[@]} -gt 0 ]; then
        git config user.name "github-actions[bot]"
        git config user.email "github-actions[bot]@users.noreply.github.com"
        git commit -m "cleanup: remove unwanted files from $branch branch" || print_warning "No changes to commit"
        print_success "Removed ${#removed_files[@]} files from $branch"
    else
        print_status "No unwanted files found on $branch"
    fi
}

# Function to validate branch structure
validate_branch() {
    local branch=$1
    print_status "Validating branch: $branch"
    
    # Checkout branch
    git checkout "$branch" 2>/dev/null || {
        print_warning "Branch $branch does not exist locally, skipping validation..."
        return 0
    }
    
    # Check for required files
    local missing_files=()
    for file in "${COMMON_FILES[@]}"; do
        if [ ! -e "$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        print_error "Missing required files on $branch: ${missing_files[*]}"
        return 1
    else
        print_success "All required files present on $branch"
    fi
    
    # Check for unwanted files
    local unwanted_found=()
    for file in "${UNWANTED_FILES[@]}"; do
        if [ -f "$file" ]; then
            unwanted_found+=("$file")
        fi
    done
    
    if [ ${#unwanted_found[@]} -gt 0 ]; then
        print_warning "Unwanted files still present on $branch: ${unwanted_found[*]}"
    else
        print_success "No unwanted files found on $branch"
    fi
}

# Main cleanup process
main() {
    print_status "Starting comprehensive branch cleanup..."
    
    # Get current branch
    current_branch=$(git branch --show-current)
    print_status "Current branch: $current_branch"
    
    # Clean main branch
    print_status "=== Cleaning main branch ==="
    clean_branch "main"
    validate_branch "main"
    
    # Clean testing branch
    print_status "=== Cleaning testing branch ==="
    clean_branch "testing"
    validate_branch "testing"
    
    # Clean feature branch if it exists
    if git show-ref --verify --quiet refs/heads/refactor/v2.0.0-enhancement; then
        print_status "=== Cleaning refactor/v2.0.0-enhancement branch ==="
        clean_branch "refactor/v2.0.0-enhancement"
        validate_branch "refactor/v2.0.0-enhancement"
    fi
    
    # Return to original branch
    git checkout "$current_branch"
    
    print_success "Branch cleanup completed!"
    print_status "Next steps:"
    print_status "1. Review changes: git status"
    print_status "2. Push changes to remote: git push origin --all"
    print_status "3. Run promotion workflow to move stable changes to main"
}

# Run main function
main "$@" 