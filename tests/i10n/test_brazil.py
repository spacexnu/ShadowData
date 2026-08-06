from shadow_data.l10n.brazil import BrazilIdentifierAnonymizer, IdentifierAnonymizer


class TestBrazilIdentifierAnonymizer:
    def test_anonymize_formatted_cpf(self):
        anonymizer = BrazilIdentifierAnonymizer('123.456.789-09')
        assert anonymizer.anonymize() == '12*.***.***-**'
        assert anonymizer.cleaned_content == '12*.***.***-**'

    def test_anonymize_bare_cpf(self):
        assert BrazilIdentifierAnonymizer('12345678909').anonymize() == '12*********'

    def test_anonymize_formatted_cnpj(self):
        assert BrazilIdentifierAnonymizer('12.345.678/0001-95').anonymize() == '12.***.***/****-**'

    def test_anonymize_bare_cnpj(self):
        assert BrazilIdentifierAnonymizer('12345678000195').anonymize() == '12************'

    def test_anonymize_cpf_inside_free_text(self):
        content = 'O CPF do cliente 42 e 123.456.789-09, cadastrado em 2024.'
        expected = 'O CPF do cliente 42 e 12*.***.***-**, cadastrado em 2024.'
        assert BrazilIdentifierAnonymizer(content).anonymize() == expected

    def test_anonymize_cnpj_inside_free_text(self):
        content = 'CNPJ 12.345.678/0001-95 emitido.'
        expected = 'CNPJ 12.***.***/****-** emitido.'
        assert BrazilIdentifierAnonymizer(content).anonymize() == expected

    def test_anonymize_multiple_identifiers(self):
        content = 'CPFs 123.456.789-09 e 987.654.321-00.'
        expected = 'CPFs 12*.***.***-** e 98*.***.***-**.'
        assert BrazilIdentifierAnonymizer(content).anonymize() == expected

    def test_cnpj_is_not_matched_as_cpf(self):
        # A CNPJ has 14 digits; the trailing 11 must not be masked as if it were a CPF.
        assert BrazilIdentifierAnonymizer('12345678000195').anonymize() == '12************'

    def test_content_without_identifier_is_unchanged(self):
        content = 'Nenhum identificador aqui, apenas 12345.'
        assert BrazilIdentifierAnonymizer(content).anonymize() == content

    def test_partial_identifier_is_unchanged(self):
        content = 'Numero incompleto 123.456.789'
        assert BrazilIdentifierAnonymizer(content).anonymize() == content

    def test_deprecated_alias_points_to_the_same_class(self):
        assert IdentifierAnonymizer is BrazilIdentifierAnonymizer
