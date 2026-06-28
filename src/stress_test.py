# ==========================================================
# Stress Testing Module
# ==========================================================
#
# This module applies predefined market stress scenarios
# to estimate the potential impact on a stock's price.
#
# Implemented Scenarios
# ---------------------
# • Market Correction (-10%)
# • Bear Market (-20%)
# • Market Crash (-30%)
# • COVID Crash (-35%)
# • Financial Crisis (-50%)
#
# These scenarios help investors understand how their
# portfolio might perform under adverse market conditions.
#
# ==========================================================


# ==========================================================
# Run Stress Test
# ==========================================================

def run_stress_test(
    current_price,
    scenario
):
    """
    Apply a predefined market stress scenario to the
    current stock price.

    The function reduces the current price by the
    percentage associated with the selected scenario.

    Available Scenarios
    -------------------
    • Market Correction : -10%
    • Bear Market       : -20%
    • Market Crash      : -30%
    • COVID Crash       : -35%
    • Financial Crisis  : -50%

    Parameters
    ----------
    current_price : float
        Current market price of the stock.

    scenario : str
        Name of the stress scenario.

    Returns
    -------
    float
        Estimated stock price after applying the
        selected market shock.

    Raises
    ------
    ValueError
        If an invalid scenario name is provided.
    """

    # ======================================================
    # Predefined Market Stress Scenarios
    # ======================================================

    scenarios = {

        "Market Correction": 0.10,

        "Bear Market": 0.20,

        "Market Crash": 0.30,

        "COVID Crash": 0.35,

        "Financial Crisis": 0.50

    }

    # ======================================================
    # Validate User Input
    # ======================================================

    if scenario not in scenarios:

        raise ValueError(
            "Invalid stress scenario."
        )

    # ======================================================
    # Apply Market Shock
    # ======================================================

    shock = scenarios[scenario]

    stressed_price = current_price * (
        1 - shock
    )

    return stressed_price