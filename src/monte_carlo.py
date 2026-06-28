# ==========================================================
# Monte Carlo Simulation Module
# ==========================================================
#
# This module implements Monte Carlo simulation using the
# Geometric Brownian Motion (GBM) model.
#
# It provides functions to:
#
# 1. Generate random market shocks
# 2. Simulate the next stock price
# 3. Simulate a single future price path
# 4. Simulate multiple future price paths
#
# The simulated paths are used for:
#
# • Future price forecasting
# • Portfolio valuation
# • Monte Carlo Value at Risk (VaR)
# • Probability of loss estimation
#
# ==========================================================

import numpy as np

# ==========================================================
# Generate Random Market Shock
# ==========================================================

def generate_random_shock():
    """
    Generate a random shock from a standard normal
    distribution.

    The random value represents an unexpected market
    movement and is used in the Geometric Brownian Motion
    model.

    Returns
    -------
    float
        Standard normally distributed random variable.
    """

    return np.random.normal(0, 1)


# ==========================================================
# Simulate Next Stock Price
# ==========================================================

def simulate_next_price(
    current_price,
    mu,
    sigma,
    dt=1 / 252
):
    """
    Simulate the next stock price using the
    Geometric Brownian Motion (GBM) model.

    Parameters
    ----------
    current_price : float
        Current stock price.

    mu : float
        Expected annual return (drift).

    sigma : float
        Annualized volatility.

    dt : float, default = 1/252
        Time step representing one trading day.

    Returns
    -------
    float
        Simulated stock price for the next trading day.
    """

    z = generate_random_shock()

    next_price = current_price * np.exp(
        (mu - 0.5 * sigma**2) * dt
        + sigma * np.sqrt(dt) * z
    )

    return next_price


# ==========================================================
# Simulate a Single Price Path
# ==========================================================

def simulate_price_path(
    current_price,
    mu,
    sigma,
    days=252
):
    """
    Simulate one possible future stock price path.

    Each trading day is generated using the GBM model.

    Parameters
    ----------
    current_price : float
        Initial stock price.

    mu : float
        Expected annual return.

    sigma : float
        Annualized volatility.

    days : int, default = 252
        Number of trading days to simulate.

    Returns
    -------
    list
        Simulated stock prices including the initial price.
    """

    prices = [current_price]

    for _ in range(days):

        next_price = simulate_next_price(
            prices[-1],
            mu,
            sigma
        )

        prices.append(next_price)

    return prices


# ==========================================================
# Simulate Multiple Price Paths
# ==========================================================

def simulate_multiple_paths(
    current_price,
    mu,
    sigma,
    days=252,
    simulations=1000
):
    """
    Generate multiple Monte Carlo simulation paths.

    Each path represents one possible future evolution of
    the stock price.

    Parameters
    ----------
    current_price : float
        Initial stock price.

    mu : float
        Expected annual return.

    sigma : float
        Annualized volatility.

    days : int, default = 252
        Number of trading days to simulate.

    simulations : int, default = 1000
        Number of Monte Carlo simulations.

    Returns
    -------
    numpy.ndarray
        Two-dimensional array where:

        Rows    -> Simulation number

        Columns -> Simulated stock prices over time
    """

    all_paths = []

    for _ in range(simulations):

        path = simulate_price_path(
            current_price,
            mu,
            sigma,
            days
        )

        all_paths.append(path)

    return np.array(all_paths)