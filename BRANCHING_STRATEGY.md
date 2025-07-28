# Branching Strategy

## Overview

This project follows a **testing→main** workflow designed for maximum stability and rapid development. The branching strategy ensures that all changes are thoroughly tested before reaching production while maintaining a clean, organized repository structure.

## Branch Structure

### Main Branches

#### `main` Branch
- **Purpose**: Production-ready, stable releases
- **Protection**: Strict protection rules enforced
- **Content**: Only stable, tested features and bug fixes
- **Deployment**: Automatic deployment to production
- **Required Files**: 
  - `README.md`
  - `CHANGELOG.md`
  - `LICENSE`
  - `setup.py`
  - `pyproject.toml`
  - `requirements.txt`
  - `VERSION`

#### `testing` Branch
- **Purpose**: Development and testing of new features
- **Protection**: Moderate protection with automated testing
- **Content**: Latest features, bug fixes, and experimental changes
- **Deployment**: Automatic deployment to GitHub Pages (documentation)
- **Required Files**:
  - `README.md`
  - `LICENSE`
  - `setup.py`
  - `pyproject.toml`
  - `requirements.txt`
  - `VERSION`
  - `docs/` directory with website files

### Feature Branches (Optional)

#### `feature/*` Branches
- **Purpose**: Development of specific features
- **Naming**: `feature/feature-name`
- **Lifecycle**: Created from `testing`, merged back to `testing`
- **Example**: `feature/advanced-monitoring`, `feature/ui-improvements`

#### `bugfix/*` Branches
- **Purpose**: Fixing specific bugs
- **Naming**: `bugfix/bug-description`
- **Lifecycle**: Created from `testing`, merged back to `testing`
- **Example**: `bugfix/connection-timeout`, `bugfix/memory-leak`

#### `hotfix/*` Branches
- **Purpose**: Critical fixes for production
- **Naming**: `hotfix/critical-issue`
- **Lifecycle**: Created from `main`, merged to both `main` and `testing`
- **Example**: `hotfix/security-vulnerability`, `hotfix/crash-fix`

## Workflow

### Development Workflow

1. **Feature Development**
   ```bash
   git checkout testing
   git pull origin testing
   git checkout -b feature/new-feature
   # Make changes
   git commit -m "feat: add new feature"
   git push origin feature/new-feature
   # Create Pull Request to testing
   ```

2. **Testing and Review**
   - All changes go through Pull Request review
   - Automated tests must pass
   - Code review required for all changes
   - Documentation updates required

3. **Release Process**
   ```bash
   # Merge testing to main for release
   git checkout main
   git merge testing
   git tag v2.0.0
   git push origin main --tags
   ```

### Branch Protection Rules

#### Main Branch Protection
- **Require pull request reviews**: Yes (2 reviewers)
- **Dismiss stale PR approvals**: Yes
- **Require status checks**: Yes
- **Require branches to be up to date**: Yes
- **Restrict pushes**: Yes (only maintainers)
- **Required files**: `CHANGELOG.md`, `README.md`, `LICENSE`

#### Testing Branch Protection
- **Require pull request reviews**: Yes (1 reviewer)
- **Dismiss stale PR approvals**: Yes
- **Require status checks**: Yes
- **Require branches to be up to date**: Yes
- **Restrict pushes**: Yes (only maintainers)
- **Required files**: `README.md`, `LICENSE`

## File Organization

### Main Branch Files
```
├── README.md              # Project documentation
├── CHANGELOG.md           # Release history
├── LICENSE                # MIT License
├── setup.py              # Python package setup
├── pyproject.toml        # Modern Python packaging
├── requirements.txt      # Python dependencies
├── VERSION               # Current version
├── src/                  # Source code
├── utils/                # Utility modules
├── tests/                # Test files
├── scripts/              # Build and deployment scripts
└── .github/              # GitHub configuration
```

### Testing Branch Files
```
├── README.md              # Project documentation
├── LICENSE                # MIT License
├── setup.py              # Python package setup
├── pyproject.toml        # Modern Python packaging
├── requirements.txt      # Python dependencies
├── VERSION               # Current version
├── src/                  # Source code
├── utils/                # Utility modules
├── tests/                # Test files
├── scripts/              # Build and deployment scripts
├── docs/                 # Website documentation
│   ├── index.html        # Homepage
│   ├── installation.html # Installation guide
│   ├── styles.css        # Website styles
│   └── ...               # Other website files
└── .github/              # GitHub configuration
```

## Version Management

### Version Format
- **Format**: `MAJOR.MINOR.PATCH` (e.g., `2.0.0`)
- **File**: `VERSION` file contains current version
- **Changelog**: `CHANGELOG.md` tracks all changes

### Version Bumping
- **MAJOR**: Breaking changes, major features
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, minor improvements

## Deployment Strategy

### GitHub Pages Deployment
- **Source**: `testing` branch
- **Directory**: `/docs` folder
- **URL**: `https://nightcodex7.github.io/warp-nextdns-wireguard/`
- **Automatic**: Updates on every push to `testing`

### Release Deployment
- **Source**: `main` branch
- **Trigger**: Manual release creation
- **Artifacts**: GitHub Releases with binaries
- **Documentation**: Updated automatically

## Best Practices

### Commit Messages
- **Format**: `type(scope): description`
- **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- **Example**: `feat(cli): add interactive setup wizard`

### Pull Request Guidelines
- **Title**: Clear, descriptive title
- **Description**: Detailed description of changes
- **Checklist**: Required items checklist
- **Labels**: Appropriate labels for categorization

### Code Quality
- **Linting**: All code must pass linting checks
- **Testing**: All new features must have tests
- **Documentation**: All public APIs must be documented
- **Security**: Security review for sensitive changes

## Automation

### GitHub Actions
- **CI/CD**: Automated testing and deployment
- **Branch Protection**: Automated enforcement of rules
- **Code Quality**: Automated linting and testing
- **Documentation**: Automated website deployment

### Workflow Files
- `.github/workflows/branch-protection.yml`: Branch validation
- `.github/workflows/deploy.yml`: Website deployment
- `.github/workflows/test.yml`: Automated testing

## Emergency Procedures

### Hotfix Process
1. Create hotfix branch from `main`
2. Make minimal required changes
3. Test thoroughly
4. Merge to `main` and `testing`
5. Create new patch release

### Rollback Process
1. Identify the problematic commit
2. Create rollback branch from previous stable commit
3. Test the rollback
4. Merge to `main` and `testing`
5. Create emergency release

## Contact and Support

For questions about this branching strategy:
- **Issues**: [GitHub Issues](https://github.com/nightcodex7/warp-nextdns-wireguard/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nightcodex7/warp-nextdns-wireguard/discussions)
- **Developer**: [@nightcodex7](https://github.com/nightcodex7)

---

**Last Updated**: February 2025  
**Version**: 2.0.0  
**Maintainer**: [@nightcodex7](https://github.com/nightcodex7) 