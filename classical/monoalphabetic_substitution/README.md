# Monoalphabetic Substitution Cipher and Cryptanalysis

## Objective

Implement a Monoalphabetic Substitution Cipher and perform
cryptanalysis using frequency analysis, word-frequency analysis,
and pattern analysis.

## Plaintext

The plaintext is selected from the assigned page of
"Modern Cryptography" by Katz and Lindell.

For Group 14:
Assigned page = Group Number + 30 = 44

## Functions Implemented

1. frequency_analysis()
2. word_frequency_analysis()
3. pattern_analysis()
4. apply_substitution()
5. display_partial_plaintext()
6. verify_solution()

## Cryptanalysis

The ciphertext is analyzed using:

- Letter frequency
- One-letter words
- Two-letter words
- Three-letter words
- Repeated words
- Repeated-letter patterns

Candidate substitutions are tested iteratively until
meaningful plaintext is recovered.

## Verification

The recovered plaintext is re-encrypted using the recovered
substitution key. The regenerated ciphertext is compared with
the original ciphertext.

## Compilation

g++ main.cpp -o substitution

## Execution

./substitution
