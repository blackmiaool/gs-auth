import hashlib
from cryptography.fernet import Fernet
import base64


def key2bytes(key: str):
    result = hashlib.sha256(key.encode('utf-8'))
    return base64.urlsafe_b64encode(result.digest())


def encrypt(key: str, content: str):
    f = Fernet(key2bytes(key))
    return f.encrypt(str.encode(content)).decode("utf-8")


def decrypt(key: str, content: str):
    f = Fernet(key2bytes(key))
    return f.decrypt(str.encode(content)).decode("utf-8")
