import base64
import os
from cryptography.fernet import Fernet

# Generate or load master encryption key
_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
_FERNET = Fernet(_KEY.encode() if isinstance(_KEY, str) else _KEY)


def encrypt_sensitive_data(plaintext: str) -> str:
    """Encrypt sensitive PII (SSN, Account numbers, Card numbers) using AES-256 (Fernet)."""
    if not plaintext:
        return ""
    return _FERNET.encrypt(plaintext.encode()).decode()


def decrypt_sensitive_data(ciphertext: str) -> str:
    """Decrypt AES-256 encrypted ciphertext back to plaintext."""
    if not ciphertext:
        return ""
    try:
        return _FERNET.decrypt(ciphertext.encode()).decode()
    except Exception:
        return "[ENCRYPTED_DATA]"
