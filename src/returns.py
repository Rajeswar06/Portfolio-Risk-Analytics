import pandas as pd


def calculate_daily_return(data):
    """
    Calculate arithmetic daily returns
    using the Close price.
    """

    data["Daily Return"] = data["Close"].pct_change()

    return data
import numpy as np

def calculate_log_return(data):
    """
    Calculate logarithmic daily returns
    using the Close price.
    """

    data["Log Return"] = np.log(
        data["Close"] / data["Close"].shift(1)
    )

    return data
def calculate_cumulative_return(data):
    """
    Calculate cumulative return from daily returns.
    """

    data["Cumulative Return"] = (
        (1 + data["Daily Return"]).cumprod() - 1
    )

    return data

def calculate_rolling_mean(data, window=20):
    """
    Calculate rolling mean of daily returns.
    """

    data["Rolling Mean"] = (
        data["Daily Return"]
        .rolling(window=window)
        .mean()
    )

    return data