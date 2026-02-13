#!/usr/bin/env python3
"""
🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill
S-DNA: AOI-2026-0213-SDNA-OMEGA

Nexus Oracle Ω — Bayesian Fusion Engine
9 independent agent signals → 1 unified verdict.

Architecture:
  Input Layer  → 3 collectors (Eye, Sound, Blade)
  Fusion Layer → 1 aggregator (Brain) — Bayesian log-odds
  Oversight    → Oracle veto + Med circuit breaker

Copyright (c) 2026 Aoineco & Co. All rights reserved.
STEALTH CLASSIFICATION: Internal use only.
"""

import math
import time
import json
import hashlib
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Literal
from datetime import datetime, timezone, timedelta

# ─── S-DNA Metadata ─────────────────────────────────────
__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-OMEGA",
    "author_agent": "aoineco-collective",
    "org": "aoineco-co",
    "created": "2026-02-13T11:45:00+09:00",
    "tier": "premium",
    "nexus_compatible": True,
    "classification": "stealth",
}

KST = timezone(timedelta(hours=9))


# ═══════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════

@dataclass
class AgentSignal:
    """A single agent's analysis signal."""
    agent_id: str
    agent_name: str
    direction: Literal["LONG", "SHORT", "NEUTRAL"]
    confidence: float          # 0.0 ~ 1.0
    weight: float              # Agent's influence in fusion (0.0 ~ 1.0)
    data_sources: List[str]    # What data this signal is based on
    reasoning: str             # Brief explanation
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(KST).isoformat()
        # Clamp confidence
        self.confidence = max(0.0, min(1.0, self.confidence))
        self.weight = max(0.0, min(1.0, self.weight))


@dataclass
class OmegaVerdict:
    """The unified output of the Omega Fusion Engine."""
    direction: Literal["LONG", "SHORT", "HOLD"]
    confidence: float
    omega_odds: float
    signals_used: int
    signals_rejected: int
    veto_applied: bool
    veto_reason: Optional[str]
    circuit_breaker: bool
    risk_score: float              # 0~100
    position_size_kelly: float     # Kelly Criterion suggested size
    signal_breakdown: List[Dict]
    timestamp: str = ""
    engine_version: str = "omega-v1.0"
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(KST).isoformat()


@dataclass 
class RiskState:
    """Tracks cumulative risk for circuit breaker."""
    daily_pnl_percent: float = 0.0
    max_drawdown_limit: float = 3.0   # 3% daily max
    consecutive_losses: int = 0
    max_consecutive: int = 5
    total_trades_today: int = 0
    
    @property
    def is_breaker_triggered(self) -> bool:
        return (
            self.daily_pnl_percent <= -self.max_drawdown_limit or
            self.consecutive_losses >= self.max_consecutive
        )


# ═══════════════════════════════════════════════════════════
# AGENT ROLE DEFINITIONS
# ═══════════════════════════════════════════════════════════

AGENT_ROSTER = {
    # ─── INPUT LAYER ──────────────────────────────────
    "blue_eye": {
        "name": "👁️ 청안 (Blue-Eye)",
        "role": "Market Data Harvester",
        "weight": 0.25,
        "sources": ["binance_ohlcv", "pyth_oracle", "onchain_whale_tx"],
    },
    "blue_sound": {
        "name": "📢 청음 (Blue_Sound)",
        "role": "Sentiment Scanner",
        "weight": 0.15,
        "sources": ["fear_greed_index", "social_mentions", "funding_rate"],
    },
    "blue_blade": {
        "name": "⚔️ 청검 (Blue-Blade)",
        "role": "Security & Anomaly Detector",
        "weight": 0.15,
        "sources": ["exchange_withdrawals", "smart_contract_exploits", "rug_patterns"],
    },
    
    # ─── FUSION LAYER ─────────────────────────────────
    "blue_brain": {
        "name": "🧠 청뇌 (Blue-Brain)",
        "role": "Bayesian Fusion Commander",
        "weight": 1.0,  # Brain doesn't contribute signal; it fuses them
        "sources": ["all_agent_signals"],
    },
    
    # ─── OUTPUT LAYER ─────────────────────────────────
    "blue_flash": {
        "name": "⚡ 청섬 (Blue-Flash)",
        "role": "Rapid Executor",
        "weight": 0.10,
        "sources": ["order_book_depth", "slippage_estimate"],
    },
    "blue_record": {
        "name": "🗂️ 청비 (Blue-Record)",
        "role": "Historian & Archivist",
        "weight": 0.0,   # Record doesn't influence verdict
        "sources": ["historical_verdicts", "pnl_archive"],
    },
    
    # ─── OVERSIGHT LAYER ──────────────────────────────
    "oracle": {
        "name": "🧿 청령 (Oracle)",
        "role": "Quality Assurance & Veto Gate",
        "weight": 0.10,
        "sources": ["macro_regime", "correlation_analysis"],
    },
    "blue_gear": {
        "name": "⚙️ 청기 (Blue-Gear)",
        "role": "Infrastructure Monitor",
        "weight": 0.0,   # Gear monitors infra, not market
        "sources": ["api_health", "latency_metrics"],
    },
    "blue_med": {
        "name": "💊 청약 (Blue-Med)",
        "role": "Risk Hedge & Circuit Breaker",
        "weight": 0.10,
        "sources": ["volatility_index", "max_drawdown_sim"],
    },
}

# Only these agents contribute directional signals to fusion
SIGNAL_AGENTS = ["blue_eye", "blue_sound", "blue_blade", "blue_flash", "oracle", "blue_med"]


# ═══════════════════════════════════════════════════════════
# OMEGA FUSION ENGINE (THE CORE)
# ═══════════════════════════════════════════════════════════

class OmegaFusionEngine:
    """
    Bayesian Log-Odds Fusion Engine.
    
    Mathematical Foundation:
    ─────────────────────────
    Prior odds: O(H) = P(H) / P(¬H) = 1.0 (neutral 50:50)
    
    For each agent signal:
      Likelihood Ratio (LR) = confidence / (1 - confidence)
      If SHORT: LR = 1 / LR  (invert for bearish)
      Weighted LR = LR ^ weight
    
    Posterior odds = Prior × Π(Weighted LR for each agent)
    Final probability = Posterior / (1 + Posterior)
    
    This ensures:
    - Independent signals are properly combined
    - High-confidence signals have more impact
    - Agent weights control influence proportionally
    - Result is a calibrated probability
    """
    
    VERSION = "omega-v1.0"
    
    # ─── Governance Thresholds ────────────────────────
    ORACLE_VETO_THRESHOLD = 0.55    # Below this → force HOLD
    MIN_SIGNALS_REQUIRED = 2        # Need at least 2 signals
    MIN_CONFIDENCE_INPUT = 0.50     # Ignore signals below 50%
    KELLY_FRACTION = 0.25           # Quarter-Kelly for safety
    
    def __init__(self, risk_state: Optional[RiskState] = None):
        self.risk_state = risk_state or RiskState()
        self.signals: List[AgentSignal] = []
        self.rejected: List[Dict] = []
    
    def ingest_signal(self, signal: AgentSignal) -> bool:
        """
        Ingest a signal from an agent.
        Returns True if accepted, False if rejected.
        """
        # Validate: agent must be in signal roster
        if signal.agent_id not in SIGNAL_AGENTS:
            self.rejected.append({
                "agent": signal.agent_id,
                "reason": "Not a signal-contributing agent",
            })
            return False
        
        # Validate: confidence must meet minimum
        if signal.confidence < self.MIN_CONFIDENCE_INPUT:
            self.rejected.append({
                "agent": signal.agent_id,
                "reason": f"Confidence {signal.confidence:.2f} < {self.MIN_CONFIDENCE_INPUT}",
            })
            return False
        
        # Validate: direction must be actionable
        if signal.direction == "NEUTRAL":
            self.rejected.append({
                "agent": signal.agent_id,
                "reason": "Neutral signals don't contribute to fusion",
            })
            return False
        
        self.signals.append(signal)
        return True
    
    def fuse(self) -> OmegaVerdict:
        """
        Execute Bayesian fusion across all ingested signals.
        This is the heart of Nexus Oracle Ω.
        """
        # ─── Pre-check: Circuit Breaker ───────────────
        if self.risk_state.is_breaker_triggered:
            return OmegaVerdict(
                direction="HOLD",
                confidence=0.0,
                omega_odds=1.0,
                signals_used=0,
                signals_rejected=len(self.rejected),
                veto_applied=False,
                veto_reason=None,
                circuit_breaker=True,
                risk_score=100.0,
                position_size_kelly=0.0,
                signal_breakdown=[],
            )
        
        # ─── Pre-check: Minimum signals ───────────────
        if len(self.signals) < self.MIN_SIGNALS_REQUIRED:
            return OmegaVerdict(
                direction="HOLD",
                confidence=0.0,
                omega_odds=1.0,
                signals_used=len(self.signals),
                signals_rejected=len(self.rejected),
                veto_applied=False,
                veto_reason=f"Insufficient signals: {len(self.signals)} < {self.MIN_SIGNALS_REQUIRED}",
                circuit_breaker=False,
                risk_score=50.0,
                position_size_kelly=0.0,
                signal_breakdown=[],
            )
        
        # ─── Bayesian Log-Odds Fusion ─────────────────
        log_odds = 0.0  # ln(prior odds) = ln(1) = 0
        breakdown = []
        
        for sig in self.signals:
            # Convert confidence to likelihood ratio
            # Clamp to avoid division by zero
            conf = max(0.501, min(0.999, sig.confidence))
            lr = conf / (1.0 - conf)
            
            # Invert for SHORT signals
            if sig.direction == "SHORT":
                lr = 1.0 / lr
            
            # Apply agent weight via log-space
            # weighted_log_lr = weight * ln(lr)
            weighted_log_lr = sig.weight * math.log(lr)
            log_odds += weighted_log_lr
            
            breakdown.append({
                "agent": sig.agent_name,
                "agent_id": sig.agent_id,
                "direction": sig.direction,
                "confidence": round(sig.confidence, 4),
                "weight": sig.weight,
                "likelihood_ratio": round(lr, 4),
                "weighted_log_lr": round(weighted_log_lr, 4),
                "reasoning": sig.reasoning,
            })
        
        # Convert log-odds back to probability
        # P = exp(log_odds) / (1 + exp(log_odds))
        # Use sigmoid for numerical stability
        omega_prob = self._sigmoid(log_odds)
        omega_odds = math.exp(log_odds) if abs(log_odds) < 500 else float('inf')
        
        # ─── Determine Direction ──────────────────────
        if omega_prob > 0.5:
            raw_direction = "LONG"
            raw_confidence = omega_prob
        elif omega_prob < 0.5:
            raw_direction = "SHORT"
            raw_confidence = 1.0 - omega_prob
        else:
            raw_direction = "HOLD"
            raw_confidence = 0.5
        
        # ─── Oracle Veto Gate ─────────────────────────
        veto_applied = False
        veto_reason = None
        final_direction = raw_direction
        
        if raw_confidence < self.ORACLE_VETO_THRESHOLD:
            veto_applied = True
            veto_reason = (
                f"Oracle veto: confidence {raw_confidence:.4f} "
                f"< threshold {self.ORACLE_VETO_THRESHOLD}"
            )
            final_direction = "HOLD"
        
        # ─── Risk Score ───────────────────────────────
        # Higher risk when: low confidence, high volatility signals,
        # conflicting directions
        direction_set = set(s.direction for s in self.signals)
        conflict_penalty = 20.0 if len(direction_set) > 1 else 0.0
        confidence_risk = (1.0 - raw_confidence) * 60.0
        drawdown_risk = min(abs(self.risk_state.daily_pnl_percent) * 10, 20.0)
        risk_score = min(100.0, confidence_risk + conflict_penalty + drawdown_risk)
        
        # ─── Kelly Criterion Position Sizing ──────────
        # f* = (bp - q) / b
        # where b = odds, p = win prob, q = 1 - p
        # We use quarter-Kelly for safety
        if final_direction != "HOLD" and raw_confidence > 0.5:
            edge = raw_confidence - 0.5
            kelly_full = edge / 0.5  # Simplified for even-odds
            kelly_safe = kelly_full * self.KELLY_FRACTION
            position_size = max(0.0, min(0.25, kelly_safe))  # Cap at 25%
        else:
            position_size = 0.0
        
        return OmegaVerdict(
            direction=final_direction,
            confidence=round(raw_confidence, 4),
            omega_odds=round(omega_odds, 4),
            signals_used=len(self.signals),
            signals_rejected=len(self.rejected),
            veto_applied=veto_applied,
            veto_reason=veto_reason,
            circuit_breaker=False,
            risk_score=round(risk_score, 2),
            position_size_kelly=round(position_size, 4),
            signal_breakdown=breakdown,
        )
    
    @staticmethod
    def _sigmoid(x: float) -> float:
        """Numerically stable sigmoid function."""
        if x >= 0:
            z = math.exp(-x)
            return 1.0 / (1.0 + z)
        else:
            z = math.exp(x)
            return z / (1.0 + z)
    
    def reset(self):
        """Reset engine for next cycle."""
        self.signals = []
        self.rejected = []


# ═══════════════════════════════════════════════════════════
# SETTLEMENT & ARCHIVAL
# ═══════════════════════════════════════════════════════════

class OmegaSettlement:
    """Post-verdict settlement: PnL tracking and risk state updates."""
    
    def __init__(self, risk_state: RiskState):
        self.risk_state = risk_state
    
    def settle(self, verdict: OmegaVerdict, actual_outcome: Literal["LONG", "SHORT"],
               pnl_percent: float) -> Dict:
        """
        Settle a completed trade cycle.
        Updates risk state for circuit breaker logic.
        """
        was_correct = (verdict.direction == actual_outcome)
        
        # Update risk state
        self.risk_state.daily_pnl_percent += pnl_percent
        self.risk_state.total_trades_today += 1
        
        if was_correct:
            self.risk_state.consecutive_losses = 0
        else:
            self.risk_state.consecutive_losses += 1
        
        return {
            "verdict_direction": verdict.direction,
            "actual_outcome": actual_outcome,
            "correct": was_correct,
            "pnl_percent": round(pnl_percent, 4),
            "cumulative_pnl": round(self.risk_state.daily_pnl_percent, 4),
            "consecutive_losses": self.risk_state.consecutive_losses,
            "circuit_breaker_active": self.risk_state.is_breaker_triggered,
            "trades_today": self.risk_state.total_trades_today,
            "timestamp": datetime.now(KST).isoformat(),
        }


# ═══════════════════════════════════════════════════════════
# SaaS API INTERFACE
# ═══════════════════════════════════════════════════════════

class NexusOracleAPI:
    """
    Public-facing SaaS API for Nexus Oracle Ω.
    Customers call this; internal 9-agent engine runs behind it.
    """
    
    PRICING = {
        "omega_full": 0.50,      # Full analysis with breakdown
        "omega_signal": 0.10,    # Direction + confidence only
        "omega_free": 0.00,      # Demo: direction only, no breakdown
    }
    
    def __init__(self):
        self.risk_state = RiskState()
        self.engine = OmegaFusionEngine(self.risk_state)
        self.settlement = OmegaSettlement(self.risk_state)
        self.call_count = 0
    
    def analyze(self, ticker: str, signals: List[AgentSignal],
                tier: str = "omega_full") -> Dict:
        """
        Main API endpoint.
        In production: signals are generated internally by our 9 agents.
        For testing: signals can be injected externally.
        """
        self.call_count += 1
        self.engine.reset()
        
        # Ingest all signals
        for sig in signals:
            self.engine.ingest_signal(sig)
        
        # Execute fusion
        verdict = self.engine.fuse()
        
        # Format response based on tier
        if tier == "omega_free":
            return {
                "ticker": ticker,
                "direction": verdict.direction,
                "engine": "nexus-oracle-omega",
                "note": "Upgrade to omega_full for confidence scores and breakdown",
            }
        elif tier == "omega_signal":
            return {
                "ticker": ticker,
                "direction": verdict.direction,
                "confidence": verdict.confidence,
                "risk_score": verdict.risk_score,
                "engine": "nexus-oracle-omega",
            }
        else:  # omega_full
            return {
                "ticker": ticker,
                "direction": verdict.direction,
                "confidence": verdict.confidence,
                "omega_odds": verdict.omega_odds,
                "risk_score": verdict.risk_score,
                "position_size_kelly": verdict.position_size_kelly,
                "signals_used": verdict.signals_used,
                "signals_rejected": verdict.signals_rejected,
                "veto_applied": verdict.veto_applied,
                "veto_reason": verdict.veto_reason,
                "circuit_breaker": verdict.circuit_breaker,
                "signal_breakdown": verdict.signal_breakdown,
                "engine": "nexus-oracle-omega",
                "version": verdict.engine_version,
                "timestamp": verdict.timestamp,
            }
    
    def get_stats(self) -> Dict:
        """API usage statistics."""
        return {
            "total_calls": self.call_count,
            "daily_pnl": self.risk_state.daily_pnl_percent,
            "trades_today": self.risk_state.total_trades_today,
            "circuit_breaker_active": self.risk_state.is_breaker_triggered,
        }


# ═══════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ═══════════════════════════════════════════════════════════

def demo():
    """Run a demonstration of the Omega Fusion Engine."""
    print("=" * 60)
    print("🧿 NEXUS ORACLE Ω — Bayesian Fusion Demo")
    print("   9 Minds. 1 Verdict. Zero Blind Spots.")
    print("=" * 60)
    
    api = NexusOracleAPI()
    
    # Simulate 6 agent signals
    signals = [
        AgentSignal(
            agent_id="blue_eye",
            agent_name="👁️ 청안 (Blue-Eye)",
            direction="LONG",
            confidence=0.72,
            weight=0.25,
            data_sources=["binance_5m_ohlcv", "pyth_btc_oracle"],
            reasoning="BTC breaking above 20-period MA on 5m. Volume increasing.",
        ),
        AgentSignal(
            agent_id="blue_sound",
            agent_name="📢 청음 (Blue_Sound)",
            direction="LONG",
            confidence=0.61,
            weight=0.15,
            data_sources=["fear_greed_index", "x_sentiment"],
            reasoning="Fear & Greed at 62 (Greed). Social mentions trending up.",
        ),
        AgentSignal(
            agent_id="blue_blade",
            agent_name="⚔️ 청검 (Blue-Blade)",
            direction="SHORT",
            confidence=0.68,
            weight=0.15,
            data_sources=["exchange_net_flow", "whale_alert"],
            reasoning="Large exchange inflows detected. Possible sell pressure.",
        ),
        AgentSignal(
            agent_id="blue_flash",
            agent_name="⚡ 청섬 (Blue-Flash)",
            direction="LONG",
            confidence=0.58,
            weight=0.10,
            data_sources=["order_book_depth"],
            reasoning="Bid wall at $65,800 looks solid. Low slippage for entry.",
        ),
        AgentSignal(
            agent_id="oracle",
            agent_name="🧿 청령 (Oracle)",
            direction="LONG",
            confidence=0.65,
            weight=0.10,
            data_sources=["macro_regime", "btc_dominance"],
            reasoning="Macro regime: Risk-On. BTC dominance stable.",
        ),
        AgentSignal(
            agent_id="blue_med",
            agent_name="💊 청약 (Blue-Med)",
            direction="LONG",
            confidence=0.55,
            weight=0.10,
            data_sources=["volatility_30d", "max_drawdown_sim"],
            reasoning="30d volatility moderate. Drawdown sim shows 1.8% max risk.",
        ),
    ]
    
    # Execute analysis
    result = api.analyze("BTC-USD", signals, tier="omega_full")
    
    # Display results
    print(f"\n📊 Ticker: {result['ticker']}")
    print(f"🎯 Direction: {result['direction']}")
    print(f"📈 Confidence: {result['confidence']:.2%}")
    print(f"⚖️  Omega Odds: {result['omega_odds']}")
    print(f"🎲 Risk Score: {result['risk_score']}/100")
    print(f"💰 Position Size (Kelly): {result['position_size_kelly']:.2%}")
    print(f"🛡️  Veto Applied: {result['veto_applied']}")
    if result['veto_reason']:
        print(f"   Reason: {result['veto_reason']}")
    print(f"🔌 Circuit Breaker: {result['circuit_breaker']}")
    print(f"\n📡 Signals Used: {result['signals_used']} | Rejected: {result['signals_rejected']}")
    
    print("\n─── Signal Breakdown ───")
    for sig in result.get('signal_breakdown', []):
        arrow = "🟢" if sig['direction'] == "LONG" else "🔴"
        print(f"  {arrow} {sig['agent']}: {sig['direction']} "
              f"(conf: {sig['confidence']:.0%}, weight: {sig['weight']}, "
              f"LR: {sig['likelihood_ratio']:.3f})")
        print(f"     └─ {sig['reasoning']}")
    
    print(f"\n⏰ Timestamp: {result['timestamp']}")
    print(f"🔧 Engine: {result['engine']} {result['version']}")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    demo()
