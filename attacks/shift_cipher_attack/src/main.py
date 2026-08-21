from shift_cipher import encrypt
from brute_force_dictionary import load_dictionary, dictionary_attack


ciphertext = encrypt("THIS IS A SECRET MESSAGE", 5)

print("Ciphertext:")
print(ciphertext)

dictionary = load_dictionary(
    "../dictionary/english_words.txt"
)

key, plaintext, score = dictionary_attack(
    ciphertext,
    dictionary
)

print("\nPredicted Key:", key)
print("Decrypted Text:", plaintext)
print("Dictionary Score:", score)
