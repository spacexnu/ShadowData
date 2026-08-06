import pytest

from shadow_data.anonymization import Ipv4Anonymization


class TestIpv4Anonymization:
    def test_anonymize_single_ipv4(self):
        text = 'The IP is 192.168.1.100.'
        expected_output = 'The IP is 192.X.X.X.'

        assert Ipv4Anonymization.anonymize_ipv4(text) == expected_output

    def test_anonymize_multiple_ipv4(self):
        text = 'The first IP is 192.168.1.100, and the second IP is 10.0.0.1.'
        expected_output = 'The first IP is 192.X.X.X, and the second IP is 10.X.X.X.'

        assert Ipv4Anonymization.anonymize_ipv4(text) == expected_output

    def test_no_ipv4_found(self):
        text = 'There is no IP address here.'
        expected_output = text

        assert Ipv4Anonymization.anonymize_ipv4(text) == expected_output

    def test_anonymize_partial_ipv4(self):
        text = 'The IP address is 192.168.'
        expected_output = text

        assert Ipv4Anonymization.anonymize_ipv4(text) == expected_output

    @pytest.mark.parametrize(
        'text',
        [
            'Not an IP: 999.1.1.1',
            'Not an IP: 256.256.256.256',
            'Not an IP: 192.168.1.300',
            'A version number 1.2.3.4.5.6',
        ],
    )
    def test_out_of_range_octets_are_not_treated_as_ipv4(self, text):
        assert Ipv4Anonymization.anonymize_ipv4(text) == text

    def test_boundary_octets_are_anonymized(self):
        text = 'Range 0.0.0.0 to 255.255.255.255'
        assert Ipv4Anonymization.anonymize_ipv4(text) == 'Range 0.X.X.X to 255.X.X.X'

    def test_custom_pattern_masks_every_octet(self):
        text = 'The IP is 192.168.1.100.'
        assert Ipv4Anonymization.anonymize_ipv4(text, pattern='X.X.X.X') == 'The IP is X.X.X.X.'
