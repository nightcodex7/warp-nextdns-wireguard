# Branch Management Guide

## Branch Structure

```
master (complete)
├── main (production)
└── testing (development + docs)
```

### 🌟 Master Branch
- **Purpose**: Complete repository mirror
- **Contains**: Everything from main + testing
- **Auto-sync**: Via GitHub Actions on push to main/testing
- **Use**: Clone this for complete codebase

### 🚀 Main Branch  
- **Purpose**: Production-ready code
- **Contains**: Source code only (no docs/)
- **Protected**: Strict rules enforced
- **Deploy**: Use for production releases

### 🧪 Testing Branch
- **Purpose**: Development and documentation
- **Contains**: All code + docs/ for GitHub Pages
- **Features**: All new development happens here
- **Pages**: GitHub Pages serves from testing/docs/

## Workflow

### For Developers

```bash
# Get complete codebase
git clone -b master <repo-url>

# Or work on specific branch
git clone -b testing <repo-url>  # For development
git clone -b main <repo-url>     # For production only
```

### Development Flow

1. **Feature Development**
   ```bash
   git checkout testing
   git pull origin testing
   # Make changes
   git add .
   git commit -m "feat: description"
   git push origin testing
   ```

2. **Production Release**
   - Use the promote-to-main workflow
   - Automated via GitHub Actions
   - Removes docs/ and dev files automatically

3. **Master Sync**
   - Automatic on push to main/testing
   - Manual trigger: Actions → Branch Sync → Run workflow

## Branch Rules

### Enforced Automatically

1. **No docs/ on main branch**
2. **No summary files anywhere**
3. **No file-specific versioning**
4. **Proper directory structure**
5. **Clean commit history**

### File Organization

```
├── src/           # Source code
├── scripts/       # Build scripts  
├── utils/         # Utilities
├── tests/         # Tests
├── docs/          # Website (testing only)
├── .github/       # Workflows
└── VERSION        # Single version source
```

## Best Practices

### ✅ DO
- Use testing branch for all development
- Keep commits atomic and well-described
- Update CHANGELOG.md with version changes
- Test locally before pushing
- Use conventional commit messages

### ❌ DON'T
- Push docs/ to main branch
- Create summary files
- Add version numbers to filenames
- Commit temporary files
- Force push without coordination

## Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code restructuring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

## Troubleshooting

### Merge Conflicts
```bash
# If master sync fails
git checkout master
git pull origin master
git merge origin/main --strategy-option=theirs
git merge origin/testing --strategy-option=theirs
git push origin master
```

### Wrong Branch
```bash
# If you accidentally commit to wrong branch
git stash
git checkout correct-branch
git stash pop
```

### Clean State
```bash
# Reset to clean state
git clean -fd
git reset --hard origin/branch-name
```

## Automation

### GitHub Actions
- **Branch Protection Check**: Validates file rules
- **Branch Sync**: Keeps master updated
- **Promote to Main**: Moves code to production
- **Docs Deploy**: Updates GitHub Pages

### Pre-commit Hooks
- Prevents docs/ on main
- Blocks summary files
- Validates structure

## Quick Reference

| Branch | Purpose | Contains | Push Rights |
|--------|---------|----------|-------------|
| master | Complete mirror | Everything | Auto-sync only |
| main | Production | Code only | Protected |
| testing | Development | Code + Docs | Developers |

## Questions?

Check:
1. VERSIONING_RULES.md
2. BRANCH_PROTECTION_RULES.md
3. GitHub Actions logs
4. Issue tracker