# Localized anonymization for Brazilian individual (CPF) and corporate (CNPJ) tax IDs.

Identifiers are matched anywhere in the text. Separators are preserved and only the
first two digits stay visible.

```python
from shadow_data.l10n.brazil import BrazilIdentifierAnonymizer

# Anonymize CPF

cpf = '806.846.761-09'
anonymized_cpf = BrazilIdentifierAnonymizer(cpf).anonymize()
print(f'Original CPF: {cpf} : Anonymized CPF: {anonymized_cpf}')

cnpj = '26.283.050/0001-17'
anonymized_cnpj = BrazilIdentifierAnonymizer(cnpj).anonymize()
print(f'Original CNPJ: {cnpj} : Anonymized CNPJ: {anonymized_cnpj}')

# It also works on free-form text

text = 'O CPF do titular e 806.846.761-09 e o CNPJ da empresa e 26.283.050/0001-17.'
print(BrazilIdentifierAnonymizer(text).anonymize())
```

### Results

```plain
Original CPF: 806.846.761-09 : Anonymized CPF: 80*.***.***-**
Original CNPJ: 26.283.050/0001-17 : Anonymized CNPJ: 26.***.***/****-**
O CPF do titular e 80*.***.***-** e o CNPJ da empresa e 26.***.***/****-**.
```
