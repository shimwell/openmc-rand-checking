"""
Wrapper for TestU01 library to test OpenMC's random number generator.

TestU01 is a modern replacement/extension of DIEHARD that includes:
- SmallCrush (quick battery)
- Crush (standard battery)
- BigCrush (extensive battery)

This uses ctypes to call TestU01's C library directly.
"""

import ctypes
import ctypes.util
import openmc
import openmc.lib
import sys

print("=" * 70)
print("OpenMC Random Number Generator - TestU01 Testing")
print("=" * 70)

# Try to load TestU01 library
testu01_lib = None
for libname in ['testu01', 'libtestu01.so', 'libtestu01.so.0']:
    try:
        lib_path = ctypes.util.find_library(libname)
        if lib_path:
            testu01_lib = ctypes.CDLL(lib_path)
            print(f"Loaded TestU01 library: {lib_path}")
            break
    except:
        continue

if testu01_lib is None:
    print("\nERROR: TestU01 library not found!")
    print("\nTo install TestU01:")
    print("1. Download: wget http://simul.iro.umontreal.ca/testu01/TestU01.zip")
    print("2. Extract and build:")
    print("   unzip TestU01.zip")
    print("   cd TestU01-*")
    print("   ./configure")
    print("   make")
    print("   sudo make install")
    print("\nAlternatively, you can:")
    print("1. Generate binary stream: python diehard_generator.py")
    print("2. Use online DIEHARD tools or other RNG test suites")
    sys.exit(1)

print("\nNote: Full TestU01 integration requires custom C wrapper.")
print("For now, please use one of these methods:")
print("\n1. Generate binary stream and use external tools:")
print("   python diehard_generator.py")
print("\n2. Use the PractRand test suite (modern alternative):")
print("   git clone https://github.com/lemire/testingRNG")
print("   # Follow instructions to test random_stream.bin")
print("\n3. Use the Knuth tests (already implemented):")
print("   python rand.py")
print("\n" + "=" * 70)

# For future implementation: proper TestU01 wrapper
# This would require creating a C wrapper that bridges OpenMC's RNG
# to TestU01's expected function signatures
print("\nFuture enhancement: Full TestU01 integration via C wrapper")
print("Current status: Use external binary stream testing")
