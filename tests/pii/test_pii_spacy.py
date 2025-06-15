import pytest
from unittest.mock import patch, MagicMock

pytest.importorskip('spacy')  # Skip this test if spacy is not installed
from spacy import Language

from shadow_data.pii.enums import ModelLang, ModelCore, ModelSize
from shadow_data.pii.spacy import ModelSelector, SensitiveData
import subprocess


class TestModelSelector:
    def test_select_valid_model(self):
        with patch('spacy.load') as mock_spacy_load:
            mock_spacy_load.return_value = MagicMock()

            lang = ModelLang.ENGLISH
            core = ModelCore.NEWS
            size = ModelSize.SMALL

            nlp = ModelSelector.select(lang, core, size)

            mock_spacy_load.assert_called_once_with('en_core_news_sm')
            assert isinstance(nlp, MagicMock)

    def test_select_invalid_lang_type(self):
        core = ModelCore.NEWS
        size = ModelSize

        with pytest.raises(TypeError):
            ModelSelector.select('en', core, size)

    def test_select_invalid_core_type(self):
        lang = ModelLang.ENGLISH
        size = ModelSize.SMALL

        with pytest.raises(TypeError):
            ModelSelector.select(lang, 'core', size)

    def test_select_invalid_size_type(self):
        lang = ModelLang.ENGLISH
        core = ModelCore.NEWS

        with pytest.raises(TypeError):
            ModelSelector.select(lang, core, 'big')

    def test_select_model_download(self):
        with patch('spacy.load') as mock_spacy_load, patch('subprocess.run') as mock_subprocess_run:
            mock_spacy_load.side_effect = [OSError, MagicMock()]

            mock_subprocess_run.return_value = MagicMock()

            lang = ModelLang.ENGLISH
            core = ModelCore.NEWS
            size = ModelSize.SMALL

            nlp = ModelSelector.select(lang, core, size)

            mock_subprocess_run.assert_called_once_with(
                ['python', '-m', 'spacy', 'download', 'en_core_news_sm'], check=True
            )
            assert mock_spacy_load.call_count == 2
            assert isinstance(nlp, MagicMock)

    def test_select_model_download_failure(self):
        with patch('spacy.load', side_effect=OSError), patch(
            'subprocess.run', side_effect=subprocess.CalledProcessError(1, 'cmd')
        ) as mock_subprocess_run:
            lang = ModelLang.ENGLISH
            core = ModelCore.NEWS
            size = ModelSize.SMALL

            with pytest.raises(RuntimeError):
                ModelSelector.select(lang, core, size)

            mock_subprocess_run.assert_called_once_with(
                ['python', '-m', 'spacy', 'download', 'en_core_news_sm'], check=True
            )


class TestSensitiveData:
    @pytest.fixture
    def sensitive_data_instance(self):
        return SensitiveData()

    @pytest.fixture
    def mock_nlp(self, monkeypatch):
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_doc.ents = [
            MagicMock(text='John Doe', label_='PER'),
            MagicMock(text='New York', label_='LOC'),
            MagicMock(text='Acme Corp', label_='ORG'),
            MagicMock(text='Miscellaneous', label_='MISC'),
            MagicMock(text='NonSensitive', label_='NON_SENSITIVE'),
        ]
        mock_nlp.return_value = mock_doc

        monkeypatch.setattr(SensitiveData, 'set_model', lambda self, *args: mock_nlp)
        return mock_nlp

    @pytest.fixture
    def mock_empty_nlp(self, monkeypatch):
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_doc.ents = []
        mock_nlp.return_value = mock_doc

        monkeypatch.setattr(SensitiveData, 'set_model', lambda self, *args: mock_nlp)
        return mock_nlp

    def test_identify_sensitive_data(self, sensitive_data_instance, mock_nlp):
        content = (
            'John Doe works at Acme Corp in New York. Miscellaneous information about something. NonSensitive data.'
        )
        expected_output = [('John Doe', 'PER'), ('New York', 'LOC'), ('Acme Corp', 'ORG'), ('Miscellaneous', 'MISC')]

        result = sensitive_data_instance.identify_sensitive_data(
            ModelLang.ENGLISH, ModelCore.NEWS, ModelSize.SMALL, content
        )
        assert result == expected_output

    def test_identify_sensitive_data_empty(self, sensitive_data_instance, mock_empty_nlp):
        # Test with empty content
        content = ''
        expected_output = []

        result = sensitive_data_instance.identify_sensitive_data(
            ModelLang.ENGLISH, ModelCore.NEWS, ModelSize.SMALL, content
        )
        assert result == expected_output

    def test_identify_sensitive_data_no_entities(self, sensitive_data_instance, mock_nlp):
        mock_nlp.return_value.ents = []  # No entities
        content = 'This is a sentence with no sensitive data.'
        expected_output = []

        result = sensitive_data_instance.identify_sensitive_data(
            ModelLang.ENGLISH, ModelCore.NEWS, ModelSize.SMALL, content
        )
        assert result == expected_output

    def test_set_model(self):
        model_lang = ModelLang.PORTUGUESE
        model_core = ModelCore.NEWS
        model_size = ModelSize.SMALL
        expected_language = Language()

        model_selector_mock = MagicMock(spec=ModelSelector)
        model_selector_mock.select.return_value = expected_language

        with patch('shadow_data.pii.spacy.ModelSelector', return_value=model_selector_mock):
            sensitive_data = SensitiveData()

            result = sensitive_data.set_model(model_lang, model_core, model_size)

            model_selector_mock.select.assert_called_once_with(model_lang, model_core, model_size)
            assert result == expected_language
