
import random
import secrets
import string
from pathlib import Path

def generate_keystream(seed, length):
    rng = random.Random(seed)
    return bytes(rng.getrandbits(8) for _ in range(length))


def encrypt_decrypt(data, seed):
    key = generate_keystream(seed, len(data))
    return bytes(a ^ b for a, b in zip(data, key))


# Generate random prefix and known plaintext
prefix_length = secrets.randbelow(16) + 5
prefix = ''.join(
    secrets.choice(string.ascii_letters + string.digits)
    for _ in range(prefix_length)
)

plaintext = (prefix + "A" * 14).encode()

# Encrypt using a random 16-bit seed
original_seed = secrets.randbelow(65536)
ciphertext = encrypt_decrypt(plaintext, original_seed)

print("ORIGINAL PLAINTEXT:", plaintext.decode())
print("ORIGINAL SEED:", original_seed)
print("CIPHERTEXT (HEX):", ciphertext.hex())

# Brute-force all possible 16-bit seeds
known = b"A" * 14
recovered_seed = None
recovered_plaintext = None

for seed in range(65536):
    decrypted = encrypt_decrypt(ciphertext, seed)

    if known in decrypted:
        recovered_seed = seed
        recovered_plaintext = decrypted
        break

print("\nSEED RECOVERY")
print("Recovered Seed:", recovered_seed)

if recovered_seed is not None:
    print("Decrypted Plaintext:", recovered_plaintext.decode())
    print("Seed Correct:", recovered_seed == original_seed)
    print("Plaintext Verified:", recovered_plaintext == plaintext)
    print("Known Sequence Found:", known in recovered_plaintext)

    output = f"""PART A - MT19937 STREAM CIPHER

Original Plaintext: {plaintext.decode()}
Original Seed: {original_seed}
Ciphertext (Hex): {ciphertext.hex()}
Recovered Seed: {recovered_seed}
Decrypted Plaintext: {recovered_plaintext.decode()}
Seed Correct: {recovered_seed == original_seed}
Plaintext Verified: {recovered_plaintext == plaintext}
Known Sequence Found: {known in recovered_plaintext}
"""

    output_path = Path(__file__).resolve().parent.parent / "outputs" / "part_a_results.txt"
    output_path.write_text(output)
    print("\nResults saved to:", output_path)
else:
    print("No matching seed found.")
