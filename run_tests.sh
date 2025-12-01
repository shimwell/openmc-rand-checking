#!/bin/bash
# Script to run complete RNG validation test suite

echo "======================================================================"
echo "OpenMC Random Number Generator - Test Suite"
echo "======================================================================"
echo ""

# Test Case 1: Knuth's Statistical Tests
echo "TEST CASE 1: Knuth's Statistical Tests"
echo "----------------------------------------------------------------------"
python knuth.py
KNUTH_EXIT=$?
echo ""

# Test Case 2: Generate stream for DIEHARD/TestU01
echo "TEST CASE 2: Marsaglia's DIEHARD - Random Stream Generation"
echo "----------------------------------------------------------------------"
python diehard_generator.py
DIEHARD_GEN_EXIT=$?
echo ""

# Run dieharder tests on generated stream
if [ $DIEHARD_GEN_EXIT -eq 0 ]; then
    echo "TEST CASE 2: Running DIEHARD Tests (dieharder)"
    echo "----------------------------------------------------------------------"
    if command -v dieharder &> /dev/null; then
        dieharder -a -g 201 -f random_stream.bin
        DIEHARD_TEST_EXIT=$?
    else
        echo "⚠ dieharder not installed. Skipping DIEHARD tests."
        echo "Install with: sudo apt install dieharder"
        DIEHARD_TEST_EXIT=0  # Don't fail if dieharder is not installed
    fi
else
    DIEHARD_TEST_EXIT=1
fi
echo ""

# Summary
echo "======================================================================"
echo "Test Suite Summary"
echo "======================================================================"
if [ $KNUTH_EXIT -eq 0 ]; then
    echo "✓ Test Case 1 (Knuth's Tests): PASSED"
else
    echo "✗ Test Case 1 (Knuth's Tests): FAILED"
    exit 1
fi

if [ $DIEHARD_GEN_EXIT -eq 0 ]; then
    echo "✓ Test Case 2 (DIEHARD Stream): GENERATED"
    if [ $DIEHARD_TEST_EXIT -eq 0 ] && command -v dieharder &> /dev/null; then
        echo "✓ Test Case 2 (DIEHARD Tests): COMPLETED"
    elif ! command -v dieharder &> /dev/null; then
        echo "⚠ Test Case 2 (DIEHARD Tests): SKIPPED (dieharder not installed)"
    else
        echo "✗ Test Case 2 (DIEHARD Tests): FAILED"
    fi
else
    echo "✗ Test Case 2 (DIEHARD Stream): FAILED"
    exit 1
fi
echo "======================================================================"
