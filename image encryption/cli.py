"""
Command-line interface for image encryption/decryption.
"""

import argparse
import sys
from pathlib import Path
from image_encryption import ImageEncryptor


def main():
    parser = argparse.ArgumentParser(
        description='Encrypt or decrypt images with multiple cipher modes'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt an image')
    encrypt_parser.add_argument('input', help='Input image path')
    encrypt_parser.add_argument('output', help='Output encrypted image path')
    encrypt_parser.add_argument(
        '--mode',
        choices=['CBC', 'CFB', 'OFB', 'CTR'],
        default='CBC',
        help='Cipher mode (default: CBC)'
    )
    encrypt_parser.add_argument(
        '--key',
        help='Encryption key file path (if not provided, generates a new key)'
    )
    encrypt_parser.add_argument(
        '--save-key',
        help='Path to save the encryption key'
    )
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt an image')
    decrypt_parser.add_argument('input', help='Input encrypted image path')
    decrypt_parser.add_argument('output', help='Output decrypted image path')
    decrypt_parser.add_argument(
        '--mode',
        choices=['CBC', 'CFB', 'OFB', 'CTR'],
        default='CBC',
        help='Cipher mode (must match encryption mode)'
    )
    decrypt_parser.add_argument(
        '--key',
        required=True,
        help='Encryption key file path'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'encrypt':
            # Load or generate key
            if args.key:
                key = ImageEncryptor.load_key(args.key)
            else:
                key = None
            
            # Create encryptor
            encryptor = ImageEncryptor(key=key, mode=args.mode)
            
            # Encrypt image
            iv = encryptor.encrypt_image(args.input, args.output)
            
            print(f"[OK] Image encrypted successfully!")
            print(f"  Input: {args.input}")
            print(f"  Output: {args.output}")
            print(f"  Mode: {args.mode}")
            print(f"  IV: {iv.hex()}")
            
            # Save key if requested
            if args.save_key:
                encryptor.save_key(args.save_key)
                print(f"  Key saved to: {args.save_key}")
            else:
                print(f"  Key (hex): {encryptor.get_key_hex()}")
                print("  [WARNING] Save this key securely! You'll need it for decryption.")
        
        elif args.command == 'decrypt':
            # Load key
            key = ImageEncryptor.load_key(args.key)
            
            # Create encryptor (with same mode)
            encryptor = ImageEncryptor(key=key, mode=args.mode)
            
            # Decrypt image
            encryptor.decrypt_image(args.input, args.output)
            
            print(f"[OK] Image decrypted successfully!")
            print(f"  Input: {args.input}")
            print(f"  Output: {args.output}")
            print(f"  Mode: {args.mode}")
    
    except FileNotFoundError as e:
        print(f"[ERROR] File not found - {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
