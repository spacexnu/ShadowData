import pytest
from cryptography.fernet import Fernet, InvalidToken
from shadow_data.exceptions import CipherKeyNotFoundError, InvalidCipherKeyError
from shadow_data.cryptohash.symmetric_cipher import Symmetric


class TestSymmetric:
    def test_init_with_valid_cipher_key(self):
        key = Fernet.generate_key()
        symmetric = Symmetric(key)
        assert symmetric.cipher_key == key

    def test_create_key(self):
        symmetric = Symmetric()
        key = symmetric.create_key()
        assert isinstance(key, bytes)
        assert symmetric.cipher_key == key

    def test_set_valid_cipher_key(self):
        symmetric = Symmetric()
        key = Fernet.generate_key()
        symmetric.cipher_key = key
        assert symmetric.cipher_key == key

    def test_set_invalid_cipher_key(self):
        symmetric = Symmetric()
        with pytest.raises(InvalidCipherKeyError):
            symmetric.cipher_key = b'invalid_key'

    def test_encrypt_decrypt(self):
        symmetric = Symmetric()
        symmetric.create_key()
        plaintext = 'Hello, World!'
        ciphertext = symmetric.encrypt(plaintext)
        assert isinstance(ciphertext, bytes)
        decrypted_text = symmetric.decrypt(ciphertext)
        assert decrypted_text == plaintext

    def test_encrypt_without_key(self):
        symmetric = Symmetric()
        with pytest.raises(CipherKeyNotFoundError):
            symmetric.encrypt('Hello, World!')

    def test_decrypt_without_key(self):
        symmetric = Symmetric()
        with pytest.raises(CipherKeyNotFoundError):
            symmetric.decrypt(b'some_ciphertext')

    def test_decrypt_invalid_ciphertext(self):
        symmetric = Symmetric()
        symmetric.create_key()
        with pytest.raises(InvalidToken):
            symmetric.decrypt(b'invalid_ciphertext')

    def test_encrypt_with_existent_key(self):
        symmetric = Symmetric()
        key = Fernet.generate_key()
        content = 'Hello, World!'
        symmetric.cipher_key = key
        encrypted_content = symmetric.encrypt(content)
        assert symmetric.cipher_key == key
        assert symmetric.decrypt(encrypted_content) == content

    def test_get_cipher_key(self):
        symmetric = Symmetric()
        key = symmetric.create_key()
        assert symmetric.cipher_key == key
