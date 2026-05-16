# RLdC Core Skeleton

This repository provides a clean starting point for building the RLdC trading bot. It separates concerns into modular components and avoids legacy complexity.

## Structure

- `backend/core/scanner/market_scanner.py`: placeholder for the market scanning pipeline (universe selection, scoring, validation).
- `backend/core/reconcile/portfolio_reconcile.py`: placeholder for portfolio reconciliation logic with Binance.
- `backend/core/risk/risk.py`: defines basic risk parameters and helpers (e.g. min order notional).
- `backend/core/engine/decision_engine.py`: coordinates scanning and risk modules to produce trade decisions.
- `backend/core/runtime/`: runtime settings such as mode (demo/live).
- `backend/integrations/`: location for exchange and messaging integrations (e.g. Binance client, Telegram bot).
- `api/`, `overlay/`, `web/`: placeholders for future API and UI layers.
- `tests/`: place your unit tests here.
- `docs/`: documentation.

## Getting Started

1. **Clone this repository** or copy the skeleton into your project directory.
2. Implement the scanning logic in `market_scanner.py` to fetch real market data.
3. Implement risk checks in `risk.py` and update parameters as needed.
4. Write a Binance client under `backend/integrations/binance` that exposes methods for account snapshots and order execution.
5. Implement reconciliation logic in `portfolio_reconcile.py` to keep your database in sync with Binance.
6. Build the state machine in `decision_engine.py` to handle the full trade lifecycle: signal generation, order submission, monitoring, and exit.
7. Add tests under `tests/` to validate each component.
8. Extend `api/`, `overlay/`, and `web/` as needed for user interfaces.

This skeleton does not include any legacy code, `.env` files, or compiled dependencies. Use it as a foundation to develop a robust and consistent trading bot.
