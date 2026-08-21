# chi_square_attack.py

from shift_cipher import decrypt


ENGLISH_FREQUENCIES = {
    'a': 0.08167,
    'b': 0.01492,
    'c': 0.02782,
    'd': 0.04253,
    'e': 0.12702,
    'f': 0.02228,
    'g': 0.02015,
    'h': 0.06094,
    'i': 0.06966,
    'j': 0.00153,
    'k': 0.00772,
    'l': 0.04025,
    'm': 0.02406,
    'n': 0.06749,
    'o': 0.07507,
    'p': 0.01929,
    'q': 0.00095,
    'r': 0.05987,
    's': 0.06327,
    't': 0.09056,
    'u': 0.02758,
    'v': 0.00978,
    'w': 0.02360,
    'x': 0.00150,
    'y': 0.01974,
    'z': 0.00074
}


def calculate_chi_square(text):
    """
    Calculate Chi-Square score for a text.

    Lower score means the text is more similar
    to normal English letter frequencies.
    """

    text = text.lower()

    letters = []

    for char in text:
        if char.isalpha():
            letters.append(char)

    total_letters = len(letters)

    if total_letters == 0:
        return float("inf")

    observed = {}

    for letter in ENGLISH_FREQUENCIES:
        observed[letter] = 0

    for letter in letters:
        observed[letter] += 1

    chi_square = 0.0

    for letter in ENGLISH_FREQUENCIES:

        expected = (
            ENGLISH_FREQUENCIES[letter] * total_letters
        )

        actual = observed[letter]

        chi_square += (
            (actual - expected) ** 2
        ) / expected

    return chi_square


def chi_square_attack(ciphertext):
    """
    Try all 26 keys and select the plaintext
    with the lowest Chi-Square score.
    """

    results = []

    for key in range(26):

        plaintext = decrypt(ciphertext, key)

        score = calculate_chi_square(plaintext)

        results.append({
            "key": key,
            "plaintext": plaintext,
            "score": score
        })

    # Lower Chi-Square score is better
    best_result = min(results, key=lambda x: x["score"])

    return best_result, results
