import matplotlib.pyplot as plt
import seaborn as sns

PALETTE = sns.color_palette('pastel')

import plotly.graph_objects as go
import pandas as pd

def create_distribution_plot(df, x_var, hue_var):
    """
    Creates a Plotly distribution plot for a numerical variable, 
    overlaid with the distribution for each category of a hue variable.

    Args:
        df (pd.DataFrame): The input DataFrame.
        x_var (str): The name of the numerical variable for the x-axis.
        hue_var (str): The name of the categorical variable for grouping.

    Returns:
        plotly.graph_objects.Figure: The resulting Plotly figure.
    """
    # Initialize the figure
    fig = go.Figure()

    # Add the overall distribution
    fig.add_trace(go.Histogram(
        x=df[x_var],
        name="Overall",
        opacity=0.5,
        histnorm='probability density',  # Normalize to make densities comparable
        marker=dict(color='gray')
    ))

    # Add distributions for each category in the hue variable
    for hue_value in df[hue_var].unique():
        filtered_df = df[df[hue_var] == hue_value]
        fig.add_trace(go.Histogram(
            x=filtered_df[x_var],
            name=f"{hue_var}: {hue_value}",
            opacity=0.5,
            histnorm='probability density'
        ))

    # Update layout for better readability
    fig.update_layout(
        title=f"Distribution of {x_var} by {hue_var}",
        xaxis_title=x_var,
        yaxis_title="Density",
        barmode="overlay",  # Overlay the histograms
        template="plotly_white"
    )

    return fig
