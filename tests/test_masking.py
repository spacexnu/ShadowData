import pytest

from shadow_data.exceptions import InvalidCreditCardError, InvalidEmailError
from shadow_data.masking import (
    mask,
    mask_credit_card,
    mask_digits,
    partial_email,
    passes_luhn,
)

# Test card numbers published by payment providers for exactly this purpose.
VALID_VISA = '4111111111111111'
VALID_MASTERCARD = '5555555555554444'
VALID_AMEX = '378282246310005'


class TestMask:
    @pytest.mark.parametrize(
        'text, keep_first, keep_last, expected',
        [
            ('sensitive', 0, 0, '*********'),
            ('sensitive', 2, 0, 'se*******'),
            ('sensitive', 0, 3, '******ive'),
            ('sensitive', 1, 1, 's*******e'),
        ],
    )
    def test_keeps_only_the_requested_window(self, text, keep_first, keep_last, expected):
        assert mask(text, keep_first=keep_first, keep_last=keep_last) == expected

    @pytest.mark.parametrize(
        'text, keep_first, keep_last',
        [
            ('abc', 3, 0),
            ('abc', 0, 3),
            ('abc', 2, 2),
            ('', 0, 0),
        ],
    )
    def test_never_returns_the_input_unchanged(self, text, keep_first, keep_last):
        result = mask(text, keep_first=keep_first, keep_last=keep_last)
        assert result == '*' * len(text)
        assert result != text or text == ''

    def test_custom_mask_char(self):
        assert mask('sensitive', keep_last=3, mask_char='#') == '######ive'

    @pytest.mark.parametrize('keep_first, keep_last', [(-1, 0), (0, -1)])
    def test_negative_window_is_rejected(self, keep_first, keep_last):
        with pytest.raises(ValueError, match='negative'):
            mask('sensitive', keep_first=keep_first, keep_last=keep_last)

    @pytest.mark.parametrize('mask_char', ['', '**'])
    def test_mask_char_must_be_a_single_character(self, mask_char):
        with pytest.raises(ValueError, match='single character'):
            mask('sensitive', mask_char=mask_char)


class TestMaskDigits:
    def test_preserves_separators(self):
        assert mask_digits('4111 1111 1111 1111', keep_last=4) == '**** **** **** 1111'

    def test_masks_every_digit_by_default(self):
        assert mask_digits('123-456') == '***-***'

    def test_leaves_non_digits_untouched(self):
        assert mask_digits('order AB-1234', keep_last=2) == 'order AB-**34'

    def test_keep_last_larger_than_the_digit_count_masks_everything(self):
        assert mask_digits('12', keep_last=5) == '**'

    def test_rejects_invalid_options(self):
        with pytest.raises(ValueError):
            mask_digits('1234', keep_last=-1)


class TestMaskCreditCard:
    @pytest.mark.parametrize(
        'number, expected',
        [
            (VALID_VISA, '************1111'),
            ('4111 1111 1111 1111', '**** **** **** 1111'),
            ('4111-1111-1111-1111', '****-****-****-1111'),
            (VALID_MASTERCARD, '************4444'),
            (VALID_AMEX, '***********0005'),
        ],
    )
    def test_keeps_the_last_four_digits(self, number, expected):
        assert mask_credit_card(number) == expected

    @pytest.mark.parametrize(
        'number',
        [
            '4111111111111112',  # fails the Luhn checksum
            '411111111111',  # valid length, wrong checksum
            '1234567890',  # too short
            '41111111111111111111',  # too long
            'not a card',
        ],
    )
    def test_rejects_values_that_are_not_card_numbers(self, number):
        with pytest.raises(InvalidCreditCardError):
            mask_credit_card(number)

    def test_custom_mask_char(self):
        assert mask_credit_card(VALID_VISA, mask_char='x') == 'xxxxxxxxxxxx1111'


class TestPassesLuhn:
    @pytest.mark.parametrize('digits', [VALID_VISA, VALID_MASTERCARD, VALID_AMEX, '0000000000000000'])
    def test_accepts_valid_checksums(self, digits):
        assert passes_luhn(digits)

    @pytest.mark.parametrize('digits', ['4111111111111112', '', '12a4', '   '])
    def test_rejects_invalid_input(self, digits):
        assert passes_luhn(digits) is False


class TestPartialEmail:
    @pytest.mark.parametrize(
        'email, expected',
        [
            ('user@example.com', 'u***@e******.com'),
            ('user@example.co.uk', 'u***@e******.co.uk'),
            ('a@example.com', '*@e******.com'),
            ('user@a.com', 'u***@*.com'),
        ],
    )
    def test_keeps_the_first_character_of_user_and_domain(self, email, expected):
        assert partial_email(email) == expected

    def test_custom_mask_char(self):
        assert partial_email('user@example.com', mask_char='.') == 'u...@e.......com'

    @pytest.mark.parametrize('email', ['userexample.com', '@example.com', 'user@', 'user@example'])
    def test_rejects_invalid_emails(self, email):
        with pytest.raises(InvalidEmailError):
            partial_email(email)
