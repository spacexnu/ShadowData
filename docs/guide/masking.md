# Masking

Masking keeps a value recognizable to a human while hiding most of it — the last four
digits of a card on a receipt, for example. Use
[anonymization](anonymization.md) instead when the value should not be recognizable at all.

All helpers live in `shadow_data.masking`.

!!! info "Masking never returns its input unchanged"

    When the window you ask to keep covers the whole value, the whole value is masked
    instead. For a privacy library, "returned the original data" is the worst possible
    failure mode, so it is ruled out by construction.

## `mask`

Masks every character except the first `keep_first` and the last `keep_last`.

```python
from shadow_data.masking import mask

mask('sensitive')  # '*********'
mask('sensitive', keep_last=3)  # '******ive'
mask('sensitive', keep_first=1, keep_last=1)  # 's*******e'
mask('sensitive', keep_last=3, mask_char='#')  # '######ive'
```

When the window covers everything, everything is masked:

```python
mask('abc', keep_last=3)  # '***'
mask('abc', keep_first=2, keep_last=2)  # '***'
```

`ValueError` is raised for a negative window, or for a `mask_char` that is not exactly one
character.

A common use is trimming secrets down to an identifiable prefix:

```python
from shadow_data.masking import mask

print(mask('sk_live_51H8xKzLmNpQrStUv', keep_first=7, keep_last=4))
```

```plain
sk_live**************StUv
```

## `mask_digits`

Masks digits while leaving separators — and any other non-digit — in place. Useful for any
formatted identifier.

```python
from shadow_data.masking import mask_digits

mask_digits('4111 1111 1111 1111', keep_last=4)  # '**** **** **** 1111'
mask_digits('order AB-1234', keep_last=2)  # 'order AB-**34'
mask_digits('123-456')  # '***-***'
```

Asking to keep more digits than the value has masks everything:

```python
mask_digits('12', keep_last=5)  # '**'
```

## `mask_credit_card`

Masks a card number, keeping the last 4 digits and the original spacing.

```python
from shadow_data.masking import mask_credit_card

mask_credit_card('4111 1111 1111 1111')  # '**** **** **** 1111'
mask_credit_card('4111-1111-1111-1111')  # '****-****-****-1111'
mask_credit_card('4111111111111111')  # '************1111'
mask_credit_card('378282246310005')  # '***********0005'
```

The value is first checked against the Luhn checksum and a plausible length of 12–19
digits. Anything else raises `InvalidCreditCardError`, so a mistyped or unrelated value is
never returned partially readable:

```python
from shadow_data.exceptions import InvalidCreditCardError
from shadow_data.masking import mask_credit_card

try:
    mask_credit_card('4111111111111112')  # fails the checksum
except InvalidCreditCardError as error:
    print(error)
```

```plain
Invalid credit card number
```

`passes_luhn` is exposed separately if you only need the checksum:

```python
from shadow_data.masking import passes_luhn

passes_luhn('4111111111111111')  # True
passes_luhn('4111111111111112')  # False
```

## `partial_email`

Keeps the first character of the user and of the first domain label.

```python
from shadow_data.masking import partial_email

partial_email('user@example.com')  # 'u***@e******.com'
partial_email('user@example.co.uk')  # 'u***@e******.co.uk'
partial_email('a@example.com')  # '*@e******.com'
```

A one-character user or label has nothing to keep, so it is masked entirely. Invalid
addresses raise `InvalidEmailError`.

Use [`EmailAnonymization.anonymize_email`](anonymization.md#email-addresses) when the user
part must be hidden completely.

## Choosing `mask_char`

Every helper accepts `mask_char`. The default `*` is the safe choice for display; pick
something else when the output goes somewhere `*` is meaningful, such as a Markdown
document or a glob pattern.

```python
from shadow_data.masking import mask_credit_card

mask_credit_card('4111111111111111', mask_char='x')  # 'xxxxxxxxxxxx1111'
```
