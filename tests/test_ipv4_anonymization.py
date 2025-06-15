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

    def test_anonymize_ipv4_custom_pattern(self):
        text = 'The IP is 192.168.1.100.'
        custom_pattern = r'\1-YYY-YYY-YYY'
        expected_output = 'The IP is 192-YYY-YYY-YYY.'

        assert Ipv4Anonymization.anonymize_ipv4(text, custom_pattern) == expected_output
