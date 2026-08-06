# PII detection

Finding sensitive values in unstructured text is a different problem from redacting them.
ShadowData uses [spaCy](https://spacy.io/) named entity recognition to locate candidates,
which you then feed to the anonymization or masking helpers.

## Installation

spaCy is an optional extra:

```bash
pip install "shadow_data[spacy]"
```

Models are downloaded separately. The model name is assembled as `{lang}_{core}_{size}`:

```bash
python -m spacy download en_core_web_sm
```

Because the extra is optional, PII detection is not re-exported from the top-level package.
Import it from its own module:

```python
from shadow_data.pii.spacy import SensitiveData
```

## Detecting entities

```python
from shadow_data.pii.enums import ModelCore, ModelLang, ModelSize
from shadow_data.pii.spacy import SensitiveData

content = 'Alice Johnson works at Example Corp in Seattle.'

detector = SensitiveData()
print(detector.identify_sensitive_data(ModelLang.ENGLISH, ModelCore.WEB, ModelSize.SMALL, content))
```

```plain
[('Alice Johnson', 'PERSON'), ('Example Corp', 'ORG'), ('Seattle', 'GPE')]
```

The result is a list of `(text, label)` pairs.

## Selecting a model

Three enums combine into the model name:

| Enum | Values |
|---|---|
| `ModelLang` | `ENGLISH`, `PORTUGUESE`, `SPANISH`, `GERMAN`, `FRENCH` |
| `ModelCore` | `NEWS` (`core_news`), `WEB` (`core_web`) |
| `ModelSize` | `SMALL`, `MEDIUM`, `LARGE`, `TRF` |

Larger models are more accurate and slower. `TRF` is transformer-based and the slowest by a
wide margin.

Not every combination exists — spaCy publishes `en_core_web_*` for English and
`xx_core_news_*` for most other languages. Asking for a model that is not installed raises
`RuntimeError` with the exact command to install it.

Passing a value that is not the right enum raises `TypeError`.

## Entity labels

spaCy pipelines use two different entity schemes, and this trips people up constantly.

- The `core_news` pipelines (and most non-English models) emit WikiNER labels: `PER`,
  `LOC`, `ORG`, `MISC`.
- The English `core_web` pipelines emit OntoNotes labels: `PERSON`, `GPE`, `FAC`, `NORP`,
  and others.

The default filter covers both schemes, so person names are reported whichever pipeline you
choose: `PER`, `PERSON`, `LOC`, `GPE`, `FAC`, `NORP`, `ORG`, `MISC`.

Pass `labels` to narrow or extend it:

```python
from shadow_data.pii.enums import ModelCore, ModelLang, ModelSize
from shadow_data.pii.spacy import SensitiveData

detector = SensitiveData()
print(
    detector.identify_sensitive_data(
        ModelLang.ENGLISH,
        ModelCore.WEB,
        ModelSize.SMALL,
        'Alice Johnson works at Example Corp in Seattle.',
        labels={'PERSON'},
    )
)
```

```plain
[('Alice Johnson', 'PERSON')]
```

## Reuse the detector

Loading a pipeline is expensive — seconds, for `TRF` models. `SensitiveData` caches each
loaded pipeline on the instance, so reuse one instance rather than constructing a new one
per call.

```python
detector = SensitiveData()

for document in documents:
    detector.identify_sensitive_data(ModelLang.ENGLISH, ModelCore.WEB, ModelSize.SMALL, document)
```

## Automatic downloads

`auto_download=True` runs `python -m spacy download <model>` in a subprocess when the model
is missing.

```python
detector.identify_sensitive_data(ModelLang.ENGLISH, ModelCore.WEB, ModelSize.SMALL, content, auto_download=True)
```

!!! warning "Opt-in for a reason"

    This installs a package at runtime. Use it in trusted setup flows and development
    environments, not in production request paths or anywhere the model name could be
    influenced by untrusted input. The default is off, and the error you get instead tells
    you exactly what to install.

## A worked example

Detection quality varies by language and model. This Portuguese example uses the large news
model:

```python
from shadow_data.pii.enums import ModelCore, ModelLang, ModelSize
from shadow_data.pii.spacy import SensitiveData

content = (
    'João Silva mora na Rua das Acácias, 123, Apartamento 5B, São Paulo, SP, 01310-000. '
    'Ele trabalha como Gerente de Projetos na TechNova Soluções, uma empresa de tecnologia '
    'em crescimento localizada na Avenida Paulista, 987, São Paulo, SP, 01311-200. '
    'Você pode contatá-lo pelo telefone (11) 91234-5678 ou pelo e-mail joao.silva@technova.com.'
)

detector = SensitiveData()
print(detector.identify_sensitive_data(ModelLang.PORTUGUESE, ModelCore.NEWS, ModelSize.LARGE, content))
```

```plain
[('João Silva', 'PER'), ('Rua das Acácias', 'LOC'), ('Apartamento 5B', 'LOC'),
 ('São Paulo', 'LOC'), ('SP', 'LOC'), ('Gerente de Projetos', 'MISC'),
 ('TechNova Soluções', 'LOC'), ('Avenida Paulista', 'LOC'), ('São Paulo', 'LOC'),
 ('SP', 'LOC'), ('joao.silva@technova.com', 'LOC')]
```

Look closely at that output. `TechNova Soluções` is labelled `LOC` rather than `ORG`, the
email address is also labelled `LOC`, and the phone number is not detected at all.

!!! note "Detection is a first pass, not a guarantee"

    NER models miss entities, mislabel them, and behave differently across languages and
    versions. Use detection to narrow down what a human or a rule-based pass should look
    at — and use the deterministic helpers
    ([anonymization](anonymization.md), [identifiers](identifiers.md)) for values with a
    known format, such as emails, phone numbers, and national IDs. Those do not guess.
