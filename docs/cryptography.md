# Cryptography

ShadowData provides symmetric encryption using Fernet from the `cryptography` package.

## Generate and use a key

```python
from shadow_data.cryptohash.symmetric_cipher import Symmetric

symmetric = Symmetric()
key = symmetric.create_key()

ciphertext = symmetric.encrypt("Hello World!")
plaintext = symmetric.decrypt(ciphertext)

print(key)
print(ciphertext)
print(plaintext)
```

## Use an existing key

```python
from shadow_data.cryptohash.symmetric_cipher import Symmetric

key = b"bpSGcODTJ1iOwxloIQJrAiYDRaqyypdCsQfg1EwVOTc="

symmetric = Symmetric(cipher_key=key)

ciphertext = symmetric.encrypt("Hello World")
plaintext = symmetric.decrypt(ciphertext)

print(ciphertext)
print(plaintext)
```

## Error handling
- `CipherKeyNotFoundError`: raised when encrypting or decrypting without a key.
- `InvalidCipherKeyError`: raised when setting an invalid Fernet key.
