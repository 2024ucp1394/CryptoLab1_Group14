# Operating System Random Number Generation Analysis

## Aim

To evaluate operating-system random-number generation
mechanisms and investigate their suitability for
cryptographic applications.

## Random Number Generators

1. Linux /dev/urandom
2. OpenSSL RAND
3. macOS SecRandomCopyBytes

## Data Generation

Each mechanism generates 1 MB of random data.

## Statistical Tests

1. Byte Frequency Distribution
2. Bit Distribution
3. Repeated Pattern Analysis
4. Serial Correlation
5. Chi-Square Test
6. Runs Test

## Implementation

Language: Python

Libraries:
- NumPy
- Pandas
- Matplotlib
- SciPy

## Execution

python3 src/random_analysis.py

## Results

Experimental results are stored in:

outputs/experimental_results.csv

Graphs are stored in:

outputs/graphs/

## Experimental Conclusion

The three random number sources were tested using byte frequency,
bit distribution, repeated byte patterns, and serial correlation.

The results help evaluate the statistical properties of the generated
random data. However, passing statistical tests does not guarantee
cryptographic security or unpredictability.
