# Localized identifiers

National identifiers follow country-specific formats, so each one gets its own anonymizer.
Both scan free-form text, mask every identifier they find, and return the cleaned content.

```python
anonymizer = UsaIdentifierAnonymizer(text)
cleaned = anonymizer.anonymize()  # also available as anonymizer.cleaned_content
```

## United States — Social Security Numbers

`UsaIdentifierAnonymizer` masks the first five digits and keeps the last four, preserving
whichever separator the text uses.

```python
from shadow_data.l10n.usa import UsaIdentifierAnonymizer

text = "Billy's SSN is 479-92-5042. Please make sure it's anonymized."
print(UsaIdentifierAnonymizer(text).anonymize())
```

```plain
Billy's SSN is XXX-XX-5042. Please make sure it's anonymized.
```

Dashes, spaces, and no separator at all are all recognized, and multiple numbers in the
same text are handled:

```python
from shadow_data.l10n.usa import UsaIdentifierAnonymizer

print(UsaIdentifierAnonymizer('SSNs are 123-45-6789, 987 65 4321 and 123456789.').anonymize())
```

```plain
SSNs are XXX-XX-6789, XXX XX 4321 and XXXXX6789.
```

Anything that is not a complete SSN is left untouched, including partial numbers
(`123-45`) and longer digit runs (`1234-56-7890`).

## Brazil — CPF and CNPJ

`BrazilIdentifierAnonymizer` handles both the individual (CPF, 11 digits) and corporate
(CNPJ, 14 digits) tax IDs. Separators are preserved and only the first two digits stay
visible.

```python
from shadow_data.l10n.brazil import BrazilIdentifierAnonymizer

print(BrazilIdentifierAnonymizer('806.846.761-09').anonymize())
print(BrazilIdentifierAnonymizer('26.283.050/0001-17').anonymize())
```

```plain
80*.***.***-**
26.***.***/****-**
```

Bare digits work too, and identifiers are found inside sentences:

```python
from shadow_data.l10n.brazil import BrazilIdentifierAnonymizer

text = 'O CPF do titular e 806.846.761-09 e o CNPJ da empresa e 26.283.050/0001-17.'
print(BrazilIdentifierAnonymizer(text).anonymize())
```

```plain
O CPF do titular e 80*.***.***-** e o CNPJ da empresa e 26.***.***/****-**.
```

CNPJ is matched before CPF, so the trailing 11 digits of a CNPJ are never mistaken for a
CPF. Content with no identifier is returned unchanged.

!!! note "No checksum validation"

    Both anonymizers match on shape, not on the CPF/CNPJ/SSN check digits. A well-formed
    but invalid number will still be masked — which is the safe direction to err in.

## Deprecated aliases

Both modules used to export a class called `IdentifierAnonymizer`, which meant importing
both required aliasing. The name still works and points at the new class:

```python
from shadow_data.l10n.brazil import IdentifierAnonymizer  # -> BrazilIdentifierAnonymizer
from shadow_data.l10n.usa import IdentifierAnonymizer  # -> UsaIdentifierAnonymizer
```

It will be removed in 2.0. Prefer `BrazilIdentifierAnonymizer` and
`UsaIdentifierAnonymizer`.

## Adding a country

Both classes extend `ClearIdentifier`, which takes the content in its constructor and
requires an `anonymize()` method returning the cleaned string:

```python
import re

from shadow_data.l10n.ClearIdentifier import ClearIdentifier


class PortugalIdentifierAnonymizer(ClearIdentifier):
    def anonymize(self) -> str:
        self.cleaned_content = re.sub(r'(?<!\d)\d{9}(?!\d)', 'XXXXXXXXX', self.content_to_anonymize)
        return self.cleaned_content
```
