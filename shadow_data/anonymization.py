import re

from shadow_data.exceptions import InvalidEmailError

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

_OCTET = r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)'
# The lookarounds reject octets outside 0-255 and dotted sequences with more than
# four parts (version strings such as 1.2.3.4.5), which are not IPv4 addresses.
_IPV4_REGEX = rf'(?<![\d.])({_OCTET})((?:\.{_OCTET}){{3}})(?!\.?\d)'


class TextProcessor:
    @staticmethod
    def replace_text(original_term: str, to_replace: str, original_content: str) -> str:
        return re.sub(re.escape(original_term), lambda _: to_replace, original_content)

    @staticmethod
    def replace_regex(pattern: str, to_replace: str, original_content: str) -> str:
        return re.sub(pattern, to_replace, original_content)


class Ipv4Anonymization:
    @staticmethod
    def anonymize_ipv4(text: str, pattern: str = r'\1.X.X.X') -> str:
        return TextProcessor.replace_regex(_IPV4_REGEX, pattern, text)


class EmailAnonymization:
    @staticmethod
    def anonymize_email(email: str) -> str:
        if not re.match(EMAIL_REGEX, email):
            raise InvalidEmailError()

        user, domain = email.split('@')
        anonymized_user = '*' * len(user)
        domain_parts = domain.split('.')
        first_label = domain_parts[0]

        # Only expose a suffix when it leaves more characters hidden than shown.
        if len(first_label) > 3:
            anonymized_label = '*' * (len(first_label) - 3) + first_label[-3:]
        else:
            anonymized_label = '*' * len(first_label)

        anonymized_domain = '.'.join([anonymized_label] + domain_parts[1:])

        return f'{anonymized_user}@{anonymized_domain}'


class PhoneNumberAnonymization:
    @staticmethod
    def anonymize_phone_number(phone: str) -> str:
        digits = re.findall(r'\d', phone)

        if len(digits) > 4:
            masked_digits = ['*' for _ in range(len(digits) - 4)] + digits[-4:]
        else:
            masked_digits = ['*' for _ in digits]

        digit_index = 0
        result = []

        for char in phone:
            if char.isdigit():
                result.append(masked_digits[digit_index])
                digit_index += 1
            else:
                result.append(char)

        return ''.join(result)
