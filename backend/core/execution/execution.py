"""
Execution manager for RLdC_Core.

This module abstracts order submission and monitoring.  In a real
implementation it would call out to the exchange client (e.g. Binance)
to place orders, poll for fills, and return execution reports.  For
the purposes of this skeleton it simply echoes back a filled order
immediately to allow the rest of the system to be exercised without
external dependencies.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Order:
    """Simple order record used by the execution manager."""
    symbol: str
    side: str  # BUY or SELL
    quantity: float
    price: float
    status: str = "NEW"
    order_id: Optional[str] = None


class ExecutionManager:
    """Stubbed execution manager that simulates placing orders."""

    def __init__(self, exchange_client=None):
        # exchange_client would be the real Binance client.  It is kept
        # optional here to avoid import errors when no client is available.
        self.exchange_client = exchange_client

    def submit_order(self, symbol: str, side: str, quantity: float, price: float) -> Order:
        """
        Simulate submission of an order.  Returns an Order with status
        immediately set to FILLED.  In a real implementation this would
        call the exchange API and poll until filled.
        """
        order = Order(symbol=symbol, side=side, quantity=quantity, price=price)
        # If an exchange client is provided, call it.  Otherwise, simulate.
        if self.exchange_client is not None:
            # Example of what a real call might look like:
            # result = self.exchange_client.place_order(symbol, side, quantity, price)
            # order.order_id = result.get("orderId")
            # order.status = result.get("status", "NEW")
            # For demonstration we'll just pass through to the stub below.
            pass
        # Immediately mark as filled for the skeleton.
        order.status = "FILLED"
        order.order_id = "demo-order"
        return order

    def cancel_order(self, order: Order) -> None:
        """Cancel an existing order.  Stub implementation."""
        order.status = "CANCELED"
