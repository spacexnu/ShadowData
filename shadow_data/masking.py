"""Format-preserving masking helpers.

Unlike the anonymization helpers, these functions are meant for values that must
stay recognizable to a human (a support agent confirming the last four digits of
a card, for example) while keeping the bulk of the value hidden.
"""

import re

from shadow_data.anonymization import EMAIL_REGEX
from shadow_data.exceptions import InvalidCreditCardError, InvalidEmailError
from shadow_data.utils import only_digits

DEFAULT_MASK_CHAR = '*'

CARD_VISIBLE_DIGITS = 4
MIN_CARD_DIGITS = 12
MAX_CARD_DIGITS = 19


def mask(text: str, *, keep_first: int = 0, keep_last: int = 0, mask_char: str = DEFAULT_MASK_CHAR) -> str:
    """Masks every character except the first `keep_first` and last `keep_last`.

    When the window to keep covers the whole value, everything is masked instead:
    a masking helper must never return its input unchanged.
    """
    _validate_options(keep_first, keep_last, mask_char)

    if keep_first + keep_last >= len(text):
        return mask_char * len(text)

    hidden = len(text) - keep_first - keep_last
    kept_suffix = text[len(text) - keep_last :] if keep_last else ''

    return text[:keep_first] + mask_char * hidden + kept_suffix


def mask_digits(text: str, *, keep_last: int = 0, mask_char: str = DEFAULT_MASK_CHAR) -> str:
    """Masks the digits of `text`, leaving the last `keep_last` and any separator intact."""
    _validate_options(0, keep_last, mask_char)

    digits = only_digits(text)
    visible_from = len(digits) - keep_last if keep_last < len(digits) else len(digits)

    seen = 0
    result = []

    for char in text:
        if char.isdigit():
            result.append(char if seen >= visible_from else mask_char)
            seen += 1
        else:
            result.append(char)

    return ''.join(result)


def mask_credit_card(number: str, *, mask_char: str = DEFAULT_MASK_CHAR) -> str:
    """Masks a credit card number, keeping the last 4 digits and the original spacing.

    Raises `InvalidCreditCardError` when the value is not a plausible card number,
    so that a mistyped or unrelated value is never returned partially readable.
    """
    digits = only_digits(number)

    if not MIN_CARD_DIGITS <= len(digits) <= MAX_CARD_DIGITS or not passes_luhn(digits):
        raise InvalidCreditCardError()

    return mask_digits(number, keep_last=CARD_VISIBLE_DIGITS, mask_char=mask_char)


def partial_email(email: str, *, mask_char: str = DEFAULT_MASK_CHAR) -> str:
    """Masks an email while keeping the first character of the user and of the domain.

    Use `EmailAnonymization.anonymize_email` when the user part must be hidden entirely.
    """
    if not re.match(EMAIL_REGEX, email):
        raise InvalidEmailError()

    user, domain = email.split('@')
    first_label, *remaining_labels = domain.split('.')

    masked_user = mask(user, keep_first=1, mask_char=mask_char)
    masked_label = mask(first_label, keep_first=1, mask_char=mask_char)

    return '@'.join([masked_user, '.'.join([masked_label, *remaining_labels])])


def passes_luhn(digits: str) -> bool:
    """Checks a digit string against the Luhn checksum used by payment card numbers."""
    if not digits.isdigit():
        return False

    total = 0

    for index, char in enumerate(reversed(digits)):
        value = int(char)
        if index % 2 == 1:
            value *= 2
            if value > 9:
                value -= 9
        total += value

    return total % 10 == 0


def _validate_options(keep_first: int, keep_last: int, mask_char: str) -> None:
    if keep_first < 0 or keep_last < 0:
        raise ValueError('keep_first and keep_last must not be negative')
    if len(mask_char) != 1:
        raise ValueError('mask_char must be a single character')
