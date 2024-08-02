#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import sys

def read_uvvis_file(filename):
    return pd.read_csv(filename, comment='#', sep='\s+', header=None, 
                       names=['Wavelength', 'Epsilon', 'DY/DX'])

# Check if a filename is provided
if len(sys.argv) != 2:
    print("Usage: python3 script_name.py <input_file.txt>")
    sys.exit(1)

# Get the input filename
input_file = sys.argv[1]

# Read the data from the file
data = read_uvvis_file(input_file)

# Set the colour
COLOR = "#E75B64"

# Create the plot
plt.figure(figsize=(12, 6))

# Plot the spectrum
plt.plot(data['Wavelength'], data['Epsilon'], color=COLOR)

# Set labels and title
plt.xlabel('Wavelength (nm)')
plt.ylabel('ε (Molar absorptivity)')
plt.title(f'UV-Vis Spectrum of {input_file}')

# Set x-axis limits
plt.xlim(100, 500)

# Add grid
plt.grid(True, linestyle='--', alpha=0.7)

# Save the plot
output_base = input_file.rsplit('.', 1)[0]  # Remove file extension
plt.savefig(f'{output_base}_uvvis_spectrum.svg', format='svg')
plt.savefig(f'{output_base}_uvvis_spectrum.png', format='png')

# Show the plot
plt.show()
