# Contributing Guide

> **How to contribute to WARP + NextDNS Manager**

Thank you for your interest in contributing to WARP + NextDNS Manager! This guide will help you get started.

## 🤝 How to Contribute

We welcome contributions from the community! Here are the main ways you can contribute:

### 🐛 Bug Reports

Found a bug? Please report it by creating an issue with:

- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **System information** (OS, Python version, etc.)
- **Error messages and logs**

### 💡 Feature Requests

Have an idea for a new feature? Create an issue with:

- **Description** of the feature
- **Use case** and benefits
- **Implementation suggestions** (if any)
- **Priority level** (low/medium/high)

### 📝 Documentation

Help improve our documentation by:

- **Fixing typos** and grammar errors
- **Adding examples** and use cases
- **Improving clarity** of existing content
- **Translating** to other languages

### 🔧 Code Contributions

Want to contribute code? Follow these steps:

## 🚀 Getting Started

### Prerequisites

- **Python 3.7+** installed
- **Git** for version control
- **Basic knowledge** of Python and networking
- **Development environment** set up

### Development Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub first, then clone your fork
   git clone https://github.com/YOUR_USERNAME/warp-nextdns-wireguard.git
   cd warp-nextdns-wireguard
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes**
   - Write your code
   - Add tests
   - Update documentation
   - Follow coding standards

5. **Test your changes**
   ```bash
   # Run tests
   python -m pytest tests/
   
   # Run linting
   flake8 .
   black .
   
   # Test the CLI
   python cli.py --help
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select the `testing` branch as target
   - Fill out the PR template

## 📋 Development Guidelines

### Code Style

We follow these coding standards:

- **Python**: PEP 8 style guide
- **Line length**: 88 characters (Black formatter)
- **Type hints**: Use type hints for all functions
- **Docstrings**: Follow Google docstring format
- **Comments**: Clear, concise comments

### Code Formatting

```bash
# Install development tools
pip install black flake8 isort mypy

# Format code
black .
isort .

# Check code quality
flake8 .
mypy .
```

### Testing

Write tests for all new functionality:

```python
# Example test structure
def test_new_feature():
    """Test the new feature functionality."""
    # Arrange
    expected = "expected result"
    
    # Act
    result = new_feature()
    
    # Assert
    assert result == expected
```

### Documentation

Update documentation for any changes:

- **README.md**: Update if adding new features
- **docs/**: Update relevant documentation files
- **Inline comments**: Add comments for complex logic
- **Type hints**: Include type hints for all functions

## 🏗️ Project Structure

```
warp-nextdns-wireguard/
├── core.py                 # Main application logic
├── cli.py                  # Command-line interface
├── utils/                  # Utility modules
│   ├── platform_utils.py   # Platform-specific operations
│   ├── wgcf_manager.py     # WGCF management
│   ├── nextdns_manager.py  # NextDNS management
│   └── installer_manager.py # Installation utilities
├── tests/                  # Test files
│   ├── test_core.py        # Core functionality tests
│   ├── test_cli.py         # CLI tests
│   └── test_utils.py       # Utility tests
├── docs/                   # Documentation
│   ├── index.md           # Main documentation
│   ├── installation.md    # Installation guide
│   ├── usage.md           # Usage guide
│   └── ...
├── .github/               # GitHub configuration
│   └── workflows/         # CI/CD workflows
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
└── README.md             # Project overview
```

## 🔧 Development Workflow

### Branch Strategy

- **`main`**: Stable releases only
- **`testing`**: Development and beta releases
- **Feature branches**: `feature/description`
- **Bug fix branches**: `fix/description`
- **Documentation branches**: `docs/description`

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

Examples:
```bash
git commit -m "feat(cli): add new command for status monitoring"
git commit -m "fix(wgcf): resolve permission issues on Windows"
git commit -m "docs(installation): update Ubuntu installation steps"
```

### Pull Request Process

1. **Create PR** to `testing` branch
2. **Fill out PR template** completely
3. **Ensure tests pass** and code is formatted
4. **Request review** from maintainers
5. **Address feedback** and make requested changes
6. **Get approval** from at least one maintainer
7. **Merge** when ready

## 🧪 Testing Guidelines

### Test Structure

```python
# tests/test_feature.py
import pytest
from unittest.mock import patch, MagicMock

class TestFeature:
    """Test suite for feature functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.test_data = {"key": "value"}
    
    def test_feature_basic_functionality(self):
        """Test basic feature functionality."""
        # Test implementation
        pass
    
    def test_feature_error_handling(self):
        """Test feature error handling."""
        # Test error cases
        pass
    
    @patch('module.external_dependency')
    def test_feature_with_mock(self, mock_dependency):
        """Test feature with mocked dependencies."""
        # Test with mocks
        pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_core.py

# Run with coverage
pytest --cov=core --cov=utils

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_core.py::TestFeature::test_feature_basic_functionality
```

### Test Coverage

Maintain high test coverage:

- **Unit tests**: Test individual functions
- **Integration tests**: Test component interactions
- **End-to-end tests**: Test complete workflows
- **Platform tests**: Test on different OS platforms

## 📚 Documentation Standards

### Markdown Guidelines

- **Clear headings** with proper hierarchy
- **Code blocks** with language specification
- **Links** to related documentation
- **Images** with alt text
- **Tables** for structured information

### Documentation Structure

```markdown
# Page Title

> Brief description

## Section Heading

Content with clear explanations.

### Subsection

More detailed content.

```python
# Code examples
def example_function():
    """Example function."""
    return "example"
```

## Related Links

- [Link to related page](link)
- [External resource](https://example.com)
```

## 🔍 Code Review Process

### What We Look For

- **Functionality**: Does the code work as intended?
- **Code quality**: Is the code clean and maintainable?
- **Testing**: Are there adequate tests?
- **Documentation**: Is documentation updated?
- **Security**: Are there security implications?
- **Performance**: Are there performance concerns?

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Error handling is appropriate
- [ ] Logging is adequate
- [ ] Cross-platform compatibility

## 🚀 Release Process

### Version Management

- **Semantic versioning**: MAJOR.MINOR.PATCH
- **VERSION file**: Contains current version
- **Changelog**: Document all changes
- **Release notes**: Summarize changes

### Release Steps

1. **Update version** in VERSION file
2. **Update changelog** with new changes
3. **Create release branch** from testing
4. **Run full test suite**
5. **Build and test executables**
6. **Create GitHub release**
7. **Merge to main** branch
8. **Update documentation**

## 🤝 Community Guidelines

### Code of Conduct

- **Be respectful** and inclusive
- **Help others** learn and grow
- **Provide constructive feedback**
- **Follow project guidelines**
- **Report issues** appropriately

### Communication

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and help
- **Pull Requests**: For code contributions
- **Discord/Slack**: For real-time discussion (if available)

## 🎯 Areas for Contribution

### High Priority

- **Bug fixes** and stability improvements
- **Cross-platform compatibility**
- **Performance optimizations**
- **Security enhancements**
- **Documentation improvements**

### Medium Priority

- **New features** and functionality
- **UI/UX improvements**
- **Integration with other tools**
- **Monitoring and logging**
- **Testing improvements**

### Low Priority

- **Code refactoring**
- **Style improvements**
- **Minor optimizations**
- **Additional examples**
- **Translations**

## 📞 Getting Help

### Before Asking

1. **Check existing issues** and discussions
2. **Read the documentation** thoroughly
3. **Search for similar problems**
4. **Try to reproduce** the issue
5. **Gather relevant information**

### When Asking for Help

- **Be specific** about your problem
- **Include system information**
- **Provide error messages**
- **Show what you've tried**
- **Be patient** and respectful

## 🙏 Recognition

Contributors are recognized in:

- **README.md**: List of contributors
- **Release notes**: Credit for contributions
- **GitHub contributors**: Automatic recognition
- **Documentation**: Credit for documentation

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (GNU General Public License v3).

---

**Ready to contribute?** Start by [forking the repository](https://github.com/nightcodex7/warp-nextdns-wireguard/fork) and creating your first pull request! 