def calculate_max_drawdown(data):
    """
    Calculate Maximum Drawdown using
    cumulative returns.
    """

    cumulative = (1 + data["Daily Return"]).cumprod()

    running_max = cumulative.cummax()

    drawdown = (cumulative - running_max) / running_max

    max_drawdown = drawdown.min()

    return max_drawdown

def calculate_sharpe_ratio(
    data,
    annualized_volatility,
    risk_free_rate=0.05
):
    """
    Calculate the annualized Sharpe Ratio.
    """

    mean_daily_return = data["Daily Return"].mean()

    annual_return = (
        (1 + mean_daily_return) ** 252
    ) - 1

    excess_return = annual_return - risk_free_rate

    sharpe_ratio = excess_return / annualized_volatility

    return sharpe_ratio

def calculate_sortino_ratio(
    data,
    annualized_downside_deviation,
    risk_free_rate=0.05
):
    """
    Calculate the annualized Sortino Ratio.
    """

    mean_daily_return = data["Daily Return"].mean()

    annual_return = (
        (1 + mean_daily_return) ** 252
    ) - 1

    excess_return = annual_return - risk_free_rate

    sortino_ratio = (
    excess_return
    / annualized_downside_deviation
)

    return sortino_ratio