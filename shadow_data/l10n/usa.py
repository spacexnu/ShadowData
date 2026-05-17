import re

from shadow_data.l10n.ClearIdentifier import ClearIdentifier


class IdentifierAnonymizer(ClearIdentifier):
    def anonymize(self):
        ssn_pattern = r'(?<!\d)(\d{3})([- ]?)(\d{2})([- ]?)(\d{4})(?!\d)'
        self.cleaned_content = re.sub(ssn_pattern, self._mask_ssn, self.content_to_anonymize)

    @staticmethod
    def _mask_ssn(match: re.Match) -> str:
        first_separator = match.group(2)
        second_separator = match.group(4)
        return f'XXX{first_separator}XX{second_separator}{match.group(5)}'
