# Getting started

## Requirements

Python 3.10 or newer.

## Installation

```bash
pip install shadow_data
```

PII detection depends on spaCy, which is an optional extra:

```bash
pip install "shadow_data[spacy]"
```

spaCy models are downloaded separately. Install the one you plan to use:

```bash
python -m spacy download en_core_web_sm
```

## Your first anonymization

```python
from shadow_data import EmailAnonymization, Ipv4Anonymization, PhoneNumberAnonymization

text = 'Contact me at user@example.com or 415-555-0199. Server: 10.0.0.1'

print(Ipv4Anonymization.anonymize_ipv4(text))
print(EmailAnonymization.anonymize_email('user@example.com'))
print(PhoneNumberAnonymization.anonymize_phone_number('415-555-0199'))
```

```plain
Contact me at user@example.com or 415-555-0199. Server: 10.X.X.X
****@****ple.com
***-***-0199
```

## A full tour

The script below touches every part of the library. It is also available in the repository
as `examples/quickstart.py`.

```python
from shadow_data.anonymization import (
    EmailAnonymization,
    Ipv4Anonymization,
    PhoneNumberAnonymization,
    TextProcessor,
)
from shadow_data.cryptohash.symmetric_cipher import Symmetric
from shadow_data.l10n.brazil import BrazilIdentifierAnonymizer
from shadow_data.l10n.usa import UsaIdentifierAnonymizer
from shadow_data.masking import mask_credit_card, partial_email
from shadow_data.reversible import Pseudonymizer

text = 'Contact me at user@example.com or 415-555-0199. Server: 10.0.0.1'

anonymized_text = Ipv4Anonymization.anonymize_ipv4(text)
anonymized_text = TextProcessor.replace_text('Contact', 'Reach', anonymized_text)

print(anonymized_text)
print(EmailAnonymization.anonymize_email('user@example.com'))
print(PhoneNumberAnonymization.anonymize_phone_number('415-555-0199'))

print(UsaIdentifierAnonymizer("Billy's SSN is 479-92-5042.").anonymize())
print(BrazilIdentifierAnonymizer('806.846.761-09').anonymize())

print(mask_credit_card('4111 1111 1111 1111'))
print(partial_email('user@example.com'))

pseudonymizer = Pseudonymizer()
token = pseudonymizer.pseudonymize('user@example.com')

print(token)
print(pseudonymizer.depseudonymize(token))

symmetric = Symmetric()
key = symmetric.create_key()

ciphertext = symmetric.encrypt('hello')
plaintext = symmetric.decrypt(ciphertext)

print(ciphertext)
print(plaintext)
```

```plain
Reach me at user@example.com or 415-555-0199. Server: 10.X.X.X
****@****ple.com
***-***-0199
Billy's SSN is XXX-XX-5042.
80*.***.***-**
**** **** **** 1111
u***@e******.com
gAAAAABqdIcLaY7VdzuClEbUZnAw0s7a0KPKZqlvMDFQR1hGRaZM6Wzsv22KVZ4vZS_...
user@example.com
b'gAAAAABqdIcL2K15BFBa59brc87JieYR1pThiUdFY30SbzZJI6yollP5z7FqRjQG...'
hello
```

## Importing

Everything except the optional spaCy integration is available from the top-level package:

```python
from shadow_data import mask_credit_card, Pseudonymizer, __version__
```

The submodules work equally well, and are what the guide uses so it is always clear where a
name comes from:

```python
from shadow_data.masking import mask_credit_card
```

PII detection is deliberately **not** re-exported from `shadow_data`, so that importing the
package never requires the spaCy extra. Import it from its own module:

```python
from shadow_data.pii.spacy import SensitiveData
```

## Next steps

- [Choosing a technique](guide/choosing.md) — anonymize, mask, pseudonymize, or encrypt?
- [API reference](reference.md) — every public name in one place.
