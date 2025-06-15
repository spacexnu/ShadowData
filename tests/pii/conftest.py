import pytest
import importlib.util


def is_module_available(module_name):
    """Check if a module is available without importing it"""
    return importlib.util.find_spec(module_name) is not None


def pytest_collection_modifyitems(items):
    """Skip tests that require spacy if spacy is not installed"""
    if not is_module_available('spacy'):
        skip_spacy = pytest.mark.skip(reason='Spacy module not installed')
        for item in items:
            if 'test_pii_spacy.py' in item.nodeid:
                item.add_marker(skip_spacy)
