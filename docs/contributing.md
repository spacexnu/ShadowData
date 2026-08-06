# Contributing

## Setup

ShadowData uses [Poetry](https://python-poetry.org/).

```bash
git clone https://github.com/spacexnu/ShadowData.git
cd ShadowData
poetry install --with dev,docs --extras spacy
```

## Checks

`make all` runs everything CI runs. Run it before opening a pull request.

```bash
make all
```

Individual targets:

| Target | What it does |
|---|---|
| `make test` | Run the test suite |
| `make coverage` | Run tests with a coverage report |
| `make check` | Lint with ruff |
| `make check-fix` | Lint and apply safe fixes |
| `make format` | Format with ruff |
| `make typecheck` | Run mypy |
| `make docs` | Build this documentation |
| `make docs-serve` | Serve the docs with live reload |

## Standards

- **Coverage** must stay at or above 90%. It currently sits at 100%.
- **mypy** runs in strict mode over `shadow_data/`.
- **ruff** enforces `E`, `F`, `I`, `UP`, `B`, and `S` (flake8-bandit), with single quotes
  and a 120-character line length.
- Every bug fix lands with a test that fails on the old behavior.

## Writing docs

The site is built with [MkDocs](https://www.mkdocs.org/) and Material for MkDocs. Pages
live in `docs/` and the navigation is defined in `mkdocs.yml`.

```bash
make docs-serve   # http://127.0.0.1:8000
```

The build runs with `--strict`, so a broken internal link fails the build rather than
shipping.

**Verify your examples.** Every code block in this documentation was executed and its
output pasted in. If you add an example, run it. If its output cannot be reproduced —
because it depends on a generated key, say — note that in the text rather than inventing a
plausible value.

## Security-sensitive changes

This is a library people use to protect personal data, so a few things get extra scrutiny
in review:

- A helper must never return its input unchanged when it was asked to hide something.
- Changing how much of a value stays visible is a behavior change worth a changelog entry
  and, if it widens exposure, a major version.
- Anything that reveals part of a value should say so explicitly in its docstring and docs.

## Releasing

1. Update the version in `pyproject.toml` and `shadow_data/__init__.py` — a test enforces
   that they match.
2. Move the `Unreleased` section of `CHANGELOG.md` under the new version.
3. Tag and publish a GitHub release. The publish workflow builds the distributions and
   uploads them to PyPI via trusted publishing, after checking that the tag matches the
   version in `pyproject.toml`.
