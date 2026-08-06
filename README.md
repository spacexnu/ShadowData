![Build Status](https://github.com/spacexnu/ShadowData/actions/workflows/main.yml/badge.svg)

# ShadowData

A Python library for anonymizing, masking, and encrypting sensitive data with a small,
focused API.

📖 **[Documentation](https://spacexnu.github.io/ShadowData/)**

## Features

- **Anonymization** — free-form text, IPv4 addresses, emails, phone numbers
- **Localized identifiers** — US SSN, Brazil CPF/CNPJ
- **Masking** — credit cards with Luhn validation, formatted identifiers, partial emails
- **Pseudonymization** — reversible tokens, plus deterministic tokens for joins
- **Encryption** — symmetric encryption and decryption via Fernet
- **PII detection** — named entity recognition with spaCy (optional extra)

## Installation

Requires Python 3.10 or newer.

```bash
pip install shadow_data
```

With PII detection:

```bash
pip install "shadow_data[spacy]"
python -m spacy download en_core_web_sm
```

## Quickstart

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

See [Getting started](https://spacexnu.github.io/ShadowData/getting-started/) for a full
tour, and [Choosing a technique](https://spacexnu.github.io/ShadowData/guide/choosing/) if
you are unsure which helper fits your case.

## Development

```bash
poetry install --with dev,docs --extras spacy
make all   # ruff, mypy, docs build, and pytest with coverage
```

See [Contributing](https://spacexnu.github.io/ShadowData/contributing/).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT — see [LICENSE](LICENSE).
