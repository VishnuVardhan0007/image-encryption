# Image Encryption

A professional Python tool for encrypting and decrypting images using AES encryption with multiple cipher modes and random Initialization Vectors (IVs).

## Features

- **Secure Encryption**: AES-256 encryption with multiple cipher modes (CBC, CFB, OFB, CTR)
- **Random IVs**: Each image gets a unique random IV for enhanced security
- **Key Management**: Secure key generation and storage
- **Multiple Modes**: Support for different modes of operation to understand tradeoffs

## Requirements

- Python 3.7+
- `cryptography` library
- `Pillow` library

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Encrypt an Image

```bash
python cli.py encrypt input.jpg encrypted.bin --mode CBC --save-key key.bin
```

This will:
- Encrypt `input.jpg` using CBC mode
- Save the encrypted image to `encrypted.bin`
- Generate a random key and save it to `key.bin`
- Generate a random IV for this encryption

### Decrypt an Image

```bash
python cli.py decrypt encrypted.bin decrypted.jpg --mode CBC --key key.bin
```

This will:
- Decrypt `encrypted.bin` using the provided key
- Save the decrypted image to `decrypted.jpg`
- Use the same cipher mode as encryption

### Available Cipher Modes

- **CBC** (Cipher Block Chaining): Default mode, requires padding
- **CFB** (Cipher Feedback): Stream cipher mode
- **OFB** (Output Feedback): Stream cipher mode
- **CTR** (Counter): Stream cipher mode, no padding needed

## Programmatic Usage

```python
from image_encryption import ImageEncryptor

# Create encryptor (generates random key)
encryptor = ImageEncryptor(mode='CBC')

# Encrypt image
encryptor.encrypt_image('input.jpg', 'encrypted.bin')

# Save key for later use
encryptor.save_key('key.bin')

# Decrypt image
decryptor = ImageEncryptor(key=ImageEncryptor.load_key('key.bin'), mode='CBC')
decryptor.decrypt_image('encrypted.bin', 'decrypted.jpg')
```

## Security Notes

- **Key Security**: Always store encryption keys securely. Never commit keys to version control.
- **IV Storage**: IVs are automatically prepended to encrypted files for convenience.
- **Mode Selection**: Different modes have different security properties:
  - CBC: Good general-purpose mode, but requires padding
  - CFB/OFB: Stream-like operation, good for real-time encryption
  - CTR: Parallelizable, no padding needed, but requires unique nonces

## Learning Outcomes

- Binary data encryption with AES
- Secure key handling practices
- Understanding tradeoffs between different modes of operation
- IV/nonce management in cryptography
