"""
Auto-Responder Utility
Handles automatic responses to user prompts and terminal interactions
"""

import subprocess
import time
import threading
from typing import List, Optional, Callable, Dict
import logging

logger = logging.getLogger(__name__)

class AutoResponder:
    """Handles automatic responses to terminal prompts"""
    
    def __init__(self):
        self.default_responses = {
            'yes': ['y', 'yes', 'Y', 'YES'],
            'no': ['n', 'no', 'N', 'NO'],
            'accept': ['a', 'accept', 'A', 'ACCEPT'],
            'run': ['r', 'run', 'R', 'RUN'],
            'continue': ['c', 'continue', 'C', 'CONTINUE'],
            'enter': ['', '\n', '\r\n']
        }
    
    def run_with_auto_responses(self, cmd: List[str], responses: List[str] = None, timeout: int = 60) -> Dict:
        """Run command with automatic responses"""
        try:
            if responses is None:
                responses = ['\n'] * 10  # Default: press Enter 10 times
            
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Send responses
            for response in responses:
                try:
                    process.stdin.write(response + '\n')
                    process.stdin.flush()
                    time.sleep(0.5)  # Small delay between responses
                except Exception as e:
                    logger.warning(f"Failed to send response '{response}': {e}")
                    break
            
            # Wait for completion
            stdout, stderr = process.communicate(timeout=timeout)
            
            return {
                'success': process.returncode == 0,
                'returncode': process.returncode,
                'stdout': stdout,
                'stderr': stderr
            }
            
        except subprocess.TimeoutExpired:
            process.kill()
            return {
                'success': False,
                'error': 'Command timed out',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'returncode': -1
            }
    
    def run_interactive_command(self, cmd: List[str], expected_prompts: List[str] = None) -> Dict:
        """Run interactive command with automatic responses"""
        if expected_prompts is None:
            expected_prompts = ['y', 'y', 'y', '\n', '\n', '\n']  # Default responses
        
        return self.run_with_auto_responses(cmd, expected_prompts)
    
    def handle_stuck_process(self, process: subprocess.Popen, max_attempts: int = 5) -> bool:
        """Handle stuck process by sending Enter key multiple times"""
        for attempt in range(max_attempts):
            try:
                process.stdin.write('\n')
                process.stdin.flush()
                time.sleep(1)
                
                # Check if process is still running
                if process.poll() is not None:
                    return True
                    
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
        
        return False
    
    def auto_accept_all(self, cmd: List[str]) -> Dict:
        """Run command with automatic acceptance of all prompts"""
        responses = ['y', 'y', 'y', 'yes', 'accept', 'run', 'continue'] + ['\n'] * 10
        return self.run_with_auto_responses(cmd, responses)
    
    def auto_continue(self, cmd: List[str]) -> Dict:
        """Run command with automatic continuation (Enter key)"""
        responses = ['\n'] * 20  # Press Enter 20 times
        return self.run_with_auto_responses(cmd, responses)

# Global instance
auto_responder = AutoResponder() 