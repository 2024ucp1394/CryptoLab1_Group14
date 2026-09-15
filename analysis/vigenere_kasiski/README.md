# Vigenère Cipher Cryptanalysis using Kasiski Examination

## Group Number

**Group 14**

## Aim

To implement cryptanalysis of the Vigenère Cipher using **Kasiski Examination and Frequency Analysis** to recover the probable key and decrypt the given ciphertext.

## Objectives

The program performs the following tasks:

1. Preprocesses the ciphertext.
2. Finds repeated patterns.
3. Calculates distances between repeated patterns.
4. Finds factors of the distances.
5. Estimates the key length using Kasiski Examination.
6. Divides the ciphertext into groups according to the estimated key length.
7. Performs frequency analysis on each group.
8. Determines the probable key.
9. Decrypts the ciphertext using the recovered key.
10. Verifies the result by re-encrypting the plaintext.

## Files

```text
vigenere_kasiski/
├── main.cpp
├── cipher.txt
├── README.md
└── outputs/
```

### File Description

* `main.cpp` – Contains the C++ implementation.
* `cipher.txt` – Contains the given ciphertext.
* `README.md` – Description and usage of the assignment.
* `outputs/` – Contains the program output.

## User-Defined Functions

| Function                   | Purpose                                                             |
| -------------------------- | ------------------------------------------------------------------- |
| `clean_ciphertext()`       | Removes spaces and special characters and normalizes the ciphertext |
| `find_repeated_patterns()` | Identifies repeated sequences                                       |
| `calculate_distances()`    | Calculates distances between repeated occurrences                   |
| `find_factors()`           | Finds factors of the distances                                      |
| `kasiski_analysis()`       | Suggests candidate key lengths                                      |
| `calculate_ic()`           | Calculates Index of Coincidence                                     |
| `split_into_groups()`      | Divides ciphertext according to key length                          |
| `frequency_analysis()`     | Calculates A–Z frequency for each group                             |
| `find_shift()`             | Estimates the Caesar shift for a group                              |
| `find_key()`               | Combines shifts to obtain the probable key                          |
| `vigenere_decrypt()`       | Decrypts the ciphertext                                             |
| `vigenere_encrypt()`       | Re-encrypts the plaintext                                           |
| `verify()`                 | Verifies the recovered result                                       |

## Methodology

### 1. Preprocessing

The ciphertext is converted to uppercase and spaces and special characters are removed.

### 2. Kasiski Examination

Repeated character sequences are located in the ciphertext. The distances between their occurrences are calculated. The factors of these distances are used to estimate possible key lengths.

### 3. Frequency Analysis

The ciphertext is divided into groups according to the estimated key length. Each group is analysed using letter frequencies.

### 4. Key Recovery

A probable Caesar shift is found for each group. These shifts are combined to obtain the probable Vigenère key.

### 5. Decryption

The recovered key is used to decrypt the ciphertext and obtain the plaintext.

### 6. Verification

The recovered plaintext is re-encrypted using the recovered key. The generated ciphertext is compared with the original ciphertext.

If both are identical, the result is verified successfully.

## Compilation

Run the following command inside the assignment folder:

```bash
g++ main.cpp -o main
```

## Execution

The program reads the ciphertext from `cipher.txt`:

```bash
./main
```

To save the output:

```bash
./main > outputs/output.txt
```

## Expected Output

The program displays:

```text
Estimated Key Length: ...

Frequency Table for Each Group:
...

Recovered Key: ...

Recovered Plaintext:
...

Verification: Successful
```

## Conclusion

The program demonstrates the cryptanalysis of a Vigenère Cipher using **Kasiski Examination and frequency analysis**. The probable key length and key are recovered, the ciphertext is decrypted, and the result is verified by re-encryption.

