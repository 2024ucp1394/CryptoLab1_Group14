from shift_cipher import decrypt


def load_dictionary(filename):
    words = set()

    with open(filename, "r") as file:
        for line in file:
            word = line.strip().lower()

            if word:
                words.add(word)

    return words


def score_text(text, dictionary):
    words = text.lower().split()

    score = 0

    for word in words:
        word = ''.join(ch for ch in word if ch.isalpha())

        if word in dictionary:
            score += 1

    return score


def dictionary_attack(ciphertext, dictionary):

    results = []

    best_key = None
    best_plaintext = None
    best_score = -1

    for key in range(26):

        plaintext = decrypt(ciphertext, key)

        score = score_text(plaintext, dictionary)

        results.append({
            "key": key,
            "score": score,
            "plaintext": plaintext
        })

        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    best = {
        "key": best_key,
        "score": best_score,
        "plaintext": best_plaintext
    }

    return best, results
