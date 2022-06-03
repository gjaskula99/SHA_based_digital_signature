# SHA-based digital signature

Implemented as a task for Network Security class at Poznan University of Technology.

This program is an implementation of file's digital signature based on SHA3 and RSA asymetric encryption. Implemented in Python with PyQT-based GUI. Program computes hash of input file, encrypts it with public key and save as signature. Validation is performed by taking same input file, signature file and proper private key. If computed hash is equal to one decrypted from signature file we may considor input file as valid.

Options for both signing and validation are present in GUI menu.

## Signing

1. Select file you want to sign
2. Wait for RSA keys and hash being computed
3. Save signature file in choosen destination
4. Program will output public key which can be copied or save directly to .PEM file. Public key is being shown only at this stage - THERE IS NO WAY TO RECOVER IT LATER

Secondary option prompts user for seed used to generate RSA keys. Third uses signed file as seed for RNG (unsafe but requested by university, source: <https://www.il-pib.pl/czasopisma/JTIT/2019/1/125.pdf>).

## Validation

1. Select file that was signed
2. Select coresponding signature file
3. Select .PEM file containing RSA private key
4. Program will decrypt signature file and check if hashes are equal prompting user with the result

## Known issues / comments

- ~~Program will crash if no/invalid file will be selected. Exceptions handling will be added in future (if I won't be too lazy).~~
- Program was checked with text and PDF files. Hash can be computed for any input so it should work with any type of file. Howerer it is not guaranteed.
- Program was tested under Win 10/11, MacOS 12 and Ubuntu 18 and runs fine (as long as dependencies are satisfied).
- Private key is being exported/imported in PEM format. Results such as signature and PEM key are saved as bytes.
