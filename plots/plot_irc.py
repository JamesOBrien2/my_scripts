#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

def read_irc_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()[4:]  # Skip the header lines
    data = [line.split() for line in lines]
    return pd.DataFrame(data, columns=['IRC', 'Total_Energy'], dtype=float)

# Set up argument parser
parser = argparse.ArgumentParser(description='Plot IRC data from two files.')
parser.add_argument('-f', '--forward', required=True, help='Forward pathway file')
parser.add_argument('-b', '--backward', required=True, help='Backward pathway file')
args = parser.parse_args()

# Read the data from files
forward_df = read_irc_file(args.forward)
backward_df = read_irc_file(args.backward)

# Reverse the backward pathway and negate its IRC values
backward_df['IRC'] = -backward_df['IRC']
backward_df = backward_df.iloc[::-1].reset_index(drop=True)

# Combine the backward and forward data
df = pd.concat([backward_df, forward_df.iloc[1:]], ignore_index=True)

# Display the first few rows of the DataFrame
print(df.head())

# Display the last few rows of the DataFrame
print(df.tail())

# Settings
COLORS = ["#C8534A", "#EAA895"]

# Create a figure and axis object
fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(df['IRC'], df['Total_Energy'], color=COLORS[0], alpha=0.8)

# Add labels and title
ax.set_xlabel("Intrinsic Reaction Coordinate (IRC)")
ax.set_ylabel("Energy (Ha)")
ax.set_title("Total Energy vs. IRC")

# Save the plot
plt.savefig('irc_plot.svg', format='svg')
plt.savefig('irc_plot.png', format='png')

# Show the plot
plt.show()
