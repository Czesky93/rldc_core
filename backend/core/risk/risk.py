"""
Risk management module for RLdC_Core.

Defines risk parameters and helper functions to enforce min notional, max positions, cooldowns, etc.
"""
# Minimum order notional expressed in EUR. Candidates below this threshold are
# automatically rejected. You can adjust this constant to tighten or relax
# trade size requirements.
MIN_ORDER_NOTIONAL_EUR: float = 60.0

# Minimum expected net profit percentage (after fees) required to proceed
# with a trade. If the computed edge does not meet this threshold the
# trade will be skipped.
MIN_EXPECTED_NET_PROFIT_PCT: float = 1.2

# Maximum number of open positions allowed concurrently. Trades beyond this
# limit will be rejected to prevent over‑exposure.
MAX_OPEN_POSITIONS: int = 5

# Fee percentage assumed for a round trip trade (enter + exit). This is
# a simplification; in reality fees depend on maker/taker rates and the
# asset being traded.
FEE_PCT: float = 0.1  # 0.1% fees per side (0.2% total)

def is_notional_valid(notional_value: float) -> bool:
    """Return True if the order notional meets the configured minimum.

    Parameters
    ----------
    notional_value: float
        The euro value of the trade (price * quantity).

    Returns
    -------
    bool
        Whether the notional is at least MIN_ORDER_NOTIONAL_EUR.
    """
    return notional_value >= MIN_ORDER_NOTIONAL_EUR

def compute_edge(entry_price: float, expected_exit: float, fee_pct: float = FEE_PCT) -> float:
    """Compute expected net profit percentage after fees.

    Parameters
    ----------
    entry_price: float
        The price at which the position would be opened.
    expected_exit: float
        The expected take profit price for the position.
    fee_pct: float, optional
        Percentage fee applied per side (enter or exit). Default is global
        FEE_PCT.

    Returns
    -------
    float
        Net profit percentage after subtracting estimated fees.
    """
    gross_profit_pct = (expected_exit - entry_price) / entry_price * 100.0
    net_profit_pct = gross_profit_pct - (fee_pct * 2 * 100.0)  # two sides
    return net_profit_pct


def validate_candidate(candidate: dict, open_positions: int) -> bool:
    """Validate whether a candidate trade passes risk filters.

    The candidate dictionary is expected to contain at least the keys
    `symbol`, `entry_price`, `quantity`, and `expected_exit_price`. This
    function checks the minimum notional, minimum net profit edge and the
    maximum number of open positions.

    Parameters
    ----------
    candidate: dict
        A dictionary describing the trade candidate.
    open_positions: int
        The number of currently open positions.

    Returns
    -------
    bool
        True if the trade should proceed, False otherwise.
    """
    if open_positions >= MAX_OPEN_POSITIONS:
        return False
    notional = candidate["entry_price"] * candidate["quantity"]
    if not is_notional_valid(notional):
        return False
    edge = compute_edge(candidate["entry_price"], candidate["expected_exit_price"], FEE_PCT)
    if edge < MIN_EXPECTED_NET_PROFIT_PCT:
        return False
    return True
