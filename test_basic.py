"""Basic tests for WARP NextDNS Manager."""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.platform_utils import PlatformUtils
from utils.navigation_manager import NavigationManager


def test_platform_utils():
    """Test platform utilities."""
    platform = PlatformUtils()
    
    # Test system detection
    assert platform.system in ["linux", "windows", "darwin"]
    assert isinstance(platform.is_linux, bool)
    assert isinstance(platform.is_windows, bool)
    assert isinstance(platform.is_macos, bool)
    
    # Test system info
    info = platform.get_system_info()
    assert isinstance(info, dict)
    assert "os" in info
    assert "platform" in info
    assert "python" in info


def test_navigation_manager():
    """Test navigation manager."""
    nav = NavigationManager(auto_mode=True)
    
    # Test auto-confirm
    assert nav.auto_confirm("Test?") == True
    assert nav.auto_confirm("Test?", default=False) == False
    
    # Test auto-prompt
    assert nav.auto_prompt("Test?", default="yes") == "yes"


def test_imports():
    """Test all imports work correctly."""
    try:
        from core import WarpNextDNSManager
        from cli import cli
        from utils.wgcf_manager import WGCFManager
        from utils.nextdns_manager import NextDNSManager
        from utils.installer_manager import InstallerManager
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])