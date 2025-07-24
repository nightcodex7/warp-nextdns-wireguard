# Versioning Rules

## Unified Versioning System

This project uses a **unified versioning system** where:

1. **Single Version Source**: The `VERSION` file in the root directory is the only source of truth
2. **No File-Specific Versions**: CSS, JS, and HTML files do not have individual version numbers
3. **Changelog Only**: Version history is tracked only in `CHANGELOG.md`

## Rules

### ✅ Allowed
- `VERSION` file in root (e.g., `2.1.0`)
- Version references in `CHANGELOG.md`
- Version in `setup.py` and `pyproject.toml` (read from VERSION file)

### ❌ Not Allowed
- `styles.css?v=1.0.0` → Use `styles.css`
- `script.js?version=2.0` → Use `script.js`
- `file-v1.html` → Use `file.html`
- Multiple VERSION files

## Branch Structure

### Master Branch
- **Purpose**: Complete repository tracking
- **Contains**: All files from both main and testing branches
- **Use Case**: For developers who need the complete codebase
- **Auto-sync**: Automatically synced when main or testing updates

### Main Branch
- **Purpose**: Production-ready code only
- **Contains**: Source code without docs/
- **Use Case**: Production deployments

### Testing Branch
- **Purpose**: Development and documentation
- **Contains**: Everything including docs/
- **Use Case**: Development and GitHub Pages

## Enforcement

These rules are enforced by:
1. Pre-commit hooks
2. GitHub Actions workflows
3. Branch protection rules

## Cache Busting

For production deployments, use build tools or server configuration for cache busting instead of file versioning:
- Use content hashes in build process
- Configure proper HTTP cache headers
- Use service workers for advanced caching