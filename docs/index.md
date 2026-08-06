# ShadowData

A Python library for anonymizing, masking, and encrypting sensitive data with a small,
focused API.

[Get started](getting-started.md){ .md-button .md-button--primary }
[View on GitHub](https://github.com/spacexnu/ShadowData){ .md-button }

## What it does

<div class="grid cards" markdown>

-   **Anonymization**

    Irreversibly redact free-form text, IPv4 addresses, emails, and phone numbers.

    [:octicons-arrow-right-24: Anonymization](guide/anonymization.md)

-   **Localized identifiers**

    Mask US Social Security Numbers and Brazilian CPF/CNPJ anywhere in a text.

    [:octicons-arrow-right-24: Identifiers](guide/identifiers.md)

-   **Masking**

    Keep a value recognizable to a human while hiding most of it — card numbers,
    formatted identifiers, partial emails.

    [:octicons-arrow-right-24: Masking](guide/masking.md)

-   **Pseudonymization**

    Replace values with tokens you can reverse with a key, or join on across datasets.

    [:octicons-arrow-right-24: Pseudonymization](guide/pseudonymization.md)

-   **Encryption**

    Symmetric encryption and decryption built on Fernet.

    [:octicons-arrow-right-24: Encryption](guide/encryption.md)

-   **PII detection**

    Find names, places, and organizations in text with spaCy.

    [:octicons-arrow-right-24: PII detection](guide/pii-detection.md)

</div>

## At a glance

```python
from shadow_data import (
    EmailAnonymization,
    Pseudonymizer,
    UsaIdentifierAnonymizer,
    mask_credit_card,
)

EmailAnonymization.anonymize_email('user@example.com')  # '****@****ple.com'
UsaIdentifierAnonymizer('SSN: 479-92-5042').anonymize()  # 'SSN: XXX-XX-5042'
mask_credit_card('4111 1111 1111 1111')  # '**** **** **** 1111'

pseudonymizer = Pseudonymizer()
token = pseudonymizer.pseudonymize('user@example.com')
pseudonymizer.depseudonymize(token)  # 'user@example.com'
```

## Not sure which one you need?

The techniques differ in whether the original value can be recovered and in how much of it
remains readable. [Choosing a technique](guide/choosing.md) walks through the trade-offs.

## Project status

ShadowData requires Python 3.10 or newer, ships type information (`py.typed`), and is
checked with mypy in strict mode. It is released under the MIT License.
