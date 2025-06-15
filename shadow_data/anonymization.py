"""Anonymization module for sensitive data.

This module provides classes for anonymizing different types of sensitive data
such as IP addresses, email addresses, and phone numbers.
"""

import re
from typing import List, Pattern

from shadow_data.exceptions import InvalidEmailError


class TextProcessor:
    """Utility class for text processing and replacement operations."""

    @staticmethod
    def replace_text(original_term: str, to_replace: str, original_content: str) -> str:
        """Replace occurrences of a term in a text with another term.

        Args:
            original_term: The term or pattern to be replaced.
            to_replace: The replacement term.
            original_content: The original text content.

        Returns:
            The text with replacements applied.
        """
        return re.sub(original_term, to_replace, original_content)


class Ipv4Anonymization:
    """Class for anonymizing IPv4 addresses in text."""

    # Compiled regex pattern for better performance
    _IPV4_PATTERN: Pattern[str] = re.compile(r'\b(\d{1,3})(\.\d{1,3}){3}\b')

    @classmethod
    def anonymize_ipv4(cls, text: str, pattern: str = r'\1.X.X.X') -> str:
        """Anonymize IPv4 addresses in text.

        Replaces the last three octets of IPv4 addresses with 'X.X.X' by default,
        preserving the first octet.

        Args:
            text: The text containing IPv4 addresses to anonymize.
            pattern: The replacement pattern. Default is '\\1.X.X.X'.

        Returns:
            The text with anonymized IPv4 addresses.
        """
        return TextProcessor.replace_text(cls._IPV4_PATTERN, pattern, text)


class EmailAnonymization:
    """Class for anonymizing email addresses."""

    # Compiled regex pattern for better performance
    _EMAIL_REGEX: Pattern[str] = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    @classmethod
    def anonymize_email(cls, email: str) -> str:
        """Anonymize an email address.

        Masks the username part completely with asterisks (*).
        For the domain part, preserves the last 3 characters of the domain name
        and all subdomains.

        Args:
            email: The email address to anonymize.

        Returns:
            The anonymized email address.

        Raises:
            InvalidEmailError: If the email format is invalid.
        """
        if not cls._EMAIL_REGEX.match(email):
            raise InvalidEmailError()

        try:
            user, domain = email.split('@')
            anonymized_user = '*' * len(user)

            domain_parts = domain.split('.')
            if len(domain_parts[0]) <= 3:
                # If domain name is 3 chars or less, don't mask it
                anonymized_domain = domain_parts[0]
            else:
                # Mask all but the last 3 characters of the domain name
                anonymized_domain = '*' * (len(domain_parts[0]) - 3) + domain_parts[0][-3:]

            anonymized_domain += '.' + '.'.join(domain_parts[1:])

            return f'{anonymized_user}@{anonymized_domain}'
        except (ValueError, IndexError):
            # Additional error handling for edge cases
            raise InvalidEmailError()


class PhoneNumberAnonymization:
    """Class for anonymizing phone numbers."""

    @staticmethod
    def anonymize_phone_number(phone: str) -> str:
        """Anonymize a phone number.

        Masks all digits except the last 4 with asterisks (*),
        preserving all non-digit characters (spaces, hyphens, parentheses, etc.).
        If the phone number has 4 or fewer digits, it remains unchanged.

        Args:
            phone: The phone number to anonymize.

        Returns:
            The anonymized phone number.
        """
        # Find all digits in the phone number
        digits: List[str] = re.findall(r'\d', phone)

        if len(digits) > 4:
            # Create a list of masked digits (all but the last 4 are masked)
            masked_digits: List[str] = ['*' for _ in range(len(digits) - 4)] + digits[-4:]
            digit_index: int = 0
            result: List[str] = []

            # Reconstruct the phone number, replacing digits with masked ones
            for char in phone:
                if char.isdigit():
                    result.append(masked_digits[digit_index])
                    digit_index += 1
                else:
                    result.append(char)

            return ''.join(result)

        # If 4 or fewer digits, return unchanged
        return phone
