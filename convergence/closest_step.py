#!/usr/bin/python3

# This script takes in a file path as an argument and returns the step that is closest to being fully optimized.
# The script uses the convergence data and thresholds from the file to determine the step that is closest to being fully optimized.
# The step that is closest to being fully optimized is the step that has the smallest total difference between the threshold and the convergence value for each key.

# Created by: James O'Brien
# Date: 06/07/2024
# Usage: closest_step <gaussian16 .log file>

import sys
from my_functions import convergence_data, find_closest_to_optimised_step

file_path = sys.argv[1]
convergence_data, thresholds = convergence_data(file_path)
closest_step = find_closest_to_optimised_step(convergence_data, thresholds)
print(f"The step closest to being fully optimized is: Step {closest_step}")