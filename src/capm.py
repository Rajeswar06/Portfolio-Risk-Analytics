# ==========================================================
# CAPM (Capital Asset Pricing Model) Calculations
# ==========================================================
#
# This module contains functions required to calculate
# CAPM-based performance metrics, including:
#
# 1. Market Returns
# 2. Alignment of Stock and Benchmark Returns
# 3. Beta
# 4. Alpha (Jensen's Alpha)
# 5. Expected Return using CAPM
#
# These metrics are used to evaluate the relationship
# between a stock and its benchmark index.
# ==========================================================

import pandas as pd


# ==========================================================
# Calculate Market Returns
# ==========================================================

def calculate_market_return(market_data):
    """
    Calculate daily percentage returns for the benchmark index.

    Parameters
    ----------
    market_data : pandas.DataFrame
        Benchmark index historical price data.

    Returns
    -------
    pandas.DataFrame
        Original dataframe with an additional
        'Market Return' column.
    """

    market_data["Market Return"] = (
        market_data["Close"].pct_change()
    )

    return market_data


# ==========================================================
# Align Stock Returns with Market Returns
# ==========================================================

def align_returns(stock_data, market_data):
    """
    Align stock daily returns and benchmark daily returns
    based on common trading dates.

    Parameters
    ----------
    stock_data : pandas.DataFrame
        Historical stock price data containing
        'Daily Return'.

    market_data : pandas.DataFrame
        Historical benchmark data containing
        'Market Return'.

    Returns
    -------
    pandas.DataFrame
        Combined dataframe with:

        - Stock Return
        - Market Return

        Missing values are removed.
    """

    combined_data = pd.concat(
        [
            stock_data["Daily Return"],
            market_data["Market Return"]
        ],
        axis=1
    )

    combined_data.columns = [
        "Stock Return",
        "Market Return"
    ]

    combined_data = combined_data.dropna()

    return combined_data


# ==========================================================
# Calculate Beta
# ==========================================================

def calculate_beta(combined_data):
    """
    Calculate the stock's Beta relative to the benchmark.

    Beta measures how sensitive a stock is to
    movements in the overall market.

    Formula
    -------
    Beta = Covariance(Stock, Market) /
           Variance(Market)

    Parameters
    ----------
    combined_data : pandas.DataFrame
        Dataframe containing aligned stock and
        market returns.

    Returns
    -------
    float
        Beta coefficient.
    """

    covariance = combined_data["Stock Return"].cov(
        combined_data["Market Return"]
    )

    market_variance = combined_data["Market Return"].var()

    beta = covariance / market_variance

    return beta


# ==========================================================
# Calculate Jensen's Alpha
# ==========================================================

def calculate_alpha(cagr, expected_return):
    """
    Calculate Jensen's Alpha.

    Alpha measures the excess return generated
    by the stock compared to its CAPM expected return.

    Formula
    -------
    Alpha = CAGR - Expected Return

    Parameters
    ----------
    cagr : float
        Compound Annual Growth Rate of the stock.

    expected_return : float
        Expected annual return calculated using CAPM.

    Returns
    -------
    float
        Jensen's Alpha.
    """

    alpha = cagr - expected_return

    return alpha


# ==========================================================
# Calculate Expected Return (CAPM)
# ==========================================================

def calculate_expected_return(
    market_data,
    beta,
    risk_free_rate=0.05
):
    """
    Calculate the expected annual return using the
    Capital Asset Pricing Model (CAPM).

    Formula
    -------
    Expected Return =
        Risk-Free Rate +
        Beta × (Market Return − Risk-Free Rate)

    Daily market returns are annualized assuming
    252 trading days in a year.

    Parameters
    ----------
    market_data : pandas.DataFrame
        Benchmark data containing 'Market Return'.

    beta : float
        Beta of the stock.

    risk_free_rate : float, default=0.05
        Annual risk-free rate expressed as a decimal.

    Returns
    -------
    float
        Expected annual return according to CAPM.
    """

    market_daily_return = (
        market_data["Market Return"].mean()
    )

    annual_market_return = (
        (1 + market_daily_return) ** 252
    ) - 1

    expected_return = (
        risk_free_rate
        + beta * (
            annual_market_return
            - risk_free_rate
        )
    )

    return expected_return