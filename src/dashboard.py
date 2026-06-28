# ==========================================================
# Portfolio Risk Analytics Dashboard
# ==========================================================
#
# Interactive Streamlit dashboard for portfolio risk analysis.
#
# Features
# --------
# • Historical stock analysis
# • CAPM analysis
# • Value at Risk (VaR)
# • Monte Carlo simulation
# • Portfolio performance metrics
# • PDF report generation
#
# Supported Market
# ----------------
# National Stock Exchange (NSE), India
#
# ==========================================================


# ==========================================================
# Import Required Libraries
# ==========================================================

import datetime
import os

import streamlit as st
import yfinance as yf


# ==========================================================
# Import Project Modules
# ==========================================================

from report_generator import generate_pdf

from data_loader import (
    download_stock_data,
    download_market_data,
)

from returns import (
    calculate_daily_return,
    calculate_log_return,
    calculate_cumulative_return,
    calculate_rolling_mean,
    calculate_cagr
)

from volatility import (
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
    simulate_multiple_paths
)

from visualization import (
    plot_monte_carlo_paths,
    plot_final_price_distribution
)


# ==========================================================
# Streamlit Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Portfolio Risk Analytics",
    layout="wide"
)


# ==========================================================
# Sidebar
# ==========================================================
#
# Collect all user inputs required for the analysis.
#
# Inputs
# ------
# • Stock Symbol
# • Benchmark Index
# • Analysis Period
# • Risk-Free Rate
# • Investment Amount
#
# ==========================================================

st.sidebar.header("Portfolio Settings")


# ----------------------------------------------------------
# Stock Selection
# ----------------------------------------------------------

stock = st.sidebar.text_input(
    "Enter NSE Stock Symbol",
    value="RELIANCE"
).upper()


# ----------------------------------------------------------
# Benchmark Selection
# ----------------------------------------------------------

benchmark = st.sidebar.selectbox(
    "Benchmark Index",
    [
        "NIFTY 50",
        "NIFTY BANK",
        "NIFTY IT"
    ]
)

benchmark_map = {

    "NIFTY 50": "^NSEI",

    "NIFTY BANK": "^NSEBANK",

    "NIFTY IT": "^CNXIT"

}


# ----------------------------------------------------------
# Analysis Period
# ----------------------------------------------------------

start_date = st.sidebar.date_input(
    "Start Date",
    value=datetime.date(2020, 1, 1),
    min_value=datetime.date(2000, 1, 1),
    max_value=datetime.date.today()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=datetime.date.today(),
    min_value=datetime.date(2000, 1, 1),
    max_value=datetime.date.today()
)


# Validate selected dates

if start_date >= end_date:

    st.sidebar.error(
        "End Date must be after Start Date."
    )

    st.stop()


# ----------------------------------------------------------
# Risk-Free Rate
# ----------------------------------------------------------

risk_free_rate = st.sidebar.slider(
    "Risk-Free Rate (%)",
    min_value=0.0,
    max_value=10.0,
    value=5.0,
    step=0.5
)


# ----------------------------------------------------------
# Investment Amount
# ----------------------------------------------------------

investment = st.sidebar.number_input(
    "Investment Amount",
    min_value=1000,
    value=100000,
    step=1000
)


# ----------------------------------------------------------
# Run Analysis Button
# ----------------------------------------------------------

analyze = st.sidebar.button(
    "Analyze Portfolio"
)


# ==========================================================
# Begin Portfolio Analysis
# ==========================================================

if analyze:


    # ======================================================
    # Cache Downloaded Data
    # ======================================================
    #
    # Prevents repeated downloads when only dashboard
    # widgets change.
    #
    # ======================================================

    @st.cache_data
    def load_stock_data(
        ticker,
        start_date,
        end_date
    ):

        return download_stock_data(
            ticker,
            start_date,
            end_date
        )


    # ======================================================
    # Download Stock Data
    # ======================================================

    try:

        data = load_stock_data(
            stock + ".NS",
            str(start_date),
            str(end_date)
        )

        if data.empty:

            st.error(
                "Invalid NSE stock symbol."
            )

            st.stop()

    except Exception:

        st.error(
            "Unable to download stock data."
        )

        st.stop()


    # ======================================================
    # Download Benchmark Data
    # ======================================================

    try:

        market_data = load_stock_data(
            benchmark_map[benchmark],
            str(start_date),
            str(end_date)
        )

    except Exception:

        st.error(
            "Unable to download benchmark data."
        )

        st.stop()

        # ======================================================
    # Financial Calculations
    # ======================================================
    #
    # Calculate all financial metrics required for the
    # dashboard.
    #
    # ======================================================

    # ------------------------------------------------------
    # Market Returns
    # ------------------------------------------------------

    market_data = calculate_market_return(
        market_data
    )

    market_data = market_data.rename(
        columns={
            "Daily Return": "Market Return"
        }
    )

    # ------------------------------------------------------
    # Stock Returns
    # ------------------------------------------------------

    data = calculate_daily_return(data)

    data = calculate_log_return(data)

    data = calculate_cumulative_return(data)

    data = calculate_rolling_mean(data)

    cagr = calculate_cagr(data)

    # ------------------------------------------------------
    # CAPM Calculations
    # ------------------------------------------------------

    combined_data = align_returns(
        data,
        market_data
    )

    beta = calculate_beta(
        combined_data
    )

    expected_return = (
        calculate_expected_return(
            market_data,
            beta
        )
    )

    alpha = calculate_alpha(
        cagr,
        expected_return
    )

    # ------------------------------------------------------
    # Volatility
    # ------------------------------------------------------

    daily_volatility = (
        calculate_daily_volatility(
            data
        )
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

    # ------------------------------------------------------
    # Value at Risk
    # ------------------------------------------------------

    historical_var = (
        calculate_historical_var(
            data
        )
    )

    parametric_var = (
        calculate_parametric_var(
            data
        )
    )

    cvar = calculate_cvar(
        data
    )

    monte_carlo_var = (
        calculate_monte_carlo_var(
            data
        )
    )

    # ------------------------------------------------------
    # Current Stock Price
    # ------------------------------------------------------

    current_price = (
        data["Close"]
        .iloc[-1]
        .squeeze()
    )

    # ======================================================
    # Company Information
    # ======================================================
    #
    # Retrieve company metadata from Yahoo Finance.
    #
    # ======================================================

    info = yf.Ticker(
        stock + ".NS"
    ).info

    logo = info.get(
        "logo_url",
        ""
    )

    company_name = info.get(
        "longName",
        stock
    )

    sector = info.get(
        "sector",
        "N/A"
    )

    industry = info.get(
        "industry",
        "N/A"
    )

    # ======================================================
    # Dashboard Header
    # ======================================================

    st.title(
        "Portfolio Risk Analytics Engine"
    )

    st.caption(
        "Quantitative Finance Dashboard"
    )

    st.markdown(
        f"## {company_name}"
    )

    if logo:

        st.image(
            logo,
            width=80
        )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Ticker:** {stock}"
        )

        st.write(
            f"**Sector:** {sector}"
        )

        st.write(
            f"**Industry:** {industry}"
        )

    with col2:

        st.info(
            f"Benchmark Index : {benchmark}"
        )

        st.write(
            f"**Analysis Period:** "
            f"{start_date.strftime('%d %b %Y')} "
            f"→ "
            f"{end_date.strftime('%d %b %Y')}"
        )

        st.write(
            "**Generated:** "
            f"{datetime.datetime.now().strftime('%d %b %Y %I:%M %p')}"
        )

    st.divider()

    # ======================================================
    # Portfolio Calculations
    # ======================================================

    shares = investment / current_price

    portfolio_value = (
        current_price * shares
    )

    # ======================================================
    # Monte Carlo Simulation
    # ======================================================

    all_paths = simulate_multiple_paths(
        current_price,
        cagr,
        annualized_volatility
    )

    final_prices = all_paths[:, -1]

    expected_price = final_prices.mean()

    best_case = final_prices.max()

    worst_case = final_prices.min()

    expected_portfolio = (
        expected_price * shares
    )

    best_portfolio = (
        best_case * shares
    )

    worst_portfolio = (
        worst_case * shares
    )

    probability_of_loss = (
        final_prices < current_price
    ).mean()

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
    # PDF Report Generation
    # ======================================================
    #
    # Store all important metrics in a dictionary that will
    # be used by report_generator.py to generate the PDF.
    #
    # ======================================================

    report = {

        "Company": company_name,

        "Ticker": stock,

        "Sector": sector,

        "Industry": industry,

        "Benchmark": benchmark,

        "Analysis Period":
            f"{start_date.strftime('%d %b %Y')} - "
            f"{end_date.strftime('%d %b %Y')}",

        "Current Stock Price":
            f"₹{current_price:,.2f}",

        "Investment Amount":
            f"₹{investment:,.2f}",

        "Current Portfolio Value":
            f"₹{portfolio_value:,.2f}",

        "Expected Portfolio Value":
            f"₹{expected_portfolio:,.2f}",

        "Best Portfolio Value":
            f"₹{best_portfolio:,.2f}",

        "Worst Portfolio Value":
            f"₹{worst_portfolio:,.2f}",

        "CAGR":
            f"{cagr:.2%}",

        "Annual Volatility":
            f"{annualized_volatility:.2%}",

        "Sharpe Ratio":
            f"{sharpe_ratio:.2f}",

        "Sortino Ratio":
            f"{sortino_ratio:.2f}",

        "Beta":
            f"{beta:.2f}",

        "Alpha":
            f"{alpha:.2%}",

        "Historical VaR":
            f"{historical_var:.2%}",

        "Parametric VaR":
            f"{parametric_var:.2%}",

        "Conditional VaR":
            f"{cvar:.2%}",

        "Monte Carlo VaR":
            f"{monte_carlo_var:.2%}",

        "Probability of Loss":
            f"{probability_of_loss:.2%}"

    }

    pdf = generate_pdf(report)

    # ======================================================
    # Investment Summary
    # ======================================================

    st.header("Investment Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Current Stock Price",
            f"₹{current_price:,.2f}"
        )

        st.metric(
            "Current Portfolio Value",
            f"₹{portfolio_value:,.2f}"
        )

    with col2:

        st.metric(
            "Number of Shares",
            f"{shares:.2f} Shares"
        )

        st.metric(
            "Benchmark Index",
            benchmark
        )

    st.divider()

    # ======================================================
    # Return Metrics
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Return Metrics")

        st.metric(
            "CAGR",
            f"{cagr:.2%}"
        )

        st.metric(
            "Annual Volatility",
            f"{annualized_volatility:.2%}"
        )

        st.metric(
            "Maximum Drawdown",
            f"{max_drawdown:.2%}"
        )

    with col2:

        st.subheader("Risk Metrics")

        st.metric(
            "Sharpe Ratio",
            f"{sharpe_ratio:.2f}"
        )

        st.metric(
            "Sortino Ratio",
            f"{sortino_ratio:.2f}"
        )

        st.metric(
            "Beta",
            f"{beta:.2f}"
        )

        st.metric(
            "Expected Return",
            f"{expected_return:.2%}"
        )

        st.metric(
            "Alpha",
            f"{alpha:.2%}"
        )

    st.divider()

    # ======================================================
    # Value at Risk (VaR)
    # ======================================================

    st.subheader("Value at Risk")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Historical VaR",
            f"{historical_var:.2%}"
        )

        st.metric(
            "Parametric VaR",
            f"{parametric_var:.2%}"
        )

    with col2:

        st.metric(
            "Conditional VaR",
            f"{cvar:.2%}"
        )

        st.metric(
            "Monte Carlo VaR",
            f"{monte_carlo_var:.2%}"
        )

    st.divider()

    # ======================================================
    # Monte Carlo Summary
    # ======================================================

    st.subheader("Monte Carlo Simulation")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Expected Price",
            f"₹{expected_price:,.2f}"
        )

        st.metric(
            "Best Case Price",
            f"₹{best_case:,.2f}"
        )

    with col2:

        st.metric(
            "Worst Case Price",
            f"₹{worst_case:,.2f}"
        )

        st.metric(
            "Probability of Loss",
            f"{probability_of_loss:.2%}"
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Expected Portfolio Value",
            f"₹{expected_portfolio:,.2f}"
        )

        st.metric(
            "Best Portfolio Value",
            f"₹{best_portfolio:,.2f}"
        )

    with col2:

        st.metric(
            "Worst Portfolio Value",
            f"₹{worst_portfolio:,.2f}"
        )

    st.divider()    

        # ======================================================
    # Monte Carlo Visualization
    # ======================================================
    #
    # Display the simulated price paths and the
    # distribution of the final simulated prices.
    #
    # The figures are also saved as PNG images so they
    # can be embedded into the generated PDF report.
    #
    # ======================================================

    st.subheader("Monte Carlo Price Paths")

    BASE_DIR = os.path.dirname(__file__)

    fig1 = plot_monte_carlo_paths(
        all_paths
    )

    fig1.write_image(
        os.path.join(
            BASE_DIR,
            "monte_carlo_paths.png"
        )
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.divider()

    # ======================================================
    # Distribution of Final Prices
    # ======================================================

    st.subheader(
        "Distribution of Final Simulated Prices"
    )

    fig2 = plot_final_price_distribution(
        final_prices
    )

    fig2.write_image(
        os.path.join(
            BASE_DIR,
            "distribution.png"
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    # ======================================================
    # Export Report
    # ======================================================
    #
    # Allow the user to download the complete portfolio
    # risk analysis report as a PDF.
    #
    # The report includes:
    #
    # • Company Information
    # • Investment Summary
    # • Risk Metrics
    # • Return Metrics
    # • Value at Risk
    # • Monte Carlo Results
    # • Charts
    #
    # ======================================================

    st.subheader("Export Report")

    st.download_button(
        label="📄 Download Portfolio Report (PDF)",
        data=pdf,
        file_name=f"{stock}_Portfolio_Report.pdf",
        mime="application/pdf"
    )
        

        
    