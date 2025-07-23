"""
Basic tests for WARP + NextDNS Manager
"""
import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that core modules can be imported"""
    try:
        import core
        assert core is not None
    except ImportError as e:
        pytest.fail(f"Failed to import core module: {e}")

def test_cli_imports():
    """Test that CLI module can be imported"""
    try:
        import cli
        assert cli is not None
    except ImportError as e:
        pytest.fail(f"Failed to import cli module: {e}")

def test_utils_imports():
    """Test that utility modules can be imported"""
    try:
        from utils import platform_utils
        assert platform_utils is not None
    except ImportError as e:
        pytest.fail(f"Failed to import platform_utils module: {e}")

def test_basic_functionality():
    """Test basic functionality"""
    # This is a placeholder test
    assert True

def test_version_file():
    """Test that VERSION file exists"""
    version_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION')
    assert os.path.exists(version_file), "VERSION file should exist"

def test_requirements_file():
    """Test that requirements.txt exists"""
    requirements_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requirements.txt')
    assert os.path.exists(requirements_file), "requirements.txt file should exist"

def test_mkdocs_config():
    """Test that mkdocs.yml exists"""
    mkdocs_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mkdocs.yml')
    assert os.path.exists(mkdocs_file), "mkdocs.yml file should exist" 