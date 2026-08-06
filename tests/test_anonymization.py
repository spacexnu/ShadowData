from shadow_data.anonymization import Ipv4Anonymization, TextProcessor


def test_anonymize_single_term():
    original_content = "The user's name is João Silva."
    original_term = 'João Silva'
    to_replace = 'ANONYMOUS'

    expected_output = "The user's name is ANONYMOUS."

    assert TextProcessor.replace_text(original_term, to_replace, original_content) == expected_output


def test_anonymize_multiple_occurrences():
    original_content = 'João Silva bought a car. João Silva sold a house.'
    original_term = 'João Silva'
    to_replace = 'ANONYMOUS'

    expected_output = 'ANONYMOUS bought a car. ANONYMOUS sold a house.'

    assert TextProcessor.replace_text(original_term, to_replace, original_content) == expected_output


def test_anonymize_no_match():
    original_content = "The user's name is Carlos Pereira."
    original_term = 'João Silva'
    to_replace = 'ANONYMOUS'

    expected_output = original_content

    assert TextProcessor.replace_text(original_term, to_replace, original_content) == expected_output


def test_anonymize_partial_match():
    original_content = 'João Silva bought a car. João sold a house.'
    original_term = 'João Silva'
    to_replace = 'ANONYMOUS'

    expected_output = 'ANONYMOUS bought a car. João sold a house.'

    assert TextProcessor.replace_text(original_term, to_replace, original_content) == expected_output


def test_anonymize_single_ipv4():
    text = 'The IP is 192.168.1.100.'
    expected_output = 'The IP is 192.X.X.X.'

    assert Ipv4Anonymization.anonymize_ipv4(text) == expected_output


def test_anonymize_multiple_ipv4():
    text = 'The first IP is 192.168.1.100, and the second IP is 10.0.0.1.'
    expected_output = 'The first IP is 192.X.X.X, and the second IP is 10.X.X.X.'

    assert Ipv4Anonymization.anonymize_ipv4(text) == expected_output


def test_no_ipv4_found():
    text = 'There is no IP address here.'
    expected_output = text

    assert Ipv4Anonymization.anonymize_ipv4(text) == expected_output


def test_anonymize_partial_ipv4():
    text = 'The IP address is 192.168.'
    expected_output = text

    assert Ipv4Anonymization.anonymize_ipv4(text) == expected_output
