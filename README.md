![Build Status](https://github.com/spacexnu/ShadowData/actions/workflows/main.yml/badge.svg)

# ShadowData
A Python library for anonymizing, masking, and encrypting sensitive data with a small, focused API.

## What it does today
- Text and pattern anonymization (free-form text replacement, IPv4, email, phone)
- Localized identifiers (US SSN, Brazil CPF/CNPJ)
- Symmetric encryption and decryption (Fernet)
- PII detection via spaCy (optional extra)

Planned: richer masking helpers and reversible transforms.

## Installation

```bash
pip install shadow_data
```

Optional spaCy support:

```bash
pip install shadow_data[spacy]
```

spaCy models are downloaded automatically at runtime when needed. To install manually:

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
from shadow_data.l10n.usa import IdentifierAnonymizer

text = "Contact me at user@example.com or 415-555-0199. Server: 10.0.0.1"
anonymized_text = Ipv4Anonymization.anonymize_ipv4(text)
anonymized_text = TextProcessor.replace_text("Contact", "Reach", anonymized_text)
email = EmailAnonymization.anonymize_email("user@example.com")
phone = PhoneNumberAnonymization.anonymize_phone_number("415-555-0199")
print(anonymized_text, email, phone)

ssn = "Billy's SSN is 479-92-5042."
ssn_anonymizer = IdentifierAnonymizer(ssn)
ssn_anonymizer.anonymize()
print(ssn_anonymizer.cleaned_content)

symmetric = Symmetric()
key = symmetric.create_key()
ciphertext = symmetric.encrypt("hello")
plaintext = symmetric.decrypt(ciphertext)
print(key, ciphertext, plaintext)
```

## Docs
- `docs/README.md`
- `docs/usage.md`
- `docs/cryptography.md`
- `docs/pii.md`

## Examples
- `examples/quickstart.py`
- `examples/anonymization.md`
- `examples/i10n_us.md`
- `examples/i10n_brazil.md`
- `examples/pii_nlp.md`
- `examples/symmetric_cipher.md`

## Testing

```bash
poetry run pytest -vvv
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b my-new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push the branch (`git push origin my-new-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License - see `LICENSE` for details.
