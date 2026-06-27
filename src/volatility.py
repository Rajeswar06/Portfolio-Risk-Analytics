import numpy as np

def calculate_rolling_volatility(data, window=20):
    """
    Calculate rolling volatility using
    the standard deviation of daily returns.
    """

    data["Rolling Volatility"] = (
        data["Daily Return"]
        .rolling(window=window)
        .std()
    )

    return data

def calculate_daily_volatility(data):
    """
    Calculate the overall daily volatility.
    """

    daily_volatility = data["Daily Return"].std()

    return daily_volatility

def calculate_annualized_volatility(daily_volatility):
    """
    Convert daily volatility into annualized volatility.
    """

    annualized_volatility = daily_volatility * np.sqrt(252)

    return annualized_volatility

def calculate_downside_deviation(data):
    """
    Calculate downside deviation using only
    negative daily returns.
    """

    downside_returns = data["Daily Return"][
        data["Daily Return"] < 0
    ]

    downside_deviation = downside_returns.std()

    return downside_deviation

def calculate_annualized_downside_deviation(downside_deviation):
    """
    Convert daily downside deviation
    into annualized downside deviation.
    """

    annualized_downside_deviation = downside_deviation * np.sqrt(252)

    return annualized_downside_deviation