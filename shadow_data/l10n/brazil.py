import re

from shadow_data.l10n.ClearIdentifier import ClearIdentifier

CNPJ_PATTERN = r'(?<!\d)\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}(?!\d)'
CPF_PATTERN = r'(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)'

_VISIBLE_LEADING_DIGITS = 2


class BrazilIdentifierAnonymizer(ClearIdentifier):
    """Masks Brazilian CPF and CNPJ identifiers found anywhere in the content.

    Separators are preserved and only the first two digits of each identifier
    remain visible.
    """

    def anonymize(self) -> str:
        content = re.sub(CNPJ_PATTERN, self._mask_identifier, self.content_to_anonymize)
        self.cleaned_content = re.sub(CPF_PATTERN, self._mask_identifier, content)
        return self.cleaned_content

    @staticmethod
    def _mask_identifier(match: re.Match[str]) -> str:
        seen_digits = 0
        masked = []

        for char in match.group(0):
            if char.isdigit():
                seen_digits += 1
                masked.append(char if seen_digits <= _VISIBLE_LEADING_DIGITS else '*')
            else:
                masked.append(char)

        return ''.join(masked)


# Deprecated alias kept for backwards compatibility; removed in 2.0.
IdentifierAnonymizer = BrazilIdentifierAnonymizer
