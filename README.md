# Random Number Generator Testing for OpenMC

**Purpose:** Verify the correctness of the random number generator implemented in OpenMC based on Linear Congruential Generators (LCGs).

## Installation

### 1. Install OpenMC from this branch

expose-rand-number-to-openmc.lib

https://github.com/shimwell/openmc/tree/expose-rand-number-to-openmc.lib

### 2. Install dieharder (Optional - for Test Case 2)

```bash
sudo apt install dieharder
```

**Note:** The `run_tests.sh` script will automatically run dieharder tests if installed, or skip them if not available.

## Running the Tests

Run both test cases with a single command:

```bash
./run_tests.sh
```

This will execute:
- **Test Case 1:** Knuth's Statistical Tests
- **Test Case 2:** Generate binary random stream and run DIEHARD tests (if dieharder is installed)

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

Generates binary random stream file (`random_stream.bin`) for testing with DIEHARD [15].

**Acceptance Criteria:** Should pass all test batteries with no systematic failures.

The `run_tests.sh` script automatically runs dieharder tests if installed. Manual testing:
```bash
# Use dieharder
dieharder -a -g 201 -f random_stream.bin
```

**Note:** Use `-g 201` for raw binary files

## Test Method

1. Random stream generating program uses OpenMC's LCG implementation via `openmc.lib.prn()`
2. Statistical tests are applied to the generated random stream
3. If both test cases pass acceptance criteria, the RNG is verified as correct

## References

- [13] Knuth, D. E. (1997). *The Art of Computer Programming, Volume 2: Seminumerical Algorithms* (3rd ed.)
- [14] Variations on Knuth's statistical tests
- [15] Marsaglia, G. (1995). *DIEHARD: A Battery of Tests of Randomness*
