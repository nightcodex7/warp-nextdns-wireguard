# Branch Protection Rules

This document outlines the branch protection rules implemented for the WARP + NextDNS Manager project.

## Overview

The project uses a two-branch strategy:
- **`main`** - Production-ready code only
- **`testing`** - Development, documentation, and all features

## Branch-Specific File Rules

### Main Branch

The `main` branch is restricted to production code only. The following files/directories are **NOT ALLOWED** on main:

1. **Documentation Website** (`docs/`)
   - GitHub Pages is configured to serve from the `testing` branch
   - All documentation updates should be made on `testing`

2. **Development Workflows** (`.github/workflows/`)
   - Only allowed workflows on main:
     - `main-release.yml`
     - `promote-to-main.yml`
     - `branch-protection-check.yml`
   - All other workflows should remain on `testing`

3. **Development Configuration Files**
   - `.github/pre-commit-config.yml`
   - `.github/branch-protection.yml`
   - Branch management scripts (`setup-branch-protection.py`, `cleanup-branch-files.py`)

### Testing Branch

The `testing` branch can contain all files, including:
- Documentation (`docs/`)
- All GitHub workflows
- Development configuration files
- Test files
- Branch management scripts

## Protection Mechanisms

### 1. Pre-commit Hook (Local)

A pre-commit hook is installed in `.git/hooks/pre-commit` that:
- Automatically checks files being committed
- Blocks commits containing prohibited files on `main`
- Provides clear error messages

To temporarily bypass (use with caution):
```bash
git commit --no-verify
```

### 2. GitHub Workflow (Remote)

The `branch-protection-check.yml` workflow:
- Runs on all pushes and PRs to `main`
- Validates that no prohibited files exist
- Fails the CI if violations are found

### 3. Branch Cleanup Scripts

Two scripts help maintain branch hygiene:

1. **`setup-branch-protection.py`** (testing branch only)
   - Sets up pre-commit hooks
   - Creates branch-specific .gitignore files
   - Installs protection mechanisms

2. **`cleanup-branch-files.py`** (testing branch only)
   - Removes prohibited files from branches
   - Run this after switching branches to ensure compliance

## GitHub Pages Configuration

GitHub Pages is configured to:
- Source: `testing` branch
- Folder: `/docs`
- URL: https://[username].github.io/[repository]/

This ensures documentation is always served from the testing branch while keeping main clean.

## Workflow

1. **Development**: All work happens on `testing`
2. **Documentation**: Update docs on `testing`, changes are automatically deployed
3. **Production Release**: Use the promote-to-main workflow to move stable code to `main`
4. **Main Branch**: Automatically cleaned of non-production files

## Enforcement

The protection rules are enforced at multiple levels:
1. **Local**: Pre-commit hooks prevent accidental commits
2. **Remote**: GitHub workflows block prohibited files
3. **Automated**: Cleanup scripts maintain branch integrity

## Troubleshooting

If you accidentally commit prohibited files to main:
1. Use `git reset` to undo the commit locally
2. Run `cleanup-branch-files.py` to remove prohibited files
3. Commit the cleanup changes
4. Force push if necessary (be careful with this)

## Summary

- `main` = Production code only (no docs/, limited workflows)
- `testing` = Everything (development, docs, all workflows)
- GitHub Pages serves from `testing/docs/`
- Multiple protection layers ensure compliance