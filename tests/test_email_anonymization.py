import pytest
from unittest.mock import patch, MagicMock

from shadow_data.anonymization import EmailAnonymization
from shadow_data.exceptions import InvalidEmailError


class TestEmailAnonymization:
    def test_anonymize_email_valid(self):
        email = 'user@example.com'
        expected = '****@****ple.com'
        result = EmailAnonymization.anonymize_email(email)
        assert result == expected

    def test_anonymize_email_short_domain(self):
        email = 'user@ex.com'
        expected = '****@ex.com'
        result = EmailAnonymization.anonymize_email(email)
        assert result == expected

    def test_anonymize_email_no_domain(self):
        email = 'user@'
        with pytest.raises(InvalidEmailError):
            EmailAnonymization.anonymize_email(email)

    def test_anonymize_email_no_user(self):
        email = '@example.com'
        with pytest.raises(InvalidEmailError):
            EmailAnonymization.anonymize_email(email)

    def test_anonymize_email_invalid_format(self):
        email = 'userexample.com'
        with pytest.raises(InvalidEmailError):
            EmailAnonymization.anonymize_email(email)

    def test_anonymize_email_multiple_subdomains(self):
        email = 'user@sub.example.com'
        expected = '****@sub.example.com'
        result = EmailAnonymization.anonymize_email(email)
        assert result == expected

    def test_anonymize_email_exception_handling(self):
        # This test covers the exception handling in the try-except block
        # by creating a scenario where email.split('@') succeeds but
        # domain.split('.') would cause an IndexError
        email = 'user@.'
        with pytest.raises(InvalidEmailError):
            EmailAnonymization.anonymize_email(email)

    def test_anonymize_email_edge_cases(self):
        """Test edge cases that trigger exception handling in anonymize_email.

        This test covers lines 95-97 in anonymization.py by testing emails that
        pass the regex validation but cause exceptions during processing.
        """
        # Test case 1: Email with a valid format but will cause issues during processing
        # This should trigger the except block for ValueError/IndexError
        with pytest.raises(InvalidEmailError):
            # This email has a valid format according to the regex but will cause
            # an IndexError when trying to access domain_parts[0] because the domain
            # part after @ doesn't have any dots
            EmailAnonymization.anonymize_email("user@nodots")

        # Test case 2: Another edge case that should trigger the except block
        with pytest.raises(InvalidEmailError):
            # This email has multiple @ symbols which will pass the regex but
            # cause a ValueError when unpacking the result of email.split('@')
            EmailAnonymization.anonymize_email("user@domain@example.com")
