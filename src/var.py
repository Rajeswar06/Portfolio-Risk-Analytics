# ==========================================================
# Value at Risk (VaR) Module
# ==========================================================
#
# This module implements multiple Value at Risk (VaR)
# methodologies used to estimate the potential downside
# risk of an investment portfolio.
#
# Implemented Methods
# -------------------
# • Historical Value at Risk
# • Parametric (Variance-Covariance) VaR
# • Conditional Value at Risk (CVaR)
# • Monte Carlo Value at Risk
#
# ==========================================================

import numpy as np
from scipy.stats import norm


# ==========================================================
# Historical Value at Risk
# ==========================================================

def calculate_historical_var(
    data,
    confidence_level=0.95
):
    """
    Calculate Historical Value at Risk (VaR).
    """

    if not 0 < confidence_level < 1:

        raise ValueError(
            "confidence_level must be between 0 and 1."
        )

    returns = data["Daily Return"].dropna()

    var = np.percentile(
        returns,
        (1 - confidence_level) * 100
    )

    return var


# ==========================================================
# Parametric Value at Risk
# ==========================================================

def calculate_parametric_var(
    data,
    confidence_level=0.95
):
    """
    Calculate Parametric (Variance-Covariance)
    Value at Risk.
    """

    if not 0 < confidence_level < 1:

        raise ValueError(
            "confidence_level must be between 0 and 1."
        )

    returns = data["Daily Return"].dropna()

    mean_return = returns.mean()

    volatility = returns.std()

    z_score = norm.ppf(
        1 - confidence_level
    )

    var = (
        mean_return
        + z_score * volatility
    )

    return var


# ==========================================================
# Conditional Value at Risk (CVaR)
# ==========================================================

def calculate_cvar(
    data,
    confidence_level=0.95
):
    """
    Calculate Conditional Value at Risk (CVaR),
    also known as Expected Shortfall.
    """

    if not 0 < confidence_level < 1:

        raise ValueError(
            "confidence_level must be between 0 and 1."
        )

    returns = data["Daily Return"].dropna()

    historical_var = calculate_historical_var(
        data,
        confidence_level
    )

    worst_returns = returns[
        returns <= historical_var
    ]

    cvar = worst_returns.mean()

    return cvar


# ==========================================================
# Monte Carlo Value at Risk
# ==========================================================

def calculate_monte_carlo_var(
    data,
    confidence_level=0.95,
    simulations=10000
):
    """
    Calculate Monte Carlo Value at Risk.
    """

    if not 0 < confidence_level < 1:

        raise ValueError(
            "confidence_level must be between 0 and 1."
        )

    returns = data["Daily Return"].dropna()

    mean_return = returns.mean()

    volatility = returns.std()

    # Ensure reproducible Monte Carlo results
    np.random.seed(42)

    simulated_returns = np.random.normal(
        loc=mean_return,
        scale=volatility,
        size=simulations
    )

    monte_carlo_var = np.percentile(
        simulated_returns,
        (1 - confidence_level) * 100
    )

    return monte_carlo_var