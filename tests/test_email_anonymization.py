import pytest

from shadow_data.anonymization import EmailAnonymization
from shadow_data.exceptions import InvalidEmailError


class TestEmailAnonymization:
    def test_anonymize_email_valid(self):
        email = 'user@example.com'
        expected = '****@****ple.com'
        result = EmailAnonymization.anonymize_email(email)
        assert result == expected

    @pytest.mark.parametrize(
        'email, expected',
        [
            ('user@ex.com', '****@**.com'),
            ('user@abc.com', '****@***.com'),
            ('user@abcd.com', '****@*bcd.com'),
            ('user@a.io', '****@*.io'),
        ],
    )
    def test_anonymize_email_short_domain_is_fully_masked(self, email, expected):
        assert EmailAnonymization.anonymize_email(email) == expected

    def test_anonymize_email_multi_label_domain(self):
        assert EmailAnonymization.anonymize_email('user@example.co.uk') == '****@****ple.co.uk'

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
