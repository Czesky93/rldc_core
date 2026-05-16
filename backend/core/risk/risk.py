"""
Risk management module for RLdC_Core.

Defines risk parameters and helper functions to enforce min notional, max positions, cooldowns, etc.
"""
MIN_ORDER_NOTIONAL_EUR = 60.0
MIN_EXPECTED_NET_PROFIT_PCT = 1.2
MAX_OPEN_POSITIONS = 5

def is_notional_valid(notional_value: float) -> bool:
    """Check if order notional meets minimum requirement."""
    return notional_value >= MIN_ORDER_NOTIONAL_EUR

def compute_edge(entry_price: float, expected_exit: float, fee_pct: float) -> float:
    """Compute expected net profit percentage after fees."""
    gross_profit_pct = (expected_exit - entry_price) / entry_price * 100
    net_profit_pct = gross_profit_pct - fee_pct * 100
    return net_profit_pct
