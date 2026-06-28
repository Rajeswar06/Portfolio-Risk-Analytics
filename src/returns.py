# ==========================================================
# Returns Calculation Module
# ==========================================================
#
# This module contains functions for calculating different
# types of investment returns used throughout the
# Portfolio Risk Analytics project.
#
# The implemented metrics include:
#
# • Daily Returns
# • Weekly Returns
# • Monthly Returns
# • Annual Returns
# • Logarithmic Returns
# • Cumulative Returns
# • Rolling Mean Returns
# • Compound Annual Growth Rate (CAGR)
#
# ==========================================================

import numpy as np
import pandas as pd


# ==========================================================
# Calculate Daily Returns
# ==========================================================

def calculate_daily_return(data):
    """
    Calculate arithmetic daily returns using the closing price.

    Formula
    -------
    Daily Return =
        (Today's Close / Yesterday's Close) - 1

    Parameters
    ----------
    data : pandas.DataFrame
        Historical stock price data.

    Returns
    -------
    pandas.DataFrame
        DataFrame with an additional
        'Daily Return' column.
    """

    data["Daily Return"] = (
        data["Close"].pct_change()
    )

    return data


# ==========================================================
# Calculate Weekly Returns
# ==========================================================

def calculate_weekly_return(data):
    """
    Calculate weekly returns based on the last closing
    price of each week.

    Parameters
    ----------
    data : pandas.DataFrame
        Historical stock price data.

    Returns
    -------
    pandas.Series
        Weekly percentage returns.
    """

    weekly_prices = (
        data["Close"]
        .resample("W")
        .last()
    )

    weekly_returns = (
        weekly_prices.pct_change()
    )

    return weekly_returns


# ==========================================================
# Calculate Logarithmic Returns
# ==========================================================

def calculate_log_return(data):
    """
    Calculate logarithmic daily returns.

    Log returns are commonly used in quantitative finance
    because they are time additive.

    Formula
    -------
    ln(Current Price / Previous Price)

    Parameters
    ----------
    data : pandas.DataFrame
        Historical stock price data.

    Returns
    -------
    pandas.DataFrame
        DataFrame with an additional
        'Log Return' column.
    """

    data["Log Return"] = np.log(
        data["Close"] /
        data["Close"].shift(1)
    )

    return data


# ==========================================================
# Calculate Cumulative Return
# ==========================================================

def calculate_cumulative_return(data):
    """
    Calculate cumulative return from daily returns.

    Formula
    -------
    (1 + Daily Return).cumprod() - 1

    Parameters
    ----------
    data : pandas.DataFrame
        Historical stock price data.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the cumulative return.
    """

    data["Cumulative Return"] = (
        (1 + data["Daily Return"])
        .cumprod() - 1
    )

    return data


# ==========================================================
# Calculate Rolling Mean
# ==========================================================

def calculate_rolling_mean(
    data,
    window=20
):
    """
    Calculate the rolling average of daily returns.

    A 20-day window is commonly used to represent
    approximately one trading month.

    Parameters
    ----------
    data : pandas.DataFrame
        Historical stock price data.

    window : int, default=20
        Rolling window size.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the rolling mean.
    """

    data["Rolling Mean"] = (

        data["Daily Return"]

        .rolling(window=window)

        .mean()

    )

    return data


# ==========================================================
# Calculate Monthly Returns
# ==========================================================

def calculate_monthly_return(data):
    """
    Calculate monthly percentage returns using the
    final closing price of each month.

    Parameters
    ----------
    data : pandas.DataFrame
        Historical stock price data.

    Returns
    -------
    pandas.Series
        Monthly returns.
    """

    monthly_prices = (

        data["Close"]

        .resample("ME")

        .last()

    )

    monthly_returns = (
        monthly_prices.pct_change()
    )

    return monthly_returns


# ==========================================================
# Calculate Annual Returns
# ==========================================================

def calculate_annual_return(data):
    """
    Calculate annual returns using the last closing
    price of each calendar year.

    Parameters
    ----------
    data : pandas.DataFrame
        Historical stock price data.

    Returns
    -------
    pandas.Series
        Annual returns.
    """

    annual_prices = (

        data["Close"]

        .resample("YE")

        .last()

    )

    annual_returns = (
        annual_prices.pct_change()
    )

    return annual_returns


# ==========================================================
# Calculate Compound Annual Growth Rate (CAGR)
# ==========================================================

def calculate_cagr(data):
    """
    Calculate the Compound Annual Growth Rate (CAGR).

    CAGR represents the average annual growth rate of an
    investment over the selected analysis period.

    Formula
    -------
                  Ending Price
    CAGR = -------------------------- ^ (1 / Years) - 1
            Beginning Price

    Parameters
    ----------
    data : pandas.DataFrame
        Historical stock price data.

    Returns
    -------
    float
        Compound Annual Growth Rate.
    """

    close_prices = (
        data["Close"]
        .squeeze()
    )

    beginning_price = close_prices.iloc[0]

    ending_price = close_prices.iloc[-1]

    number_of_days = (
        close_prices.index[-1]
        - close_prices.index[0]
    ).days

    number_of_years = (
        number_of_days / 365.25
    )

    cagr = (

        (ending_price / beginning_price)

        ** (1 / number_of_years)

    ) - 1

    return cagr