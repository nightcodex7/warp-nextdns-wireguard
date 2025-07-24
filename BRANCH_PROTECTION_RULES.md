# Branch Protection Rules

This document outlines the branch protection rules and file organization standards for the WARP + NextDNS Manager project.

## Branch Strategy

The project uses a two-branch strategy:
- **`main`** - Production-ready code only
- **`testing`** - Development, documentation, and all features

## File Organization Standards

### Directory Structure

```
warp-nextdns-wireguard/
├── src/                    # Source code
│   ├── __init__.py
│   ├── cli.py             # CLI interface
│   ├── core.py            # Core functionality
│   └── main.py            # Entry point
├── scripts/               # Build and deployment scripts
│   ├── __init__.py
│   ├── build.py
│   └── deploy.py
├── utils/                 # Utility modules
│   └── *.py
├── tests/                 # Test files
│   └── test_*.py
├── docs/                  # Documentation (testing branch only)
│   ├── *.html
│   ├── *.css
│   └── favicon.*
├── .github/               # GitHub workflows and configs
│   └── workflows/
├── README.md              # Project documentation
├── LICENSE                # License file
├── CHANGELOG.md           # Version history
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
├── pyproject.toml        # Modern Python packaging
└── VERSION               # Version file
```

### Files NOT Allowed

The following files/patterns are **permanently banned** from the repository:

1. **Summary Files**
   - `*_SUMMARY.md`
   - `*_summary.md`
   - Any file with "summary" in the name

2. **Temporary Files**
   - `*.tmp`, `*.temp`
   - `*.bak`, `*~`
   - `.DS_Store`, `Thumbs.db`

3. **Branch-Specific on Main**
   - `docs/` directory (testing branch only)
   - Development workflows
   - Branch management scripts

## Branch-Specific Rules

### Main Branch

**Allowed:**
- Source code (`src/`, `utils/`, `scripts/`)
- Tests (`tests/`)
- Essential documentation (README.md, LICENSE, etc.)
- Production workflows:
  - `main-release.yml`
  - `promote-to-main.yml`
  - `branch-protection-check.yml`

**NOT Allowed:**
- `docs/` directory
- Development workflows
- Summary files
- Temporary files

### Testing Branch

**Allowed:**
- Everything from main branch
- `docs/` directory for GitHub Pages
- All workflows
- Development tools

## Enforcement

### 1. .gitignore Rules

The `.gitignore` file includes:
```
*_SUMMARY.md
*_summary.md
*.tmp
*.temp
docs/  # On main branch only
```

### 2. Pre-commit Hook

A pre-commit hook prevents:
- Pushing docs/ to main
- Committing summary files
- Committing temporary files

### 3. GitHub Workflow

The `branch-protection-check.yml` workflow validates:
- No prohibited files on main
- Proper directory structure
- File naming conventions

## File Naming Conventions

1. **Python Files**: `lowercase_with_underscores.py`
2. **Documentation**: `UPPERCASE.md` for important docs
3. **Config Files**: Standard names (`.gitignore`, `pyproject.toml`)
4. **No Spaces**: Use hyphens or underscores

## Import Standards

With the new structure:
```python
# In src/main.py
from src.cli import CLI
from src.core import Core

# In src/cli.py
from .core import Core  # Relative import within package
```

## Summary

- Keep the codebase clean and organized
- No summary files ever
- Documentation only on testing branch
- Follow Python packaging standards
- Use proper import statements