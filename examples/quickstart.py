from shadow_data.anonymization import (
    EmailAnonymization,
    Ipv4Anonymization,
    PhoneNumberAnonymization,
    TextProcessor,
)
from shadow_data.cryptohash.symmetric_cipher import Symmetric
from shadow_data.l10n.brazil import IdentifierAnonymizer as BrazilIdentifierAnonymizer
from shadow_data.l10n.usa import IdentifierAnonymizer as UsaIdentifierAnonymizer

text = "Contact me at user@example.com or 415-555-0199. Server: 10.0.0.1"

anonymized_text = Ipv4Anonymization.anonymize_ipv4(text)
anonymized_text = TextProcessor.replace_text("Contact", "Reach", anonymized_text)
email = EmailAnonymization.anonymize_email("user@example.com")
phone = PhoneNumberAnonymization.anonymize_phone_number("415-555-0199")

print(anonymized_text)
print(email)
print(phone)

ssn_text = "Billy's SSN is 479-92-5042."
ssn_anonymizer = UsaIdentifierAnonymizer(ssn_text)
ssn_anonymizer.anonymize()
print(ssn_anonymizer.cleaned_content)

cpf = "806.846.761-09"
cpf_anonymizer = BrazilIdentifierAnonymizer(cpf)
cpf_anonymizer.anonymize()
print(cpf_anonymizer.cleaned_content)

symmetric = Symmetric()
key = symmetric.create_key()

ciphertext = symmetric.encrypt("hello")
plaintext = symmetric.decrypt(ciphertext)

print(key)
print(ciphertext)
print(plaintext)
