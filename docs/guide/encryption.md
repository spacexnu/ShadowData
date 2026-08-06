# Encryption

`Symmetric` wraps [Fernet](https://cryptography.io/en/latest/fernet/) from the
`cryptography` package. Fernet provides authenticated symmetric encryption: a token cannot
be decrypted or tampered with without the key.

```python
from shadow_data.cryptohash.symmetric_cipher import Symmetric
```

## Generate a key

```python
from shadow_data.cryptohash.symmetric_cipher import Symmetric

symmetric = Symmetric()
key = symmetric.create_key()

ciphertext = symmetric.encrypt('Hello World!')
plaintext = symmetric.decrypt(ciphertext)

print(ciphertext)
print(plaintext)
```

```plain
b'gAAAAABqdIcL2K15BFBa59brc87JieYR1pThiUdFY30SbzZJI6yollP5z7FqRjQG...'
Hello World!
```

`encrypt` takes a `str` and returns `bytes`; `decrypt` does the reverse.

## Use an existing key

Pass the key to the constructor, or assign it afterwards. Both paths validate it.

```python
from shadow_data.cryptohash.symmetric_cipher import Symmetric

key = b'bpSGcODTJ1iOwxloIQJrAiYDRaqyypdCsQfg1EwVOTc='

symmetric = Symmetric(cipher_key=key)
print(symmetric.decrypt(symmetric.encrypt('Hello World')))
```

```python
from shadow_data.cryptohash.symmetric_cipher import Symmetric

symmetric = Symmetric()
symmetric.cipher_key = b'bpSGcODTJ1iOwxloIQJrAiYDRaqyypdCsQfg1EwVOTc='
```

!!! danger "Key handling"

    The key above is an example from this documentation — never use a published key.
    Generate your own with `create_key()`, store it in a secrets manager or environment
    variable, and keep it out of source control and logs.

## Errors

| Exception | Raised when |
|---|---|
| `CipherKeyNotFoundError` | Encrypting or decrypting before a key was created or set |
| `InvalidCipherKeyError` | Constructing or assigning a key Fernet does not accept |

```python
from shadow_data.cryptohash.symmetric_cipher import Symmetric
from shadow_data.exceptions import CipherKeyNotFoundError

try:
    Symmetric().encrypt('no key yet')
except CipherKeyNotFoundError as error:
    print(error)
```

```plain
Cipher key not found. Please create or set a key before encryption/decryption.
```

Both inherit from `CustomError`, so you can catch the whole family at once:

```python
from shadow_data.exceptions import CustomError
```

## When to use something else

If you are replacing values in a dataset rather than encrypting a blob of text, use
[`Pseudonymizer`](pseudonymization.md). It is built on this class but returns strings,
handles key derivation for deterministic tokens, and raises a domain-specific error for
invalid tokens.
