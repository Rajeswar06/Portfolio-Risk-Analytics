# ==========================================================
# Covariance Matrix Calculation
# ==========================================================
#
# This module contains functions related to covariance
# calculations for portfolio analysis.
#
# The covariance matrix measures how asset returns move
# relative to one another and is a key input for:
#
# • Portfolio Risk Analysis
# • Modern Portfolio Theory (MPT)
# • Efficient Frontier
# • Portfolio Optimization
# ==========================================================


# ==========================================================
# Calculate Covariance Matrix
# ==========================================================

def calculate_covariance_matrix(returns):
    """
    Calculate the covariance matrix of asset returns.

    The covariance matrix measures the degree to which
    different assets move together.

    Interpretation
    --------------
    • Positive covariance:
      Assets tend to move in the same direction.

    • Negative covariance:
      Assets tend to move in opposite directions.

    • Zero covariance:
      Assets have little or no linear relationship.

    Parameters
    ----------
    returns : pandas.DataFrame
        DataFrame containing daily returns of one or
        more assets.

        Each column represents one asset.
        Each row represents one trading day.

    Returns
    -------
    pandas.DataFrame
        Covariance matrix of the asset returns.
    """

    covariance_matrix = returns.cov()

    return covariance_matrix