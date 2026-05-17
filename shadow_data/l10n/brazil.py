from shadow_data.anonymization import TextProcessor
from shadow_data.l10n.ClearIdentifier import ClearIdentifier
from shadow_data.utils import only_digits


class IdentifierAnonymizer(ClearIdentifier):
    def anonymize(self):
        clean_identifier = only_digits(self.content_to_anonymize)
        if len(clean_identifier) == 11:  # CPF
            return self._anonymize_cpf(clean_identifier)
        elif len(clean_identifier) == 14:  # CNPJ
            return self._anonymize_cnpj(clean_identifier)
        else:
            raise ValueError('Invalid identifier length')

    def _anonymize_cpf(self, content: str):
        self.cleaned_content = TextProcessor.replace_regex(r'(\d{2})(\d{9})', r'\1*********', content)

    def _anonymize_cnpj(self, content: str):
        self.cleaned_content = TextProcessor.replace_regex(r'(\d{2})(\d{12})', r'\1************', content)
