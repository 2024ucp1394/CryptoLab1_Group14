# Assignment 10: MT19937 Stream Cipher and Predictable Token Attack

## Aim
To understand why MT19937, a statistical pseudo-random number generator, is unsuitable for cryptographic applications by implementing a stream cipher, recovering a weak seed, and predicting timestamp-based password reset tokens.

## Objectives
1. Implement a toy stream cipher using MT19937.
2. Perform encryption and decryption using XOR.
3. Recover a 16-bit seed using a known-plaintext attack.
4. Generate a simulated password reset token using a timestamp seed.
5. Predict the token by searching possible timestamps.
6. Understand the security weaknesses of MT19937.

## Software Requirements
- Ubuntu Linux
- Python 3
- Python built-in `random` module
- VS Code or Nano editor

## Project Structure

```text
mt19937_stream_cipher_token_attack/
├── src/
│   ├── part_a_stream_cipher.py
│   └── part_b_token_attack.py
├── outputs/
│   ├── part_a_results.txt
│   └── part_b_results.txt
└── README.md
```

## Part A: MT19937 Stream Cipher

### Theory
MT19937 is a pseudo-random number generator that produces a sequence of numbers using the Mersenne Twister algorithm. Python's built-in `random` module uses MT19937.

A stream cipher encrypts plaintext by XORing each plaintext byte with a generated keystream byte.

**Encryption:**

Ciphertext = Plaintext XOR Keystream

**Decryption:**

Plaintext = Ciphertext XOR Keystream

The same operation is used for encryption and decryption.

### Algorithm
1. Generate a random 16-bit seed.
2. Generate a random printable prefix containing 5–20 characters.
3. Append 14 consecutive A characters to the prefix.
4. Initialize MT19937 using the generated seed.
5. Generate one 8-bit keystream value for each plaintext byte.
6. XOR the plaintext with the keystream to obtain ciphertext.
7. Try all 65,536 possible seeds.
8. Decrypt the ciphertext using each candidate seed.
9. Search for the known sequence of 14 consecutive A characters.
10. Recover the matching seed and verify the complete plaintext.

### Execution

```bash
python3 attacks/mt19937_stream_cipher_token_attack/src/part_a_stream_cipher.py
```

### Result
The program successfully recovered the original 16-bit seed and decrypted the complete ciphertext. The recovered plaintext contained the known sequence of 14 consecutive A characters.

## Part B: Predictable Password Reset Token Attack

### Theory
A password reset token should be unpredictable. In this experiment, a simulated application generates a 16-byte token using MT19937 seeded with the current Unix timestamp.

A Unix timestamp represents the number of seconds elapsed since January 1, 1970.

If an attacker knows the approximate time of token generation, they can test possible timestamps and compare the generated tokens with the observed token.

### Algorithm
1. Record the current Unix timestamp.
2. Initialize MT19937 using that timestamp as the seed.
3. Generate 16 consecutive 8-bit outputs.
4. Combine the outputs to create a 16-byte token.
5. Display the token in hexadecimal format.
6. Define a search interval from T-300 to T+300 seconds.
7. Generate a candidate token for every timestamp in the interval.
8. Compare each candidate token with the observed token.
9. Recover the matching timestamp.
10. Regenerate the token using the recovered timestamp and verify the result.

### Execution

```bash
python3 attacks/mt19937_stream_cipher_token_attack/src/part_b_token_attack.py
```

### Result
The program successfully predicted the simulated password reset token by searching the timestamp interval. The recovered timestamp generated the same 16-byte token.

## Pseudocode

### Part A: Seed Recovery

```text
Generate plaintext with random prefix and 14 A characters
Choose a random 16-bit seed
Generate MT19937 keystream
Encrypt plaintext using XOR

For each seed from 0 to 65535:
    Generate keystream
    Decrypt ciphertext
    If decrypted text contains 14 consecutive A characters:
        Save the seed
        Verify complete plaintext
        Stop
```

### Part B: Token Prediction

```text
Record current timestamp T
Generate token using MT19937 seeded with T

For each timestamp from T-300 to T+300:
    Generate a candidate token
    Compare candidate with observed token

    If both tokens match:
        Recover timestamp
        Regenerate token
        Verify the match
        Stop
```

## Observations

1. MT19937 produces statistically well-distributed pseudo-random values but is not designed for cryptographic security.
2. A known plaintext sequence can help identify a weak seed through brute-force search.
3. A 16-bit seed has only 65,536 possible values, making exhaustive search practical.
4. Timestamp-based seeds are predictable when the approximate generation time is known.
5. A small timestamp search interval makes token prediction practical in this simulated experiment.

## Why MT19937 Is Not Cryptographically Secure

- Its internal state can be reconstructed from sufficient output.
- Its output is deterministic when the seed is known.
- Weak or predictable seeds make brute-force attacks possible.
- It does not provide the security properties required of a cryptographically secure random number generator.

Cryptographic applications should use secure random-number generators such as Python's `secrets` module or operating-system cryptographic random APIs.

## Experimental Conclusion

In Part A, the 16-bit seed of the MT19937-based stream cipher
was recovered using known plaintext.

In Part B, the timestamp used as the random seed was recovered
by searching a limited time window.

These experiments demonstrate why MT19937 should not be used
for cryptographic applications. A cryptographically secure
random number generator should be used instead.
