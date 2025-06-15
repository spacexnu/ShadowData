import pytest

from shadow_data.anonymization import PhoneNumberAnonymization


class TestPhoneNumberAnonymization:
    @pytest.mark.parametrize(
        'phone, expected',
        [
            ('+55 (11) 91234-5678', '+** (**) *****-5678'),
            ('(11) 91234-5678', '(**) *****-5678'),
            ('11 91234-5678', '** *****-5678'),
            ('+1 (123) 456-7890', '+* (***) ***-7890'),
            ('(123) 456-7890', '(***) ***-7890'),
            ('123-456-7890', '***-***-7890'),
            ('+44 20 7946 0958', '+** ** **** 0958'),
            ('+91 22 1234 5678', '+** ** **** 5678'),
            ('+91 22 123 4567', '+** ** *** 4567'),
            ('+551199998877', '+********8877'),
            ('1199998877', '******8877'),
            ('1234', '1234'),
        ],
    )
    def test_anonymize_phone_number(self, phone, expected):
        assert PhoneNumberAnonymization.anonymize_phone_number(phone) == expected

    def test_anonymize_phone_number_exactly_4_digits(self):
        phone = '1234'
        expected = '1234'
        assert PhoneNumberAnonymization.anonymize_phone_number(phone) == expected

    def test_anonymize_phone_number_fewer_than_4_digits(self):
        phone = '123'
        expected = '123'
        assert PhoneNumberAnonymization.anonymize_phone_number(phone) == expected

    def test_anonymize_phone_number_no_digits(self):
        phone = '(+) -'
        expected = '(+) -'
        assert PhoneNumberAnonymization.anonymize_phone_number(phone) == expected
