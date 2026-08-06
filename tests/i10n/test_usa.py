from shadow_data.l10n.usa import IdentifierAnonymizer, UsaIdentifierAnonymizer


class TestIdentifierAnonymizer:
    def test_anonymize_returns_the_cleaned_content(self):
        anonymizer = UsaIdentifierAnonymizer('My SSN is 123-45-6789.')
        assert anonymizer.anonymize() == 'My SSN is XXX-XX-6789.'

    def test_deprecated_alias_points_to_the_same_class(self):
        assert IdentifierAnonymizer is UsaIdentifierAnonymizer

    def test_anonymize_ssn(self):
        content = 'My SSN is 123-45-6789.'
        expected_output = 'My SSN is XXX-XX-6789.'
        anonymizer = IdentifierAnonymizer(content)
        anonymizer.anonymize()
        assert anonymizer.cleaned_content == expected_output

    def test_anonymize_multiple_ssns(self):
        content = 'SSNs are 123-45-6789 and 987-65-4321.'
        expected_output = 'SSNs are XXX-XX-6789 and XXX-XX-4321.'
        anonymizer = IdentifierAnonymizer(content)
        anonymizer.anonymize()
        assert anonymizer.cleaned_content == expected_output

    def test_anonymize_no_ssn(self):
        content = 'There is no SSN here.'
        expected_output = 'There is no SSN here.'
        anonymizer = IdentifierAnonymizer(content)
        anonymizer.anonymize()
        assert anonymizer.cleaned_content == expected_output

    def test_anonymize_partial_ssn(self):
        content = 'Partial SSN 123-45 is not complete.'
        expected_output = 'Partial SSN 123-45 is not complete.'
        anonymizer = IdentifierAnonymizer(content)
        anonymizer.anonymize()
        assert anonymizer.cleaned_content == expected_output

    def test_anonymize_invalid_ssn_format(self):
        content = 'Invalid SSN 1234-56-7890.'
        expected_output = 'Invalid SSN 1234-56-7890.'
        anonymizer = IdentifierAnonymizer(content)
        anonymizer.anonymize()
        assert anonymizer.cleaned_content == expected_output

    def test_anonymize_ssn_with_spaces(self):
        content = 'SSN is 123 45 6789.'
        expected_output = 'SSN is XXX XX 6789.'
        anonymizer = IdentifierAnonymizer(content)
        anonymizer.anonymize()
        assert anonymizer.cleaned_content == expected_output

    def test_anonymize_compact_ssn(self):
        content = 'SSN is 123456789.'
        expected_output = 'SSN is XXXXX6789.'
        anonymizer = IdentifierAnonymizer(content)
        anonymizer.anonymize()
        assert anonymizer.cleaned_content == expected_output
