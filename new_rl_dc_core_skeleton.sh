#!/usr/bin/env bash
# new_rl_dc_core_skeleton.sh
#
# This script bootstraps a clean project structure for the RLdC trading bot.
# The goal is to separate concerns into modular packages and avoid legacy
# entanglement. It creates a directory tree, populates Python packages with
# placeholder __init__.py files, and writes minimal example modules for
# market scanning, portfolio reconciliation, risk management, and a decision
# engine. A README is generated to describe the repository layout and next
# steps.
#
# Usage:
#   ./new_rl_dc_core_skeleton.sh [target_dir]
#
# If no target directory is provided, it defaults to RLdC_Core.

set -e

TARGET_DIR="${1:-RLdC_Core}"

echo "Creating RLdC core skeleton in $TARGET_DIR..."

# Create the directory structure
mkdir -p "$TARGET_DIR/backend/core/engine" \
         "$TARGET_DIR/backend/core/execution" \
         "$TARGET_DIR/backend/core/reconcile" \
         "$TARGET_DIR/backend/core/risk" \
         "$TARGET_DIR/backend/core/scanner" \
         "$TARGET_DIR/backend/core/portfolio" \
         "$TARGET_DIR/backend/core/runtime" \
         "$TARGET_DIR/backend/integrations/binance" \
         "$TARGET_DIR/backend/integrations/telegram" \
         "$TARGET_DIR/api" \
         "$TARGET_DIR/overlay" \
         "$TARGET_DIR/web" \
         "$TARGET_DIR/tests" \
         "$TARGET_DIR/docs"

# Add __init__.py files to make packages importable
find "$TARGET_DIR" -type d | while read -r d; do
  # Skip .git or other hidden directories
  base="$(basename "$d")"
  if [[ "$base" = ".git" ]]; then
    continue
  fi
  init_file="$d/__init__.py"
  if [[ ! -f "$init_file" ]]; then
    echo "# Auto-generated package" > "$init_file"
  fi
done

# Create market scanner placeholder
cat > "$TARGET_DIR/backend/core/scanner/market_scanner.py" <<'PY'
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

@dataclass
class Candidate:
    symbol: str
    score: float
    confidence: float
    reason: Optional[str] = None

def scan_universe() -> List[Candidate]:
    """Placeholder scanning function."""
    # TODO: implement scanning of market data from Binance
    return []

def score_candidates(candidates: List[Candidate]) -> List[Candidate]:
    """Sort candidates by score descending."""
    return sorted(candidates, key=lambda c: c.score, reverse=True)

def validate_candidate(candidate: Candidate) -> bool:
    """Apply basic filters. Returns True if candidate is tradeable."""
    # TODO: implement min notional, trend checks, confidence threshold, etc.
    return candidate.score > 0

def pick_executable_candidate(candidates: List[Candidate]) -> Optional[Candidate]:
    """Select the first candidate that passes validation."""
    for c in candidates:
        if validate_candidate(c):
            return c
    return None
PY

# Create portfolio reconciliation placeholder
cat > "$TARGET_DIR/backend/core/reconcile/portfolio_reconcile.py" <<'PY'
"""
Portfolio reconciliation module for RLdC_Core.

This module defines functions to reconcile the local database state with Binance as source of truth.
It should detect missing positions, orphaned trades, mismatched quantities, and fix them accordingly.

Functions here are placeholders; integration with the database and Binance API should be implemented.
"""
def reconcile_with_binance(db_session, binance_client):
    """
    Reconcile positions and balances with Binance.

    Parameters:
    - db_session: active database session
    - binance_client: client providing get_account_snapshots and get_trade_history

    Returns:
    - summary dict with lists of created, updated and closed positions.
    """
    # TODO: implement reconciliation logic
    return {
        "created": [],
        "updated": [],
        "closed": [],
        "errors": []
    }
PY

# Create risk module placeholder
cat > "$TARGET_DIR/backend/core/risk/risk.py" <<'PY'
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
PY

# Create decision engine placeholder
cat > "$TARGET_DIR/backend/core/engine/decision_engine.py" <<'PY'
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
PY

# Create runtime settings placeholder
cat > "$TARGET_DIR/backend/core/runtime/__init__.py" <<'PY'
"""
Runtime configuration for RLdC_Core.

This package should expose functions to load and manage runtime settings (e.g. live/demo mode, account selection).
Currently contains placeholder variables.
"""

MODE = "demo"  # or "live"
PY

# Create README.md
cat > "$TARGET_DIR/README.md" <<'MD'
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
MD

echo "RLdC Core skeleton created at $TARGET_DIR."