"""
Market scanner for RLdC_Core.

This module provides the scanning pipeline:
 - scan_universe: gather tradeable symbols and market data
 - score_candidates: compute ranking based on trend, volume, volatility, etc.
 - validate_candidate: apply risk and quality filters (min notional, confidence, cooldown, etc.)
 - pick_executable_candidate: choose the best validated candidate.

For now, functions are placeholders.
"""
from dataclasses import dataclass
from typing import List, Optional

from ..risk import risk  # import risk for type checking and validation
from ...integrations.binance.client import BinanceClient, MarketTick

@dataclass
class Candidate:
    """Representation of a trade candidate.

    Attributes
    ----------
    symbol: str
        Trading pair symbol, e.g. 'BTCUSDC'.
    score: float
        Ranking score; higher is better.
    confidence: float
        Confidence metric (0..1). Unused in simple scanner.
    entry_price: float
        Price at which the candidate would be entered.
    quantity: float
        Quantity to trade.
    expected_exit_price: float
        Target exit price used to compute edge.
    reason: Optional[str]
        Optional string describing why the candidate was selected or rejected.
    """

    symbol: str
    score: float
    confidence: float
    entry_price: float
    quantity: float
    expected_exit_price: float
    reason: Optional[str] = None

def scan_universe(client: BinanceClient) -> List[Candidate]:
    """Scan the market universe and generate trade candidates.

    This simple implementation iterates over the Binance client's supported
    symbols, retrieves a pseudo‑random market tick for each, and
    constructs a Candidate with a random score. The quantity is chosen
    such that the notional (price * quantity) meets or slightly exceeds
    the minimum order size defined in the risk module. The expected exit
    price is set to a small percentage above the entry price.

    Parameters
    ----------
    client: BinanceClient
        The Binance client to fetch market ticks.

    Returns
    -------
    List[Candidate]
        A list of candidate objects with basic fields populated.
    """
    candidates: List[Candidate] = []
    for symbol in client.SUPPORTED_SYMBOLS:
        tick: MarketTick = client.get_market_data(symbol)
        # Determine a minimum quantity to meet the notional requirement
        # We'll use a small multiplier and adjust upward until notional >= MIN_ORDER_NOTIONAL_EUR
        qty = 0.001  # starting quantity (approx for BTC)
        notional = tick.price * qty
        while notional < risk.MIN_ORDER_NOTIONAL_EUR:
            qty *= 2
            notional = tick.price * qty
            # To avoid infinite loop in case of extremely low price assets
            if qty > 1000:
                break
        # Determine a simple expected exit price (1.5% above entry)
        expected_exit_price = tick.price * 1.015
        # Generate a random score for demonstration
        score = risk.MIN_EXPECTED_NET_PROFIT_PCT + (tick.price % 3)  # simple heuristic
        candidate = Candidate(
            symbol=symbol,
            score=score,
            confidence=1.0,
            entry_price=tick.price,
            quantity=qty,
            expected_exit_price=expected_exit_price,
            reason=None,
        )
        candidates.append(candidate)
    return candidates

def score_candidates(candidates: List[Candidate]) -> List[Candidate]:
    """Sort candidates by descending score.

    Parameters
    ----------
    candidates: List[Candidate]
        Candidates produced by :func:`scan_universe`.

    Returns
    -------
    List[Candidate]
        Sorted candidates with highest scores first.
    """
    return sorted(candidates, key=lambda c: c.score, reverse=True)

def validate_candidate(candidate: Candidate, open_positions: int) -> bool:
    """Apply risk checks to determine if a candidate is tradeable.

    This function delegates the core risk logic to :func:`risk.validate_candidate`
    by converting the Candidate dataclass into a dictionary containing
    the necessary keys. Additional filters (e.g. momentum, volume) can
    be implemented here or inside the risk module.

    Parameters
    ----------
    candidate: Candidate
        Candidate under evaluation.
    open_positions: int
        Current number of open positions used to enforce maximum
        concurrent trades.

    Returns
    -------
    bool
        True if the candidate passes the risk checks, False otherwise.
    """
    candidate_dict = {
        "symbol": candidate.symbol,
        "entry_price": candidate.entry_price,
        "quantity": candidate.quantity,
        "expected_exit_price": candidate.expected_exit_price,
    }
    return risk.validate_candidate(candidate_dict, open_positions)

def pick_executable_candidate(candidates: List[Candidate], open_positions: int) -> Optional[Candidate]:
    """Select the first candidate that passes the validate_candidate check.

    Parameters
    ----------
    candidates: List[Candidate]
        Candidates sorted by score.
    open_positions: int
        Number of currently open positions.

    Returns
    -------
    Optional[Candidate]
        The first valid candidate or None if none are tradeable.
    """
    for c in candidates:
        if validate_candidate(c, open_positions):
            return c
    return None
