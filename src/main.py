from data_loader import download_stock_data
from returns import (
    calculate_daily_return,
    calculate_log_return,
    calculate_cumulative_return,
    calculate_rolling_mean
)
from volatility import (
    calculate_rolling_volatility,
    calculate_daily_volatility,
    calculate_annualized_volatility,
    calculate_downside_deviation,
    calculate_annualized_downside_deviation
)
from risk_metrics import (
    calculate_max_drawdown,
    calculate_sharpe_ratio,
    calculate_sortino_ratio
)

def main():
    ticker = "AAPL"
    start_date = "2020-01-01"
    end_date = "2024-01-01"

    data = download_stock_data(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date
    )

    data = calculate_daily_return(data)

    data = calculate_log_return(data)

    data = calculate_cumulative_return(data)

    data = calculate_rolling_mean(data)

    data = calculate_rolling_volatility(data)

    daily_volatility = calculate_daily_volatility(data)

    annualized_volatility = calculate_annualized_volatility(
    daily_volatility
)
    
    downside_deviation = calculate_downside_deviation(data)

    annualized_downside_deviation = (
    calculate_annualized_downside_deviation(
        downside_deviation
    )
)

    max_drawdown = calculate_max_drawdown(data)

    sharpe_ratio = calculate_sharpe_ratio(
    data,
    annualized_volatility
)
    
    sortino_ratio = calculate_sortino_ratio(
    data,
    annualized_downside_deviation
)

    print(f"Daily Volatility: {daily_volatility:.4f}")
    print(f"Annualized Volatility: {annualized_volatility:.4f}")
    print(f"Downside Deviation: {downside_deviation:.4f}")
    print(f"Maximum Drawdown: {max_drawdown:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
    print(f"Sortino Ratio: {sortino_ratio:.4f}")

if __name__ == "__main__": 
    main()