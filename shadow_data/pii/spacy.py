import subprocess
import sys
from collections.abc import Iterable

import spacy
from spacy.language import Language

from shadow_data.pii.enums import ModelCore, ModelLang, ModelSize

# spaCy uses two different entity schemes. The `*_core_news_*` models (and most
# non-English pipelines) emit the WikiNER-style labels PER/LOC/ORG/MISC, while
# the English `*_core_web_*` models use the OntoNotes labels PERSON/GPE/FAC/NORP.
# Filtering on only one scheme silently misses entities, so the default covers both.
DEFAULT_SENSITIVE_LABELS = frozenset(
    {
        'PER',
        'PERSON',
        'LOC',
        'GPE',
        'FAC',
        'NORP',
        'ORG',
        'MISC',
    }
)


class ModelSelector:
    @staticmethod
    def select(lang: ModelLang, core: ModelCore, size: ModelSize, auto_download: bool = False) -> Language:
        """
        Loads a spaCy model by combining language, core news, and size.

        Parameters:
        - lang (ModelLang): The language model.
        - core (ModelCoreNews): The core news model.
        - size (ModelSize): The size of the model.
        - auto_download (bool): Download the model via `spacy download` when missing.

        Returns:
        - nlp: The loaded spaCy model.

        Raises:
        - TypeError: If any of the parameters are not of the expected type.
        """
        if not isinstance(lang, ModelLang):
            raise TypeError(f'Expected lang to be an instance of ModelLang, got {type(lang).__name__}')
        if not isinstance(core, ModelCore):
            raise TypeError(f'Expected core to be an instance of ModelCoreNews, got {type(core).__name__}')
        if not isinstance(size, ModelSize):
            raise TypeError(f'Expected size to be an instance of ModelSize, got {type(size).__name__}')

        model_name = f'{lang.value}_{core.value}_{size.value}'
        try:
            nlp = spacy.load(model_name)
        except OSError as error:
            if not auto_download:
                raise RuntimeError(
                    f'Model {model_name} is not installed. Install it with: '
                    f'{sys.executable} -m spacy download {model_name}'
                ) from error
            try:
                # The command is fully built from this interpreter's path and an
                # enum-derived model name, so no external input reaches the shell.
                subprocess.run(  # noqa: S603
                    [sys.executable, '-m', 'spacy', 'download', model_name], check=True
                )
                nlp = spacy.load(model_name)
            except subprocess.CalledProcessError as download_error:
                raise RuntimeError(f'Could not download and load model {model_name}') from download_error
        return nlp


class SensitiveData:
    def __init__(self) -> None:
        self._model_cache: dict[tuple[ModelLang, ModelCore, ModelSize], Language] = {}

    def set_model(
        self, model_lang: ModelLang, model_core: ModelCore, model_size: ModelSize, auto_download: bool = False
    ) -> Language:
        """Loads a pipeline, reusing a previously loaded one for the same combination.

        Loading is expensive (seconds for `trf` models), so the result is cached
        on the instance.
        """
        cache_key = (model_lang, model_core, model_size)
        cached = self._model_cache.get(cache_key)
        if cached is not None:
            return cached

        model_selector = ModelSelector()
        nlp = model_selector.select(model_lang, model_core, model_size, auto_download=auto_download)
        self._model_cache[cache_key] = nlp
        return nlp

    def identify_sensitive_data(
        self,
        model_lang: ModelLang,
        model_core: ModelCore,
        model_size: ModelSize,
        content: str,
        auto_download: bool = False,
        labels: Iterable[str] | None = None,
    ) -> list[tuple[str, str]]:
        nlp = self.set_model(model_lang, model_core, model_size, auto_download=auto_download)
        doc = nlp(content)

        wanted_labels = DEFAULT_SENSITIVE_LABELS if labels is None else frozenset(labels)

        return [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in wanted_labels]
