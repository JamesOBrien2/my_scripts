#!/usr/bin/python3
import sys
import plotext as plt
from my_functions import convergence_data, process_convergence_data

def plot_convergence(data, title, threshold):
    plt.clf()
    plt.plot(data)
    plt.title(title)
    plt.xlabel("Optimization Step")
    plt.ylabel("Value")
    
    threshold_line = [threshold] * len(data)
    plt.scatter(range(len(data)), threshold_line, marker='-', color='red', label="Threshold")
    
    plt.show()

if __name__ == "__main__":
    file_path = sys.argv[1]
    convergence_data, thresholds = convergence_data(file_path)

    processed_convergence_data = process_convergence_data(convergence_data)

    for key, values in processed_convergence_data.items():
        plot_convergence(values, key, thresholds[key])