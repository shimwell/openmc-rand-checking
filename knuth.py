import openmc
import openmc.lib
import numpy as np
from scipy import stats

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def print_result(test_name, p_value, threshold=0.01):
    """Print test result with color coding"""
    passed = p_value > threshold
    color = GREEN if passed else RED
    status = 'PASS' if passed else 'FAIL'
    print(f"Result: {color}{status}{RESET} (p-value > {threshold})")

# --- Create minimal model in memory ---
m = openmc.Material()
m.add_element("H", 1)
m.add_element("O", 1)
m.set_density("g/cm3", 1.0)

matfile = openmc.Materials([m])

sphere = openmc.Sphere(r=1.0, boundary_type='vacuum')
region = -sphere
cell = openmc.Cell(region=region, fill=m)

geom = openmc.Geometry([cell])
settings = openmc.Settings()
settings.batches = 1
settings.particles = 1

model = openmc.Model(geom, matfile, settings)
model.export_to_xml()

openmc.lib.init()

# Generate a large sample of random numbers for statistical testing
seed = 12345
n_samples = 100000
random_numbers = []
for _ in range(n_samples):
    random_value, seed = openmc.lib.prn(seed)
    random_numbers.append(random_value)

openmc.lib.finalize()

random_numbers = np.array(random_numbers)

print("=" * 70)
print("Knuth's Statistical Tests for Random Number Generators")
print("=" * 70)

# Test 1: Equidistribution Test (Frequency Test)
print("\n1. EQUIDISTRIBUTION TEST (Frequency Test)")
print("-" * 70)
# Divide [0,1) into k bins and count frequencies
k = 10
counts, bins = np.histogram(random_numbers, bins=k, range=(0, 1))
expected = n_samples / k
chi_squared = np.sum((counts - expected)**2 / expected)
df = k - 1
p_value = 1 - stats.chi2.cdf(chi_squared, df)
print(f"Chi-squared statistic: {chi_squared:.4f}")
print(f"Degrees of freedom: {df}")
print(f"P-value: {p_value:.4f}")
print_result("Equidistribution", p_value)

# Test 2: Serial Test (Correlation Test)
print("\n2. SERIAL TEST (2D Correlation)")
print("-" * 70)
# Take pairs of consecutive random numbers and check their distribution
pairs = random_numbers[:-1:2]
pairs2 = random_numbers[1::2]
k = 10
H, xedges, yedges = np.histogram2d(pairs, pairs2, bins=k, range=[[0, 1], [0, 1]])
expected = len(pairs) / (k * k)
chi_squared_2d = np.sum((H - expected)**2 / expected)
df_2d = k * k - 1
p_value_2d = 1 - stats.chi2.cdf(chi_squared_2d, df_2d)
print(f"Chi-squared statistic: {chi_squared_2d:.4f}")
print(f"Degrees of freedom: {df_2d}")
print(f"P-value: {p_value_2d:.4f}")
print_result("Serial Test", p_value_2d)

# Test 3: Gap Test
print("\n3. GAP TEST")
print("-" * 70)
# Count the gaps between occurrences in a specific range
alpha, beta = 0.3, 0.7
in_range = (random_numbers >= alpha) & (random_numbers < beta)
gaps = []
current_gap = 0
for val in in_range:
    if val:
        gaps.append(current_gap)
        current_gap = 0
    else:
        current_gap += 1

if len(gaps) > 0:
    gap_counts, _ = np.histogram(gaps, bins=range(0, min(20, max(gaps)+2)))
    p = beta - alpha
    expected_gaps = [len(gaps) * (1 - p) ** i * p for i in range(len(gap_counts))]
    # Avoid division by zero
    expected_gaps = [max(e, 0.1) for e in expected_gaps]
    chi_squared_gap = sum((o - e)**2 / e for o, e in zip(gap_counts, expected_gaps))
    df_gap = len(gap_counts) - 1
    p_value_gap = 1 - stats.chi2.cdf(chi_squared_gap, df_gap)
    print(f"Range: [{alpha}, {beta})")
    print(f"Number of gaps analyzed: {len(gaps)}")
    print(f"Chi-squared statistic: {chi_squared_gap:.4f}")
    print(f"P-value: {p_value_gap:.4f}")
    print_result("Gap Test", p_value_gap)

# Test 4: Poker Test
print("\n4. POKER TEST")
print("-" * 70)
# Divide numbers into groups and check for patterns
# For d=10 (base 10), we expect specific probabilities for each pattern
d = 10  # number of possible values (0-9)
k = 5   # hand size
groups = (random_numbers * d).astype(int)
patterns = []
for i in range(0, len(groups) - k + 1, k):
    hand = groups[i:i+k]
    unique = len(set(hand))
    patterns.append(unique)

pattern_counts = np.bincount(patterns, minlength=6)[1:]  # 1 to 5 unique

# Theoretical probabilities for poker test (Knuth Vol 2, Section 3.3.2)
# Based on Stirling numbers and combinatorics
n_hands = len(patterns)
# P(all different) = d!/(d^k * (d-k)!)
# P(one pair) etc. - these are based on Stirling numbers of the second kind
# For d=10, k=5:
expected_probs = np.array([
    0.0003,      # All same (5 of a kind) - very rare
    0.0504,      # 2 distinct values (4 of a kind or full house)
    0.5040,      # 3 distinct values (3 of a kind or two pair)
    0.4320,      # 4 distinct values (one pair)
    0.3024       # All different (no pairs)
])
# Normalize to ensure they sum to 1
expected_probs = expected_probs / expected_probs.sum()
expected_counts = expected_probs * n_hands

# Only use categories with sufficient expected counts (>5)
valid = expected_counts >= 5
if valid.sum() > 1:
    chi_squared_poker = np.sum((pattern_counts[valid] - expected_counts[valid])**2 / expected_counts[valid])
    df_poker = valid.sum() - 1
    p_value_poker = 1 - stats.chi2.cdf(chi_squared_poker, df_poker)
else:
    chi_squared_poker = 0
    p_value_poker = 1.0
    
print(f"Hands analyzed: {n_hands}")
print(f"Observed distribution (1-5 unique): {pattern_counts}")
print(f"Expected distribution: {expected_counts.astype(int)}")
print(f"Chi-squared statistic: {chi_squared_poker:.4f}")
print(f"P-value: {p_value_poker:.4f}")
print_result("Poker Test", p_value_poker)

# Test 5: Runs Test (Monotonicity)
print("\n5. RUNS TEST (Monotonicity)")
print("-" * 70)
# Count runs of increasing/decreasing values
runs_up = 0
runs_down = 0
current_run_length = 1
going_up = None

for i in range(1, len(random_numbers)):
    if random_numbers[i] > random_numbers[i-1]:
        if going_up == True:
            current_run_length += 1
        else:
            if going_up == False:
                runs_down += 1
            current_run_length = 1
            going_up = True
    else:
        if going_up == False:
            current_run_length += 1
        else:
            if going_up == True:
                runs_up += 1
            current_run_length = 1
            going_up = False

total_runs = runs_up + runs_down
expected_runs = (2 * n_samples - 1) / 3
variance_runs = (16 * n_samples - 29) / 90
z_score = (total_runs - expected_runs) / np.sqrt(variance_runs)
p_value_runs = 2 * (1 - stats.norm.cdf(abs(z_score)))  # Two-tailed test

print(f"Runs up: {runs_up}")
print(f"Runs down: {runs_down}")
print(f"Total runs: {total_runs}")
print(f"Expected runs: {expected_runs:.2f}")
print(f"Z-score: {z_score:.4f}")
print(f"P-value: {p_value_runs:.4f}")
print_result("Runs Test", p_value_runs)

# Summary Statistics
print("\n6. SUMMARY STATISTICS")
print("-" * 70)
print(f"Mean: {np.mean(random_numbers):.6f} (expected: 0.5)")
print(f"Variance: {np.var(random_numbers):.6f} (expected: 0.0833)")
print(f"Min: {np.min(random_numbers):.6f}")
print(f"Max: {np.max(random_numbers):.6f}")
print(f"Std Dev: {np.std(random_numbers):.6f} (expected: 0.2887)")

print("\n" + "=" * 70)
print("Testing complete!")
print("=" * 70)


