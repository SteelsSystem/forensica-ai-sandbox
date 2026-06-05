import base64, hashlib, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from config.settings import settings

def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
    return kdf.derive(password)

def encrypt(plaintext: str) -> str:
    salt = os.urandom(16); key = derive_key(settings.encryption_key.encode(), salt)
    nonce = os.urandom(12)
    ct = AESGCM(key).encrypt(nonce, plaintext.encode(), None)
    return base64.urlsafe_b64encode(salt + nonce + ct).decode()

def decrypt(token: str) -> str:
    blob = base64.urlsafe_b64decode(token.encode())
    salt, nonce, ct = blob[:16], blob[16:28], blob[28:]
    return AESGCM(derive_key(settings.encryption_key.encode(), salt)).decrypt(nonce, ct, None).decode()

def hash_fact(payload: str) -> str:
    return hashlib.sha256(payload.encode()).hexdigest()
