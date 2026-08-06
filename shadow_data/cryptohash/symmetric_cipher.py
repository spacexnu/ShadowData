from cryptography.fernet import Fernet, InvalidToken

from shadow_data.exceptions import CipherKeyNotFoundError, InvalidCipherKeyError


class Symmetric:
    def __init__(self, cipher_key: bytes | None = None):
        if cipher_key is not None:
            self._validate_cipher_key(cipher_key)
        self._cipher_key = cipher_key

    def create_key(self) -> bytes:
        self._cipher_key = Fernet.generate_key()
        return self._cipher_key

    @property
    def cipher_key(self) -> bytes | None:
        return self._cipher_key

    @cipher_key.setter
    def cipher_key(self, key: bytes) -> None:
        self._validate_cipher_key(key)
        self._cipher_key = key

    def encrypt(self, plaintext: str) -> bytes:
        fernet = self._get_fernet_instance()
        return fernet.encrypt(plaintext.encode())

    def decrypt(self, ciphertext: bytes) -> str:
        fernet = self._get_fernet_instance()
        return fernet.decrypt(ciphertext).decode()

    def _get_fernet_instance(self) -> Fernet:
        return Fernet(self._check_cipher_key())

    def _check_cipher_key(self) -> bytes:
        if not self._cipher_key:
            raise CipherKeyNotFoundError()
        return self._cipher_key

    def _validate_cipher_key(self, key: bytes) -> None:
        try:
            Fernet(key)
        except (ValueError, InvalidToken) as error:
            raise InvalidCipherKeyError() from error
