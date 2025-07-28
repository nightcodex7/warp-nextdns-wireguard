# Contributing to WARP + NextDNS Manager

Thank you for your interest in contributing to WARP + NextDNS Manager! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

Before creating bug reports, please check the existing issues to avoid duplicates. When creating an issue, please include:

- **Clear and descriptive title**
- **Detailed description** of the problem
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **System information** (OS, Python version, etc.)
- **Screenshots** if applicable

### Feature Requests

We welcome feature requests! Please:

- **Describe the feature** in detail
- **Explain the use case** and benefits
- **Consider implementation complexity**
- **Check if similar features exist**

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following our coding standards
4. **Test your changes** thoroughly
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## 📋 Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Local Development

```bash
# Clone the repository
git clone https://github.com/nightcodex7/warp-nextdns-wireguard.git
cd warp-nextdns-wireguard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_enhanced.txt

# Run tests
python -m pytest

# Start development server
python main.py
```

### Code Style

We follow PEP 8 with some modifications:

- **Line length**: 120 characters
- **Indentation**: 4 spaces
- **Docstrings**: Google style
- **Type hints**: Required for public functions

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Maintain test coverage above 80%

## 🏗️ Project Structure

```
warp-nextdns-wireguard/
├── main.py                # Main CLI entry point
├── cli.py                 # Command-line interface

├── core.py                # Core WARP manager functionality

├── requirements.txt       # Basic dependencies

├── utils/                 # Utility modules
│   ├── platform_utils.py  # Cross-platform utilities
│   ├── error_handler.py   # Error handling
│   ├── network_monitor.py # Network monitoring
│   ├── security_manager.py # Security features
│   └── backup_manager.py  # Backup management
├── templates/             # HTML templates
├── static/                # Static assets
├── docs/                  # Documentation
└── tests/                 # Test files
```

## 🔧 Development Guidelines

### Code Quality

- **Write clean, readable code**
- **Add comments** for complex logic
- **Use meaningful variable names**
- **Handle errors gracefully**
- **Follow DRY principles**

### Security

- **Never commit sensitive data**
- **Validate all inputs**
- **Use secure defaults**
- **Follow security best practices**

### Performance

- **Optimize for efficiency**
- **Minimize resource usage**
- **Use async operations when appropriate**
- **Profile code for bottlenecks**

## 📝 Documentation

### Code Documentation

- **Docstrings** for all public functions
- **Type hints** for better IDE support
- **Inline comments** for complex logic
- **README updates** for new features

### User Documentation

- **Update installation instructions**
- **Add usage examples**
- **Document configuration options**
- **Include troubleshooting guides**

## 🧪 Testing

### Test Types

- **Unit tests**: Individual functions
- **Integration tests**: Component interaction
- **End-to-end tests**: Full workflow
- **Performance tests**: Load and stress

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_feature.py

# Run with verbose output
python -m pytest -v
```

## 🚀 Release Process

### Version Management

- **Semantic versioning** (MAJOR.MINOR.PATCH)
- **Update VERSION file**
- **Update CHANGELOG.md**
- **Create release tags**

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version bumped
- [ ] Changelog updated
- [ ] Release notes written
- [ ] Tag created
- [ ] GitHub release published

## 🤝 Community Guidelines

### Communication

- **Be respectful** and inclusive
- **Use clear language**
- **Provide constructive feedback**
- **Help other contributors**

### Code of Conduct

We follow the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## 💰 Support This Project

If you find this project helpful, consider supporting its development:

[![Buy Me a Coffee](https://img.shields.io/badge/☕-Buy%20Me%20a%20Coffee-orange?style=for-the-badge)](https://buymeacoffee.com/nightcode)
[![Ko-fi](https://img.shields.io/badge/💙-Support%20on%20Ko--fi-blue?style=for-the-badge)](https://ko-fi.com/nightcode)

Your support helps maintain and improve this project!

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check the docs folder
- **Wiki**: For detailed guides and tutorials

## 🏆 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **GitHub contributors** page
- **Release notes** for significant contributions
- **Project documentation**

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to WARP + NextDNS Manager! 🚀 