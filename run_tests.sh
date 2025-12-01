#!/bin/bash
# Script to run complete RNG validation test suite

echo "======================================================================"
echo "OpenMC Random Number Generator - Complete Test Suite"
echo "======================================================================"
echo ""

# Test Case 1: Knuth's Statistical Tests
echo "TEST CASE 1: Knuth's Statistical Tests"
echo "----------------------------------------------------------------------"
python rand.py
KNUTH_EXIT=$?
echo ""

# Test Case 2: Generate stream for DIEHARD/TestU01
echo "TEST CASE 2: Generating Random Stream for DIEHARD/TestU01"
echo "----------------------------------------------------------------------"
python diehard_generator.py
DIEHARD_GEN_EXIT=$?
echo ""

# Summary
echo "======================================================================"
echo "Test Suite Summary"
echo "======================================================================"
if [ $KNUTH_EXIT -eq 0 ]; then
    echo "✓ Knuth's Statistical Tests: COMPLETED"
else
    echo "✗ Knuth's Statistical Tests: FAILED"
fi

if [ $DIEHARD_GEN_EXIT -eq 0 ]; then
    echo "✓ Random Stream Generation: COMPLETED"
    echo ""
    echo "Next steps for DIEHARD/TestU01 testing:"
    echo "  1. Use TestU01: python testu01_wrapper.py"
    echo "  2. Or use PractRand: cat random_stream.bin | RNG_test stdin32"
    echo "  3. Or use dieharder: dieharder -a -g 202 -f random_stream.bin"
else
    echo "✗ Random Stream Generation: FAILED"
fi
echo "======================================================================"
