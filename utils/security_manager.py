"""
Security management utilities for WARP + NextDNS Manager
"""

import os
import ssl
import hashlib
import secrets
import base64
import ipaddress
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import logging
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)

class SecurityManager:
    """Security management for encryption, certificates, and validation"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / '.warp' / 'security'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Security settings
        self.encryption_key = None
        self.certificate_path = self.config_dir / 'certificate.pem'
        self.private_key_path = self.config_dir / 'private_key.pem'
        self.public_key_path = self.config_dir / 'public_key.pem'
        
        # Initialize security components
        self._initialize_security()
    
    def _initialize_security(self):
        """Initialize security components"""
        try:
            # Generate or load encryption key
            self._load_or_generate_encryption_key()
            
            # Generate or load certificates
            self._load_or_generate_certificates()
            
            logger.info("Security manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize security manager: {e}")
    
    def _load_or_generate_encryption_key(self):
        """Load existing encryption key or generate new one"""
        key_file = self.config_dir / 'encryption_key.bin'
        
        if key_file.exists():
            try:
                with open(key_file, 'rb') as f:
                    self.encryption_key = f.read()
                logger.info("Loaded existing encryption key")
            except Exception as e:
                logger.warning(f"Failed to load encryption key: {e}")
                self._generate_encryption_key(key_file)
        else:
            self._generate_encryption_key(key_file)
    
    def _generate_encryption_key(self, key_file: Path):
        """Generate new encryption key"""
        self.encryption_key = secrets.token_bytes(32)  # 256-bit key
        
        try:
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
            
            # Set restrictive permissions
            os.chmod(key_file, 0o600)
            logger.info("Generated new encryption key")
        except Exception as e:
            logger.error(f"Failed to save encryption key: {e}")
    
    def _load_or_generate_certificates(self):
        """Load existing certificates or generate new ones"""
        if (self.certificate_path.exists() and 
            self.private_key_path.exists() and 
            self.public_key_path.exists()):
            try:
                # Validate existing certificates
                if self._validate_certificates():
                    logger.info("Loaded existing certificates")
                    return
                else:
                    logger.warning("Existing certificates are invalid, generating new ones")
            except Exception as e:
                logger.warning(f"Failed to validate certificates: {e}")
        
        self._generate_certificates()
    
    def _generate_certificates(self):
        """Generate new SSL certificates"""
        try:
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            
            # Generate public key
            public_key = private_key.public_key()
            
            # Create certificate
            subject = issuer = x509.Name([
                x509.NameAttribute(x509.NameOID.COUNTRY_NAME, "US"),
                x509.NameAttribute(x509.NameOID.STATE_OR_PROVINCE_NAME, "CA"),
                x509.NameAttribute(x509.NameOID.LOCALITY_NAME, "San Francisco"),
                x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, "WARP NextDNS Manager"),
                x509.NameAttribute(x509.NameOID.COMMON_NAME, "localhost"),
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                public_key
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=365)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName("localhost"),
                    x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                ]),
                critical=False,
            ).sign(private_key, hashes.SHA256(), default_backend())
            
            # Save private key
            with open(self.private_key_path, 'wb') as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            # Save public key
            with open(self.public_key_path, 'wb') as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
            
            # Save certificate
            with open(self.certificate_path, 'wb') as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            
            # Set restrictive permissions
            os.chmod(self.private_key_path, 0o600)
            os.chmod(self.public_key_path, 0o644)
            os.chmod(self.certificate_path, 0o644)
            
            logger.info("Generated new SSL certificates")
            
        except Exception as e:
            logger.error(f"Failed to generate certificates: {e}")
    
    def _validate_certificates(self) -> bool:
        """Validate existing certificates"""
        try:
            # Load certificate
            with open(self.certificate_path, 'rb') as f:
                cert_data = f.read()
            
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            
            # Check if certificate is still valid
            now = datetime.utcnow()
            if now < cert.not_valid_before or now > cert.not_valid_after:
                return False
            
            # Check if certificate expires soon (within 30 days)
            if cert.not_valid_after - now < timedelta(days=30):
                logger.warning("Certificate expires soon")
            
            return True
            
        except Exception as e:
            logger.error(f"Certificate validation failed: {e}")
            return False
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt data using AES-256-GCM"""
        try:
            # Generate random IV
            iv = secrets.token_bytes(12)
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(self.encryption_key),
                modes.GCM(iv),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            
            # Encrypt data
            ciphertext = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
            
            # Combine IV, ciphertext, and tag
            encrypted_data = iv + encryptor.tag + ciphertext
            
            # Return base64 encoded
            return base64.b64encode(encrypted_data).decode('utf-8')
            
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt data using AES-256-GCM"""
        try:
            # Decode base64
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            
            # Extract IV, tag, and ciphertext
            iv = encrypted_bytes[:12]
            tag = encrypted_bytes[12:28]
            ciphertext = encrypted_bytes[28:]
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(self.encryption_key),
                modes.GCM(iv, tag),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            
            # Decrypt data
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            return plaintext.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
    
    def hash_password(self, password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """Hash password using PBKDF2"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Use PBKDF2 with SHA256
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000,  # 100k iterations
            dklen=32
        )
        
        return base64.b64encode(key).decode('utf-8'), salt
    
    def verify_password(self, password: str, hashed_password: str, salt: str) -> bool:
        """Verify password against hash"""
        try:
            computed_hash, _ = self.hash_password(password, salt)
            return secrets.compare_digest(computed_hash, hashed_password)
        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            return False
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate secure random token"""
        return secrets.token_urlsafe(length)
    
    def validate_config_file(self, config_path: Path) -> Dict:
        """Validate configuration file security"""
        results = {
            'valid': True,
            'issues': [],
            'recommendations': []
        }
        
        try:
            if not config_path.exists():
                results['valid'] = False
                results['issues'].append("Configuration file does not exist")
                return results
            
            # Check file permissions
            stat = config_path.stat()
            mode = stat.st_mode & 0o777
            
            if mode != 0o600:
                results['issues'].append(f"Configuration file has insecure permissions: {oct(mode)}")
                results['recommendations'].append("Set file permissions to 600")
            
            # Check file content
            with open(config_path, 'r') as f:
                content = f.read()
            
            # Check for sensitive data in plain text
            sensitive_patterns = [
                'password',
                'secret',
                'key',
                'token',
                'api_key'
            ]
            
            for pattern in sensitive_patterns:
                if pattern in content.lower():
                    results['issues'].append(f"Potential sensitive data found: {pattern}")
                    results['recommendations'].append(f"Encrypt or remove sensitive data: {pattern}")
            
            if results['issues']:
                results['valid'] = False
            
        except Exception as e:
            results['valid'] = False
            results['issues'].append(f"Validation error: {e}")
        
        return results
    
    def secure_config_file(self, config_path: Path, sensitive_keys: List[str]) -> bool:
        """Secure configuration file by encrypting sensitive data"""
        try:
            if not config_path.exists():
                return False
            
            # Read current config
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            # Encrypt sensitive values
            modified = False
            for key in sensitive_keys:
                if key in config_data and isinstance(config_data[key], str):
                    if not config_data[key].startswith('encrypted:'):
                        encrypted_value = self.encrypt_data(config_data[key])
                        config_data[key] = f"encrypted:{encrypted_value}"
                        modified = True
            
            # Save encrypted config
            if modified:
                with open(config_path, 'w') as f:
                    json.dump(config_data, f, indent=2)
                
                # Set secure permissions
                os.chmod(config_path, 0o600)
                logger.info(f"Secured configuration file: {config_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to secure configuration file: {e}")
            return False
    
    def get_security_report(self) -> Dict:
        """Generate security report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'encryption_key': {
                'exists': self.encryption_key is not None,
                'length': len(self.encryption_key) if self.encryption_key else 0
            },
            'certificates': {
                'certificate_exists': self.certificate_path.exists(),
                'private_key_exists': self.private_key_path.exists(),
                'public_key_exists': self.public_key_path.exists(),
                'valid': self._validate_certificates() if self.certificate_path.exists() else False
            },
            'file_permissions': {},
            'recommendations': []
        }
        
        # Check file permissions
        for file_path in [self.certificate_path, self.private_key_path, self.public_key_path]:
            if file_path.exists():
                stat = file_path.stat()
                mode = stat.st_mode & 0o777
                report['file_permissions'][file_path.name] = {
                    'permissions': oct(mode),
                    'secure': mode == 0o600 or mode == 0o644
                }
        
        # Generate recommendations
        if not report['encryption_key']['exists']:
            report['recommendations'].append("Encryption key is missing")
        
        if not report['certificates']['valid']:
            report['recommendations'].append("SSL certificates are invalid or missing")
        
        for file_name, perm_info in report['file_permissions'].items():
            if not perm_info['secure']:
                report['recommendations'].append(f"File {file_name} has insecure permissions")
        
        if not report['recommendations']:
            report['recommendations'].append("Security configuration is good")
        
        return report
    
    def cleanup_old_files(self, max_age_days: int = 30):
        """Clean up old security files"""
        try:
            current_time = datetime.now()
            cleaned_files = []
            
            for file_path in self.config_dir.glob('*'):
                if file_path.is_file():
                    file_age = current_time - datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_age.days > max_age_days:
                        file_path.unlink()
                        cleaned_files.append(file_path.name)
            
            if cleaned_files:
                logger.info(f"Cleaned up old security files: {cleaned_files}")
            
        except Exception as e:
            logger.error(f"Failed to cleanup old files: {e}")

# Global security manager instance
security_manager = SecurityManager() 