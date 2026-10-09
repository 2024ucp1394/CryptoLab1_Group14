from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16
queries = 0

# Demo setup: the key is hidden from the attack function.
# In your assignment, replace this setup with the given ciphertext and oracle.
key = get_random_bytes(BLOCK_SIZE)
iv = get_random_bytes(BLOCK_SIZE)

message = b"Hello World!"
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(message, BLOCK_SIZE))

# Oracle: reveals only whether padding is valid.
def padding_oracle(test_iv, test_ciphertext):
    global queries
    queries += 1

    try:
        aes = AES.new(key, AES.MODE_CBC, test_iv)
        decrypted = aes.decrypt(test_ciphertext)
        unpad(decrypted, BLOCK_SIZE)
        return True
    except ValueError:
        return False

# Recover one plaintext block without knowing the key.
def attack_block(previous, target):
    intermediate = bytearray(BLOCK_SIZE)
    plaintext = bytearray(BLOCK_SIZE)
    modified = bytearray(previous)

    for pad_value in range(1, BLOCK_SIZE + 1):
        pos = BLOCK_SIZE - pad_value

        # Force already recovered bytes to have the desired padding.
        for j in range(pos + 1, BLOCK_SIZE):
            modified[j] = intermediate[j] ^ pad_value

        for guess in range(256):
            modified[pos] = guess

            if padding_oracle(bytes(modified), target):
                # Reject accidental valid padding when possible.
                if pos > 0:
                    check = bytearray(modified)
                    check[pos - 1] ^= 1
                    if not padding_oracle(bytes(check), target):
                        continue

                intermediate[pos] = guess ^ pad_value
                plaintext[pos] = intermediate[pos] ^ previous[pos]
                break
        else:
            raise RuntimeError("Could not recover a byte")

    return bytes(plaintext)

# Attack each ciphertext block independently.
blocks = [
    ciphertext[i:i + BLOCK_SIZE]
    for i in range(0, len(ciphertext), BLOCK_SIZE)
]

recovered = b""
previous = iv

for block in blocks:
    recovered += attack_block(previous, block)
    previous = block

# Remove the original PKCS#7 padding.
recovered = unpad(recovered, BLOCK_SIZE)

print("Ciphertext:", ciphertext.hex())
print("Recovered plaintext:", recovered.decode("utf-8"))
print("Total oracle queries:", queries)
