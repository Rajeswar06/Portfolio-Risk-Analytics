# ==========================================================
# Portfolio Risk Analytics Engine
# ==========================================================
#
# This is the main entry point of the project.
#
# The program performs:
#
# 1. Historical data download
# 2. Return calculations
# 3. Volatility analysis
# 4. Risk metrics
# 5. CAPM analysis
# 6. Monte Carlo simulation
# 7. Stress testing
# 8. Data visualization
#
# ==========================================================


# ==========================================================
# Import Required Libraries
# ==========================================================

import numpy as np
import yfinance as yf


# ==========================================================
# Import Project Modules
# ==========================================================

from data_loader import (
    download_stock_data,
    download_market_data,
    download_multiple_stocks
)

from returns import (
    calculate_daily_return,
    calculate_log_return,
    calculate_cumulative_return,
    calculate_rolling_mean,
    calculate_weekly_return,
    calculate_monthly_return,
    calculate_annual_return,
    calculate_cagr
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

from capm import (
    calculate_market_return,
    align_returns,
    calculate_beta,
    calculate_alpha,
    calculate_expected_return
)

from var import (
    calculate_historical_var,
    calculate_parametric_var,
    calculate_cvar,
    calculate_monte_carlo_var
)

from monte_carlo import (
    simulate_next_price,
    simulate_price_path,
    simulate_multiple_paths
)

from visualization import (
    plot_monte_carlo_paths,
    plot_final_price_distribution
)

from stress_test import run_stress_test


# ==========================================================
# Main Function
# ==========================================================

def main():
    """
    Main driver function for the Portfolio Risk Analytics
    Engine.

    Workflow
    --------
    1. Download stock and benchmark data
    2. Calculate returns
    3. Calculate volatility
    4. Calculate risk metrics
    5. Perform CAPM analysis
    6. Run Monte Carlo simulation
    7. Perform stress testing
    8. Display results
    """

    # ======================================================
    # User Inputs
    # ======================================================

    ticker = (
        input("Enter NSE Stock Symbol: ")
        .upper()
        + ".NS"
    )

    start_date = "2020-01-01"
    end_date = "2024-01-01"

    benchmark = "^NSEI"

    # ======================================================
    # Download Historical Data
    # ======================================================

    print("\nDownloading stock data...\n")

    data = download_stock_data(
        ticker,
        start_date,
        end_date
    )

    market_data = download_market_data(
        benchmark,
        start_date,
        end_date
    )

    # ======================================================
    # Calculate Benchmark Returns
    # ======================================================

    market_data = calculate_market_return(
        market_data
    )

    # ======================================================
    # Calculate Stock Returns
    # ======================================================

    data = calculate_daily_return(data)

    data = calculate_log_return(data)

    data = calculate_cumulative_return(data)

    data = calculate_rolling_mean(data)

    # ======================================================
    # Calculate Returns for Different Time Horizons
    # ======================================================

    weekly_returns = calculate_weekly_return(data)

    monthly_returns = calculate_monthly_return(data)

    annual_returns = calculate_annual_return(data)

    cagr = calculate_cagr(data)

    # ======================================================
    # Value at Risk (VaR)
    # ======================================================

    historical_var = calculate_historical_var(data)

    parametric_var = calculate_parametric_var(data)

    cvar = calculate_cvar(data)

    monte_carlo_var = calculate_monte_carlo_var(data)

    # ======================================================
    # Volatility Calculations
    # ======================================================

    data = calculate_rolling_volatility(data)

    daily_volatility = calculate_daily_volatility(
        data
    )

    annualized_volatility = (
        calculate_annualized_volatility(
            daily_volatility
        )
    )

    downside_deviation = (
        calculate_downside_deviation(
            data
        )
    )

    annualized_downside_deviation = (
        calculate_annualized_downside_deviation(
            downside_deviation
        )
    )

        # ======================================================
    # Portfolio Risk Metrics
    # ======================================================

    max_drawdown = calculate_max_drawdown(
        data
    )

    sharpe_ratio = calculate_sharpe_ratio(
        cagr,
        annualized_volatility
    )

    sortino_ratio = calculate_sortino_ratio(
        cagr,
        annualized_downside_deviation
    )

    # ======================================================
    # CAPM Analysis
    # ======================================================
    #
    # Align stock and benchmark returns before calculating
    # Beta, Expected Return and Alpha.
    #
    # Beta measures the stock's sensitivity to the market.
    # Alpha measures excess return over the CAPM expected
    # return.
    # ======================================================

    combined_data = align_returns(
        data,
        market_data
    )

    beta = calculate_beta(
        combined_data
    )

    expected_return = calculate_expected_return(
        market_data,
        beta
    )

    alpha = calculate_alpha(
        cagr,
        expected_return
    )

    # ======================================================
    # Current Stock Price
    # ======================================================

    current_price = (
        data["Close"]
        .iloc[-1]
        .squeeze()
    )

    # ======================================================
    # Monte Carlo Simulation
    # ======================================================
    #
    # Generate multiple possible future price paths using
    # Geometric Brownian Motion assumptions.
    # ======================================================

    all_paths = simulate_multiple_paths(
        current_price,
        cagr,
        annualized_volatility
    )

    print(
        f"\nSimulation Shape: {all_paths.shape}"
    )

    # ======================================================
    # Simulation Statistics
    # ======================================================

    final_prices = all_paths[:, -1]

    expected_price = final_prices.mean()

    best_case = final_prices.max()

    worst_case = final_prices.min()

    probability_of_loss = (
        final_prices < current_price
    ).mean()

    # ======================================================
    # 95% Confidence Interval
    # ======================================================

    lower_bound = np.percentile(
        final_prices,
        2.5
    )

    upper_bound = np.percentile(
        final_prices,
        97.5
    )

    # ======================================================
    # Monte Carlo Results
    # ======================================================

    print()

    print(f"Expected Price: {expected_price:.2f}")

    print(f"Best Case Price: {best_case:.2f}")

    print(f"Worst Case Price: {worst_case:.2f}")

    print(
        f"Probability of Loss: "
        f"{probability_of_loss:.2%}"
    )

    print(
        f"95% Confidence Interval: "
        f"{lower_bound:.2f} - {upper_bound:.2f}"
    )

    # ======================================================
    # Portfolio Risk Analytics Summary
    # ======================================================

    print(
        "\n========== PORTFOLIO RISK ANALYTICS ==========\n"
    )

    print(f"CAGR: {cagr:.2%}")

    print(
        f"Daily Volatility: "
        f"{daily_volatility:.4f}"
    )

    print(
        f"Annualized Volatility: "
        f"{annualized_volatility:.4f}"
    )

    print(
        f"Downside Deviation: "
        f"{downside_deviation:.4f}"
    )

    print(
        "Annualized Downside Deviation: "
        f"{annualized_downside_deviation:.4f}"
    )

    print(
        f"Maximum Drawdown: {max_drawdown:.2%}"
    )

    print(
        f"Sharpe Ratio: {sharpe_ratio:.4f}"
    )

    print(
        f"Sortino Ratio: {sortino_ratio:.4f}"
    )

    print(
        f"Beta: {beta:.4f}"
    )

    print(
        f"Expected Return (CAPM): "
        f"{expected_return:.2%}"
    )

    print(
        f"Alpha: {alpha:.2%}"
    )

    print(
        f"Historical VaR (95%): "
        f"{historical_var:.2%}"
    )

    print(
        f"Parametric VaR (95%): "
        f"{parametric_var:.2%}"
    )

    print(
        f"Conditional VaR (95%): "
        f"{cvar:.2%}"
    )

    print(
        f"Monte Carlo VaR (95%): "
        f"{monte_carlo_var:.2%}"
    )

    print(
        "\n=============================================="
    )

        # ======================================================
    # Visualization
    # ======================================================
    #
    # Display Monte Carlo simulation results.
    # ======================================================

    plot_monte_carlo_paths(
        all_paths
    )

    plot_final_price_distribution(
        final_prices
    )

    # ======================================================
    # Stress Testing
    # ======================================================
    #
    # Evaluate the stock under predefined market scenarios.
    # ======================================================

    market_correction = run_stress_test(
        current_price,
        "Market Correction"
    )

    bear_market = run_stress_test(
        current_price,
        "Bear Market"
    )

    market_crash = run_stress_test(
        current_price,
        "Market Crash"
    )

    covid_crash = run_stress_test(
        current_price,
        "COVID Crash"
    )

    financial_crisis = run_stress_test(
        current_price,
        "Financial Crisis"
    )

    # ======================================================
    # Stress Test Summary
    # ======================================================

    print(
        "\n========== STRESS TEST ==========\n"
    )

    print(
        f"Market Correction (-10%): "
        f"{market_correction:.2f}"
    )

    print(
        f"Bear Market (-20%): "
        f"{bear_market:.2f}"
    )

    print(
        f"Market Crash (-30%): "
        f"{market_crash:.2f}"
    )

    print(
        f"COVID Crash (-35%): "
        f"{covid_crash:.2f}"
    )

    print(
        f"Financial Crisis (-50%): "
        f"{financial_crisis:.2f}"
    )


# ==========================================================
# Program Entry Point
# ==========================================================

if __name__ == "__main__":
    main()