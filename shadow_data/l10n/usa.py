import re

from shadow_data.l10n.ClearIdentifier import ClearIdentifier

SSN_PATTERN = r'(?<!\d)(\d{3})([- ]?)(\d{2})([- ]?)(\d{4})(?!\d)'


class UsaIdentifierAnonymizer(ClearIdentifier):
    """Masks US Social Security Numbers found anywhere in the content."""

    def anonymize(self) -> str:
        self.cleaned_content = re.sub(SSN_PATTERN, self._mask_ssn, self.content_to_anonymize)
        return self.cleaned_content

    @staticmethod
    def _mask_ssn(match: re.Match[str]) -> str:
        first_separator = match.group(2)
        second_separator = match.group(4)
        return f'XXX{first_separator}XX{second_separator}{match.group(5)}'


# Deprecated alias kept for backwards compatibility; removed in 2.0.
IdentifierAnonymizer = UsaIdentifierAnonymizer
