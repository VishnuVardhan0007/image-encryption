"""
Image Encryption Module
Supports multiple cipher modes with random IVs for secure image encryption.
"""

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from PIL import Image
import secrets


class ImageEncryptor:
    """Handles image encryption and decryption with multiple cipher modes."""
    
    # Supported cipher modes
    MODES = {
        'CBC': modes.CBC,
        'CFB': modes.CFB,
        'OFB': modes.OFB,
        'CTR': modes.CTR,
    }
    
    def __init__(self, key: bytes = None, mode: str = 'CBC'):
        """
        Initialize the encryptor.
        
        Args:
            key: Encryption key (32 bytes for AES-256). If None, generates a random key.
            mode: Cipher mode ('CBC', 'CFB', 'OFB', or 'CTR')
        """
        if key is None:
            key = secrets.token_bytes(32)  # AES-256 key
        
        if len(key) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes (AES-128, AES-192, or AES-256)")
        
        if mode not in self.MODES:
            raise ValueError(f"Mode must be one of: {', '.join(self.MODES.keys())}")
        
        self.key = key
        self.mode_name = mode
        self.backend = default_backend()
    
    def _generate_iv(self) -> bytes:
        """Generate a random 16-byte IV."""
        return secrets.token_bytes(16)
    
    def _pad_data(self, data: bytes) -> bytes:
        """Pad data to block size for block cipher modes."""
        padder = padding.PKCS7(128).padder()
        return padder.update(data) + padder.finalize()
    
    def _unpad_data(self, data: bytes) -> bytes:
        """Remove padding from decrypted data."""
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(data) + unpadder.finalize()
    
    def encrypt_image(self, image_path: str, output_path: str) -> bytes:
        """
        Encrypt an image file.
        
        Args:
            image_path: Path to the input image
            output_path: Path to save the encrypted image
            
        Returns:
            IV used for encryption (needed for decryption)
        """
        # Read image as bytes
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # Generate random IV
        iv = self._generate_iv()
        
        # Create cipher
        mode_class = self.MODES[self.mode_name]
        
        # For CTR mode, use nonce instead of IV
        if self.mode_name == 'CTR':
            cipher = Cipher(
                algorithms.AES(self.key),
                mode_class(iv),
                backend=self.backend
            )
        else:
            cipher = Cipher(
                algorithms.AES(self.key),
                mode_class(iv),
                backend=self.backend
            )
        
        encryptor = cipher.encryptor()
        
        # Pad data for block cipher modes (except CTR)
        if self.mode_name != 'CTR':
            image_data = self._pad_data(image_data)
        
        # Encrypt
        encrypted_data = encryptor.update(image_data) + encryptor.finalize()
        
        # Save encrypted image with IV prepended
        with open(output_path, 'wb') as f:
            f.write(iv + encrypted_data)
        
        return iv
    
    def decrypt_image(self, encrypted_path: str, output_path: str) -> None:
        """
        Decrypt an image file.
        
        Args:
            encrypted_path: Path to the encrypted image
            output_path: Path to save the decrypted image
        """
        # Read encrypted data
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Extract IV (first 16 bytes) and encrypted content
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Create cipher
        mode_class = self.MODES[self.mode_name]
        cipher = Cipher(
            algorithms.AES(self.key),
            mode_class(iv),
            backend=self.backend
        )
        
        decryptor = cipher.decryptor()
        
        # Decrypt
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding for block cipher modes (except CTR)
        if self.mode_name != 'CTR':
            decrypted_data = self._unpad_data(decrypted_data)
        
        # Save decrypted image
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
    
    def save_key(self, key_path: str) -> None:
        """Save the encryption key to a file."""
        with open(key_path, 'wb') as f:
            f.write(self.key)
    
    @staticmethod
    def load_key(key_path: str) -> bytes:
        """Load an encryption key from a file."""
        with open(key_path, 'rb') as f:
            return f.read()
    
    def get_key_hex(self) -> str:
        """Get the encryption key as a hexadecimal string."""
        return self.key.hex()
