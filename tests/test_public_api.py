from pathlib import Path

import pytest

import shadow_data

PYPROJECT = Path(__file__).resolve().parent.parent / 'pyproject.toml'


class TestPublicApi:
    def test_every_exported_name_is_importable(self):
        for name in shadow_data.__all__:
            assert hasattr(shadow_data, name), f'{name} is listed in __all__ but not exported'

    def test_version_matches_pyproject(self):
        tomllib = pytest.importorskip('tomllib', reason='tomllib requires Python 3.11+')
        metadata = tomllib.loads(PYPROJECT.read_text(encoding='utf-8'))
        assert shadow_data.__version__ == metadata['tool']['poetry']['version']

    def test_package_ships_a_py_typed_marker(self):
        assert (Path(shadow_data.__file__).parent / 'py.typed').is_file()

    def test_spacy_is_not_imported_by_the_top_level_package(self):
        # The spaCy extra is optional, so importing shadow_data must not require it.
        assert 'shadow_data.pii.spacy' not in dir(shadow_data)
