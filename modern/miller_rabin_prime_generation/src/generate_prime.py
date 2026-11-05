import secrets
import time
from sympy import isprime


BITS = 512
ROUNDS = 20


def generate_candidate(bits):
    n = secrets.randbits(bits)
    n = n | (1 << (bits - 1)) | 1
    return n


def miller_rabin(n, rounds):
    if n < 2:
        return False, []

    if n in (2, 3):
        return True, []

    if n % 2 == 0:
        return False, []

    d = n - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s += 1

    bases = set()

    while len(bases) < rounds:
        bases.add(secrets.randbelow(n - 3) + 2)

    bases = list(bases)

    for a in bases:
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for r in range(s - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                break
        else:
            return False, bases

    return True, bases


def main():

    start = time.perf_counter()

    candidates_tested = 0

    while True:

        candidate = generate_candidate(BITS)
        candidates_tested += 1

        result, bases = miller_rabin(candidate, ROUNDS)

        if result:
            break

    actual_bits = candidate.bit_length()

    independent_check = isprime(candidate)

    end = time.perf_counter()

    execution_time = end - start

    print("\nMILLER-RABIN PRIME GENERATION")
    print("--------------------------------")

    print("Generated Prime:")
    print(candidate)

    print("\nAssigned Bit Length:", BITS)
    print("Actual Bit Length:", actual_bits)

    print("Candidates Tested:", candidates_tested)
    print("Miller-Rabin Rounds:", ROUNDS)

    print("\nBases Used:")
    print(bases)

    print("\nMiller-Rabin Result: PASS")
    print("Independent Verification:", independent_check)

    print("Execution Time:", execution_time, "seconds")

    with open("modern/miller_rabin_prime_generation/outputs/results.txt", "w") as f:

        f.write("MILLER-RABIN PRIME GENERATION\n")
        f.write("--------------------------------\n")

        f.write("Generated Prime:\n")
        f.write(str(candidate) + "\n\n")

        f.write("Assigned Bit Length: " + str(BITS) + "\n")
        f.write("Actual Bit Length: " + str(actual_bits) + "\n")

        f.write("Candidates Tested: " + str(candidates_tested) + "\n")
        f.write("Miller-Rabin Rounds: " + str(ROUNDS) + "\n")

        f.write("\nBases Used:\n")
        f.write(str(bases) + "\n")

        f.write("\nMiller-Rabin Result: PASS\n")
        f.write("Independent Verification: " + str(independent_check) + "\n")

        f.write("Execution Time: " + str(execution_time) + " seconds\n")


if __name__ == "__main__":
    main()
