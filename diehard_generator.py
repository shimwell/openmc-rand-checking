"""
Generate binary random stream file for DIEHARD/TestU01 testing.

This program generates a large binary file of random numbers using OpenMC's
random number generator for testing with external test suites like DIEHARD
or TestU01.
"""

import openmc
import openmc.lib
import struct
import sys

# Configuration
OUTPUT_FILE = "random_stream.bin"
NUM_SAMPLES = 10_000_000  # 10 million random numbers (40 MB for 32-bit ints)

print("=" * 70)
print("OpenMC Random Number Generator - DIEHARD Stream Generator")
print("=" * 70)
print(f"Output file: {OUTPUT_FILE}")
print(f"Number of samples: {NUM_SAMPLES:,}")
print(f"File size: ~{NUM_SAMPLES * 4 / (1024*1024):.1f} MB")
print("=" * 70)

# Create minimal OpenMC model (required for initialization)
print("\nInitializing OpenMC...")
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

# Generate random stream
print("Generating random stream...")
seed = 12345

with open(OUTPUT_FILE, 'wb') as f:
    for i in range(NUM_SAMPLES):
        random_value, seed = openmc.lib.prn(seed)
        
        # Convert to 32-bit unsigned integer (0 to 2^32-1)
        # DIEHARD expects 32-bit integers
        uint32_value = int(random_value * (2**32 - 1))
        
        # Write as binary
        f.write(struct.pack('I', uint32_value))
        
        # Progress indicator
        if (i + 1) % 1_000_000 == 0:
            print(f"  Progress: {i+1:,} / {NUM_SAMPLES:,} ({100*(i+1)/NUM_SAMPLES:.1f}%)")

openmc.lib.finalize()

print("\n" + "=" * 70)
print("Random stream generation complete!")
print("=" * 70)
print(f"\nGenerated file: {OUTPUT_FILE}")
print(f"File contains {NUM_SAMPLES:,} random 32-bit unsigned integers")
print("\nNext steps:")
print("\n1. Run dieharder (use raw binary input):")
print(f"   dieharder -a -g 201 -f {OUTPUT_FILE}")
print("   Note: -g 201 reads raw binary file")
print("\n2. Or use PractRand:")
print(f"   cat {OUTPUT_FILE} | RNG_test stdin32")
print("\n3. Or use TestU01:")
print("   - Create C wrapper in TestU01-1.2.3/examples/")
print("   - Use ufile_CreateReadBin() to read binary stream")
print("=" * 70)
