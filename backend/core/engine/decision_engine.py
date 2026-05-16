"""
Decision engine for RLdC_Core.

Coordinates scanning, risk evaluation, order creation, and state transitions.
"""
from dataclasses import dataclass
from typing import Optional

from ..scanner.market_scanner import scan_universe, score_candidates, pick_executable_candidate
from ..risk.risk import is_notional_valid, compute_edge, MIN_EXPECTED_NET_PROFIT_PCT

@dataclass
class TradeDecision:
    symbol: str
    entry_price: float
    expected_exit: float
    reason: str

def generate_trade_decision() -> Optional[TradeDecision]:
    """
    Run the scanner and risk modules to produce a trade decision.
    Returns a TradeDecision or None if no suitable candidate exists.
    """
    candidates = scan_universe()
    candidates = score_candidates(candidates)
    candidate = pick_executable_candidate(candidates)
    if candidate:
        # Placeholder values; in reality entry_price should be fetched from market
        entry_price = 1.0
        expected_exit = 1.02
        notional_value = entry_price  # For demonstration
        if not is_notional_valid(notional_value):
            return None
        edge = compute_edge(entry_price, expected_exit, fee_pct=0.001)
        if edge < MIN_EXPECTED_NET_PROFIT_PCT:
            return None
        return TradeDecision(symbol=candidate.symbol, entry_price=entry_price, expected_exit=expected_exit, reason="Scanner selected")
    return None
