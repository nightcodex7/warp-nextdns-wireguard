"""
Error handling utilities for the WARP + NextDNS Manager
"""

import os
import sys
import traceback
import logging
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from pathlib import Path
import json

class ErrorHandler:
    """Comprehensive error handling system"""
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file or self._get_default_log_file()
        self.error_callbacks: List[Callable] = []
        self.recovery_strategies: Dict[str, Callable] = {}
        self.setup_logging()
        
    def _get_default_log_file(self) -> str:
        """Get default log file path"""
        # Check for CI environment variable first
        ci_log_dir = os.environ.get('WARP_NEXTDNS_LOG_DIR')
        if ci_log_dir:
            log_dir = Path(ci_log_dir)
        elif sys.platform == "win32":
            log_dir = Path.home() / ".warp" / "logs"
        else:
            log_dir = Path("/var/log/warp-nextdns")
        
        log_dir.mkdir(parents=True, exist_ok=True)
        return str(log_dir / "error.log")
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, error: Exception, context: str = "", 
                    user_friendly: bool = True) -> Dict[str, Any]:
        """Handle an error with comprehensive logging and recovery"""
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'traceback': traceback.format_exc(),
            'user_friendly_message': self._get_user_friendly_message(error, context),
            'recovery_suggestions': self._get_recovery_suggestions(error, context),
            'severity': self._get_error_severity(error),
            'handled': False
        }
        
        # Log the error
        self.logger.error(f"Error in {context}: {error}")
        self.logger.debug(f"Full traceback: {error_info['traceback']}")
        
        # Try to recover automatically
        recovery_result = self._attempt_recovery(error, context)
        if recovery_result['success']:
            error_info['handled'] = True
            error_info['recovery_message'] = recovery_result['message']
            self.logger.info(f"Error recovered automatically: {recovery_result['message']}")
        
        # Call error callbacks
        for callback in self.error_callbacks:
            try:
                callback(error_info)
            except Exception as callback_error:
                self.logger.error(f"Error in error callback: {callback_error}")
        
        # Return error information
        return error_info
    
    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        """Get user-friendly error message"""
        error_type = type(error).__name__
        
        # Common error messages
        error_messages = {
            'FileNotFoundError': {
                'default': 'Required file or directory not found',
                'wgcf': 'wgcf tool not found. Please install it first.',
                'wireguard': 'WireGuard configuration not found',
                'nextdns': 'NextDNS configuration not found'
            },
            'PermissionError': {
                'default': 'Permission denied. Try running with administrator privileges.',
                'wireguard': 'Permission denied accessing WireGuard. Run with sudo.',
                'nextdns': 'Permission denied accessing NextDNS configuration.'
            },
            'ConnectionError': {
                'default': 'Network connection failed. Check your internet connection.',
                'warp': 'Failed to connect to Cloudflare WARP servers.',
                'nextdns': 'Failed to connect to NextDNS servers.'
            },
            'TimeoutError': {
                'default': 'Operation timed out. Please try again.',
                'warp': 'WARP connection timed out.',
                'nextdns': 'NextDNS connection timed out.'
            },
            'subprocess.TimeoutExpired': {
                'default': 'Command execution timed out.',
                'wgcf': 'wgcf command timed out.',
                'wireguard': 'WireGuard command timed out.'
            },
            'subprocess.CalledProcessError': {
                'default': 'Command execution failed.',
                'wgcf': 'wgcf command failed.',
                'wireguard': 'WireGuard command failed.',
                'nextdns': 'NextDNS command failed.'
            }
        }
        
        # Get specific message for error type and context
        if error_type in error_messages:
            if context in error_messages[error_type]:
                return error_messages[error_type][context]
            else:
                return error_messages[error_type]['default']
        
        # Generic message for unknown errors
        return f"An unexpected error occurred: {str(error)}"
    
    def _get_recovery_suggestions(self, error: Exception, context: str) -> List[str]:
        """Get recovery suggestions for the error"""
        suggestions = []
        error_type = type(error).__name__
        
        if error_type == 'FileNotFoundError':
            if 'wgcf' in context:
                suggestions.extend([
                    "Install wgcf using the 'Install wgcf' button",
                    "Download wgcf manually from https://github.com/ViRb3/wgcf/releases",
                    "Ensure wgcf is in your system PATH"
                ])
            elif 'wireguard' in context:
                suggestions.extend([
                    "Run WireGuard setup using the 'Setup Config' button",
                    "Check if WireGuard is properly installed",
                    "Verify configuration file permissions"
                ])
            elif 'nextdns' in context:
                suggestions.extend([
                    "Install NextDNS CLI using your package manager",
                    "Configure NextDNS with your profile ID",
                    "Check NextDNS configuration file"
                ])
        
        elif error_type == 'PermissionError':
            suggestions.extend([
                "Run the application with administrator privileges",
                "Check file and directory permissions",
                "Use sudo for Linux operations"
            ])
        
        elif error_type == 'ConnectionError':
            suggestions.extend([
                "Check your internet connection",
                "Verify firewall settings",
                "Try using a different network",
                "Check if Cloudflare/NextDNS services are accessible"
            ])
        
        elif error_type == 'TimeoutError':
            suggestions.extend([
                "Check your internet connection speed",
                "Try again in a few moments",
                "Check if the service is experiencing issues"
            ])
        
        # Always add general suggestions
        suggestions.extend([
            "Check the logs for more detailed information",
            "Restart the application",
            "Contact support if the issue persists"
        ])
        
        return suggestions
    
    def _get_error_severity(self, error: Exception) -> str:
        """Determine error severity"""
        error_type = type(error).__name__
        
        # Critical errors
        critical_errors = ['KeyboardInterrupt', 'SystemExit']
        if error_type in critical_errors:
            return 'critical'
        
        # High severity errors
        high_severity = ['PermissionError', 'ConnectionError', 'TimeoutError']
        if error_type in high_severity:
            return 'high'
        
        # Medium severity errors
        medium_severity = ['FileNotFoundError', 'subprocess.CalledProcessError']
        if error_type in medium_severity:
            return 'medium'
        
        # Low severity errors
        return 'low'
    
    def _attempt_recovery(self, error: Exception, context: str) -> Dict[str, Any]:
        """Attempt automatic error recovery"""
        error_type = type(error).__name__
        
        # Check if we have a recovery strategy
        if context in self.recovery_strategies:
            try:
                result = self.recovery_strategies[context](error)
                return result
            except Exception as recovery_error:
                self.logger.error(f"Recovery strategy failed: {recovery_error}")
        
        # Default recovery attempts
        if error_type == 'FileNotFoundError':
            return self._recover_file_not_found(error, context)
        elif error_type == 'PermissionError':
            return self._recover_permission_error(error, context)
        elif error_type == 'ConnectionError':
            return self._recover_connection_error(error, context)
        
        return {'success': False, 'message': 'No automatic recovery available'}
    
    def _recover_file_not_found(self, error: Exception, context: str) -> Dict[str, Any]:
        """Recover from FileNotFoundError"""
        if 'wgcf' in context:
            # Try to find wgcf in common locations
            common_paths = ['wgcf', '/usr/local/bin/wgcf', '/usr/bin/wgcf']
            for path in common_paths:
                if os.path.exists(path):
                    return {
                        'success': True,
                        'message': f'Found wgcf at {path}',
                        'path': path
                    }
        
        return {'success': False, 'message': 'File not found, manual intervention required'}
    
    def _recover_permission_error(self, error: Exception, context: str) -> Dict[str, Any]:
        """Recover from PermissionError"""
        # For permission errors, we can't automatically fix them
        # but we can provide better error messages
        return {
            'success': False,
            'message': 'Permission error requires manual intervention'
        }
    
    def _recover_connection_error(self, error: Exception, context: str) -> Dict[str, Any]:
        """Recover from ConnectionError"""
        # Try to check internet connectivity
        try:
            import requests
            response = requests.get('https://www.cloudflare.com/cdn-cgi/trace', timeout=5)
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Internet connectivity restored'
                }
        except:
            pass
        
        return {'success': False, 'message': 'Connection error, check network settings'}
    
    def add_error_callback(self, callback: Callable[[Dict], None]):
        """Add a callback function to be called when errors occur"""
        self.error_callbacks.append(callback)
    
    def add_recovery_strategy(self, context: str, strategy: Callable[[Exception], Dict]):
        """Add a custom recovery strategy for a specific context"""
        self.recovery_strategies[context] = strategy
    
    def get_error_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get error summary for the last N hours"""
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
            
            cutoff_time = datetime.now().timestamp() - (hours * 3600)
            recent_errors = []
            
            for line in lines:
                if 'ERROR' in line:
                    try:
                        # Parse timestamp from log line
                        timestamp_str = line.split(' - ')[0]
                        timestamp = datetime.fromisoformat(timestamp_str.replace(',', '.'))
                        if timestamp.timestamp() > cutoff_time:
                            recent_errors.append(line.strip())
                    except:
                        continue
            
            return {
                'total_errors': len(recent_errors),
                'time_period_hours': hours,
                'errors': recent_errors[-10:]  # Last 10 errors
            }
        except Exception as e:
            return {
                'error': f'Failed to get error summary: {e}',
                'total_errors': 0
            }
    
    def clear_logs(self) -> bool:
        """Clear error logs"""
        try:
            with open(self.log_file, 'w') as f:
                f.write('')
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear logs: {e}")
            return False

# Global error handler instance
error_handler = ErrorHandler()

def handle_error_decorator(context: str = ""):
    """Decorator to automatically handle errors in functions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_info = error_handler.handle_error(e, context)
                # Re-raise the error if it couldn't be handled
                if not error_info['handled']:
                    raise
                return None
        return wrapper
    return decorator

def safe_execute(func: Callable, *args, context: str = "", **kwargs) -> Dict[str, Any]:
    """Safely execute a function with error handling"""
    try:
        result = func(*args, **kwargs)
        return {
            'success': True,
            'result': result,
            'error': None
        }
    except Exception as e:
        error_info = error_handler.handle_error(e, context)
        return {
            'success': False,
            'result': None,
            'error': error_info
        } 