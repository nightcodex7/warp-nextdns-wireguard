"""Tests for platform utilities."""

from utils.platform_utils import PlatformUtils


def test_platform_utils_initialization():
    """Test PlatformUtils initialization."""
    platform = PlatformUtils()
    assert platform is not None
    assert hasattr(platform, "system")
    assert hasattr(platform, "is_linux")
    assert hasattr(platform, "is_windows")
    # macOS detection exists but is not supported
    assert hasattr(platform, "is_macos")


def test_system_info():
    """Test system info retrieval."""
    platform = PlatformUtils()
    info = platform.get_system_info()

    assert isinstance(info, dict)
    assert "os" in info
    assert "platform" in info
    assert "version" in info
    assert "machine" in info
    assert "python" in info


def test_command_exists():
    """Test command existence check."""
    platform = PlatformUtils()

    # Test with a command that should exist
    assert platform.command_exists("python") or platform.command_exists("python3")

    # Test with a command that shouldn't exist
    assert not platform.command_exists("nonexistentcommand12345")


def test_package_manager_detection():
    """Test package manager detection."""
    platform = PlatformUtils()
    pm = platform.get_package_manager()

    # Should return None on non-Linux systems
    if not platform.is_linux:
        assert pm is None
    else:
        # On Linux, should return a valid package manager or None
        assert pm is None or pm in ["apt", "yum", "dnf", "pacman", "zypper"]
