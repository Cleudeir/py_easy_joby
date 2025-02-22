from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from dotenv import load_dotenv
import os
import base64
import hashlib

# Load environment variables from .env file
load_dotenv()

def get_encryption_key() -> bytes:
    """
    Retrieves and derives a 32-byte AES encryption key from the environment variable.

    Returns:
    - bytes: The 32-byte encryption key.

    Raises:
    - ValueError: If the encryption key is missing or improperly formatted.
    """
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("ENCRYPTION_KEY not found in .env file.")
    
    # Ensure key is 32 bytes (AES-256 requires 32-byte key)
    return hashlib.sha256(key.encode()).digest()

def encrypt_folder(folder_path: str) -> str:  
    key = get_encryption_key()  # Retrieve encryption key
    cipher = AES.new(key, AES.MODE_ECB)  # Use AES in ECB mode
    padded_data = pad(folder_path.encode(), AES.block_size)  # Pad input to match AES block size
    encrypted_path = cipher.encrypt(padded_data)  # Encrypt data
    return base64.urlsafe_b64encode(encrypted_path).decode()  # Encode to Base64 for storage

def decrypt_folder(encrypted_folder_path: str) -> str:    
    key = get_encryption_key()  # Retrieve encryption key
    cipher = AES.new(key, AES.MODE_ECB)  # Use AES in ECB mode
    encrypted_data = base64.urlsafe_b64decode(encrypted_folder_path)  # Decode Base64
    decrypted_path = unpad(cipher.decrypt(encrypted_data), AES.block_size)  # Decrypt and remove padding
    return decrypted_path.decode()

