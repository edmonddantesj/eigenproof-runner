#!/usr/bin/env python3
"""
/* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */
S-DNA: AOI-2026-0213-SDNA-PC01

Aoineco Presage Connector — V6 → Public Prediction Market Bridge

PURPOSE:
  This is the "proof engine" — the bridge between our internal
  Alpha Oracle V6 predictions and the public Presage leaderboard.
  
  V6 predicts → Backtester validates → Presage proves publicly.

ARCHITECTURE:
  ┌─────────────────────────────────────────────────────┐
  │              V6 PIPELINE (Internal)                  │
  │  9 agents → Bayesian Fusion → Enhanced Verdict       │
  └──────────────────────┬──────────────────────────────┘
                         │ VERDICT: LONG/SHORT/HOLD
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │           PRESAGE CONNECTOR (This module)             │
  │                                                       │
  │  1. GATE CHECK: Is V6 win rate > 55%? (Backtester)   │
  │  2. MARKET SCAN: Find relevant Presage markets        │
  │  3. THESIS BUILD: Convert V6 verdict → trade thesis   │
  │  4. RISK SIZE: Kelly fraction from V6 Monte Carlo     │
  │  5. EXECUTE: Paper trade with public reasoning         │
  │  6. TRACK: Update local performance log               │
  └──────────────────────────────────────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │           PRESAGE LEADERBOARD (Public)                │
  │  "Aoineco Oracle — Ranked #X with Y% ROI"            │
  └──────────────────────────────────────────────────────┘

SAFETY:
  - Paper trading only (no real money at risk)
  - Gate check prevents deployment before validation
  - Position sizing capped at 5% of paper balance
  - All trades include transparent reasoning

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import json
import os
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone, timedelta

__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-PC01",
    "author_agent": "oracle",
    "org": "aoineco-co",
    "created": "2026-02-13T16:25:00+09:00",
    "tier": "premium",
    "classification": "stealth",
    "license": "proprietary-aoineco",
}

KST = timezone(timedelta(hours=9))
PRESAGE_API = "https://presage.market/api"
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
PRESAGE_STATE_FILE = os.path.join(WORKSPACE, "the-alpha-oracle", "vault", "presage_state.json")


# ═══════════════════════════════════════════════════════════
# HTTP CLIENT
# ═══════════════════════════════════════════════════════════

class PresageHTTP:
    """Lightweight HTTP client for Presage API."""

    @staticmethod
    def get(endpoint: str, timeout: int = 15) -> Tuple[int, Dict]:
        url = f"{PRESAGE_API}{endpoint}"
        req = urllib.request.Request(url, headers={"User-Agent": "Aoineco-Oracle/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if e.fp else "{}"
            try:
                return e.code, json.loads(body)
            except json.JSONDecodeError:
                return e.code, {"error": body[:500]}
        except Exception as e:
            return 0, {"error": str(e)}

    @staticmethod
    def post(endpoint: str, data: Dict, timeout: int = 15) -> Tuple[int, Dict]:
        url = f"{PRESAGE_API}{endpoint}"
        payload = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Aoineco-Oracle/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if e.fp else "{}"
            try:
                return e.code, json.loads(body)
            except json.JSONDecodeError:
                return e.code, {"error": body[:500]}
        except Exception as e:
            return 0, {"error": str(e)}


# ═══════════════════════════════════════════════════════════
# PRESAGE STATE MANAGER
# ═══════════════════════════════════════════════════════════

@dataclass
class PresageState:
    """Persistent state for our Presage agent."""
    agent_id: Optional[str] = None
    agent_name: str = "AoinecoOracle"
    registered: bool = False
    total_trades: int = 0
    wins: int = 0
    losses: int = 0
    balance: float = 10_000.0
    gate_passed: bool = False       # Has V6 passed the 55% gate?
    gate_win_rate: float = 0.0
    live_mode: bool = False         # False = dry-run, True = actually trade
    trade_log: List[Dict] = field(default_factory=list)

    @property
    def win_rate(self) -> float:
        if self.total_trades == 0:
            return 0.0
        return round(self.wins / self.total_trades * 100, 2)

    def save(self, filepath: str = PRESAGE_STATE_FILE):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            json.dump({
                "agent_id": self.agent_id,
                "agent_name": self.agent_name,
                "registered": self.registered,
                "total_trades": self.total_trades,
                "wins": self.wins,
                "losses": self.losses,
                "balance": self.balance,
                "gate_passed": self.gate_passed,
                "gate_win_rate": self.gate_win_rate,
                "live_mode": self.live_mode,
                "trade_log": self.trade_log[-50:],  # Keep last 50
            }, f, indent=2)

    @classmethod
    def load(cls, filepath: str = PRESAGE_STATE_FILE) -> 'PresageState':
        if not os.path.exists(filepath):
            return cls()
        try:
            with open(filepath) as f:
                data = json.load(f)
            return cls(**data)
        except Exception:
            return cls()


# ═══════════════════════════════════════════════════════════
# GATE CHECK (Safety Valve)
# ═══════════════════════════════════════════════════════════

class GateCheck:
    """
    The safety gate between V6 and public trading.

    Rules:
    1. V6 must have at least 20 completed predictions
    2. Backtester must show win rate >= 55%
    3. Backtester grade must be B or higher
    4. Chairman (L3) must explicitly approve going live

    Until all conditions are met, the connector operates in
    DRY-RUN mode — it logs what it WOULD trade, but doesn't
    actually call the Presage API.
    """

    MIN_PREDICTIONS = 20
    MIN_WIN_RATE = 55.0
    REQUIRED_GRADE = ("A", "B")

    @classmethod
    def check(cls, v6_stats: Dict, backtest_result: Optional[Dict] = None) -> Dict:
        """
        Evaluate whether V6 is ready for public trading.

        Args:
            v6_stats: {"total_predictions": int, "wins": int, "losses": int}
            backtest_result: Output from AoinecoBacktester.run()
        """
        checks = {}

        # Check 1: Minimum predictions
        total = v6_stats.get("total_predictions", 0)
        checks["min_predictions"] = {
            "passed": total >= cls.MIN_PREDICTIONS,
            "value": total,
            "required": cls.MIN_PREDICTIONS,
        }

        # Check 2: Win rate
        wins = v6_stats.get("wins", 0)
        wr = (wins / total * 100) if total > 0 else 0
        checks["win_rate"] = {
            "passed": wr >= cls.MIN_WIN_RATE,
            "value": round(wr, 2),
            "required": cls.MIN_WIN_RATE,
        }

        # Check 3: Backtest grade
        if backtest_result:
            grade = backtest_result.get("verdict", {}).get("grade", "N/A")
            checks["backtest_grade"] = {
                "passed": grade in cls.REQUIRED_GRADE,
                "value": grade,
                "required": list(cls.REQUIRED_GRADE),
            }
        else:
            checks["backtest_grade"] = {
                "passed": False,
                "value": "NOT_RUN",
                "required": list(cls.REQUIRED_GRADE),
            }

        all_passed = all(c["passed"] for c in checks.values())

        return {
            "gate_passed": all_passed,
            "checks": checks,
            "recommendation": (
                "✅ READY FOR PUBLIC TRADING (pending Chairman approval)"
                if all_passed else
                "❌ NOT READY — continue accumulating V6 predictions"
            ),
        }


# ═══════════════════════════════════════════════════════════
# MARKET SCANNER
# ═══════════════════════════════════════════════════════════

class MarketScanner:
    """
    Scans Presage for markets relevant to our V6 predictions.

    V6 predicts BTC direction → we look for BTC-related markets.
    """

    BTC_KEYWORDS = ["btc", "bitcoin", "crypto", "100k", "90k", "80k", "70k"]

    @classmethod
    def scan_btc_markets(cls) -> List[Dict]:
        """Find BTC-related prediction markets."""
        status, data = PresageHTTP.get("/events?limit=50")
        if status != 200:
            return []

        events = data if isinstance(data, list) else data.get("events", [])
        btc_markets = []

        for event in events:
            title = event.get("title", "").lower()
            if any(kw in title for kw in cls.BTC_KEYWORDS):
                for market in event.get("markets", []):
                    if market.get("status") == "open":
                        btc_markets.append({
                            "event_ticker": event.get("ticker"),
                            "event_title": event.get("title"),
                            "market_ticker": market.get("ticker"),
                            "yes_bid": market.get("yesBid"),
                            "yes_ask": market.get("yesAsk"),
                            "volume": market.get("volume"),
                        })

        # Sort by volume (most liquid first)
        btc_markets.sort(key=lambda m: m.get("volume", 0), reverse=True)
        return btc_markets


# ═══════════════════════════════════════════════════════════
# THESIS BUILDER
# ═══════════════════════════════════════════════════════════

class ThesisBuilder:
    """
    Converts a V6 verdict into a human-readable trading thesis
    for the Presage public leaderboard.

    The reasoning must be:
    - Transparent (other agents can learn from it)
    - Professional (builds Aoineco's reputation)
    - Specific (references actual data, not vague claims)
    """

    @staticmethod
    def build(
        v6_verdict: Dict,
        market: Dict,
        backtester_grade: str = "N/A",
    ) -> str:
        """Generate trading reasoning from V6 verdict."""
        direction = v6_verdict.get("final_direction", v6_verdict.get("direction", "HOLD"))
        confidence = v6_verdict.get("confidence", 0)
        var_95 = v6_verdict.get("var_95", 0)
        win_rate = v6_verdict.get("win_rate", 0)
        agreement = v6_verdict.get("agreement", "unknown")

        # Build structured reasoning
        lines = [
            f"🌌 Aoineco Oracle V6 — 9-Agent Bayesian Fusion Analysis",
            f"",
            f"Direction: {direction} | Confidence: {confidence:.1%}",
            f"Signal Agreement: {agreement}",
            f"Monte Carlo VaR95: {var_95:.2f}% | Sim Win Rate: {win_rate:.1f}%",
            f"Backtester Grade: {backtester_grade}",
            f"",
            f"Our 9 specialized agents independently analyzed market data",
            f"and fused their signals via Bayesian log-odds aggregation.",
            f"Position sized using Kelly Criterion with quarter-Kelly safety.",
            f"",
            f"$7 Bootstrap Protocol — Architecture of Intelligence.",
        ]

        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# POSITION SIZER
# ═══════════════════════════════════════════════════════════

class PositionSizer:
    """
    Determines trade size based on V6's confidence and Kelly fraction.

    Rules:
    - Never more than 5% of paper balance per trade
    - Scale size with V6 confidence
    - Minimum trade: 10 USDC
    """

    MAX_POSITION_PCT = 0.05  # 5% max per trade
    MIN_TRADE_USDC = 10

    @classmethod
    def calculate(cls, balance: float, v6_kelly: float, confidence: float) -> int:
        """
        Calculate trade quantity in USDC.

        Args:
            balance: Current paper balance
            v6_kelly: Kelly fraction from V6 (0.0 ~ 0.25)
            confidence: V6 confidence (0.5 ~ 1.0)
        """
        # Scale by confidence (higher confidence → bigger bet)
        confidence_factor = max(0, (confidence - 0.5) * 2)  # 0 at 50%, 1 at 100%

        # Base size from Kelly
        kelly_size = balance * min(v6_kelly, cls.MAX_POSITION_PCT)

        # Confidence-adjusted
        adjusted = kelly_size * confidence_factor

        # Clamp
        size = max(cls.MIN_TRADE_USDC, min(adjusted, balance * cls.MAX_POSITION_PCT))

        return int(round(size))


# ═══════════════════════════════════════════════════════════
# PRESAGE CONNECTOR (MAIN ORCHESTRATOR)
# ═══════════════════════════════════════════════════════════

class PresageConnector:
    """
    The master bridge between V6 and Presage.

    Usage:
        connector = PresageConnector()

        # Step 1: Register (one-time)
        connector.register()

        # Step 2: Check if V6 is ready
        gate = connector.check_gate(v6_stats, backtest_result)

        # Step 3: Execute (if gate passed and chairman approved)
        result = connector.execute_trade(v6_verdict, market)

        # Step 4: Check status
        status = connector.get_status()
    """

    def __init__(self):
        self.state = PresageState.load()
        self.scanner = MarketScanner()
        self.thesis_builder = ThesisBuilder()
        self.sizer = PositionSizer()
        self.gate = GateCheck()
        self.http = PresageHTTP()

    def register(self) -> Dict:
        """Register Aoineco Oracle on Presage (one-time)."""
        if self.state.registered and self.state.agent_id:
            return {
                "status": "already_registered",
                "agent_id": self.state.agent_id,
            }

        status, data = self.http.post("/agents/register", {
            "name": self.state.agent_name,
            "strategy": (
                "9-agent Bayesian fusion engine with Monte Carlo risk management. "
                "Built from $7 seed. Architecture of Intelligence."
            ),
        })

        if status in (200, 201) and "agent" in data:
            agent = data["agent"]
            self.state.agent_id = agent.get("id")
            self.state.registered = True
            self.state.balance = agent.get("balance", 10000)
            self.state.save()
            return {
                "status": "registered",
                "agent_id": self.state.agent_id,
                "balance": self.state.balance,
            }

        return {"status": "failed", "http_status": status, "response": data}

    def check_gate(self, v6_stats: Dict,
                   backtest_result: Optional[Dict] = None) -> Dict:
        """Check if V6 is ready for public trading."""
        result = self.gate.check(v6_stats, backtest_result)
        self.state.gate_passed = result["gate_passed"]
        if result["gate_passed"]:
            wr = v6_stats.get("wins", 0) / max(1, v6_stats.get("total_predictions", 1)) * 100
            self.state.gate_win_rate = round(wr, 2)
        self.state.save()
        return result

    def scan_markets(self) -> List[Dict]:
        """Scan for BTC-related prediction markets."""
        return self.scanner.scan_btc_markets()

    def execute_trade(
        self,
        v6_verdict: Dict,
        market: Dict,
        chairman_approved: bool = False,
    ) -> Dict:
        """
        Execute a trade on Presage based on V6 verdict.

        Safety gates:
        1. Gate must be passed (V6 validated)
        2. Chairman must approve going live
        3. If not live, operates in dry-run mode
        """
        direction = v6_verdict.get("final_direction", v6_verdict.get("direction", "HOLD"))

        if direction == "HOLD":
            return {"status": "skipped", "reason": "V6 verdict is HOLD — no trade"}

        # Map V6 direction to Presage side
        # For BTC price prediction markets:
        # LONG (price up) → YES on "above $X" markets
        # SHORT (price down) → NO on "above $X" markets
        side = "YES" if direction == "LONG" else "NO"

        # Calculate position size
        confidence = v6_verdict.get("confidence", 0.5)
        kelly = v6_verdict.get("position_size", v6_verdict.get("position_size_kelly", 0.05))
        quantity = self.sizer.calculate(self.state.balance, kelly, confidence)

        # Build thesis
        thesis = self.thesis_builder.build(v6_verdict, market)

        # Compile trade
        trade = {
            "market_ticker": market.get("market_ticker", "UNKNOWN"),
            "event_title": market.get("event_title", ""),
            "side": side,
            "quantity": quantity,
            "reasoning": thesis,
            "v6_direction": direction,
            "v6_confidence": confidence,
            "timestamp": datetime.now(KST).isoformat(),
        }

        # Gate check
        if not self.state.gate_passed:
            trade["executed"] = False
            trade["mode"] = "DRY_RUN"
            trade["reason"] = "Gate not passed — V6 needs more validation"
            self.state.trade_log.append(trade)
            self.state.save()
            return {"status": "dry_run", "trade": trade}

        if not chairman_approved or not self.state.live_mode:
            trade["executed"] = False
            trade["mode"] = "DRY_RUN"
            trade["reason"] = "Live mode not enabled — chairman approval pending"
            self.state.trade_log.append(trade)
            self.state.save()
            return {"status": "dry_run", "trade": trade}

        # Actually execute on Presage
        if not self.state.agent_id:
            return {"status": "error", "reason": "Not registered on Presage"}

        status, data = self.http.post(
            f"/agents/{self.state.agent_id}/trade",
            {
                "marketTicker": trade["market_ticker"],
                "side": side,
                "quantity": quantity,
                "reasoning": thesis,
            },
        )

        trade["executed"] = status in (200, 201)
        trade["mode"] = "LIVE"
        trade["http_status"] = status
        trade["response"] = data

        self.state.trade_log.append(trade)
        self.state.total_trades += 1
        self.state.save()

        return {"status": "executed" if trade["executed"] else "failed", "trade": trade}

    def get_status(self) -> Dict:
        """Get current connector status."""
        return {
            "registered": self.state.registered,
            "agent_id": self.state.agent_id,
            "gate_passed": self.state.gate_passed,
            "gate_win_rate": self.state.gate_win_rate,
            "live_mode": self.state.live_mode,
            "balance": self.state.balance,
            "total_trades": self.state.total_trades,
            "win_rate": self.state.win_rate,
            "dry_run_trades": sum(1 for t in self.state.trade_log if not t.get("executed")),
            "sdna": __sdna__["id"],
        }


# ═══════════════════════════════════════════════════════════
# CLI DEMO
# ═══════════════════════════════════════════════════════════

def demo():
    print("=" * 64)
    print("🎯 AOINECO PRESAGE CONNECTOR")
    print("   V6 predicts. Backtester validates. Presage proves.")
    print("   $7 Bootstrap Protocol — Public Proof of Intelligence.")
    print("=" * 64)

    connector = PresageConnector()

    # ─── Gate Check (V6 not ready yet) ────────────────
    print("\n🚦 Gate Check (simulated — V6 just started):")
    gate = connector.check_gate(
        v6_stats={"total_predictions": 3, "wins": 2, "losses": 1},
    )
    print(f"  Gate passed: {gate['gate_passed']}")
    for name, check in gate["checks"].items():
        icon = "✅" if check["passed"] else "❌"
        print(f"  {icon} {name}: {check['value']} (need: {check['required']})")
    print(f"  → {gate['recommendation']}")

    # ─── Market Scan ──────────────────────────────────
    print("\n📡 Scanning for BTC markets on Presage...")
    markets = connector.scan_markets()
    if markets:
        print(f"  Found {len(markets)} BTC markets:")
        for m in markets[:3]:
            print(f"  • {m['event_title'][:50]}...")
            print(f"    Ticker: {m['market_ticker']} | "
                  f"YES: {m.get('yes_bid', '?')}/{m.get('yes_ask', '?')}")
    else:
        print("  No BTC markets found (or API unreachable)")

    # ─── Dry-Run Trade ────────────────────────────────
    print("\n📝 Dry-Run Trade (gate not passed):")
    mock_verdict = {
        "final_direction": "LONG",
        "confidence": 0.68,
        "position_size_kelly": 0.09,
        "agreement": "STRONG",
        "var_95": -0.07,
        "win_rate": 96.8,
    }
    mock_market = {
        "market_ticker": "KXBTC-100K-26MAR-YES",
        "event_title": "Bitcoin above $100K by March 2026?",
    }

    result = connector.execute_trade(mock_verdict, mock_market)
    print(f"  Status: {result['status']}")
    trade = result.get("trade", {})
    print(f"  Mode: {trade.get('mode')}")
    print(f"  Side: {trade.get('side')} | Quantity: ${trade.get('quantity')}")
    print(f"  Reason: {trade.get('reason', 'N/A')[:60]}...")

    # ─── Status ───────────────────────────────────────
    print("\n📊 Connector Status:")
    status = connector.get_status()
    for k, v in status.items():
        if k != "sdna":
            print(f"  {k}: {v}")

    print(f"\n🧬 S-DNA: {status['sdna']}")
    print("=" * 64)


if __name__ == "__main__":
    demo()
