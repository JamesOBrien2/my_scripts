#!/usr/bin/python3
import sys
from my_functions import read_xyz_or_com

def find_atoms(element, filename):
    atom_numbers = []
    lines = read_xyz_or_com(filename)
    
    for atom_number, line in enumerate(lines, start=1):
        parts = line.split()
        if len(parts) >= 4 and parts[0] == element:
            atom_numbers.append(atom_number)
    
    return atom_numbers

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python whichatom.py <element> <filename>")
        sys.exit(1)
    
    element = sys.argv[1]
    filename = sys.argv[2]
    
    atom_numbers = find_atoms(element, filename)
    if atom_numbers:
        print(f"{element} {', '.join(map(str, atom_numbers))}")
    else:
        print(f"No {element} atoms found in the file.")