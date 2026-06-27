import yfinance as yf


def download_stock_data(ticker, start_date, end_date):
    """
    Downloads historical stock data from Yahoo Finance.
    """

    data = yf.download(
        ticker,
        start=start_date,
        end=end_date
    )

    data.to_csv(f"data/{ticker}.csv")

    return data