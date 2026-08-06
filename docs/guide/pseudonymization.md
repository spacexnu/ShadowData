# Pseudonymization

`Pseudonymizer` replaces values with tokens that can be turned back into the original by
whoever holds the key. It offers two operations with deliberately different security
properties.

```python
from shadow_data.reversible import Pseudonymizer
```

## Reversible tokens

`pseudonymize` encrypts with Fernet, the same primitive behind
[`Symmetric`](encryption.md). Every call produces a different token for the same input, so
tokens cannot be correlated with each other.

```python
from shadow_data.reversible import Pseudonymizer

pseudonymizer = Pseudonymizer()

token = pseudonymizer.pseudonymize('user@example.com')
print(token)
print(pseudonymizer.depseudonymize(token))

# The same value encrypts differently every time.
print(pseudonymizer.pseudonymize('user@example.com') != token)
```

```plain
gAAAAABqdIcLaY7VdzuClEbUZnAw0s7a0KPKZqlvMDFQR1hGRaZM6Wzsv22KVZ4vZS_...
user@example.com
True
```

## Key handling

A key is generated when none is supplied. Read it from `key` and store it somewhere safe —
tokens are worthless without it, and there is no recovery path.

```python
from shadow_data.reversible import Pseudonymizer

pseudonymizer = Pseudonymizer()
key = pseudonymizer.key  # b'...' — store this, and not in source control

token = pseudonymizer.pseudonymize('user@example.com')

# A later process reverses the token with the stored key.
print(Pseudonymizer(key).depseudonymize(token))
```

```plain
user@example.com
```

!!! danger "The key is the whole security boundary"

    Anyone with the key can reverse every token you ever issued. Keep it in a secrets
    manager or environment variable, never in the repository, and never in logs.

`depseudonymize` raises `InvalidPseudonymError` for a token produced by a different key, a
malformed token, or a deterministic token. Constructing a `Pseudonymizer` with an invalid
key raises `InvalidCipherKeyError` immediately, rather than failing later at first use.

## Deterministic tokens

`deterministic_pseudonym` returns a stable HMAC-SHA256 token: the same input always maps to
the same token under the same key. That is what allows records to be joined across
datasets.

```python
from shadow_data.reversible import Pseudonymizer

pseudonymizer = Pseudonymizer()

orders = ['ana@example.com', 'bob@example.com', 'ana@example.com']
print([pseudonymizer.deterministic_pseudonym(email)[:12] for email in orders])
```

```plain
['5792515379f4', 'de1605d2cc99', '5792515379f4']
```

The first and third orders are visibly the same customer. That is the point of the
operation — and also its risk.

!!! warning "Deterministic tokens are linkable by design"

    Repeated values stay visible as repeated tokens, so the shape of your data leaks even
    when the values do not. And because the mapping is stable, anyone holding the key can
    confirm a guessed value by recomputing its token — a realistic attack for low-entropy
    inputs such as email addresses or national identifiers, where the space of plausible
    guesses is small.

    Prefer `pseudonymize` unless you actually need the join.

Deterministic tokens are one-way. They cannot be reversed, not even with the key:

```python
from shadow_data.exceptions import InvalidPseudonymError
from shadow_data.reversible import Pseudonymizer

pseudonymizer = Pseudonymizer()
token = pseudonymizer.deterministic_pseudonym('secret')

try:
    pseudonymizer.depseudonymize(token)
except InvalidPseudonymError as error:
    print(error)
```

```plain
Token was not produced by this key, or is not reversible
```

## Why the two modes never share key material

Both operations are driven by the same key you hold, but the HMAC subkey is derived from
the Fernet key with HKDF-SHA256 under a fixed context string
(`shadow_data.reversible.deterministic.v1`). Reusing one key directly for two different
primitives is a well-known footgun; domain-separating them means compromising one does not
directly expose the other.

The derivation is deterministic, so the same key always yields the same subkey — which is
what makes deterministic tokens stable across processes and machines.
