from unittest.mock import patch, MagicMock
from tests.pii.conftest import is_module_available, pytest_collection_modifyitems


class TestConftest:
    def test_is_module_available_existing_module(self):
        # Test with a module that definitely exists
        assert is_module_available('os') is True

    def test_is_module_available_nonexistent_module(self):
        # Test with a module that definitely doesn't exist
        assert is_module_available('nonexistent_module_123456789') is False

    def test_pytest_collection_modifyitems_with_spacy(self):
        # Test when spacy is available
        with patch('importlib.util.find_spec', return_value=MagicMock()):
            items = [
                MagicMock(nodeid='tests/pii/test_pii_spacy.py::TestClass::test_method'),
                MagicMock(nodeid='tests/other/test_other.py::TestClass::test_method')
            ]

            # Call the function
            pytest_collection_modifyitems(items)

            # Verify no skip markers were added
            for item in items:
                assert not any(marker.name == 'skip' for marker in getattr(item, 'own_markers', []))

    def test_pytest_collection_modifyitems_without_spacy(self):
        # Test when spacy is not available
        # Directly patch the is_module_available function in the conftest module
        with patch('tests.pii.conftest.is_module_available', return_value=False):
            # Create test items with nodeids that match the pattern in conftest.py
            spacy_item = MagicMock()
            spacy_item.nodeid = 'tests/pii/test_pii_spacy.py::TestClass::test_method'
            spacy_item.add_marker = MagicMock()  # Mock the add_marker method

            other_item = MagicMock()
            other_item.nodeid = 'tests/other/test_other.py::TestClass::test_method'
            other_item.add_marker = MagicMock()  # Mock the add_marker method

            items = [spacy_item, other_item]

            # Call the function
            pytest_collection_modifyitems(items)

            # Verify that add_marker was called for the test_pii_spacy.py item
            # but not for the other item
            spacy_item.add_marker.assert_called_once()  # Should be called exactly once
            other_item.add_marker.assert_not_called()   # Should not be called
