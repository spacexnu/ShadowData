![Build Status](https://github.com/spacexnu/ShadowData/actions/workflows/main.yml/badge.svg)
[![codecov](https://codecov.io/gh/spacexnu/ShadowData/branch/main/graph/badge.svg)](https://codecov.io/gh/your-username/your-repo)


# ShadowData - A sensitive data handler python library
ShadowData is a Python library designed to simplify the processing and handling of sensitive data securely and efficiently.

## Features (The project is under development)

- Data anonymization. (Work in progress)
- PII - Personal Identified Information detection using Natual Language Processing (Work in progress) 
- Encryption and decryption of sensitive data. (Work in progress)
- Data masking for privacy-preserving data handling. (Work in progress)
- Compliance with GDPR, LGPD and other data protection regulations. (Work in progress)

## Installation Instructions

```bash
pip install shadow_data
```
* Installs only the core library, without the spaCy dependency.

```bash 
pip install shadowdata[spacy]
```
* Installs spaCy automatically, based on your platform.

By default, ShadowData will automatically download the necessary language model if it’s not already installed. However, if you’d prefer to install it manually, use the following command as example:
```bash
python -m spacy download en_core_web_trf
```
Make sure to run this command within your project’s virtual environment.

[Check spaCy's documentation to know more about the Language Models.](https://spacy.io/models)

## Usage
There are some usage examples at the [examples](examples) directory

## Contributing

Contributions are welcome! Please follow the guidelines below to contribute to the project.

	1.	Fork the repository.
	2.	Create a new branch for your feature (git checkout -b my-new-feature).
	3.	Commit your changes (git commit -am 'Add new feature').
	4.	Push the branch (git push origin my-new-feature).
	5.	Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
