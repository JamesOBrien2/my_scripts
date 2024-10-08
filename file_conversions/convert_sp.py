#!/usr/bin/python3

# Author: James O'Brien
# 06-03-2024

# Description:
#       This script will add NBO, MEP, or AIM keywords to .com files for Gaussian calculations.
#       The script will create new files with the added keywords and move them to a new directory.
#       The original files will remain in the current directory.
#       This script was made for Gaussian16, but should work for other versions as well.

# Requirements:
#       - Single-Point .com files
#       - Python 3.6 or higher
#       - Run the script in the directory containing the .com files

# Usage:
#       convert_sp [-h] [--nbo] [--mep] [--aim]

import os
import shutil
import argparse

# Create a parser object
argparser = argparse.ArgumentParser(description='Convert .com files from single point to NBO or MEP calculations')
argparser.add_argument('-n', '--nbo', action='store_true', help='Add NBO keywords to .com files')
argparser.add_argument('-m', '--mep', action='store_true', help='Add MEP keywords to .com files')
argparser.add_argument('-a', '--aim', action='store_true', help='Add AIM keywords to .com files')

args = argparser.parse_args()

# Copy & Rename files
for file in os.listdir('.'):
    if file.endswith('.com'):
        if args.nbo:
            shutil.copy(file, file.replace('.com', '_nbo.com'))
        if args.mep:
            shutil.copy(file, file.replace('.com', '_mep.com'))
        if args.aim:
            shutil.copy(file, file.replace('.com', '_aim.com'))

# Add keywords to the new files
for file in os.listdir('.'):
    if args.nbo:
        if file.endswith('nbo.com'):
            with open(file, 'r') as f:
                lines = f.readlines()
            lines[0] = lines[0].strip() + ' pop=NBO\n'
            with open(file, 'w') as f:
                f.writelines(lines)
    elif args.mep:
        if file.endswith('_mep.com'):
            with open(file, 'r') as f:
                lines = f.readlines()
            lines[0] = lines[0].strip() + ' output=wfx\n'
            lines.insert(0, f'%chk={file.replace(".com", "")}.chk\n')
            lines.append(f'{file.replace("_mep.com", "")}.wfx\n\n')
            with open(file, 'w') as f:
                f.writelines(lines)
    elif args.aim:
        if file.endswith('_aim.com'):
            with open(file, 'r') as f:
                lines = f.readlines()
            if lines[-1] != '\n':
                lines.append('\n')
            lines[0] = lines[0].strip() + ' output=wfx\n'
            lines.append(f'{file.replace(".com", "")}.wfx\n\n')
            with open(file, 'w') as f:
                f.writelines(lines)

# Create a new directory for the new files
if args.nbo:
    if not os.path.exists('nbo'):
        os.makedirs('nbo', exist_ok=True)
elif args.mep:
    if not os.path.exists('mep'):
        os.makedirs('mep', exist_ok=True)
elif args.aim:
    if not os.path.exists('aim'):
        os.makedirs('aim', exist_ok=True)

# Move all new files to new directory
for file in os.listdir('.'):
    if args.nbo:
        if file.endswith('nbo.com'):
            shutil.move(file, os.path.join('nbo', file))
    elif args.mep:
        if file.endswith('_mep.com'):
            shutil.move(file, os.path.join('mep', file))
    elif args.aim:
        if file.endswith('_aim.com'):
            shutil.move(file, os.path.join('aim', file))
