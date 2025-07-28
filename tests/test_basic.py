"""Basic tests for the application"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.platform_utils import PlatformUtils
from utils.error_handler import ErrorHandler

"""
Comprehensive test suite for WARP + NextDNS Manager
"""


class TestImports:
    """Test that all modules can be imported correctly"""

    def test_core_imports(self):
        """Test core module imports"""
        try:
            from src import core

            assert core is not None
            assert hasattr(core, "WarpNextDNSManager")
        except ImportError as e:
            pytest.fail(f"Failed to import core module: {e}")

    def test_cli_imports(self):
        """Test CLI module imports"""
        try:
            from src import cli

            assert cli is not None
        except ImportError as e:
            pytest.fail(f"Failed to import cli module: {e}")

    def test_utils_imports(self):
        """Test utility module imports"""
        utils_modules = [
            "utils.platform_utils",
            "utils.installer_manager",
            "utils.wgcf_manager",
            "utils.nextdns_manager",
            "utils.error_handler",
            "utils.navigation_manager",
            "utils.backup_manager",
            "utils.network_monitor",
            "utils.security_manager",
            "utils.auto_responder",
        ]

        for module_name in utils_modules:
            try:
                module = __import__(module_name, fromlist=[""])
                assert module is not None
            except ImportError as e:
                pytest.fail(f"Failed to import {module_name}: {e}")


class TestPlatformUtils:
    """Test platform utilities"""

    def setup_method(self):
        """Setup test environment"""
        self.platform = PlatformUtils()

    def test_system_detection(self):
        """Test system detection"""
        info = self.platform.get_system_info()
        assert "os" in info
        assert "platform" in info
        assert "architecture" in info
        assert info["os"] in ["linux", "windows", "darwin"]

    def test_root_access_check(self):
        """Test root access checking"""
        # This will depend on the test environment
        result = self.platform.check_root_access()
        assert isinstance(result, bool)

    def test_command_exists(self):
        """Test command existence checking"""
        # Test with a command that should exist
        assert self.platform.command_exists("python") or self.platform.command_exists(
            "python3"
        )

        # Test with a command that shouldn't exist
        assert not self.platform.command_exists("nonexistent_command_12345")


class TestErrorHandler:
    """Test error handling system"""

    def setup_method(self):
        """Setup test environment"""
        self.error_handler = ErrorHandler()

    def test_error_handling(self):
        """Test basic error handling"""
        test_error = ValueError("Test error")
        result = self.error_handler.handle_error(test_error, "test_context")

        assert "timestamp" in result
        assert "error_type" in result
        assert "error_message" in result
        assert "context" in result
        assert result["error_type"] == "ValueError"
        assert result["error_message"] == "Test error"
        assert result["context"] == "test_context"

    def test_user_friendly_messages(self):
        """Test user-friendly error messages"""
        test_error = FileNotFoundError("No such file")
        result = self.error_handler.handle_error(test_error, "wgcf")

        assert "user_friendly_message" in result
        assert "Required file or directory not found" in result["user_friendly_message"]


class TestNavigationManager:
    """Test navigation manager"""

    def setup_method(self):
        """Setup test environment"""
        from utils.navigation_manager import NavigationManager

        self.nav = NavigationManager(auto_mode=False)

    def test_auto_confirm(self):
        """Test auto confirmation"""
        from utils.navigation_manager import NavigationManager

        # Test auto mode
        auto_nav = NavigationManager(auto_mode=True)
        result = auto_nav.auto_confirm("Test message", default=True)
        assert result is True

        # Test non-auto mode (will need to mock input)
        with patch("rich.prompt.Confirm.ask", return_value=True):
            result = self.nav.auto_confirm("Test message", default=False)
            assert result is True

    def test_auto_prompt(self):
        """Test auto prompting"""
        from utils.navigation_manager import NavigationManager

        # Test auto mode
        auto_nav = NavigationManager(auto_mode=True)
        result = auto_nav.auto_prompt("Test message", default="test_value")
        assert result == "test_value"

    def test_menu_stack(self):
        """Test menu stack operations"""
        self.nav.push_menu("test_menu")
        assert self.nav.get_current_menu() == "test_menu"

        previous = self.nav.pop_menu()
        assert previous is not None


class TestWarpNextDNSManager:
    """Test main manager class"""

    def setup_method(self):
        """Setup test environment"""
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.original_home = os.environ.get("HOME")
        os.environ["HOME"] = self.temp_dir

        # Mock the managers to avoid actual system calls
        with patch("src.core.WGCFManager"), patch("src.core.NextDNSManager"), patch(
            "src.core.InstallerManager"
        ), patch("src.core.PlatformUtils"):
            from src.core import WarpNextDNSManager

            self.manager = WarpNextDNSManager(auto_mode=False)

    def teardown_method(self):
        """Cleanup test environment"""
        if self.original_home:
            os.environ["HOME"] = self.original_home
        else:
            del os.environ["HOME"]

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Test manager initialization"""
        assert self.manager.auto_mode is False
        assert hasattr(self.manager, "platform")
        assert hasattr(self.manager, "installer")
        assert hasattr(self.manager, "wgcf_manager")
        assert hasattr(self.manager, "nextdns_manager")
        assert hasattr(self.manager, "error_handler")

    def test_get_status(self):
        """Test status retrieval"""
        with patch.object(
            self.manager, "check_internet_connection", return_value=True
        ), patch.object(
            self.manager, "get_warp_ip", return_value="1.2.3.4"
        ), patch.object(
            self.manager, "get_dns_servers", return_value=["8.8.8.8"]
        ):
            status = self.manager.get_status()

            assert "timestamp" in status
            assert "platform" in status
            assert "architecture" in status
            assert "python_version" in status
            assert "services" in status
            assert "tools" in status
            assert "network" in status

    def test_internet_connection_check(self):
        """Test internet connection checking"""
        with patch("requests.get") as mock_get:
            # Test successful connection
            mock_get.return_value.status_code = 200
            assert self.manager.check_internet_connection() is True

            # Test failed connection
            mock_get.side_effect = Exception("Connection failed")
            assert self.manager.check_internet_connection() is False

    def test_warp_ip_retrieval(self):
        """Test WARP IP retrieval"""
        with patch("requests.get") as mock_get:
            # Test successful IP retrieval
            mock_get.return_value.text = "1.2.3.4"
            assert self.manager.get_warp_ip() == "1.2.3.4"

            # Test failed IP retrieval
            mock_get.side_effect = Exception("Failed to get IP")
            assert self.manager.get_warp_ip() is None


class TestFileStructure:
    """Test project file structure"""

    def test_version_file(self):
        """Test that VERSION file exists and is valid"""
        version_file = Path(__file__).parent.parent / "VERSION"
        assert version_file.exists(), "VERSION file should exist"

        version = version_file.read_text().strip()
        assert version, "VERSION file should not be empty"
        # Check if it's a valid version format (x.y.z)
        assert len(version.split(".")) == 3, "VERSION should be in x.y.z format"

    def test_requirements_file(self):
        """Test that requirements.txt exists and is valid"""
        requirements_file = Path(__file__).parent.parent / "requirements.txt"
        assert requirements_file.exists(), "requirements.txt file should exist"

        requirements = requirements_file.read_text()
        assert requirements, "requirements.txt should not be empty"

        # Check for essential dependencies
        essential_deps = ["click", "rich", "requests"]
        for dep in essential_deps:
            assert dep in requirements, f"Missing essential dependency: {dep}"

    def test_static_website_files(self):
        """Test that static website files exist"""
        docs_dir = Path(__file__).parent.parent / "docs"
        assert docs_dir.exists(), "docs directory should exist"
        assert (docs_dir / "index.html").exists(), "index.html should exist"
        assert (docs_dir / "styles.css").exists(), "styles.css should exist"

    def test_readme_file(self):
        """Test that README.md exists and is valid"""
        readme_file = Path(__file__).parent.parent / "README.md"
        assert readme_file.exists(), "README.md file should exist"

        readme_content = readme_file.read_text()
        assert readme_content, "README.md should not be empty"
        assert (
            "WARP + NextDNS Manager" in readme_content
        ), "README should contain project name"


class TestCLICommands:
    """Test CLI command structure"""

    def test_cli_commands_exist(self):
        """Test that all expected CLI commands exist"""
        from src import cli

        expected_commands = [
            "setup",
            "start",
            "stop",
            "status",
            "monitor",
            "interactive",
            "logs",
            "backup",
            "uninstall",
            "version",
        ]

        for command in expected_commands:
            assert hasattr(cli, command), f"Missing CLI command: {command}"

    def test_cli_group_structure(self):
        """Test CLI group structure"""
        from src import cli

        # Test that cli is a Click group
        assert hasattr(cli, "cli")
        assert callable(cli.cli)


class TestCrossPlatformCompatibility:
    """Test cross-platform compatibility"""

    def test_path_handling(self):
        """Test cross-platform path handling"""
        from pathlib import Path

        # Test that paths are created correctly
        test_path = Path.home() / ".warp-nextdns"
        assert isinstance(test_path, Path)

    def test_platform_detection(self):
        """Test platform detection works on all platforms"""
        platform = PlatformUtils()
        info = platform.get_system_info()

        # Should work on any platform
        assert "os" in info
        assert "platform" in info
        assert "architecture" in info


class TestErrorRecovery:
    """Test error recovery mechanisms"""

    def test_error_recovery_strategies(self):
        """Test error recovery strategies"""
        error_handler = ErrorHandler()

        # Test adding recovery strategy
        def test_recovery(error):
            return {"success": True, "message": "Recovered"}

        error_handler.add_recovery_strategy("test_context", test_recovery)
        assert "test_context" in error_handler.recovery_strategies

    def test_error_callbacks(self):
        """Test error callbacks"""
        error_handler = ErrorHandler()
        callback_called = False

        def test_callback(error_info):
            nonlocal callback_called
            callback_called = True

        error_handler.add_error_callback(test_callback)

        # Trigger an error
        test_error = ValueError("Test error")
        error_handler.handle_error(test_error, "test_context")

        # Callback should have been called
        assert callback_called


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
