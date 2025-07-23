"""
Backup and restore management for WARP + NextDNS Manager
"""

import os
import json
import shutil
import zipfile
import tarfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
import hashlib

logger = logging.getLogger(__name__)

class BackupManager:
    """Backup and restore management system"""
    
    def __init__(self, backup_dir: Optional[Path] = None):
        self.backup_dir = backup_dir or Path.home() / '.warp' / 'backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup configuration
        self.backup_config = {
            'max_backups': 10,
            'auto_backup': True,
            'backup_interval_hours': 24,
            'include_logs': True,
            'include_security': True,
            'compression': True
        }
        
        # Load backup configuration
        self._load_backup_config()
    
    def _load_backup_config(self):
        """Load backup configuration from file"""
        config_file = self.backup_dir / 'backup_config.json'
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.backup_config.update(saved_config)
            except Exception as e:
                logger.warning(f"Failed to load backup config: {e}")
    
    def _save_backup_config(self):
        """Save backup configuration to file"""
        config_file = self.backup_dir / 'backup_config.json'
        
        try:
            with open(config_file, 'w') as f:
                json.dump(self.backup_config, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save backup config: {e}")
    
    def create_backup(self, description: str = "", include_logs: bool = None, 
                     include_security: bool = None) -> Dict:
        """Create a new backup"""
        try:
            # Use default values if not specified
            if include_logs is None:
                include_logs = self.backup_config['include_logs']
            if include_security is None:
                include_security = self.backup_config['include_security']
            
            # Create backup timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"warp_nextdns_backup_{timestamp}"
            backup_path = self.backup_dir / backup_name
            
            # Create backup directory
            backup_path.mkdir(exist_ok=True)
            
            # Backup metadata
            metadata = {
                'timestamp': datetime.now().isoformat(),
                'description': description,
                'version': '1.0.0',
                'platform': os.name,
                'include_logs': include_logs,
                'include_security': include_security,
                'files': []
            }
            
            # Backup WireGuard configuration
            self._backup_wireguard_config(backup_path, metadata)
            
            # Backup NextDNS configuration
            self._backup_nextdns_config(backup_path, metadata)
            
            # Backup logs if requested
            if include_logs:
                self._backup_logs(backup_path, metadata)
            
            # Backup security files if requested
            if include_security:
                self._backup_security_files(backup_path, metadata)
            
            # Backup application configuration
            self._backup_app_config(backup_path, metadata)
            
            # Save metadata
            with open(backup_path / 'metadata.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Create compressed archive
            archive_path = self._create_archive(backup_path, backup_name)
            
            # Clean up temporary directory
            shutil.rmtree(backup_path)
            
            # Update backup list
            self._cleanup_old_backups()
            
            logger.info(f"Backup created successfully: {archive_path}")
            
            return {
                'success': True,
                'backup_path': str(archive_path),
                'backup_name': backup_name,
                'metadata': metadata
            }
            
        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _backup_wireguard_config(self, backup_path: Path, metadata: Dict):
        """Backup WireGuard configuration"""
        wireguard_dir = Path('/etc/wireguard')
        if os.name == 'nt':  # Windows
            wireguard_dir = Path.home() / '.warp' / 'wireguard'
        
        if wireguard_dir.exists():
            backup_wg_dir = backup_path / 'wireguard'
            backup_wg_dir.mkdir(exist_ok=True)
            
            for file_path in wireguard_dir.glob('*'):
                if file_path.is_file():
                    try:
                        shutil.copy2(file_path, backup_wg_dir / file_path.name)
                        metadata['files'].append(f"wireguard/{file_path.name}")
                    except Exception as e:
                        logger.warning(f"Failed to backup {file_path}: {e}")
    
    def _backup_nextdns_config(self, backup_path: Path, metadata: Dict):
        """Backup NextDNS configuration"""
        nextdns_configs = [
            Path('/etc/nextdns.conf'),
            Path.home() / '.nextdns.conf',
            Path.home() / '.warp' / 'nextdns' / 'nextdns.conf'
        ]
        
        backup_nd_dir = backup_path / 'nextdns'
        backup_nd_dir.mkdir(exist_ok=True)
        
        for config_path in nextdns_configs:
            if config_path.exists():
                try:
                    shutil.copy2(config_path, backup_nd_dir / config_path.name)
                    metadata['files'].append(f"nextdns/{config_path.name}")
                except Exception as e:
                    logger.warning(f"Failed to backup {config_path}: {e}")
    
    def _backup_logs(self, backup_path: Path, metadata: Dict):
        """Backup log files"""
        log_dirs = [
            Path('/var/log/warp-nextdns'),
            Path.home() / '.warp' / 'logs'
        ]
        
        backup_logs_dir = backup_path / 'logs'
        backup_logs_dir.mkdir(exist_ok=True)
        
        for log_dir in log_dirs:
            if log_dir.exists():
                try:
                    for log_file in log_dir.glob('*.log'):
                        shutil.copy2(log_file, backup_logs_dir / log_file.name)
                        metadata['files'].append(f"logs/{log_file.name}")
                except Exception as e:
                    logger.warning(f"Failed to backup logs from {log_dir}: {e}")
    
    def _backup_security_files(self, backup_path: Path, metadata: Dict):
        """Backup security files"""
        security_dir = Path.home() / '.warp' / 'security'
        
        if security_dir.exists():
            backup_sec_dir = backup_path / 'security'
            backup_sec_dir.mkdir(exist_ok=True)
            
            try:
                for file_path in security_dir.glob('*'):
                    if file_path.is_file():
                        shutil.copy2(file_path, backup_sec_dir / file_path.name)
                        metadata['files'].append(f"security/{file_path.name}")
            except Exception as e:
                logger.warning(f"Failed to backup security files: {e}")
    
    def _backup_app_config(self, backup_path: Path, metadata: Dict):
        """Backup application configuration"""
        config_files = [
            Path('config.py'),
            Path('requirements.txt'),
            Path('setup.py')
        ]
        
        backup_config_dir = backup_path / 'config'
        backup_config_dir.mkdir(exist_ok=True)
        
        for config_file in config_files:
            if config_file.exists():
                try:
                    shutil.copy2(config_file, backup_config_dir / config_file.name)
                    metadata['files'].append(f"config/{config_file.name}")
                except Exception as e:
                    logger.warning(f"Failed to backup {config_file}: {e}")
    
    def _create_archive(self, backup_path: Path, backup_name: str) -> Path:
        """Create compressed archive from backup"""
        archive_path = self.backup_dir / f"{backup_name}.tar.gz"
        
        if self.backup_config['compression']:
            with tarfile.open(archive_path, 'w:gz') as tar:
                tar.add(backup_path, arcname=backup_name)
        else:
            # Create zip archive as fallback
            archive_path = self.backup_dir / f"{backup_name}.zip"
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in backup_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(backup_path)
                        zipf.write(file_path, arcname)
        
        return archive_path
    
    def restore_backup(self, backup_path: Path, restore_location: Optional[Path] = None) -> Dict:
        """Restore from backup"""
        try:
            if not backup_path.exists():
                return {
                    'success': False,
                    'error': 'Backup file not found'
                }
            
            # Extract backup
            temp_dir = self.backup_dir / f"restore_temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            temp_dir.mkdir(exist_ok=True)
            
            # Extract archive
            if backup_path.suffix == '.tar.gz':
                with tarfile.open(backup_path, 'r:gz') as tar:
                    tar.extractall(temp_dir)
            elif backup_path.suffix == '.zip':
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    zipf.extractall(temp_dir)
            else:
                return {
                    'success': False,
                    'error': 'Unsupported backup format'
                }
            
            # Find backup directory
            backup_dirs = list(temp_dir.iterdir())
            if not backup_dirs or not backup_dirs[0].is_dir():
                return {
                    'success': False,
                    'error': 'Invalid backup structure'
                }
            
            backup_dir = backup_dirs[0]
            
            # Load metadata
            metadata_file = backup_dir / 'metadata.json'
            if not metadata_file.exists():
                return {
                    'success': False,
                    'error': 'Backup metadata not found'
                }
            
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            # Restore files
            restore_location = restore_location or Path.home() / '.warp'
            restore_location.mkdir(parents=True, exist_ok=True)
            
            restored_files = []
            
            # Restore WireGuard configuration
            wg_backup = backup_dir / 'wireguard'
            if wg_backup.exists():
                wg_restore = restore_location / 'wireguard'
                wg_restore.mkdir(exist_ok=True)
                
                for file_path in wg_backup.glob('*'):
                    if file_path.is_file():
                        shutil.copy2(file_path, wg_restore / file_path.name)
                        restored_files.append(f"wireguard/{file_path.name}")
            
            # Restore NextDNS configuration
            nd_backup = backup_dir / 'nextdns'
            if nd_backup.exists():
                nd_restore = restore_location / 'nextdns'
                nd_restore.mkdir(exist_ok=True)
                
                for file_path in nd_backup.glob('*'):
                    if file_path.is_file():
                        shutil.copy2(file_path, nd_restore / file_path.name)
                        restored_files.append(f"nextdns/{file_path.name}")
            
            # Restore logs
            logs_backup = backup_dir / 'logs'
            if logs_backup.exists():
                logs_restore = restore_location / 'logs'
                logs_restore.mkdir(exist_ok=True)
                
                for file_path in logs_backup.glob('*'):
                    if file_path.is_file():
                        shutil.copy2(file_path, logs_restore / file_path.name)
                        restored_files.append(f"logs/{file_path.name}")
            
            # Restore security files
            sec_backup = backup_dir / 'security'
            if sec_backup.exists():
                sec_restore = restore_location / 'security'
                sec_restore.mkdir(exist_ok=True)
                
                for file_path in sec_backup.glob('*'):
                    if file_path.is_file():
                        shutil.copy2(file_path, sec_restore / file_path.name)
                        restored_files.append(f"security/{file_path.name}")
            
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
            
            logger.info(f"Backup restored successfully: {len(restored_files)} files")
            
            return {
                'success': True,
                'restored_files': restored_files,
                'metadata': metadata,
                'restore_location': str(restore_location)
            }
            
        except Exception as e:
            logger.error(f"Backup restoration failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_backups(self) -> List[Dict]:
        """List available backups"""
        backups = []
        
        for backup_file in self.backup_dir.glob('*.tar.gz'):
            backup_info = self._get_backup_info(backup_file)
            if backup_info:
                backups.append(backup_info)
        
        for backup_file in self.backup_dir.glob('*.zip'):
            backup_info = self._get_backup_info(backup_file)
            if backup_info:
                backups.append(backup_info)
        
        # Sort by created timestamp (newest first)
        backups.sort(key=lambda x: x['created'], reverse=True)
        
        return backups
    
    def _get_backup_info(self, backup_path: Path) -> Optional[Dict]:
        """Get information about a backup file"""
        try:
            stat = backup_path.stat()
            
            # Try to extract metadata
            metadata = None
            temp_dir = None
            
            try:
                temp_dir = self.backup_dir / f"temp_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                temp_dir.mkdir(exist_ok=True)
                
                if backup_path.suffix == '.tar.gz':
                    with tarfile.open(backup_path, 'r:gz') as tar:
                        # Find metadata file
                        for member in tar.getmembers():
                            if member.name.endswith('metadata.json'):
                                tar.extract(member, temp_dir)
                                metadata_file = temp_dir / member.name
                                with open(metadata_file, 'r') as f:
                                    metadata = json.load(f)
                                break
                elif backup_path.suffix == '.zip':
                    with zipfile.ZipFile(backup_path, 'r') as zipf:
                        # Find metadata file
                        for name in zipf.namelist():
                            if name.endswith('metadata.json'):
                                zipf.extract(name, temp_dir)
                                metadata_file = temp_dir / name
                                with open(metadata_file, 'r') as f:
                                    metadata = json.load(f)
                                break
            except Exception as e:
                logger.debug(f"Failed to extract metadata from {backup_path}: {e}")
            finally:
                if temp_dir and temp_dir.exists():
                    shutil.rmtree(temp_dir)
            
            return {
                'filename': backup_path.name,
                'path': str(backup_path),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'metadata': metadata
            }
            
        except Exception as e:
            logger.warning(f"Failed to get info for {backup_path}: {e}")
            return None
    
    def delete_backup(self, backup_path: Path) -> bool:
        """Delete a backup file"""
        try:
            if backup_path.exists():
                backup_path.unlink()
                logger.info(f"Backup deleted: {backup_path}")
                return True
            else:
                logger.warning(f"Backup not found: {backup_path}")
                return False
        except Exception as e:
            logger.error(f"Failed to delete backup {backup_path}: {e}")
            return False
    
    def _cleanup_old_backups(self):
        """Clean up old backups based on configuration"""
        backups = self.list_backups()
        
        if len(backups) > self.backup_config['max_backups']:
            # Remove oldest backups
            backups_to_remove = backups[self.backup_config['max_backups']:]
            
            for backup in backups_to_remove:
                backup_path = Path(backup['path'])
                self.delete_backup(backup_path)
    
    def verify_backup(self, backup_path: Path) -> Dict:
        """Verify backup integrity"""
        try:
            if not backup_path.exists():
                return {
                    'valid': False,
                    'error': 'Backup file not found'
                }
            
            # Check file size
            stat = backup_path.stat()
            if stat.st_size == 0:
                return {
                    'valid': False,
                    'error': 'Backup file is empty'
                }
            
            # Try to extract and verify structure
            temp_dir = self.backup_dir / f"verify_temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            temp_dir.mkdir(exist_ok=True)
            
            try:
                if backup_path.suffix == '.tar.gz':
                    with tarfile.open(backup_path, 'r:gz') as tar:
                        tar.extractall(temp_dir)
                elif backup_path.suffix == '.zip':
                    with zipfile.ZipFile(backup_path, 'r') as zipf:
                        zipf.extractall(temp_dir)
                else:
                    return {
                        'valid': False,
                        'error': 'Unsupported backup format'
                    }
                
                # Check for metadata file
                backup_dirs = list(temp_dir.iterdir())
                if not backup_dirs:
                    return {
                        'valid': False,
                        'error': 'Backup is empty'
                    }
                
                backup_dir = backup_dirs[0]
                metadata_file = backup_dir / 'metadata.json'
                
                if not metadata_file.exists():
                    return {
                        'valid': False,
                        'error': 'Backup metadata not found'
                    }
                
                # Load and validate metadata
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                # Check required fields
                required_fields = ['timestamp', 'version', 'files']
                for field in required_fields:
                    if field not in metadata:
                        return {
                            'valid': False,
                            'error': f'Missing required field: {field}'
                        }
                
                # Verify files exist
                missing_files = []
                for file_path in metadata['files']:
                    full_path = backup_dir / file_path
                    if not full_path.exists():
                        missing_files.append(file_path)
                
                if missing_files:
                    return {
                        'valid': False,
                        'error': f'Missing files in backup: {missing_files}'
                    }
                
                return {
                    'valid': True,
                    'metadata': metadata,
                    'file_count': len(metadata['files'])
                }
                
            finally:
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def get_backup_stats(self) -> Dict:
        """Get backup statistics"""
        backups = self.list_backups()
        
        total_size = sum(backup['size'] for backup in backups)
        total_count = len(backups)
        
        if total_count > 0:
            avg_size = total_size / total_count
            oldest_backup = min(backups, key=lambda x: x['created'])
            newest_backup = max(backups, key=lambda x: x['created'])
        else:
            avg_size = 0
            oldest_backup = None
            newest_backup = None
        
        return {
            'total_backups': total_count,
            'total_size': total_size,
            'average_size': avg_size,
            'oldest_backup': oldest_backup['created'] if oldest_backup else None,
            'newest_backup': newest_backup['created'] if newest_backup else None,
            'backup_dir': str(self.backup_dir),
            'max_backups': self.backup_config['max_backups']
        }

# Global backup manager instance
backup_manager = BackupManager() 