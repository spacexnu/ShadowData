# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **`shadow_data.masking`** — previously an empty stub shipped in the released package.
  `mask` keeps a chosen first/last window and hides the rest; `mask_digits` masks digits
  while preserving separators; `mask_credit_card` keeps the last 4 digits and rejects
  values that fail the Luhn checksum or a plausible length (12–19 digits) instead of
  returning them partially readable; `partial_email` keeps the first character of the user
  and domain. No helper ever returns its input unchanged: when the window to keep covers
  the whole value, the whole value is masked.
- **`shadow_data.reversible`** — previously an empty stub. `Pseudonymizer` issues reversible
  Fernet tokens (`pseudonymize` / `depseudonymize`) and stable one-way tokens
  (`deterministic_pseudonym`, HMAC-SHA256) for joining records across datasets. The HMAC
  subkey is derived from the Fernet key with HKDF-SHA256 under a fixed context string, so
  the two operations never share key material. Deterministic tokens are linkable by
  design — see `docs/reversible.md`.
- New exceptions `InvalidCreditCardError` and `InvalidPseudonymError`.
- Docs `docs/masking.md` and `docs/reversible.md`; examples `examples/masking.md` and
  `examples/reversible.md`.

- Public top-level API: the anonymizers, `Symmetric`, and the exception types are now
  importable directly from `shadow_data`, which also exposes `__version__`. The optional
  spaCy integration is deliberately left out so that importing `shadow_data` never
  requires the extra.
- `py.typed` marker, so type checkers use the annotations the package already ships.
- A documentation site built with MkDocs and Material for MkDocs, consolidating the
  previous `docs/` guides and `examples/*.md` files into a single structured site with a
  guide, an API reference, and a page on choosing between the techniques. Built with
  `--strict` in CI, so broken internal links fail the build.
- `CHANGELOG.md`, plus PyPI metadata (repository, documentation, keywords, classifiers).
- `publish.yml` workflow releasing to PyPI on GitHub release via trusted publishing (OIDC),
  with a guard that the tag matches the version in `pyproject.toml`.
- `make typecheck` and `make all` targets mirroring the CI checks.

### Changed

- Minimum Python lowered from 3.12 to 3.10; CI now tests 3.10 through 3.13.
- Ruff upgraded to 0.16 with an expanded rule set (`E`, `F`, `I`, `UP`, `B`, `S`); `S` is
  flake8-bandit. Exceptions raised while handling another exception now chain with
  `raise ... from`.
- mypy runs in strict mode over `shadow_data/` in CI.
- Coverage is measured against `shadow_data` rather than the whole tree (which counted the
  tests themselves) and the gate is raised from 80% to 90%. Current coverage is 100%.
- pytest configuration moved from `pytest.ini` into `pyproject.toml`.

### Fixed

- **PII detection missed entities from English models.** The entity filter only accepted
  the WikiNER labels (`PER`, `LOC`, `ORG`, `MISC`) emitted by the `core_news` pipelines, so
  the OntoNotes labels (`PERSON`, `GPE`, `FAC`, `NORP`) emitted by `en_core_web_*` were
  silently discarded — person names were never reported when using an English model. The
  default filter now covers both schemes and is configurable via the new `labels` argument.
- **Email anonymization exposed short domains.** `user@ex.com` was returned as
  `****@ex.com`, leaving the domain label in the clear. Domain labels of 3 characters or
  fewer are now fully masked.
- **Brazilian identifiers.** `BrazilIdentifierAnonymizer.anonymize()` returned `None` and
  stripped every digit from the input, which corrupted the result (or raised `ValueError`)
  whenever the content contained other numbers. It now matches CPF and CNPJ anywhere in
  free-form text, like the US anonymizer.
- **Short phone numbers were returned unmasked.** Numbers with 4 digits or fewer passed
  through unchanged; they are now fully masked.
- **IPv4 anonymization matched non-addresses.** Octets above 255 (`999.1.1.1`) and longer
  dotted sequences such as version strings (`1.2.3.4.5`) were treated as IP addresses.

### Changed

- `anonymize()` now returns the cleaned content in addition to setting `cleaned_content`.
- The spaCy pipeline is cached per `SensitiveData` instance instead of being reloaded on
  every `identify_sensitive_data` call.

### Deprecated

- `shadow_data.l10n.usa.IdentifierAnonymizer` and `shadow_data.l10n.brazil.IdentifierAnonymizer`
  are now aliases for `UsaIdentifierAnonymizer` and `BrazilIdentifierAnonymizer`. The old
  names will be removed in 2.0.

### Migration notes

Output changes that may affect existing callers:

| Input | Before | After |
|-------|--------|-------|
| `user@ex.com` | `****@ex.com` | `****@**.com` |
| `1234` (phone) | `1234` | `****` |
| `123.456.789-09` (CPF) | `12*********` | `12*.***.***-**` |
| `12.345.678/0001-95` (CNPJ) | `12************` | `12.***.***/****-**` |

`BrazilIdentifierAnonymizer` no longer raises `ValueError` for content that is not a valid
CPF/CNPJ; unmatched content is returned unchanged, consistent with the US anonymizer.
