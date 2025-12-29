# Usage

This guide covers the anonymization helpers and localized identifiers.

## Text replacement
`TextProcessor.replace_text` uses regular expressions for matching and replacement.

```python
from shadow_data.anonymization import TextProcessor

content = "The user's name is Alice Jones."
updated = TextProcessor.replace_text("Alice Jones", "ANONYMOUS", content)
print(updated)
```

## IPv4 anonymization
`Ipv4Anonymization.anonymize_ipv4` masks the final three octets with `X` and works on full text.

```python
from shadow_data.anonymization import Ipv4Anonymization

text = "Primary IP: 192.168.1.100"
print(Ipv4Anonymization.anonymize_ipv4(text))
```

## Email anonymization
`EmailAnonymization.anonymize_email` validates email format and replaces the user part with `*`, while keeping the last 3 characters of the first domain label.

```python
from shadow_data.anonymization import EmailAnonymization

print(EmailAnonymization.anonymize_email("user@example.com"))
```

## Phone number anonymization
`PhoneNumberAnonymization.anonymize_phone_number` preserves the last 4 digits and keeps the original formatting.

```python
from shadow_data.anonymization import PhoneNumberAnonymization

print(PhoneNumberAnonymization.anonymize_phone_number("+1 (415) 555-0199"))
```

## Localized identifiers
### US SSN

```python
from shadow_data.l10n.usa import IdentifierAnonymizer

text = "SSN: 479-92-5042"
anonymizer = IdentifierAnonymizer(text)
anonymizer.anonymize()
print(anonymizer.cleaned_content)
```

### Brazil CPF/CNPJ

```python
from shadow_data.l10n.brazil import IdentifierAnonymizer

cpf = "806.846.761-09"
cpf_anonymizer = IdentifierAnonymizer(cpf)
cpf_anonymizer.anonymize()
print(cpf_anonymizer.cleaned_content)

cnpj = "26.283.050/0001-17"
cnpj_anonymizer = IdentifierAnonymizer(cnpj)
cnpj_anonymizer.anonymize()
print(cnpj_anonymizer.cleaned_content)
```
