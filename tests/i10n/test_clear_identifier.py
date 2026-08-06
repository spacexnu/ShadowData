import pytest

from shadow_data.l10n.ClearIdentifier import ClearIdentifier


class TestClearIdentifier:
    def test_abstract_method_not_implemented(self):
        with pytest.raises(TypeError):
            ClearIdentifier('test')

    def test_anonymize_not_implemented(self):
        class IncompleteIdentifier(ClearIdentifier):
            def anonymize(self):
                super().anonymize()

        instance = IncompleteIdentifier('test')
        instance.anonymize()
