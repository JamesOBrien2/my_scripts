#!/usr/bin/python3

# Author: James O'Brien
# 16-07-24
# Script adapted from rmsd.ipynb by Dr. Iñigo Iribarren

# Description:
# This script filters all xyz files in cwd based on RMSD and energy differences.
# It calculates the RMSD between all pairs of xyz files and the energy difference between them.

# If the RMSD is less than a cutoff value and the energy difference is less than another cutoff value, the file is marked for deletion.

# The script then moves the files marked for deletion to a 'to_delete' directory.
# The script also moves the files not marked for deletion to a 'to_keep' directory.

# Must be used in the same directory as the xyz files.

# Requirements:
# - calculate_rmsd.py (https://github.com/iribirii/rmsd)

# Usage:
# rmsd -r <rmsd_cutoff> -e <energy_cutoff>


import calculate_rmsd
import glob
import numpy as np
import os
import argparse
import shutil

parser = argparse.ArgumentParser(description='RMSD and Energy filter')
parser.add_argument('-r', '--rmsd', type=float, help='RMSD cutoff', required=True)
parser.add_argument('-e', '--energy', type=float, help='Energy cutoff', required=True)
args = parser.parse_args()

folder = os.getcwd()
all_files = glob.glob(folder + '/' +  '*xyz')
all_files.sort()

# Separate conf_1.xyz from the rest of the files
conf_1 = all_files[0] if all_files else None
files = all_files[1:]
n_files = len(files)
print(f"Total files: {n_files + 1}")
print(f"Files to process: {n_files}")

results = np.zeros((n_files,n_files))
e_matrix = np.zeros((n_files,n_files))
erase = np.zeros((n_files,n_files))
to_delete = []
energies = np.zeros(n_files)

for file in range(n_files):
    f = open(files[file],'r')
    energies[file] = f.readlines()[1]
    f.close()
print(energies)

rel_energies = [ (x - energies.min())*627.5 for x in energies ]
print(rel_energies)

for i in range(n_files):
    for j in range(i+1,n_files):
        results[i,j] = calculate_rmsd.main([str(files[i]),str(files[j]),'-e'])
        results[j,i] = results[i,j]
        e_matrix[i,j] = abs(rel_energies[i] - rel_energies[j])
        e_matrix[j,i] = e_matrix[i,j]
    print(i)
        
print(results)

print(e_matrix)

rmsd_cutoff = args.rmsd
energy_cutoff = args.energy

to_delete = []
for i in range(n_files):
    for j in range(i+1,n_files):
        if ( results[i,j] < rmsd_cutoff ) and ( e_matrix[i,j] < energy_cutoff ):
            erase[i,j] = 1;
            erase[j,i] = erase[i,j];
            to_delete.append(files[j])

to_delete = list(dict.fromkeys(to_delete))

print('Remaining: ' + str(n_files - len(to_delete) + 1))  # +1 for conf_1.xyz

np.set_printoptions(precision=3)
print(results)
to_delete = list(dict.fromkeys(to_delete))
print(to_delete)

# Create 'to_keep' directory if it doesn't exist
if not os.path.exists('to_keep'):
    os.makedirs('to_keep')

# Move files not in 'to_delete' to 'to_keep'
to_keep = [file for file in files if file not in to_delete]

# Always include conf_1.xyz in to_keep
if conf_1:
    to_keep.insert(0, conf_1)

for file in to_keep:
    shutil.move(file, os.path.join('to_keep', os.path.basename(file)))

print(f"Moved {len(to_keep)} files to 'to_keep' directory")
print("Files in 'to_keep' directory:")
print(os.listdir('to_keep'))

# Create README.md file
readme_content = f"""# RMSD and Energy Filter Results

## Cutoffs Used
- RMSD cutoff: {rmsd_cutoff}
- Energy cutoff: {energy_cutoff}

## Files Kept
Number of files kept: {len(to_keep)}

List of kept files:
- conf_1.xyz
"""

for file in to_keep:
    readme_content += f"- {os.path.basename(file)}\n"

with open(os.path.join('to_keep', 'README.md'), 'w') as readme_file:
    readme_file.write(readme_content)

print("Created README.md file in 'to_keep' directory")
