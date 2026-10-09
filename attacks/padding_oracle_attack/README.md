# Padding Oracle Attack

## Aim

To demonstrate how plaintext can be recovered from AES-CBC ciphertext using a padding oracle without knowing the AES key.

## Theory

AES-CBC encrypts data in blocks of 16 bytes. During decryption, each plaintext block is obtained by XORing the decrypted ciphertext block with the previous ciphertext block. PKCS#7 padding makes the plaintext length a multiple of the block size. A padding oracle reveals whether decrypted data has valid padding. By modifying the previous ciphertext block and querying the oracle, plaintext bytes can be recovered from right to left.

## Algorithm

1. Divide the ciphertext into 16-byte blocks.
2. Select a target ciphertext block.
3. Modify the previous ciphertext block.
4. Query the padding oracle with candidate byte values.
5. Recover each plaintext byte from right to left.
6. Repeat for every block.
7. Remove PKCS#7 padding and display the recovered plaintext.

## Execution

```bash
python3 -m pip install pycryptodome
python3 attacks/padding_oracle_attack/src/padding_oracle.py
```

## Observations

* Recovered plaintext: Record the actual output.
* Total oracle queries: Record the actual count.
* The attack does not need access to the AES key.

## Security Recommendation

Use authenticated encryption such as AES-GCM. If CBC is required, authenticate ciphertext before decryption and avoid exposing distinguishable padding errors.

