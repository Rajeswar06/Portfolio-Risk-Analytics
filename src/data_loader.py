# ==========================================================
# Data Loader Module
# ==========================================================
#
# This module is responsible for downloading historical
# market data from Yahoo Finance.
#
# It supports:
#
# 1. Single Stock Download
# 2. Multiple Stock Download
# 3. Benchmark Index Download
#
# The downloaded data is used throughout the project for
# return calculations, volatility analysis, CAPM, VaR,
# Monte Carlo simulation, and portfolio analytics.
# ==========================================================

import yfinance as yf


# ==========================================================
# Download Historical Stock Data
# ==========================================================

def download_stock_data(ticker, start_date, end_date):
    """
    Download historical price data for a single stock from
    Yahoo Finance.

    The downloaded data includes:

    - Open
    - High
    - Low
    - Close
    - Volume

    The data is also saved locally as a CSV file.

    Parameters
    ----------
    ticker : str
        Stock symbol (e.g. RELIANCE.NS)

    start_date : str
        Start date of analysis.

    end_date : str
        End date of analysis.

    Returns
    -------
    pandas.DataFrame
        Historical OHLCV price data.
    """

    data = yf.download(
        ticker,
        start=start_date,
        end=end_date
    )

    # Save downloaded data locally
    data.to_csv(f"data/{ticker}.csv")

    return data


# ==========================================================
# Download Multiple Stocks
# ==========================================================

def download_multiple_stocks(
    tickers,
    start_date,
    end_date
):
    """
    Download adjusted closing prices for multiple stocks.

    Adjusted Close prices account for:

    - Dividends
    - Stock splits
    - Corporate actions

    These prices are useful for portfolio analysis.

    Parameters
    ----------
    tickers : list
        List of stock symbols.

    start_date : str
        Analysis start date.

    end_date : str
        Analysis end date.

    Returns
    -------
    pandas.DataFrame
        Adjusted closing prices for all requested stocks.
    """

    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True
    )

    close_prices = data["Close"]

    return close_prices


# ==========================================================
# Download Benchmark Index Data
# ==========================================================

def download_market_data(
    benchmark,
    start_date,
    end_date
):
    """
    Download historical price data for a benchmark index.

    Examples
    --------
    ^NSEI      -> NIFTY 50

    ^NSEBANK   -> NIFTY BANK

    ^CNXIT     -> NIFTY IT

    Parameters
    ----------
    benchmark : str
        Yahoo Finance benchmark ticker.

    start_date : str
        Analysis start date.

    end_date : str
        Analysis end date.

    Returns
    -------
    pandas.DataFrame
        Historical benchmark index data.
    """

    return yf.download(
        benchmark,
        start=start_date,
        end=end_date
    )