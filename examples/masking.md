# Format-preserving masking

Masking hides most of a value while keeping it recognizable — the opposite trade-off from
anonymization, and the right one for receipts, support screens, and audit logs.

```python
from shadow_data.masking import mask, mask_credit_card, mask_digits, partial_email

card = '4111 1111 1111 1111'
print(f'Card: {mask_credit_card(card)}')

order = 'order AB-1234'
print(f'Order: {mask_digits(order, keep_last=2)}')

email = 'user@example.com'
print(f'Email: {partial_email(email)}')

token = 'sk_live_51H8xKzLmNpQrStUv'
print(f'Token: {mask(token, keep_first=7, keep_last=4)}')
```

### Results

```plain
Card: **** **** **** 1111
Order: order AB-**34
Email: u***@e******.com
Token: sk_live**************StUv
```

Invalid card numbers are rejected rather than partially revealed:

```python
from shadow_data.exceptions import InvalidCreditCardError
from shadow_data.masking import mask_credit_card

try:
    mask_credit_card('4111111111111112')  # fails the Luhn checksum
except InvalidCreditCardError as error:
    print(error)
```

```plain
Invalid credit card number
```
