"""ShadowData — anonymize, mask, and encrypt sensitive data."""

from shadow_data.anonymization import (
    EmailAnonymization,
    Ipv4Anonymization,
    PhoneNumberAnonymization,
    TextProcessor,
)
from shadow_data.cryptohash.symmetric_cipher import Symmetric
from shadow_data.exceptions import (
    CipherKeyNotFoundError,
    CustomError,
    InvalidCipherKeyError,
    InvalidCreditCardError,
    InvalidEmailError,
    InvalidPseudonymError,
)
from shadow_data.l10n.brazil import BrazilIdentifierAnonymizer
from shadow_data.l10n.usa import UsaIdentifierAnonymizer
from shadow_data.masking import (
    mask,
    mask_credit_card,
    mask_digits,
    partial_email,
    passes_luhn,
)
from shadow_data.reversible import Pseudonymizer

__version__ = '1.0.1'

__all__ = [
    'BrazilIdentifierAnonymizer',
    'CipherKeyNotFoundError',
    'CustomError',
    'EmailAnonymization',
    'InvalidCipherKeyError',
    'InvalidCreditCardError',
    'InvalidEmailError',
    'InvalidPseudonymError',
    'Ipv4Anonymization',
    'PhoneNumberAnonymization',
    'Pseudonymizer',
    'Symmetric',
    'TextProcessor',
    'UsaIdentifierAnonymizer',
    '__version__',
    'mask',
    'mask_credit_card',
    'mask_digits',
    'partial_email',
    'passes_luhn',
]
