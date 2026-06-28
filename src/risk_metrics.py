# ==========================================================
# Portfolio Risk Metrics Module
# ==========================================================
#
# This module contains functions used to measure the
# risk-adjusted performance of an investment.
#
# Implemented Metrics
# -------------------
# • Maximum Drawdown
# • Sharpe Ratio
# • Sortino Ratio
#
# These metrics are widely used in portfolio management,
# quantitative finance, and performance evaluation.
#
# ==========================================================


# ==========================================================
# Calculate Maximum Drawdown
# ==========================================================

def calculate_max_drawdown(data):
    """
    Calculate the Maximum Drawdown (MDD) of an investment.

    Maximum Drawdown measures the largest percentage decline
    from a portfolio's peak value to its subsequent trough.

    Formula
    -------
    Drawdown =
        (Current Portfolio Value - Peak Portfolio Value)
        / Peak Portfolio Value

    Parameters
    ----------
    data : pandas.DataFrame
        Historical stock data containing the
        'Daily Return' column.

    Returns
    -------
    float
        Maximum Drawdown expressed as a decimal.
    """

    cumulative = (
        1 + data["Daily Return"]
    ).cumprod()

    running_max = cumulative.cummax()

    drawdown = (
        cumulative - running_max
    ) / running_max

    max_drawdown = drawdown.min()

    return max_drawdown


# ==========================================================
# Calculate Sharpe Ratio
# ==========================================================

def calculate_sharpe_ratio(
    cagr,
    annualized_volatility,
    risk_free_rate=0.05
):
    """
    Calculate the Sharpe Ratio.

    The Sharpe Ratio measures the amount of excess return
    generated for each unit of total risk.

    Formula
    -------
                 CAGR − Risk-Free Rate
    Sharpe = ------------------------------
              Annualized Volatility

    Parameters
    ----------
    cagr : float
        Compound Annual Growth Rate.

    annualized_volatility : float
        Annualized standard deviation of returns.

    risk_free_rate : float, default=0.05
        Annual risk-free rate.

    Returns
    -------
    float
        Sharpe Ratio.
    """

    excess_return = (
        cagr - risk_free_rate
    )

    sharpe_ratio = (
        excess_return
        / annualized_volatility
    )

    return sharpe_ratio


# ==========================================================
# Calculate Sortino Ratio
# ==========================================================

def calculate_sortino_ratio(
    cagr,
    annualized_downside_deviation,
    risk_free_rate=0.05
):
    """
    Calculate the Sortino Ratio.

    Unlike the Sharpe Ratio, the Sortino Ratio considers
    only downside volatility, making it a better measure
    when upside volatility should not be penalized.

    Formula
    -------
                 CAGR − Risk-Free Rate
    Sortino = -------------------------------
              Annualized Downside Deviation

    Parameters
    ----------
    cagr : float
        Compound Annual Growth Rate.

    annualized_downside_deviation : float
        Annualized downside deviation.

    risk_free_rate : float, default=0.05
        Annual risk-free rate.

    Returns
    -------
    float
        Sortino Ratio.
    """

    excess_return = (
        cagr - risk_free_rate
    )

    sortino_ratio = (
        excess_return
        / annualized_downside_deviation
    )

    return sortino_ratio