# Anonymization

Anonymization is one-way: it replaces a value with something that cannot be turned back
into the original. Use it for logs, exports, and test fixtures.

All helpers live in `shadow_data.anonymization`.

## Text replacement

`replace_text` treats the search term as literal text. Use `replace_regex` when you need a
regular expression.

```python
from shadow_data.anonymization import TextProcessor

content = "The user's name is Alice Jones."
print(TextProcessor.replace_text('Alice Jones', 'ANONYMOUS', content))
```

```plain
The user's name is ANONYMOUS.
```

```python
from shadow_data.anonymization import TextProcessor

content = 'Ticket IDs: 4821, 4822, 4823'
print(TextProcessor.replace_regex(r'\d{4}', 'XXXX', content))
```

```plain
Ticket IDs: XXXX, XXXX, XXXX
```

## IPv4 addresses

`anonymize_ipv4` masks the final three octets and works over full text.

```python
from shadow_data.anonymization import Ipv4Anonymization

text = 'The first IP is 192.168.1.100, and the second is 10.0.0.1.'
print(Ipv4Anonymization.anonymize_ipv4(text))
```

```plain
The first IP is 192.X.X.X, and the second is 10.X.X.X.
```

The default keeps the first octet. Since that still reveals the network, pass a pattern to
mask everything:

```python
print(Ipv4Anonymization.anonymize_ipv4('Server: 192.168.1.100', pattern='X.X.X.X'))
```

```plain
Server: X.X.X.X
```

Values that merely look like addresses are left alone: octets above 255 are rejected, and
so are longer dotted sequences such as version strings.

```python
print(Ipv4Anonymization.anonymize_ipv4('Build 1.2.3.4.5 on host 999.1.1.1'))
```

```plain
Build 1.2.3.4.5 on host 999.1.1.1
```

## Email addresses

`anonymize_email` validates the address, replaces the user part entirely, and keeps the
last 3 characters of the first domain label.

```python
from shadow_data.anonymization import EmailAnonymization

print(EmailAnonymization.anonymize_email('john@emailaddress.com'))
print(EmailAnonymization.anonymize_email('user@example.co.uk'))
```

```plain
****@*********ess.com
****@****ple.co.uk
```

Short domain labels are masked completely, because keeping 3 characters of a 3-character
label would reveal all of it:

```python
print(EmailAnonymization.anonymize_email('user@ex.com'))
```

```plain
****@**.com
```

An address that fails validation raises `InvalidEmailError` rather than being returned
partially processed.

!!! tip "Need the address to stay recognizable?"

    Use [`partial_email`](masking.md#partial_email), which keeps the first character of the
    user and domain.

## Phone numbers

`anonymize_phone_number` keeps the last 4 digits and preserves the original formatting,
whatever it is.

```python
from shadow_data.anonymization import PhoneNumberAnonymization

for phone in ['+55 (11) 91234-5678', '+1 (415) 555-0199', '+44 20 7946 0958']:
    print(PhoneNumberAnonymization.anonymize_phone_number(phone))
```

```plain
+** (**) *****-5678
+* (***) ***-0199
+** ** **** 0958
```

Numbers with 4 digits or fewer are masked completely — keeping the last 4 would reveal the
whole value.

```python
print(PhoneNumberAnonymization.anonymize_phone_number('1234'))
```

```plain
****
```
