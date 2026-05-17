# ShadowData Docs

This folder provides focused guides for the current feature set.

## Contents
- `docs/usage.md`: core anonymization helpers and localized identifiers
- `docs/cryptography.md`: symmetric encryption and key handling
- `docs/pii.md`: spaCy-based PII detection

## Quick pointers
- PII detection is optional and requires the `shadow_data[spacy]` extra.
- spaCy models must be installed before use. Runtime downloads are opt-in.
- Masking and reversible transforms are planned but not yet implemented.
