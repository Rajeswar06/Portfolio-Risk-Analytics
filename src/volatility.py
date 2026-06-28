# ==========================================================
# Volatility Analysis Module
# ==========================================================
#
# This module contains functions used to measure the
# volatility and downside risk of a stock.
#
# Implemented Metrics
# -------------------
# • Rolling Volatility
# • Daily Volatility
# • Annualized Volatility
# • Downside Deviation
# • Annualized Downside Deviation
#
# These metrics help quantify the variability of returns
# and are used throughout the Portfolio Risk Analytics
# project.
#
# ==========================================================

import numpy as np


# ==========================================================
# Calculate Rolling Volatility
# ==========================================================

def calculate_rolling_volatility(
    data,
    window=20
):
    """
    Calculate rolling volatility using the standard
    deviation of daily returns.

    A 20-day rolling window is commonly used to represent
    approximately one trading month.

    Parameters
    ----------
    data : pandas.DataFrame
        Historical stock data containing the
        'Daily Return' column.

    window : int, default=20
        Rolling window size.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the additional
        'Rolling Volatility' column.
    """

    data["Rolling Volatility"] = (

        data["Daily Return"]

        .rolling(window=window)

        .std()

    )

    return data


# ==========================================================
# Calculate Daily Volatility
# ==========================================================

def calculate_daily_volatility(data):
    """
    Calculate the overall daily volatility.

    Daily volatility is measured as the standard
    deviation of daily returns.

    Parameters
    ----------
    data : pandas.DataFrame
        Historical stock data containing
        'Daily Return'.

    Returns
    -------
    float
        Daily volatility.
    """

    daily_volatility = (
        data["Daily Return"].std()
    )

    return daily_volatility


# ==========================================================
# Calculate Annualized Volatility
# ==========================================================

def calculate_annualized_volatility(
    daily_volatility
):
    """
    Convert daily volatility into annualized volatility.

    Assumes there are 252 trading days in one year.

    Formula
    -------
    Annualized Volatility =
        Daily Volatility × √252

    Parameters
    ----------
    daily_volatility : float
        Daily standard deviation of returns.

    Returns
    -------
    float
        Annualized volatility.
    """

    annualized_volatility = (
        daily_volatility * np.sqrt(252)
    )

    return annualized_volatility


# ==========================================================
# Calculate Downside Deviation
# ==========================================================

def calculate_downside_deviation(data):
    """
    Calculate downside deviation using only
    negative daily returns.

    Unlike standard deviation, downside deviation
    measures only harmful volatility.

    Parameters
    ----------
    data : pandas.DataFrame
        Historical stock data containing
        'Daily Return'.

    Returns
    -------
    float
        Downside deviation.
    """

    downside_returns = data["Daily Return"][

        data["Daily Return"] < 0

    ]

    downside_deviation = (
        downside_returns.std()
    )

    return downside_deviation


# ==========================================================
# Calculate Annualized Downside Deviation
# ==========================================================

def calculate_annualized_downside_deviation(
    downside_deviation
):
    """
    Convert daily downside deviation into annualized
    downside deviation.

    Formula
    -------
    Annualized Downside Deviation =
        Daily Downside Deviation × √252

    Parameters
    ----------
    downside_deviation : float
        Daily downside deviation.

    Returns
    -------
    float
        Annualized downside deviation.
    """

    annualized_downside_deviation = (
        downside_deviation * np.sqrt(252)
    )

    return annualized_downside_deviation