# Random Number Generator Testing for OpenMC

**Purpose:** Verify the correctness of the random number generator implemented in OpenMC based on Linear Congruential Generators (LCGs).

## Installation

### 1. Install Python Dependencies

```bash
pip install numpy scipy
```

### 2. Build TestU01 (for Test Case 2)

TestU01 is already included in this repository. Build it:

```bash
cd TestU01-1.2.3
./configure
make
cd ..
```

## Running the Tests

Run both test cases with a single command:

```bash
./run_tests.sh
```

This will execute:
- **Test Case 1:** Knuth's Statistical Tests
- **Test Case 2:** Generate binary random stream for DIEHARD/TestU01

## Test Cases

### Test Case 1: Knuth's Statistical Tests

Implements standard statistical tests described by Knuth [13] and variations [14]:
- Equidistribution Test (Frequency Test)
- Serial Test (2D Correlation)
- Gap Test
- Poker Test
- Runs Test (Monotonicity)

**Acceptance Criteria:** All tests should have p-value > 0.01

### Test Case 2: Marsaglia's DIEHARD Test Suite

Generates binary random stream file (`random_stream.bin`) for testing with DIEHARD/TestU01 [15].

**Acceptance Criteria:** Should pass all test batteries with no systematic failures.

After generating the stream, apply DIEHARD/TestU01 tests:
```bash
# Option 1: Use dieharder (if installed)
dieharder -a -g 201 -f random_stream.bin

# Option 2: Use TestU01 library (in TestU01-1.2.3/)
# Create custom test program using TestU01 API
```

**Note:** Use `-g 201` for raw binary files (not `-g 202` which expects ASCII format)

## Test Method

1. Random stream generating program uses OpenMC's LCG implementation via `openmc.lib.prn()`
2. Statistical tests are applied to the generated random stream
3. If both test cases pass acceptance criteria, the RNG is verified as correct

## References

- [13] Knuth, D. E. (1997). *The Art of Computer Programming, Volume 2: Seminumerical Algorithms* (3rd ed.)
- [14] Variations on Knuth's statistical tests
- [15] Marsaglia, G. (1995). *DIEHARD: A Battery of Tests of Randomness*
