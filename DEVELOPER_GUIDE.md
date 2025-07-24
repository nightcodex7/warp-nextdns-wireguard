# Developer Guide - Branch File Management

## 🎯 Quick Reference

| Branch | Purpose | What to Upload | What NOT to Upload |
|--------|---------|----------------|-------------------|
| **main** | Production | Source code only | docs/, dev workflows, summaries |
| **testing** | Development | Everything except summaries | *_SUMMARY.md files |
| **master** | Complete mirror | Don't upload directly | Auto-synced only |

## 📁 Detailed File Rules by Branch

### 🚀 Main Branch (Production)

**✅ ALLOWED:**
```
src/
├── __init__.py
├── main.py
├── cli.py
└── core.py

scripts/
├── __init__.py
├── build.py
├── deploy.py
└── sync-master-local.py

utils/
└── *.py

tests/
└── test_*.py

.github/workflows/
├── main-release.yml
├── promote-to-main.yml
├── branch-protection-check.yml
└── branch-sync.yml

Root files:
- README.md
- LICENSE
- CHANGELOG.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- CONTRIBUTING.md
- VERSION
- requirements.txt
- setup.py
- pyproject.toml
- .gitignore
```

**❌ FORBIDDEN:**
- `docs/` directory (any documentation website files)
- Development workflows (ci.yml, test.yml, etc.)
- Summary files (*_SUMMARY.md, *_summary.md)
- Temporary files (*.tmp, *.temp, *.bak)
- Version-specific files (style.css?v=1.0)
- Development configs (.github/pre-commit-config.yml)
- Implementation scripts (implement_*.py, create_*.py)

### 🧪 Testing Branch (Development)

**✅ ALLOWED:**
- Everything from main branch
- `docs/` directory with all website files
- All GitHub workflows
- Development tools and scripts
- Documentation files
- Test files and fixtures

**❌ FORBIDDEN:**
- Summary files (*_SUMMARY.md, *_summary.md)
- Temporary files (*.tmp, *.temp, *.bak, *~)
- OS-specific files (.DS_Store, Thumbs.db)
- Cache files (__pycache__, *.pyc)
- Version parameters in filenames

### 🌟 Master Branch (Complete Mirror)

**⚠️ IMPORTANT:** Never commit directly to master!
- Master is auto-synced from main + testing
- Use `python scripts/sync-master-local.py` for local sync
- All files from both branches are included
- Automatic cleanup of forbidden files

## 🛠️ Common Tasks

### 1. Starting New Development

```bash
# Always start from testing branch
git checkout testing
git pull origin testing

# Create your feature
# ... make changes ...

# Check for violations before commit
python scripts/enforce-branch-structure.py

# Commit (pre-commit hook will validate)
git add .
git commit -m "feat: your feature"
git push origin testing
```

### 2. Pushing Documentation Changes

```bash
# Documentation goes to testing only
git checkout testing
cd docs/
# ... edit HTML/CSS files ...

# Remove any versioning
# BAD: <link href="styles.css?v=2.0">
# GOOD: <link href="styles.css">

git add docs/
git commit -m "docs: update website"
git push origin testing
```

### 3. Production Release

```bash
# Use the promote-to-main workflow
# This automatically removes docs/ and dev files
# Never manually copy files to main!
```

### 4. Syncing Master Branch

```bash
# Local sync (recommended)
python scripts/sync-master-local.py

# Sync and push
python scripts/sync-master-local.py --push
```

## 🚨 Error Handling

### Error: "Branch 'feature/xyz' is not allowed!"

**Solution:**
```bash
# Switch to testing branch
git checkout testing

# Cherry-pick your commits
git cherry-pick <commit-hash>

# Delete the unauthorized branch
git branch -D feature/xyz
```

### Error: "docs/ directory found on main branch!"

**Solution:**
```bash
git checkout main
git rm -rf docs/
git commit -m "fix: remove docs from main"
git push origin main
```

### Error: "Summary files found"

**Solution:**
```bash
# Find all summary files
find . -name "*_SUMMARY.md" -o -name "*_summary.md"

# Remove them
find . -name "*_SUMMARY.md" -o -name "*_summary.md" | xargs rm -f

git add -A
git commit -m "fix: remove summary files"
```

### Error: "Files with version numbers found"

**Solution:**
```bash
# In HTML files, remove version parameters
# Change: href="styles.css?v=1.0"
# To: href="styles.css"

# Check VERSION file exists and contains only version
cat VERSION  # Should show: 2.1.0
```

### Error: "Required directory 'src' not found!"

**Solution:**
```bash
# The code must follow the structure
mkdir -p src scripts utils tests
git mv main.py cli.py core.py src/
git mv build.py deploy.py scripts/
git commit -m "fix: reorganize to standard structure"
```

### Error: Push rejected (workflow permissions)

**Solution:**
```bash
# For testing branch, this is usually OK
# For main branch, use promote-to-main workflow
# For master branch, use sync script
```

## 📋 Pre-Commit Checklist

Before every commit, ensure:

- [ ] On correct branch (main/testing only)
- [ ] No summary files (*_SUMMARY.md)
- [ ] No temporary files (*.tmp, *.bak)
- [ ] No version parameters in filenames
- [ ] If main branch: no docs/ directory
- [ ] Required directories exist (src/, scripts/, utils/, tests/)
- [ ] Core files in correct locations

## 🔧 Useful Commands

```bash
# Check branch compliance
python scripts/enforce-branch-structure.py

# Fix violations automatically
python scripts/enforce-branch-structure.py --fix

# Sync master branch locally
python scripts/sync-master-local.py

# Check current branch
git branch --show-current

# See what will be committed
git status

# Test pre-commit hook
git commit --dry-run
```

## 🚫 Never Do This

1. **Never create new branches** - Only use main, testing, master
2. **Never commit directly to master** - It's auto-synced only
3. **Never force push without coordination**
4. **Never skip pre-commit hooks** (--no-verify)
5. **Never add version numbers to filenames**
6. **Never commit summary files**
7. **Never put docs/ on main branch**

## 💡 Pro Tips

1. **Use testing for everything** - It's the safest branch
2. **Let automation handle transfers** - Don't manually move files between branches
3. **Check before pushing** - Run enforce-branch-structure.py
4. **Keep commits atomic** - One feature per commit
5. **Write clear commit messages** - Follow conventional commits

## 🆘 Getting Help

If you encounter issues:

1. Check this guide first
2. Run `python scripts/enforce-branch-structure.py --fix`
3. Check GitHub Actions logs
4. Review BRANCH_PROTECTION_RULES.md
5. Ask in issues if still stuck

Remember: The system is designed to prevent mistakes. If it blocks you, there's usually a good reason!