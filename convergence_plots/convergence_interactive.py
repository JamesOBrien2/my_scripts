#!/usr/bin/python3
import sys
import plotly.graph_objects as go
from my_functions import convergence_data, process_convergence_data

def plot_convergence(data, title, threshold):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(range(len(data))),
        y=data,
        mode='lines+markers',
        name=title,
        hoverinfo='y'
    ))

    fig.add_trace(go.Scatter(
        x=list(range(len(data))),
        y=[threshold] * len(data),
        mode='lines',
        name='Threshold',
        line=dict(dash='dash', color='red')
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Optimization Step',
        yaxis_title='Value'
    )

    fig.show()

if __name__ == "__main__":
    file_path = sys.argv[1]
    convergence_data, thresholds = convergence_data(file_path)

    processed_convergence_data = process_convergence_data(convergence_data)

    for key, values in processed_convergence_data.items():
        plot_convergence(values, key, thresholds[key])