# PII Detection (spaCy)

PII detection is powered by spaCy and is an optional dependency.

## Install

```bash
pip install shadow_data[spacy]
```

## Use a model

```python
from shadow_data.pii.enums import ModelLang, ModelCore, ModelSize
from shadow_data.pii.spacy import SensitiveData

content = 'Alice Johnson works at Example Corp in Seattle.'
instance = SensitiveData()
entities = instance.identify_sensitive_data(
    ModelLang.ENGLISH,
    ModelCore.WEB,
    ModelSize.SMALL,
    content,
)
print(entities)
```

## Entity labels

spaCy pipelines use two different entity schemes. The `core_news` pipelines (and most
non-English models) emit WikiNER-style labels — `PER`, `LOC`, `ORG`, `MISC` — while the
English `core_web` pipelines use OntoNotes labels such as `PERSON`, `GPE`, `FAC`, `NORP`.

The default filter covers both schemes: `PER`, `PERSON`, `LOC`, `GPE`, `FAC`, `NORP`,
`ORG`, `MISC`. Pass `labels=` to narrow or extend it:

```python
entities = instance.identify_sensitive_data(
    ModelLang.ENGLISH,
    ModelCore.WEB,
    ModelSize.SMALL,
    content,
    labels={'PERSON', 'GPE'},
)
```

## Notes
- The model name is assembled as `{lang}_{core}_{size}` (for example, `en_core_web_sm`).
- Models must be installed before use. Pass `auto_download=True` only in trusted setup flows where runtime package installation is acceptable, since it runs `spacy download` in a subprocess.
- A loaded pipeline is cached per `SensitiveData` instance, so reuse the same instance across calls to avoid reloading the model.
