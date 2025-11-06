import os
import base64
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# PASSWORD SERVIZI -> AES-256 #

def derive_key(password: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=64 * 1024,  # 64MB -> resistente alle GPU
        parallelism=2,
        hash_len=32,
        type=Type.ID
    )


def cripta(password_chiara: str, key: bytes) -> str:
    aes = AESGCM(key)
    nonce = os.urandom(12)
    encrypted = aes.encrypt(nonce, password_chiara.encode(), None)
    return base64.b64encode(nonce + encrypted).decode()


def decripta(password_cifrata: str, key: bytes) -> str:
    aes = AESGCM(key)
    data = base64.b64decode(password_cifrata)
    nonce = data[:12]
    ct = data[12:]
    return aes.decrypt(nonce, ct, None).decode()