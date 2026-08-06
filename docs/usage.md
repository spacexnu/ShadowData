# Usage

This guide covers the anonymization helpers and localized identifiers.

## Text replacement
`TextProcessor.replace_text` treats the search term as literal text. Use `TextProcessor.replace_regex` when a regular expression is required.

```python
from shadow_data.anonymization import TextProcessor

content = "The user's name is Alice Jones."
updated = TextProcessor.replace_text('Alice Jones', 'ANONYMOUS', content)
print(updated)
```

## IPv4 anonymization
`Ipv4Anonymization.anonymize_ipv4` masks the final three octets with `X` and works on full text. Octets outside `0-255` and longer dotted sequences (such as version strings) are left untouched. Pass `pattern='X.X.X.X'` to mask the first octet as well.

```python
from shadow_data.anonymization import Ipv4Anonymization

text = 'Primary IP: 192.168.1.100'
print(Ipv4Anonymization.anonymize_ipv4(text))
```

## Email anonymization
`EmailAnonymization.anonymize_email` validates email format and replaces the user part with `*`. The first domain label keeps its last 3 characters only when it is longer than 3 characters; shorter labels are masked entirely.

```python
from shadow_data.anonymization import EmailAnonymization

print(EmailAnonymization.anonymize_email('user@example.com'))  # ****@****ple.com
print(EmailAnonymization.anonymize_email('user@ex.com'))  # ****@**.com
```

## Phone number anonymization
`PhoneNumberAnonymization.anonymize_phone_number` preserves the last 4 digits and keeps the original formatting. Numbers with 4 digits or fewer are masked completely, since keeping the last 4 would reveal the whole value.

```python
from shadow_data.anonymization import PhoneNumberAnonymization

print(PhoneNumberAnonymization.anonymize_phone_number('+1 (415) 555-0199'))
```

## Localized identifiers
Both anonymizers scan free-form text and return the cleaned content (also available as `cleaned_content`).

### US SSN

```python
from shadow_data.l10n.usa import UsaIdentifierAnonymizer

text = 'SSN: 479-92-5042'
print(UsaIdentifierAnonymizer(text).anonymize())  # SSN: XXX-XX-5042
```

### Brazil CPF/CNPJ

CPF and CNPJ are matched anywhere in the text, with separators preserved and only the first two digits left visible.

```python
from shadow_data.l10n.brazil import BrazilIdentifierAnonymizer

cpf = '806.846.761-09'
print(BrazilIdentifierAnonymizer(cpf).anonymize())  # 80*.***.***-**

cnpj = '26.283.050/0001-17'
print(BrazilIdentifierAnonymizer(cnpj).anonymize())  # 26.***.***/****-**
```

> `IdentifierAnonymizer` remains available in both modules as a deprecated alias and will be removed in 2.0.
