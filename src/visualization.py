# ==========================================================
# Visualization Module
# ==========================================================
#
# This module contains interactive Plotly visualizations
# used in the Portfolio Risk Analytics Dashboard.
#
# Available Charts
# ----------------
# • Monte Carlo Price Paths
# • Distribution of Final Simulated Prices
#
# These figures are displayed in the Streamlit dashboard
# and exported to the PDF report.
#
# ==========================================================

import numpy as np
import plotly.graph_objects as go


# ==========================================================
# Monte Carlo Price Paths
# ==========================================================

def plot_monte_carlo_paths(all_paths):
    """
    Plot Monte Carlo simulated stock price paths.

    For readability, only the first 100 simulations are
    displayed.

    Parameters
    ----------
    all_paths : numpy.ndarray
        Matrix containing simulated price paths.

        Rows    -> Simulation number

        Columns -> Trading day

    Returns
    -------
    plotly.graph_objects.Figure
        Interactive Plotly figure.
    """

    fig = go.Figure()

    # Plot first 100 simulations

    for i in range(min(100, all_paths.shape[0])):

        fig.add_trace(

            go.Scatter(

                y=all_paths[i],

                mode="lines",

                line=dict(width=1),

                opacity=0.35,

                showlegend=False,

                hovertemplate=(
                    "Trading Day %{x}<br>"
                    "Price ₹%{y:,.2f}"
                    "<extra></extra>"
                )

            )

        )

    fig.update_layout(

        title="Monte Carlo Price Simulation",

        xaxis_title="Trading Days",

        yaxis_title="Stock Price (₹)",

        template="plotly_dark",

        height=600,

        hovermode="x unified"

    )

    return fig


# ==========================================================
# Distribution of Final Simulated Prices
# ==========================================================

def plot_final_price_distribution(final_prices):
    """
    Plot the distribution of final simulated stock prices.

    A histogram is manually constructed to allow custom
    hover information for each price range.

    Parameters
    ----------
    final_prices : numpy.ndarray
        Final stock prices from every Monte Carlo
        simulation.

    Returns
    -------
    plotly.graph_objects.Figure
        Interactive histogram.
    """

    # Create histogram

    counts, bin_edges = np.histogram(
        final_prices,
        bins=30
    )

    left_edges = bin_edges[:-1]

    right_edges = bin_edges[1:]

    centers = (
        left_edges + right_edges
    ) / 2

    widths = (
        right_edges - left_edges
    )

    # Hover information

    hover_text = [

        (
            "<b>Price Range</b><br>"
            f"₹{left:,.2f} - ₹{right:,.2f}<br>"
            f"<b>Simulations</b>: {count}"
        )

        for left, right, count in zip(
            left_edges,
            right_edges,
            counts
        )

    ]

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=centers,

            y=counts,

            width=widths,

            customdata=hover_text,

            hovertemplate="%{customdata}<extra></extra>"

        )

    )

    fig.update_layout(

        title="Distribution of Final Simulated Prices",

        template="plotly_dark",

        xaxis_title="Final Stock Price (₹)",

        yaxis_title="Frequency",

        bargap=0.02,

        height=550

    )

    return fig