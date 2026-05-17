import re

from shadow_data.exceptions import InvalidEmailError


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
        return TextProcessor.replace_regex(r'\b(\d{1,3})(\.\d{1,3}){3}\b', pattern, text)


class EmailAnonymization:
    @staticmethod
    def anonymize_email(email: str) -> str:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_regex, email):
            raise InvalidEmailError()

        user, domain = email.split('@')
        anonymized_user = '*' * len(user)
        domain_parts = domain.split('.')
        anonymized_domain = '*' * (len(domain_parts[0]) - 3) + domain_parts[0][-3:] + '.' + '.'.join(domain_parts[1:])

        return f'{anonymized_user}@{anonymized_domain}'


class PhoneNumberAnonymization:
    @staticmethod
    def anonymize_phone_number(phone: str) -> str:
        digits = re.findall(r'\d', phone)

        if len(digits) > 4:
            masked_digits = ['*' for _ in range(len(digits) - 4)] + digits[-4:]
            digit_index = 0
            result = []

            for char in phone:
                if char.isdigit():
                    result.append(masked_digits[digit_index])
                    digit_index += 1
                else:
                    result.append(char)

            return ''.join(result)

        return phone
