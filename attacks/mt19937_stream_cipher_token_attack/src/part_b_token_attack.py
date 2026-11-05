
import random
import time
from pathlib import Path

# Generate a 16-byte token using MT19937
def generate_token(seed):
    rng = random.Random(seed)
    return bytes(rng.getrandbits(8) for _ in range(16))


# Record current Unix timestamp
original_timestamp = int(time.time())

# Generate simulated password reset token
observed_token = generate_token(original_timestamp)

print("PART B - PREDICTABLE PASSWORD RESET TOKEN")
print("------------------------------------------")

print("Original Timestamp:", original_timestamp)
print("Generated Token:", observed_token.hex())

# Attacker searches timestamps within T-300 to T+300
start_timestamp = original_timestamp - 300
end_timestamp = original_timestamp + 300

print("\nTOKEN PREDICTION ATTACK")
print("Search Start:", start_timestamp)
print("Search End:", end_timestamp)

recovered_timestamp = None
candidates_tested = 0

for candidate in range(start_timestamp, end_timestamp + 1):
    candidates_tested += 1

    candidate_token = generate_token(candidate)

    if candidate_token == observed_token:
        recovered_timestamp = candidate
        break

print("Candidates Tested:", candidates_tested)
print("Recovered Timestamp:", recovered_timestamp)

# Verify recovered timestamp
if recovered_timestamp is not None:
    verified_token = generate_token(recovered_timestamp)

    print("Regenerated Token:", verified_token.hex())
    print("Token Verified:", verified_token == observed_token)
    print("Timestamp Correct:", recovered_timestamp == original_timestamp)

    output = f"""PART B - PREDICTABLE PASSWORD RESET TOKEN

Original Timestamp: {original_timestamp}
Generated Token: {observed_token.hex()}

Search Start: {start_timestamp}
Search End: {end_timestamp}
Candidates Tested: {candidates_tested}

Recovered Timestamp: {recovered_timestamp}
Regenerated Token: {verified_token.hex()}
Token Verified: {verified_token == observed_token}
Timestamp Correct: {recovered_timestamp == original_timestamp}
"""

    output_path = Path(__file__).resolve().parent.parent / "outputs" / "part_b_results.txt"
    output_path.write_text(output)

    print("\nResults saved to:", output_path)

else:
    print("No matching timestamp found.")
