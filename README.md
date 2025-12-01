# Random Number Generator Testing for OpenMC

This directory contains tests to verify the correctness of OpenMC's random number generator (PCG-RXS-M-XS based on LCG).

## Test Cases

### Test Case 1: Knuth's Statistical Tests ✓
**File:** `rand.py`

Implements the standard statistical tests described by Knuth (Volume 2, Section 3.3):
- Equidistribution Test (Frequency Test)
- Serial Test (2D Correlation)
- Gap Test
- Poker Test
- Runs Test (Monotonicity)

**Run:**
```bash
python rand.py
```

### Test Case 2: DIEHARD Test Suite
**File:** `diehard_generator.py`

Generates binary random stream files for use with Marsaglia's DIEHARD test suite.

**Steps:**

1. Generate binary random stream:
```bash
python diehard_generator.py
```

2. Install DIEHARD (or use TestU01 which includes similar tests):

**Option A: DIEHARD** (original, but harder to find)
- Download from: http://www.stat.fsu.edu/pub/diehard/
- Compile and run on `random_stream.bin`

**Option B: TestU01** (recommended - modern replacement)
```bash
# Install TestU01
wget http://simul.iro.umontreal.ca/testu01/TestU01.zip
unzip TestU01.zip
cd TestU01-*
./configure
make
sudo make install
```

3. Run TestU01 tests on generated stream:
```bash
python testu01_wrapper.py
```

## Acceptance Criteria

- **Knuth Tests**: All tests should have p-value > 0.01
- **DIEHARD/TestU01**: Should pass all batteries with no systematic failures

## Test Method

1. Random stream generating program uses OpenMC's LCG implementation via `openmc.lib.prn()`
2. Statistical tests are applied to the generated random stream
3. If both test cases pass acceptance criteria, the random number generator is considered acceptable

## References

- [13] Knuth, D. E. (1997). The Art of Computer Programming, Volume 2: Seminumerical Algorithms (3rd ed.)
- [14] Variations on Knuth's statistical tests
- [15] Marsaglia, G. (1995). DIEHARD: A Battery of Tests of Randomness
