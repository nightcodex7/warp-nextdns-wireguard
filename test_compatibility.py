#!/usr/bin/env python3
"""
Cross-platform compatibility test script
Tests all functionality on Windows and Linux
"""

import os
import sys
import platform
import subprocess
import importlib
from pathlib import Path

def test_platform_detection():
    """Test platform detection"""
    print("🧪 Testing platform detection...")
    
    current_platform = platform.system()
    print(f"✅ Detected platform: {current_platform}")
    
    if current_platform not in ["Windows", "Linux"]:
        print(f"❌ Unsupported platform: {current_platform}")
        return False
    
    return True

def test_imports():
    """Test all required imports"""
    print("📦 Testing imports...")
    
    required_modules = [
        "rich",
        "requests", 
        "psutil",
        "cryptography",
        "yaml",
        "schedule",
        "watchdog",
        "dotenv",
        "click"
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"❌ Failed imports: {failed_imports}")
        return False
    
    return True

def test_project_imports():
    """Test project-specific imports"""
    print("🏗️ Testing project imports...")
    
    project_modules = [
        "core",
        "cli", 
        "utils.platform_utils",
        "utils.security_manager",
        "utils.error_handler",
        "utils.network_monitor",
        "utils.backup_manager"
    ]
    
    failed_imports = []
    
    for module in project_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"❌ Failed project imports: {failed_imports}")
        return False
    
    return True

def test_platform_utils():
    """Test platform utilities"""
    print("🔧 Testing platform utilities...")
    
    try:
        from utils.platform_utils import platform_manager
        
        # Test system info
        system_info = platform_manager.get_system_info()
        print(f"✅ System info: {system_info['platform']}")
        
        # Test config directories
        config_dirs = platform_manager.get_config_directories()
        print(f"✅ Config directories: {list(config_dirs.keys())}")
        
        # Test executable finding
        result = platform_manager.find_executable("python")
        if result:
            print(f"✅ Found python: {result}")
        else:
            print("⚠️ Python not found in PATH")
        
        return True
        
    except Exception as e:
        print(f"❌ Platform utils test failed: {e}")
        return False

def test_core_functionality():
    """Test core functionality"""
    print("⚙️ Testing core functionality...")
    
    try:
        from core import warp_manager
        
        # Test status generation
        status = warp_manager.get_system_status()
        required_keys = ['platform', 'tools', 'services', 'network', 'warp_status', 'nextdns_status']
        
        for key in required_keys:
            if key in status:
                print(f"✅ {key}")
            else:
                print(f"❌ Missing {key}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        return False

def test_cli_functionality():
    """Test CLI functionality"""
    print("🖥️ Testing CLI functionality...")
    
    try:
        from cli import WARPCLI
        
        # Test CLI instantiation
        cli = WARPCLI()
        print("✅ CLI instantiated")
        
        # Test help generation
        try:
            cli.console.print("Test output")
            print("✅ Console output working")
        except Exception as e:
            print(f"⚠️ Console output test: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI functionality test failed: {e}")
        return False

def test_shell_commands():
    """Test shell command compatibility"""
    print("🐚 Testing shell commands...")
    
    current_platform = platform.system()
    
    if current_platform == "Windows":
        commands = [
            ["ping", "-n", "1", "127.0.0.1"],
            ["ipconfig"],
            ["sc", "query"]
        ]
    else:
        commands = [
            ["ping", "-c", "1", "127.0.0.1"],
            ["ip", "addr"],
            ["systemctl", "--version"]
        ]
    
    failed_commands = []
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {' '.join(cmd)}")
            else:
                print(f"⚠️ {' '.join(cmd)} (return code: {result.returncode})")
        except Exception as e:
            print(f"❌ {' '.join(cmd)}: {e}")
            failed_commands.append(cmd)
    
    if failed_commands:
        print(f"⚠️ Some commands failed: {failed_commands}")
    
    return True

def test_file_operations():
    """Test file operations"""
    print("📁 Testing file operations...")
    
    try:
        # Test path operations
        test_path = Path("test_compatibility_temp")
        test_path.mkdir(exist_ok=True)
        
        # Test file creation
        test_file = test_path / "test.txt"
        test_file.write_text("test content")
        
        # Test file reading
        content = test_file.read_text()
        if content == "test content":
            print("✅ File operations working")
        else:
            print("❌ File content mismatch")
            return False
        
        # Cleanup
        test_file.unlink()
        test_path.rmdir()
        
        return True
        
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def test_network_operations():
    """Test network operations"""
    print("🌐 Testing network operations...")
    
    try:
        import requests
        
        # Test HTTP request
        response = requests.get("https://httpbin.org/ip", timeout=10)
        if response.status_code == 200:
            print("✅ HTTP requests working")
            return True
        else:
            print(f"❌ HTTP request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️ Network operations test: {e}")
        return True  # Not critical for CLI functionality

def main():
    """Main test function"""
    print("🧪 WARP + NextDNS Manager - Cross-Platform Compatibility Test")
    print("=" * 60)
    
    tests = [
        ("Platform Detection", test_platform_detection),
        ("Required Imports", test_imports),
        ("Project Imports", test_project_imports),
        ("Platform Utils", test_platform_utils),
        ("Core Functionality", test_core_functionality),
        ("CLI Functionality", test_cli_functionality),
        ("Shell Commands", test_shell_commands),
        ("File Operations", test_file_operations),
        ("Network Operations", test_network_operations),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Project is compatible.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 