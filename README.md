![Build Status](https://github.com/spacexnu/ShadowData/actions/workflows/main.yml/badge.svg)

# ShadowData
A Python library for anonymizing, masking, and encrypting sensitive data with a small, focused API.

## What it does today
- Text and pattern anonymization (free-form text replacement, IPv4, email, phone)
- Localized identifiers (US SSN, Brazil CPF/CNPJ)
- Format-preserving masking (credit cards with Luhn validation, digits, partial email)
- Reversible and deterministic pseudonymization
- Symmetric encryption and decryption (Fernet)
- PII detection via spaCy (optional extra)

## Installation

Requires Python 3.10 or newer.

```bash
pip install shadow_data
```

Optional spaCy support:

```bash
pip install shadow_data[spacy]
```

spaCy models must be installed before use:

```bash
python -m spacy download en_core_web_trf
```

## Quickstart

```python
from shadow_data.anonymization import (
    EmailAnonymization,
    Ipv4Anonymization,
    PhoneNumberAnonymization,
    TextProcessor,
)
from shadow_data.cryptohash.symmetric_cipher import Symmetric
from shadow_data.l10n.usa import UsaIdentifierAnonymizer
from shadow_data.masking import mask_credit_card, partial_email
from shadow_data.reversible import Pseudonymizer

text = 'Contact me at user@example.com or 415-555-0199. Server: 10.0.0.1'
anonymized_text = Ipv4Anonymization.anonymize_ipv4(text)
anonymized_text = TextProcessor.replace_text('Contact', 'Reach', anonymized_text)
email = EmailAnonymization.anonymize_email('user@example.com')
phone = PhoneNumberAnonymization.anonymize_phone_number('415-555-0199')
print(anonymized_text, email, phone)

ssn = "Billy's SSN is 479-92-5042."
print(UsaIdentifierAnonymizer(ssn).anonymize())

print(mask_credit_card('4111 1111 1111 1111'))  # **** **** **** 1111
print(partial_email('user@example.com'))  # u***@e******.com

pseudonymizer = Pseudonymizer()
token = pseudonymizer.pseudonymize('user@example.com')
print(token, pseudonymizer.depseudonymize(token))

symmetric = Symmetric()
key = symmetric.create_key()
ciphertext = symmetric.encrypt('hello')
plaintext = symmetric.decrypt(ciphertext)
print(ciphertext, plaintext)
```

## Docs
- `docs/README.md`
- `docs/usage.md`
- `docs/masking.md`
- `docs/reversible.md`
- `docs/cryptography.md`
- `docs/pii.md`

## Examples
- `examples/quickstart.py`
- `examples/anonymization.md`
- `examples/i10n_us.md`
- `examples/i10n_brazil.md`
- `examples/masking.md`
- `examples/reversible.md`
- `examples/pii_nlp.md`
- `examples/symmetric_cipher.md`

## Development

```bash
poetry install --with dev --extras spacy
make all   # ruff check, ruff format --check, mypy, pytest with coverage
```

Individual targets: `make test`, `make coverage`, `make check`, `make format`, `make typecheck`.

## Changelog
See `CHANGELOG.md`.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b my-new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push the branch (`git push origin my-new-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License - see `LICENSE` for details.
