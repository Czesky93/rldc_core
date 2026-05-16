"""Binance client integration stub.

This module defines a simple BinanceClient class with methods to fetch market
data and place orders. In a production environment this module would wrap
the official Binance REST API. The intent of this stub is to decouple the
core trading logic from the specifics of any exchange and to provide a
predictable interface for unit testing. You can later extend this class
to perform real authenticated requests.
"""

from dataclasses import dataclass
from typing import Dict, Any
import random
import time


@dataclass
class MarketTick:
    """A simple data structure representing a market tick.

    Attributes
    ----------
    symbol: str
        Trading symbol, e.g. 'BTCUSDC'.
    price: float
        Last traded price.
    timestamp: float
        Unix timestamp when the tick was generated.
    """

    symbol: str
    price: float
    timestamp: float


class BinanceClient:
    """A lightweight Binance client for demo purposes.

    This client does **not** perform any real network requests. Instead it
    generates pseudo‑random prices for a handful of hardcoded symbols.
    The class exposes methods similar to those provided by a real Binance
    client so that the rest of the codebase can be written against
    predictable interfaces.
    """

    # A small set of supported symbols for demonstration. In a real client
    # you would query the exchange for available trading pairs.
    SUPPORTED_SYMBOLS = ["BTCUSDC", "ETHUSDC", "BNBUSDC", "AVAXUSDC", "DOTUSDC"]

    def __init__(self) -> None:
        # Seed the random number generator for reproducible pseudo prices
        self._rng = random.Random(42)
        # Set up simple mid price anchors for each symbol
        self._base_prices = {
            "BTCUSDC": 65000.0,
            "ETHUSDC": 3200.0,
            "BNBUSDC": 500.0,
            "AVAXUSDC": 40.0,
            "DOTUSDC": 8.0,
        }

    def get_market_data(self, symbol: str) -> MarketTick:
        """Return a simulated market tick for the requested symbol.

        If the symbol is unsupported this raises a ValueError. The price
        returned is generated using a simple random walk around a base
        price. This is **not** a substitute for real market data.

        Parameters
        ----------
        symbol: str
            The trading symbol to fetch data for.

        Returns
        -------
        MarketTick
            A dataclass with the current price and timestamp.
        """
        if symbol not in self.SUPPORTED_SYMBOLS:
            raise ValueError(f"Unsupported symbol: {symbol}")
        # Generate a random price around the base price
        base = self._base_prices[symbol]
        change_pct = self._rng.uniform(-0.005, 0.005)  # ±0.5%
        new_price = base * (1 + change_pct)
        # Update the base price slightly for the next call
        self._base_prices[symbol] = new_price
        return MarketTick(symbol=symbol, price=round(new_price, 2), timestamp=time.time())

    def place_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """Simulate placing an order on Binance.

        This method simply returns a fake execution report indicating that
        the order was immediately filled at the current market price. A
        real client would submit a REST POST request and handle the
        exchange's response. The side argument should be either 'BUY' or
        'SELL'.

        Parameters
        ----------
        symbol: str
            Trading symbol, e.g. 'BTCUSDC'. Must be supported.
        side: str
            Either 'BUY' or 'SELL'.
        quantity: float
            Quantity to trade. Must be positive.

        Returns
        -------
        Dict[str, Any]
            A simulated execution report with keys: 'symbol', 'side',
            'quantity', 'price', 'status', 'timestamp'.
        """
        if symbol not in self.SUPPORTED_SYMBOLS:
            raise ValueError(f"Unsupported symbol: {symbol}")
        if side not in {"BUY", "SELL"}:
            raise ValueError(f"Invalid side: {side}")
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive: {quantity}")
        tick = self.get_market_data(symbol)
        # In a real client you may need to round to allowed step sizes.
        execution_report = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": tick.price,
            "status": "FILLED",
            "timestamp": tick.timestamp,
        }
        return execution_report

    def get_account_info(self) -> Dict[str, Any]:
        """Return a dummy account snapshot.

        In a real implementation this would call the Binance API to
        retrieve current balances and positions. Here we return a fixed
        snapshot with static balances for demonstration purposes.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing account balances keyed by asset.
        """
        # Provide a simple fixed snapshot of balances
        return {
            "balances": {
                "USDC": 100000.0,
                "BTC": 0.0,
                "ETH": 0.0,
                "BNB": 0.0,
                "AVAX": 0.0,
                "DOT": 0.0,
            },
            "timestamp": time.time(),
        }