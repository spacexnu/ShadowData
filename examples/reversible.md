# Reversible pseudonymization

Pseudonymization replaces a value with a token you can turn back into the original, as long
as you hold the key.

```python
from shadow_data.reversible import Pseudonymizer

pseudonymizer = Pseudonymizer()
key = pseudonymizer.key  # store this somewhere safe; tokens are worthless without it

token = pseudonymizer.pseudonymize('user@example.com')
print(f'Token: {token}')
print(f'Reversed: {pseudonymizer.depseudonymize(token)}')

# The same value encrypts to a different token every time, so tokens cannot be correlated.
print(pseudonymizer.pseudonymize('user@example.com') != token)

# A later process can reverse the token with the stored key.
print(Pseudonymizer(key).depseudonymize(token))
```

### Results

```plain
Token: gAAAAABn...
Reversed: user@example.com
True
user@example.com
```

## Joining datasets with deterministic tokens

When records must be matched across datasets, use `deterministic_pseudonym`: the same input
always maps to the same token.

```python
from shadow_data.reversible import Pseudonymizer

pseudonymizer = Pseudonymizer()

orders = ['ana@example.com', 'bob@example.com', 'ana@example.com']
print([pseudonymizer.deterministic_pseudonym(email)[:12] for email in orders])
```

```plain
['5792515379f4', 'de1605d2cc99', '5792515379f4']
```

The exact tokens depend on the key, so they differ between runs that generate a new one —
what stays true is that equal inputs produce equal tokens under the same key.

The first and third orders are visibly the same customer — that is the point, and also the
risk. Deterministic tokens leak equality and let anyone with the key confirm a guessed
value, which matters for low-entropy inputs like emails or national IDs. They are also
one-way: `depseudonymize` raises `InvalidPseudonymError` for them.
