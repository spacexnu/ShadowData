# API reference

Every public name, grouped by module. Follow the links for usage and examples.

## Top-level package

`shadow_data` re-exports everything except the optional spaCy integration, so importing the
package never requires the extra.

```python
from shadow_data import mask_credit_card, Pseudonymizer, __version__
```

| Name | Kind | See |
|---|---|---|
| `__version__` | `str` | — |
| `TextProcessor` | class | [Anonymization](guide/anonymization.md#text-replacement) |
| `Ipv4Anonymization` | class | [Anonymization](guide/anonymization.md#ipv4-addresses) |
| `EmailAnonymization` | class | [Anonymization](guide/anonymization.md#email-addresses) |
| `PhoneNumberAnonymization` | class | [Anonymization](guide/anonymization.md#phone-numbers) |
| `UsaIdentifierAnonymizer` | class | [Identifiers](guide/identifiers.md#united-states-social-security-numbers) |
| `BrazilIdentifierAnonymizer` | class | [Identifiers](guide/identifiers.md#brazil-cpf-and-cnpj) |
| `mask`, `mask_digits`, `mask_credit_card`, `partial_email`, `passes_luhn` | functions | [Masking](guide/masking.md) |
| `Pseudonymizer` | class | [Pseudonymization](guide/pseudonymization.md) |
| `Symmetric` | class | [Encryption](guide/encryption.md) |
| `CustomError` and subclasses | exceptions | [Exceptions](#exceptions) |

## `shadow_data.anonymization`

```python
class TextProcessor:
    @staticmethod
    def replace_text(original_term: str, to_replace: str, original_content: str) -> str
    @staticmethod
    def replace_regex(pattern: str, to_replace: str, original_content: str) -> str


class Ipv4Anonymization:
    @staticmethod
    def anonymize_ipv4(text: str, pattern: str = r'\1.X.X.X') -> str


class EmailAnonymization:
    @staticmethod
    def anonymize_email(email: str) -> str      # raises InvalidEmailError


class PhoneNumberAnonymization:
    @staticmethod
    def anonymize_phone_number(phone: str) -> str
```

`EMAIL_REGEX` is exposed as a module constant, and is the pattern used to validate
addresses here and in `partial_email`.

## `shadow_data.l10n`

```python
class ClearIdentifier(ABC):
    def __init__(self, content_to_anonymize: str) -> None
    cleaned_content: str
    @abstractmethod
    def anonymize(self) -> str


class UsaIdentifierAnonymizer(ClearIdentifier): ...     # shadow_data.l10n.usa
class BrazilIdentifierAnonymizer(ClearIdentifier): ...  # shadow_data.l10n.brazil
```

Both modules also export `IdentifierAnonymizer` as a deprecated alias for their own class,
removed in 2.0.

Pattern constants: `SSN_PATTERN` (usa), `CPF_PATTERN` and `CNPJ_PATTERN` (brazil).

## `shadow_data.masking`

```python
def mask(text: str, *, keep_first: int = 0, keep_last: int = 0, mask_char: str = '*') -> str
def mask_digits(text: str, *, keep_last: int = 0, mask_char: str = '*') -> str
def mask_credit_card(number: str, *, mask_char: str = '*') -> str  # raises InvalidCreditCardError
def partial_email(email: str, *, mask_char: str = '*') -> str      # raises InvalidEmailError
def passes_luhn(digits: str) -> bool
```

`mask` and `mask_digits` raise `ValueError` for a negative window or a `mask_char` that is
not exactly one character.

Constants: `DEFAULT_MASK_CHAR`, `CARD_VISIBLE_DIGITS`, `MIN_CARD_DIGITS`, `MAX_CARD_DIGITS`.

## `shadow_data.reversible`

```python
class Pseudonymizer:
    def __init__(self, key: bytes | None = None) -> None   # raises InvalidCipherKeyError
    @property
    def key(self) -> bytes
    def pseudonymize(self, value: str) -> str
    def depseudonymize(self, token: str) -> str            # raises InvalidPseudonymError
    def deterministic_pseudonym(self, value: str) -> str
```

Constant: `DETERMINISTIC_CONTEXT`, the HKDF info string used to derive the HMAC subkey.

## `shadow_data.cryptohash.symmetric_cipher`

```python
class Symmetric:
    def __init__(self, cipher_key: bytes | None = None) -> None  # raises InvalidCipherKeyError
    def create_key(self) -> bytes
    cipher_key: bytes | None                                     # settable, validated
    def encrypt(self, plaintext: str) -> bytes                   # raises CipherKeyNotFoundError
    def decrypt(self, ciphertext: bytes) -> str                  # raises CipherKeyNotFoundError
```

## `shadow_data.pii`

Requires the `spacy` extra. Not re-exported from the top-level package.

```python
class ModelSelector:
    @staticmethod
    def select(lang: ModelLang, core: ModelCore, size: ModelSize, auto_download: bool = False) -> Language


class SensitiveData:
    def set_model(self, model_lang, model_core, model_size, auto_download: bool = False) -> Language
    def identify_sensitive_data(
        self, model_lang, model_core, model_size, content: str,
        auto_download: bool = False, labels: Iterable[str] | None = None,
    ) -> list[tuple[str, str]]
```

Enums in `shadow_data.pii.enums`: `ModelLang`, `ModelCore`, `ModelSize`.
Constant: `DEFAULT_SENSITIVE_LABELS`.

`select` raises `TypeError` for a wrong enum type and `RuntimeError` when the model is
missing or cannot be downloaded.

## `shadow_data.utils`

```python
def only_digits(content: str) -> str
```

## Exceptions

All exceptions live in `shadow_data.exceptions` and inherit from `CustomError`, so a single
`except CustomError` catches the whole family.

| Exception | Raised by |
|---|---|
| `InvalidEmailError` | `anonymize_email`, `partial_email` |
| `InvalidCreditCardError` | `mask_credit_card` |
| `CipherKeyNotFoundError` | `Symmetric.encrypt`, `Symmetric.decrypt` |
| `InvalidCipherKeyError` | `Symmetric(...)`, `Symmetric.cipher_key`, `Pseudonymizer(...)` |
| `InvalidPseudonymError` | `Pseudonymizer.depseudonymize` |
