import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64, hashlib

class Crypto:
    def __init__(self):
        # cryption
        self.fernet = None

    def _keyGen_kdf(self, password):
        ascii_pwd = password.encode('ascii')
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(ascii_pwd))
        self.fernet = Fernet(key)
    def _keyGen_md5(self, password):
        ascii_pwd = password.encode('ascii')
        # def gen_fernet_key(passcode:bytes) -> bytes:
        # assert isinstance(passcode, bytes)
        hlib = hashlib.md5()
        hlib.update(ascii_pwd)
        key = base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))
        self.fernet = Fernet(key)
    def keyGen(self, password):
        self._keyGen_md5(password)
    def encrypt(self, byte_content):
        encMessage = self.fernet.encrypt(byte_content)
        return encMessage
    def decrypt(self, byte_content):
        decMessage = self.fernet.decrypt(byte_content)
        return decMessage

