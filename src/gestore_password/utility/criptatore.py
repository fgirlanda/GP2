import os
import base64
from argon2.low_level import hash_secret_raw, Type
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# PASSWORD SERVIZI -> AES-256 #

def derive_key(password_utente: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=password_utente.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=64 * 1024,  # 64MB -> resistente alle GPU
        parallelism=2,
        hash_len=32,
        type=Type.ID
    )


def cripta(password_servizio: str, key: bytes) -> str:
    aes = AESGCM(key)
    nonce = os.urandom(12)
    encrypted = aes.encrypt(nonce, password_servizio.encode(), None)
    return base64.b64encode(nonce + encrypted).decode()


def decripta(password_servizio_cifrata: str, key: bytes) -> str:
    aes = AESGCM(key)
    data = base64.b64decode(password_servizio_cifrata)
    nonce = data[:12]
    ct = data[12:]
    return aes.decrypt(nonce, ct, None).decode()

# PASSWORD MASTER

ph = PasswordHasher(
time_cost=3,       # numero di iterazioni
memory_cost=64 * 1024,  # 64 MB di RAM
parallelism=2,     # thread
hash_len=32,       # lunghezza hash
salt_len=16        # salt automatico
)
def genera_hash(password_utente):
    return ph.hash(password_utente)

def verifica_password(password_inserita, hash_salvato):
    try:
        return ph.verify(hash_salvato, password_inserita)
    except Exception:
        return False