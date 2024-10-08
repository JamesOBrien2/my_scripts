#!/usr/bin/python3
import sys
from my_functions import bohr_to_angstrom, convert_coord_to_xyz

if len(sys.argv) != 2:
    print("Usage: coord2xyz.py input_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = input_file.split('.')[0] + ".xyz"
convert_coord_to_xyz(input_file, output_file)
print(f"Conversion complete. Output written to {output_file}")
