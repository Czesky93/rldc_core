"""Simple FastAPI application for RLdC Core.

This module defines an API server that exposes endpoints for retrieving
market data, viewing current positions and triggering trades. It also
serves static files for the web UI. The server is intended for local
development and demonstration; you may want to add authentication,
error handling and persistence for production use.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from ..backend.core.engine.decision_engine import DecisionEngine
from ..backend.core.execution.execution import ExecutionManager
from ..backend.integrations.binance.client import BinanceClient
from ..backend.integrations.telegram.notifier import TelegramNotifier


app = FastAPI(title="RLdC Core API")

# Instantiate shared dependencies
client = BinanceClient()
executor = ExecutionManager(exchange_client=None)
notifier = TelegramNotifier(token=None, chat_id=None)  # stub: print to console
engine = DecisionEngine(client=client, executor=executor, notifier=notifier)


@app.get("/api/positions")
async def api_get_positions() -> dict:
    """Return a list of current open positions."""
    return {"positions": engine.get_positions()}


@app.post("/api/trade")
async def api_trade() -> dict:
    """Trigger a trade cycle. Returns execution details or a message."""
    order = engine.run_cycle()
    if order is None:
        return {"message": "No trade executed."}
    return {
        "order": {
            "symbol": order.symbol,
            "side": order.side,
            "quantity": order.quantity,
            "price": order.price,
            "status": order.status,
            "order_id": order.order_id,
        }
    }


@app.get("/api/market/{symbol}")
async def api_get_market(symbol: str) -> dict:
    """Return simulated market data for a symbol."""
    try:
        tick = client.get_market_data(symbol)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {
        "symbol": tick.symbol,
        "price": tick.price,
        "timestamp": tick.timestamp,
    }


# Serve the web portal from the `web` directory. The `index.html` will act
# as the single page application entry point.
web_dir = Path(__file__).parent.parent.parent / "web"
if web_dir.exists():
    app.mount(
        "/",
        StaticFiles(directory=str(web_dir), html=True),
        name="web",
    )