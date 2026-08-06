from shadow_data.anonymization import (
    EmailAnonymization,
    Ipv4Anonymization,
    PhoneNumberAnonymization,
    TextProcessor,
)
from shadow_data.cryptohash.symmetric_cipher import Symmetric
from shadow_data.l10n.brazil import BrazilIdentifierAnonymizer
from shadow_data.l10n.usa import UsaIdentifierAnonymizer
from shadow_data.masking import mask_credit_card, partial_email
from shadow_data.reversible import Pseudonymizer

text = 'Contact me at user@example.com or 415-555-0199. Server: 10.0.0.1'

anonymized_text = Ipv4Anonymization.anonymize_ipv4(text)
anonymized_text = TextProcessor.replace_text('Contact', 'Reach', anonymized_text)
email = EmailAnonymization.anonymize_email('user@example.com')
phone = PhoneNumberAnonymization.anonymize_phone_number('415-555-0199')

print(anonymized_text)
print(email)
print(phone)

ssn_text = "Billy's SSN is 479-92-5042."
print(UsaIdentifierAnonymizer(ssn_text).anonymize())

cpf = '806.846.761-09'
print(BrazilIdentifierAnonymizer(cpf).anonymize())

print(mask_credit_card('4111 1111 1111 1111'))
print(partial_email('user@example.com'))

pseudonymizer = Pseudonymizer()
token = pseudonymizer.pseudonymize('user@example.com')

print(token)
print(pseudonymizer.depseudonymize(token))

symmetric = Symmetric()
key = symmetric.create_key()

ciphertext = symmetric.encrypt('hello')
plaintext = symmetric.decrypt(ciphertext)

print(ciphertext)
print(plaintext)
