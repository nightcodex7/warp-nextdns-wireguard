# Documentation Deployment Guide

This guide explains the rules and procedures for deploying documentation to GitHub Pages from the `testing` branch.

## 🚀 Deployment Rules

### Branch Restrictions
- **Only the `testing` branch** can deploy to GitHub Pages
- **Only changes to the `docs/` folder** trigger automatic deployment
- **Non-documentation changes** are blocked from the testing branch

### Allowed Changes
✅ **Allowed on testing branch:**
- Files in `docs/` directory
- Documentation workflow files
- README.md updates
- Branch protection configurations

❌ **Blocked on testing branch:**
- Source code changes (`.py` files)
- Configuration files outside docs
- Binary files
- Large files (>1MB)

## 📁 Required Documentation Files

The following files must be present in the `docs/` directory:

```
docs/
├── .nojekyll                    # Required: Disables Jekyll processing
├── index.html                   # Required: Main landing page
├── installation.html            # Required: Installation guide
├── styles.css                   # Required: Main stylesheet
├── test.html                    # Optional: Test page
├── validate.html                # Optional: Validation page
└── README.md                    # Optional: Documentation index
```

## 🔧 Deployment Workflow

### Automatic Deployment
1. **Push changes** to `docs/` folder on `testing` branch
2. **Workflow triggers** automatically
3. **Validation runs** to check documentation structure
4. **Deployment proceeds** if validation passes
5. **Site updates** at `https://nightcodex7.github.io/warp-nextdns-wireguard/`

### Manual Deployment
1. Go to **Actions** tab in GitHub
2. Select **"Deploy Documentation to GitHub Pages"**
3. Click **"Run workflow"**
4. Optionally check **"Force deploy even if no docs changes"**
5. Click **"Run workflow"**

## ✅ Validation Checks

The deployment workflow performs these checks:

### File Structure Validation
- ✅ Required files present (`index.html`, `installation.html`, `styles.css`, `.nojekyll`)
- ✅ No missing critical files
- ✅ Proper directory structure

### HTML Validation
- ✅ Valid HTML5 structure
- ✅ Proper DOCTYPE declaration
- ✅ Closing tags present
- ✅ Valid syntax

### Content Validation
- ✅ Internal links working
- ✅ CSS file accessible
- ✅ Navigation consistency
- ✅ Responsive design elements

## 🚫 Common Blocked Actions

### What Gets Blocked
```bash
# ❌ These will be blocked on testing branch:
git add cli.py                    # Source code
git add requirements.txt          # Dependencies
git add .github/workflows/ci.yml  # Non-docs workflow
git add utils/                    # Source directories
```

### What's Allowed
```bash
# ✅ These are allowed on testing branch:
git add docs/index.html           # Documentation
git add docs/styles.css           # Styles
git add docs/new-page.html        # New docs
git add README.md                 # Project README
```

## 🔄 Workflow Process

### 1. Pre-commit Checks
- Documentation-only validation
- File structure verification
- HTML syntax checking
- Link validation

### 2. Push Validation
- Branch restriction enforcement
- Path-based triggering
- Change detection

### 3. Deployment Process
- Documentation validation
- Structure verification
- Artifact creation
- GitHub Pages deployment

### 4. Post-deployment
- URL generation
- Status reporting
- Error handling

## 🛠️ Troubleshooting

### Deployment Fails
1. **Check required files** are present in `docs/`
2. **Verify HTML syntax** is valid
3. **Ensure only docs changes** were made
4. **Check workflow logs** for specific errors

### Validation Errors
1. **Missing files**: Add required documentation files
2. **HTML errors**: Fix syntax issues
3. **Structure issues**: Ensure proper directory layout
4. **Link errors**: Fix broken internal links

### Force Deployment
If you need to force deployment:
1. Go to **Actions** → **Deploy Documentation to GitHub Pages**
2. Click **"Run workflow"**
3. Check **"Force deploy even if no docs changes"**
4. Click **"Run workflow"**

## 📋 Best Practices

### Documentation Structure
- Keep all documentation in `docs/` folder
- Use consistent naming conventions
- Maintain proper HTML structure
- Include navigation links

### Content Guidelines
- Write clear, concise content
- Use proper HTML semantics
- Include meta tags for SEO
- Test responsive design

### Deployment Process
- Test changes locally first
- Use descriptive commit messages
- Review workflow logs
- Verify site functionality after deployment

## 🔗 Useful Links

- **Site URL**: https://nightcodex7.github.io/warp-nextdns-wireguard/
- **GitHub Repository**: https://github.com/nightcodex7/warp-nextdns-wireguard
- **Actions**: https://github.com/nightcodex7/warp-nextdns-wireguard/actions
- **Issues**: https://github.com/nightcodex7/warp-nextdns-wireguard/issues

---

**Remember**: The `testing` branch is dedicated to documentation deployment. Keep source code changes on other branches! 