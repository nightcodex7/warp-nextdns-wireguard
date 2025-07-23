# Branching Strategy and Release Management

## 🌿 Branch Structure

### **Main Branches**
- **`main`**: Production-ready, stable releases only
- **`testing`**: Development and testing environment
- **`refactor/v2.0.0-enhancement`**: Feature development branch

### **Branch Purposes**

#### **`testing` Branch**
- **Purpose**: Development, testing, and documentation updates
- **Content**: All changes during development cycle
- **Deployment**: GitHub Pages (static website)
- **Allowed Changes**:
  - ✅ Source code development
  - ✅ Documentation updates (`docs/` folder)
  - ✅ Configuration changes
  - ✅ Test files and utilities
  - ✅ GitHub Actions workflows
  - ✅ Build scripts

#### **`main` Branch**
- **Purpose**: Stable production releases
- **Content**: Only stable, tested, and approved changes
- **Deployment**: Release artifacts and documentation
- **Allowed Changes**:
  - ✅ Stable source code releases
  - ✅ Production documentation
  - ✅ Release notes and changelog
  - ✅ Version updates
  - ❌ No development files
  - ❌ No temporary or test files

## 🔄 Development Workflow

### **1. Development Phase (testing branch)**
```bash
# Start development on testing branch
git checkout testing
git pull origin testing

# Make changes (code, docs, tests, etc.)
git add .
git commit -m "feat: add new feature"
git push origin testing
```

### **2. Testing and Validation**
- Automated tests run on `testing` branch
- Documentation updates trigger GitHub Pages deployment
- Manual testing and validation
- Code review and approval

### **3. Release Preparation**
```bash
# Create release branch from testing
git checkout testing
git checkout -b release/v1.2.0
git push origin release/v1.2.0

# Final testing and validation
# Update version numbers
# Update changelog
```

### **4. Production Release (main branch)**
```bash
# Merge stable release to main
git checkout main
git merge release/v1.2.0
git tag v1.2.0
git push origin main --tags

# Clean up release branch
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

## 📁 File Management Rules

### **Files Allowed on Both Branches**
- `README.md` - Project documentation
- `LICENSE` - License file
- `CHANGELOG.md` - Release history
- `SECURITY.md` - Security policy
- `CODE_OF_CONDUCT.md` - Community guidelines
- `CONTRIBUTING.md` - Contribution guidelines
- `requirements.txt` - Python dependencies
- `setup.py` - Package configuration
- `VERSION` - Version tracking

### **Files Only on `testing` Branch**
- `warp-nextdns-manager.spec` - PyInstaller spec (build artifact)
- `MODERN_UI_IMPLEMENTATION_SUMMARY.md` - Development notes
- `.github/workflows/pages-debug.yml` - Debug workflows
- `.github/workflows/test-trigger.yml` - Test workflows
- `.github/pre-commit-config.yml` - Development hooks
- `.github/branch-protection.yml` - Development rules

### **Files Only on `main` Branch**
- Release artifacts (generated during CI/CD)
- Production documentation only
- Stable configuration files

## 🚀 GitHub Pages Configuration

### **Static Website Setup**
- **Source**: `testing` branch
- **Folder**: `/docs` directory
- **Configuration**: `.nojekyll` file (disables Jekyll processing)
- **URL**: https://nightcodex7.github.io/warp-nextdns-wireguard/

### **Required Files in `/docs`**
- `index.html` - Main landing page
- `installation.html` - Installation guide
- `styles.css` - Main stylesheet
- `.nojekyll` - Disable Jekyll processing
- `test.html` - Test page
- `validate.html` - Validation page
- `README.md` - Documentation index
- `DEPLOYMENT_GUIDE.md` - Deployment guide

## 🔧 Automated Workflows

### **Testing Branch Workflows**
1. **Documentation Deployment** (`docs-deploy.yml`)
   - Triggers on `docs/` changes
   - Validates HTML/CSS
   - Deploys to GitHub Pages

2. **CI/CD Pipeline** (`ci.yml`)
   - Runs tests
   - Validates code quality
   - Builds artifacts

3. **Debug Workflows** (various debug files)
   - Development and testing tools

### **Main Branch Workflows**
1. **Release Pipeline** (`release.yml`)
   - Creates release artifacts
   - Updates documentation
   - Publishes to PyPI

2. **Production CI** (`ci-simple.yml`)
   - Minimal validation
   - Security checks

## 🧹 File Cleanup Strategy

### **Files to Remove from All Branches**
- `warp-nextdns-manager.spec` - Build artifact (should be generated)
- `MODERN_UI_IMPLEMENTATION_SUMMARY.md` - Development notes
- Debug workflow files (keep only essential ones)
- Temporary test files
- Build artifacts and cache files

### **Cleanup Process**
```bash
# Remove unwanted files
git rm warp-nextdns-manager.spec
git rm MODERN_UI_IMPLEMENTATION_SUMMARY.md
git rm .github/workflows/pages-debug.yml
git rm .github/workflows/test-trigger.yml

# Commit cleanup
git commit -m "cleanup: remove development and build artifacts"

# Push to testing
git push origin testing

# After testing, merge to main
git checkout main
git merge testing
git push origin main
```

## 📋 Release Checklist

### **Before Merging to Main**
- [ ] All tests pass on `testing` branch
- [ ] Documentation is up to date
- [ ] Version numbers are updated
- [ ] Changelog is updated
- [ ] Security review completed
- [ ] Performance testing passed
- [ ] Code review approved

### **After Merging to Main**
- [ ] Create and push git tag
- [ ] Verify GitHub Pages deployment
- [ ] Update release notes
- [ ] Notify stakeholders
- [ ] Monitor for issues

## 🛡️ Branch Protection

### **Testing Branch Protection**
- Require pull request reviews
- Require status checks to pass
- Restrict force pushes
- Require conversation resolution

### **Main Branch Protection**
- Require pull request reviews (2 approvals)
- Require status checks to pass
- Restrict force pushes
- Require signed commits
- Require linear history

---

**Remember**: `testing` is for development, `main` is for stable releases only! 