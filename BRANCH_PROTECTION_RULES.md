# Branch Protection Rules

This document outlines the branch protection rules and file organization standards for the WARP + NextDNS Manager project.

## Branch Strategy

The project uses a three-branch strategy with priority hierarchy:

```
master (priority: complete repository)
├── main (production code only)
└── testing (development + docs)
```

### Branch Priority Order
1. **Local changes** (always takes precedence)
2. **Master branch** (complete mirror, updated from local first)
3. **Current working branch** (main or testing)
4. **Other branches** (merged with lower priority)

## File Organization Standards

### Directory Structure

```
warp-nextdns-wireguard/
├── src/                    # Source code (REQUIRED)
│   ├── __init__.py
│   ├── cli.py             # CLI interface
│   ├── core.py            # Core functionality
│   └── main.py            # Entry point
├── scripts/               # Build and deployment scripts (REQUIRED)
│   ├── __init__.py
│   ├── build.py
│   ├── deploy.py
│   └── sync-master-local.py  # Local master sync tool
├── utils/                 # Utility modules (REQUIRED)
│   └── *.py
├── tests/                 # Test files (REQUIRED)
│   └── test_*.py
├── docs/                  # Documentation (testing/master only)
│   ├── *.html
│   ├── *.css
│   └── favicon.*
├── .github/               # GitHub workflows and configs (REQUIRED)
│   └── workflows/
├── README.md              # Project documentation (REQUIRED)
├── LICENSE                # License file (REQUIRED)
├── CHANGELOG.md           # Version history (REQUIRED)
├── requirements.txt       # Python dependencies (REQUIRED)
├── setup.py              # Package setup (REQUIRED)
├── pyproject.toml        # Modern Python packaging (REQUIRED)
└── VERSION               # Version file (REQUIRED)
```

### Files NOT Allowed (Permanent Ban)

The following files/patterns are **permanently banned** from ALL branches:

1. **Summary Files**
   - `*_SUMMARY.md`
   - `*_summary.md`
   - `*SUMMARY*` (except SETUP_SUMMARY.md if critical)
   - Any file with "summary" in the name

2. **Temporary Files**
   - `*.tmp`, `*.temp`
   - `*.bak`, `*~`
   - `.DS_Store`, `Thumbs.db`
   - `*.pyc`, `__pycache__/`

3. **Version-Specific Files**
   - `*?v=*` (URL parameters)
   - `*_v[0-9]*` (version in filename)
   - `*-v[0-9]*` (version in filename)
   - Multiple VERSION files

## Branch-Specific Rules

### Master Branch (Complete Mirror)
**Purpose**: Complete repository with all files
**Priority**: Highest - always updated from local first
**Contains**: Everything from main + testing
**Special Rules**:
- Auto-synced on every push to main/testing
- Local changes always take precedence
- Serves as single source for developers
- No direct commits (sync only)

### Main Branch (Production)
**Allowed:**
- Source code (`src/`, `utils/`, `scripts/`)
- Tests (`tests/`)
- Essential documentation (README.md, LICENSE, etc.)
- Production workflows only:
  - `main-release.yml`
  - `promote-to-main.yml`
  - `branch-protection-check.yml`
  - `branch-sync.yml`

**NOT Allowed:**
- `docs/` directory
- Development workflows
- Summary files
- Temporary files
- Test/development configurations

### Testing Branch (Development)
**Allowed:**
- Everything from main branch
- `docs/` directory for GitHub Pages
- All workflows
- Development tools
- Documentation files

**NOT Allowed:**
- Summary files
- Temporary files
- File-specific versioning

## Enforcement Mechanisms

### 1. Local Sync Script
```bash
# Sync master locally with priority
python scripts/sync-master-local.py

# Sync and push
python scripts/sync-master-local.py --push
```

### 2. Pre-commit Hook
The pre-commit hook enforces:
- No docs/ on main branch
- No summary files anywhere
- No temporary files
- Proper directory structure

### 3. GitHub Actions

#### Branch Sync Workflow
- Triggers on push to main/testing
- Prioritizes branch that triggered sync
- Handles merge conflicts automatically
- Verifies directory structure
- Cleans unwanted files

#### Branch Protection Check
- Validates file rules on every push
- Blocks prohibited files
- Ensures directory structure
- Enforces versioning rules

### 4. .gitignore Rules
Comprehensive rules including:
```
*_SUMMARY.md
*_summary.md
*.tmp
*.temp
*?v=*
docs/  # On main branch only via hook
```

## Merge Conflict Resolution

### Priority Order:
1. **Current working branch** (highest priority)
2. **Master branch** (when syncing)
3. **Other branches** (lowest priority)

### Strategies:
- `--strategy=recursive --strategy-option=theirs` for priority merges
- `--strategy=recursive --strategy-option=ours` for lower priority
- Automatic cleanup after merge

## File Validation Rules

### Required Files/Directories:
All branches must have:
- `src/` with main.py, cli.py, core.py
- `scripts/` with build.py, deploy.py
- `utils/` directory
- `tests/` directory
- `.github/workflows/`
- Core documentation files

### Automatic Cleanup:
The system automatically removes:
- Summary files
- Temporary files
- Version-specific files
- Empty directories (except required ones)

## Best Practices

### For Developers:
1. Always sync master locally first:
   ```bash
   python scripts/sync-master-local.py
   ```

2. Work on appropriate branch:
   - `testing` for new features
   - `main` for hotfixes only

3. Let automation handle branch syncing

### For CI/CD:
1. Never skip branch protection checks
2. Always verify directory structure
3. Clean up after every merge
4. Log all sync operations

## Troubleshooting

### Master Not Updating:
```bash
# Force local sync
git checkout master
git fetch --all
git reset --hard origin/master
python scripts/sync-master-local.py --push
```

### Merge Conflicts:
```bash
# Reset to clean state
git checkout testing
git pull origin testing
python scripts/sync-master-local.py
```

### File Rule Violations:
1. Check the error message
2. Remove prohibited files
3. Re-run the check
4. Commit clean state

## Summary

- **Master branch** = Complete repo, local priority
- **No summary files** = Permanently banned
- **Unified versioning** = VERSION file only
- **Automatic sync** = On every push
- **Local first** = Always prioritize local changes