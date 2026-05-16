"""Decision engine for RLdC_Core.

This module defines the `DecisionEngine` class responsible for orchestrating
market scanning, risk evaluation, order submission, and state management.
It ties together the scanner, risk, execution and notifier subsystems.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from ..scanner import market_scanner
from ..risk import risk
from ..execution.execution import ExecutionManager, Order
from ...integrations.binance.client import BinanceClient
from ...integrations.telegram.notifier import TelegramNotifier


@dataclass
class Position:
    """Represents an open trading position."""
    symbol: str
    quantity: float
    entry_price: float
    expected_exit_price: float
    order_id: str


class DecisionEngine:
    """Coordinate scanning, risk checks, and order execution.

    This class encapsulates the core trading loop. It keeps track of open
    positions to enforce risk limits and uses injected dependencies for
    market data, execution and notifications.
    """

    def __init__(self,
                 client: BinanceClient,
                 executor: ExecutionManager,
                 notifier: TelegramNotifier) -> None:
        self.client = client
        self.executor = executor
        self.notifier = notifier
        self.positions: List[Position] = []

    def run_cycle(self) -> Optional[Order]:
        """Run a single trade decision cycle.

        The engine scans the universe for candidates, sorts them by score,
        validates each candidate against risk rules, and submits an order
        for the first valid candidate. If no candidate passes validation or
        the maximum number of concurrent positions is reached, no trade
        occurs.

        Returns
        -------
        Optional[Order]
            The order executed, or None if no trade was taken.
        """
        open_positions = len(self.positions)
        # Scan market to produce candidates
        raw_candidates = market_scanner.scan_universe(self.client)
        scored_candidates = market_scanner.score_candidates(raw_candidates)
        candidate = market_scanner.pick_executable_candidate(scored_candidates, open_positions)
        if not candidate:
            return None
        # Build dictionary for risk validation
        candidate_dict = {
            "symbol": candidate.symbol,
            "entry_price": candidate.entry_price,
            "quantity": candidate.quantity,
            "expected_exit_price": candidate.expected_exit_price,
        }
        if not risk.validate_candidate(candidate_dict, open_positions):
            return None
        # Submit order through execution manager
        order = self.executor.submit_order(
            symbol=candidate.symbol,
            side="BUY",
            quantity=candidate.quantity,
            price=candidate.entry_price
        )
        # Record position
        pos = Position(
            symbol=candidate.symbol,
            quantity=candidate.quantity,
            entry_price=candidate.entry_price,
            expected_exit_price=candidate.expected_exit_price,
            order_id=order.id
        )
        self.positions.append(pos)
        # Notify via Telegram
        self.notifier.send_message(
            f"Opened {order.side} {order.symbol}: qty {order.quantity:.4f} at {order.price:.2f}"
        )
        return order

    def get_positions(self) -> List[Dict[str, Any]]:
        """Return a list of current open positions as dictionaries."""
        return [
            {
                "symbol": pos.symbol,
                "quantity": pos.quantity,
                "entry_price": pos.entry_price,
                "expected_exit_price": pos.expected_exit_price,
                "order_id": pos.order_id,
            }
            for pos in self.positions
        ]