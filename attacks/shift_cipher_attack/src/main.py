# main.py

from shift_cipher import encrypt
from brute_force_dictionary import (
    load_dictionary,
    brute_force_dictionary
)
from chi_square_attack import chi_square_attack


DICTIONARY_FILE = "../dictionary/english_words.txt"


def display_brute_force_results(results):
    print("\n" + "=" * 70)
    print("BRUTE FORCE + DICTIONARY SCORING")
    print("=" * 70)

    print(
        f"{'Key':<8}"
        f"{'Dictionary Score':<20}"
        f"Plaintext"
    )

    print("-" * 70)

    for result in results:
        print(
            f"{result['key']:<8}"
            f"{result['score']:<20}"
            f"{result['plaintext']}"
        )


def display_chi_square_results(results):
    print("\n" + "=" * 70)
    print("CHI-SQUARE ANALYSIS")
    print("=" * 70)

    print(
        f"{'Key':<8}"
        f"{'Chi-Square Score':<20}"
        f"Plaintext"
    )

    print("-" * 70)

    for result in results:
        print(
            f"{result['key']:<8}"
            f"{result['score']:<20.4f}"
            f"{result['plaintext']}"
        )


def main():

    print("=" * 70)
    print("SHIFT CIPHER CRYPTANALYSIS")
    print("=" * 70)

    plaintext = input("\nEnter plaintext: ")

    try:
        actual_key = int(input("Enter encryption key (0-25): "))

        if actual_key < 0 or actual_key > 25:
            print("Key must be between 0 and 25.")
            return

    except ValueError:
        print("Invalid key.")
        return

    # Encrypt plaintext
    ciphertext = encrypt(plaintext, actual_key)

    print("\n" + "=" * 70)
    print("ENCRYPTION")
    print("=" * 70)

    print("Plaintext :", plaintext)
    print("Actual Key:", actual_key)
    print("Ciphertext:", ciphertext)

    # Load dictionary
    dictionary = load_dictionary(DICTIONARY_FILE)

    # Dictionary attack
    dictionary_best, dictionary_results = (
        brute_force_dictionary(
            ciphertext,
            dictionary
        )
    )

    # Chi-Square attack
    chi_best, chi_results = chi_square_attack(ciphertext)

    # Display all results
    display_brute_force_results(dictionary_results)

    display_chi_square_results(chi_results)

    # Final comparison
    print("\n" + "=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)

    print("Actual Key              :", actual_key)

    print(
        "Dictionary Predicted Key:",
        dictionary_best["key"]
    )

    print(
        "Chi-Square Predicted Key:",
        chi_best["key"]
    )

    print(
        "Dictionary Correct?     :",
        dictionary_best["key"] == actual_key
    )

    print(
        "Chi-Square Correct?     :",
        chi_best["key"] == actual_key
    )

    print("\nDictionary Plaintext:")
    print(dictionary_best["plaintext"])

    print("\nChi-Square Plaintext:")
    print(chi_best["plaintext"])


if __name__ == "__main__":
    main()
