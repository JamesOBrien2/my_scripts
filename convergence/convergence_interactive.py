#!/usr/bin/python3
import sys
import plotly.graph_objects as go
from my_functions import convergence_data, find_closest_to_optimised_step

def plot_convergence(data, title, threshold, closest_step):
    fig = go.Figure()

    # Plot all steps
    fig.add_trace(go.Scatter(
        x=list(range(len(data))),
        y=data,
        mode='lines+markers',
        name=title,
        hoverinfo='y',
        marker=dict(
            color=['green' if i == closest_step else 'blue' for i in range(len(data))],
            size=[12 if i == closest_step else 6 for i in range(len(data))]
        )
    ))

    # Plot threshold line
    fig.add_trace(go.Scatter(
        x=list(range(len(data))),
        y=[threshold] * len(data),
        mode='lines',
        name='Threshold',
        line=dict(dash='dash', color='red')
    ))
    # Plot closest to optimized step
    fig.add_trace(go.Scatter(
        x=[closest_step],
        y=[data[closest_step]],
        mode='markers',
        marker=dict(color='green', size=12),
        name=f'Closest to Optimized (Step {closest_step})'
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Optimization Step',
        yaxis_title='Value'
    )

    fig.show()

file_path = sys.argv[1]
convergence_data, thresholds = convergence_data(file_path)

closest_step = find_closest_to_optimised_step(convergence_data, thresholds)

for key, values in convergence_data.items():
    plot_convergence(values, key, thresholds[key], closest_step)