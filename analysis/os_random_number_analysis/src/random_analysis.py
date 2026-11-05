import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import chisquare, norm
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent

DATA = BASE / "data"
OUTPUT = BASE / "outputs"
GRAPHS = OUTPUT / "graphs"

GRAPHS.mkdir(parents=True, exist_ok=True)

files = {
    "Linux /dev/urandom": "urandom.bin",
    "OpenSSL RAND": "openssl.bin",
    "macOS SecRandomCopyBytes": "mac_random.bin"
}

results = []

for name, filename in files.items():

    path = DATA / filename

    with open(path, "rb") as f:
        arr = np.frombuffer(f.read(), dtype=np.uint8)

    print("\n", name)
    print("--------------------------")

    print("Data Size:", len(arr), "bytes")

    # Byte Frequency Distribution

    freq = np.bincount(arr, minlength=256)

    plt.figure(figsize=(10, 4))
    plt.bar(range(256), freq)

    plt.title(name + " - Byte Frequency")
    plt.xlabel("Byte Value")
    plt.ylabel("Frequency")

    plt.savefig(GRAPHS / (filename + "_frequency.png"))
    plt.close()

    # Bit Distribution

    bits = np.unpackbits(arr)

    zeros = np.sum(bits == 0)
    ones = np.sum(bits == 1)

    print("Zero Bits:", zeros)
    print("One Bits:", ones)

    plt.figure(figsize=(5, 4))
    plt.bar(["Zeros", "Ones"], [zeros, ones])

    plt.title(name + " - Bit Distribution")
    plt.ylabel("Count")

    plt.savefig(GRAPHS / (filename + "_bits.png"))
    plt.close()

    # Repeated Patterns

    repeated = np.sum(arr[:-1] == arr[1:])

    print("Repeated Consecutive Bytes:", repeated)

    # Serial Correlation

    correlation = np.corrcoef(arr[:-1], arr[1:])[0, 1]

    print("Serial Correlation:", correlation)

    # Chi-Square Test

    expected = np.ones(256) * (len(arr) / 256)

    chi, p_value = chisquare(freq, expected)

    print("Chi-Square:", chi)
    print("P-value:", p_value)

    # Runs Test

    n = len(bits)

    runs = 1 + np.sum(bits[:-1] != bits[1:])

    expected_runs = 1 + (2 * ones * zeros) / n

    variance = (
        2 * ones * zeros * (2 * ones * zeros - n)
        / (n ** 2 * (n - 1))
    )

    z = (runs - expected_runs) / np.sqrt(variance)

    runs_p = 2 * norm.sf(abs(z))

    print("Number of Runs:", runs)
    print("Runs Test P-value:", runs_p)

    results.append({
        "Generator": name,
        "Data Size": len(arr),
        "Zero Bits": zeros,
        "One Bits": ones,
        "Repeated Bytes": repeated,
        "Serial Correlation": correlation,
        "Chi-Square": chi,
        "Chi-Square P-value": p_value,
        "Runs": runs,
        "Runs Test P-value": runs_p
    })


# Save Experimental Results

df = pd.DataFrame(results)

df.to_csv(OUTPUT / "experimental_results.csv", index=False)

print("\n==============================")
print("EXPERIMENTAL RESULTS")
print("==============================")

print(df.to_string(index=False))

print("\nResults saved successfully!")
print("Graphs saved successfully!")
