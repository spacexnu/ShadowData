"""Reversible and deterministic pseudonymization.

Two independent operations, both driven by the same key:

- `pseudonymize` / `depseudonymize` produce reversible tokens (Fernet). Each call
  yields a different token for the same input, so tokens cannot be correlated.
- `deterministic_pseudonym` produces a stable one-way token (HMAC-SHA256) for the
  same input, which is what makes joins across datasets possible — and which also
  makes the tokens linkable by design. See the warning in the method docstring.
"""

import base64
import hmac
from hashlib import sha256

from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from shadow_data.cryptohash.symmetric_cipher import Symmetric
from shadow_data.exceptions import InvalidPseudonymError

# Domain separation: the HMAC subkey must never coincide with the encryption key.
DETERMINISTIC_CONTEXT = b'shadow_data.reversible.deterministic.v1'

_SUBKEY_LENGTH = 32


class Pseudonymizer:
    """Replaces values with tokens that can be reversed with the same key.

    A key is generated when none is supplied; read it from `key` and store it
    somewhere safe, because tokens are worthless without it.
    """

    def __init__(self, key: bytes | None = None) -> None:
        cipher = Symmetric(key)
        self._cipher = cipher
        self._key = key if key is not None else cipher.create_key()
        self._deterministic_key: bytes | None = None

    @property
    def key(self) -> bytes:
        return self._key

    def pseudonymize(self, value: str) -> str:
        """Returns a reversible token. Repeated calls return different tokens."""
        return self._cipher.encrypt(value).decode()

    def depseudonymize(self, token: str) -> str:
        """Recovers the original value from a token produced by `pseudonymize`."""
        try:
            return self._cipher.decrypt(token.encode())
        except InvalidToken as error:
            raise InvalidPseudonymError() from error

    def deterministic_pseudonym(self, value: str) -> str:
        """Returns a stable, one-way token for `value`.

        The same input always maps to the same token, which is what allows records
        to be joined across datasets. That also means tokens leak equality: anyone
        holding the key can confirm a guessed value by recomputing its token, and
        repeated values stay visible as repeated tokens. Prefer `pseudonymize`
        unless linkability is a requirement.
        """
        return hmac.new(self._subkey(), value.encode(), sha256).hexdigest()

    def _subkey(self) -> bytes:
        if self._deterministic_key is None:
            self._deterministic_key = HKDF(
                algorithm=hashes.SHA256(),
                length=_SUBKEY_LENGTH,
                salt=None,
                info=DETERMINISTIC_CONTEXT,
            ).derive(base64.urlsafe_b64decode(self._key))

        return self._deterministic_key
