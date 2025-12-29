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

content = "Alice Johnson works at Example Corp in Seattle."
instance = SensitiveData()
entities = instance.identify_sensitive_data(
    ModelLang.ENGLISH,
    ModelCore.WEB,
    ModelSize.SMALL,
    content,
)
print(entities)
```

## Notes
- The model name is assembled as `{lang}_{core}_{size}` (for example, `en_core_web_sm`).
- Models are downloaded automatically on first use if missing.
- Returned entities are filtered to these labels: `PER`, `LOC`, `ORG`, `MISC`.
