# Choosing a technique

ShadowData offers four ways to handle a sensitive value. They differ in two things: whether
the original can be recovered, and how much of it stays readable.

| Technique | Reversible? | Output | Use when |
|---|---|---|---|
| [Anonymization](anonymization.md) | No | Redacted, not recognizable | The value must be gone for good — logs, exports, test fixtures |
| [Masking](masking.md) | No | Recognizable, mostly hidden | A human needs to confirm a value — receipts, support screens |
| [Pseudonymization](pseudonymization.md) | Yes, with the key | Opaque token | You need the value back later, or need to join on it |
| [Encryption](encryption.md) | Yes, with the key | Ciphertext | You need the underlying primitive directly |

## Anonymization vs. masking

Both are one-way, and the difference is intent.

Anonymization aims for *unrecognizable*: `EmailAnonymization.anonymize_email` hides the
whole user part, so `user@example.com` becomes `****@****ple.com`. Nobody reading the output
should be able to tell whose address it was.

Masking aims for *confirmable*: `partial_email` leaves the first character, so
`user@example.com` becomes `u***@e******.com`. A support agent can check that it matches
the address the customer just read out, without the full value appearing on screen.

Masking necessarily leaks more. Use it only where a human genuinely needs the hint.

## Pseudonymization: which of the two tokens?

`Pseudonymizer` offers two operations with very different properties.

`pseudonymize` produces a different token every time, even for the same input. Tokens
cannot be correlated with each other, which is the safer default.

`deterministic_pseudonym` produces the same token for the same input, which is what lets
you join records across datasets — and which also means the tokens leak equality.

!!! warning "Deterministic tokens are linkable by design"

    Repeated values stay visible as repeated tokens, and anyone holding the key can confirm
    a guessed value by recomputing its token. For low-entropy inputs such as email
    addresses or national identifiers, that is a realistic attack. Reach for
    `deterministic_pseudonym` only when you actually need the join.

## Pseudonymization vs. encryption

`Pseudonymizer` is built on `Symmetric`, the Fernet wrapper. Use `Pseudonymizer` when you
are replacing values in a dataset — it returns strings, handles key derivation for the
deterministic mode, and raises a domain-specific error for bad tokens. Use `Symmetric`
directly when you just need to encrypt a blob of text.

## What none of this does

These helpers operate on values you have already identified. Finding the sensitive values
in unstructured text is a separate problem — see [PII detection](pii-detection.md) — and
one that no model solves perfectly. Treat detection as a first pass to be reviewed, not as
a guarantee.
