import pytest

from shadow_data.exceptions import InvalidCipherKeyError, InvalidPseudonymError
from shadow_data.reversible import Pseudonymizer


class TestPseudonymizer:
    def test_generates_a_key_when_none_is_given(self):
        pseudonymizer = Pseudonymizer()
        assert isinstance(pseudonymizer.key, bytes)
        assert pseudonymizer.key

    def test_round_trip(self):
        pseudonymizer = Pseudonymizer()
        token = pseudonymizer.pseudonymize('user@example.com')
        assert pseudonymizer.depseudonymize(token) == 'user@example.com'

    def test_token_does_not_contain_the_original_value(self):
        pseudonymizer = Pseudonymizer()
        assert 'user@example.com' not in pseudonymizer.pseudonymize('user@example.com')

    def test_repeated_calls_produce_different_tokens(self):
        pseudonymizer = Pseudonymizer()
        first = pseudonymizer.pseudonymize('same value')
        second = pseudonymizer.pseudonymize('same value')

        assert first != second
        assert pseudonymizer.depseudonymize(first) == pseudonymizer.depseudonymize(second) == 'same value'

    def test_round_trip_with_an_explicit_key(self):
        key = Pseudonymizer().key
        token = Pseudonymizer(key).pseudonymize('shared secret')

        assert Pseudonymizer(key).depseudonymize(token) == 'shared secret'

    def test_empty_string_round_trips(self):
        pseudonymizer = Pseudonymizer()
        assert pseudonymizer.depseudonymize(pseudonymizer.pseudonymize('')) == ''

    def test_unicode_round_trips(self):
        pseudonymizer = Pseudonymizer()
        assert pseudonymizer.depseudonymize(pseudonymizer.pseudonymize('João Ação')) == 'João Ação'

    def test_another_key_cannot_reverse_the_token(self):
        token = Pseudonymizer().pseudonymize('secret')

        with pytest.raises(InvalidPseudonymError):
            Pseudonymizer().depseudonymize(token)

    @pytest.mark.parametrize('token', ['not-a-token', '', 'gAAAAAB'])
    def test_malformed_tokens_are_rejected(self, token):
        with pytest.raises(InvalidPseudonymError):
            Pseudonymizer().depseudonymize(token)

    def test_invalid_key_is_rejected(self):
        with pytest.raises(InvalidCipherKeyError):
            Pseudonymizer(b'not-a-valid-fernet-key')


class TestDeterministicPseudonym:
    def test_same_value_and_key_produce_the_same_token(self):
        key = Pseudonymizer().key

        assert Pseudonymizer(key).deterministic_pseudonym('user@example.com') == (
            Pseudonymizer(key).deterministic_pseudonym('user@example.com')
        )

    def test_different_values_produce_different_tokens(self):
        pseudonymizer = Pseudonymizer()

        assert pseudonymizer.deterministic_pseudonym('a') != pseudonymizer.deterministic_pseudonym('b')

    def test_different_keys_produce_different_tokens(self):
        assert Pseudonymizer().deterministic_pseudonym('same') != Pseudonymizer().deterministic_pseudonym('same')

    def test_token_is_a_sha256_hex_digest(self):
        token = Pseudonymizer().deterministic_pseudonym('user@example.com')

        assert len(token) == 64
        assert all(char in '0123456789abcdef' for char in token)

    def test_token_does_not_contain_the_original_value(self):
        assert 'user' not in Pseudonymizer().deterministic_pseudonym('user')

    def test_deterministic_tokens_are_not_reversible(self):
        pseudonymizer = Pseudonymizer()
        token = pseudonymizer.deterministic_pseudonym('secret')

        with pytest.raises(InvalidPseudonymError):
            pseudonymizer.depseudonymize(token)

    def test_subkey_is_derived_once_and_reused(self):
        pseudonymizer = Pseudonymizer()
        first = pseudonymizer.deterministic_pseudonym('value')
        second = pseudonymizer.deterministic_pseudonym('value')

        assert first == second

    def test_deterministic_subkey_differs_from_the_encryption_key(self):
        pseudonymizer = Pseudonymizer()
        pseudonymizer.deterministic_pseudonym('warm up the cache')

        assert pseudonymizer._deterministic_key != pseudonymizer.key
