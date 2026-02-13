#!/usr/bin/env python3
"""
/* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */
S-DNA: AOI-2026-0213-SDNA-V6R

Nexus Oracle Ω — V6 Rebuild Module
Alpha Oracle V6 Enhancement Pack: 3 Core Upgrades

Upgrade 1: Monte Carlo Risk Simulation (Blue-Med Enhancement)
Upgrade 2: Self-Reflection Engine (Post-Settlement Learning)
Upgrade 3: Advanced Technical Indicators (Blue-Eye Enhancement)

All logic independently reimplemented by Aoineco & Co.
No external code copied. Concepts only.

Copyright (c) 2026 Aoineco & Co. All rights reserved.
STEALTH CLASSIFICATION: Internal use only.
"""

import math
import random
import hashlib
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Literal
from datetime import datetime, timezone, timedelta

# ─── S-DNA Metadata ─────────────────────────────────────
__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-V6R",
    "author_agent": "blue_brain",
    "org": "aoineco-co",
    "created": "2026-02-13T13:30:00+09:00",
    "tier": "premium",
    "classification": "stealth",
    "parent": "AOI-2026-0213-SDNA-OMEGA",
    "rebuild_sources": [
        "concept:monte_carlo_risk_sim",
        "concept:bayesian_self_learning",
        "concept:advanced_ta_indicators",
    ],
    "license": "proprietary-aoineco",
}

KST = timezone(timedelta(hours=9))


# ═══════════════════════════════════════════════════════════
# UPGRADE 1: MONTE CARLO RISK SIMULATION
# ═══════════════════════════════════════════════════════════
# Concept source: Cryptocurrency Trader (Bayesian & Monte Carlo)
# Our implementation: Fully original — Aoineco-tailored for 
#   10-minute scalping with Kelly overlay.
# ═══════════════════════════════════════════════════════════

@dataclass
class MonteCarloConfig:
    """Configuration for Monte Carlo risk simulation."""
    n_simulations: int = 10_000
    n_steps: int = 6              # 6 steps × 10min = 1 hour horizon
    step_minutes: int = 10
    seed: Optional[int] = None


class MonteCarloRiskEngine:
    """
    💊 Blue-Med Enhancement: Monte Carlo-based risk assessment.
    
    Instead of a single "risk_score" guess, we simulate thousands of
    possible price paths based on recent volatility, then calculate:
    
    1. Value-at-Risk (VaR) — worst-case loss at 95%/99% confidence
    2. Expected Shortfall (CVaR) — average loss in worst 5% scenarios
    3. Sharpe Ratio — risk-adjusted return per unit of volatility
    4. Optimal position size — Monte Carlo-validated Kelly fraction
    
    Mathematical Model:
    ───────────────────
    For each simulation step:
      dS/S = μ·dt + σ·√dt·Z    (Geometric Brownian Motion)
      where Z ~ N(0,1)
    
    VaR_α = -Percentile(returns, α)
    CVaR_α = -E[returns | returns < -VaR_α]
    Sharpe = E[returns] / σ[returns] × √(steps_per_hour)
    """
    
    def __init__(self, config: Optional[MonteCarloConfig] = None):
        self.config = config or MonteCarloConfig()
        if self.config.seed is not None:
            random.seed(self.config.seed)
    
    def estimate_volatility(self, price_history: List[float]) -> float:
        """
        Estimate annualized volatility from recent price data.
        Uses log-returns for mathematical correctness.
        """
        if len(price_history) < 2:
            return 0.02  # Default 2% if insufficient data
        
        log_returns = []
        for i in range(1, len(price_history)):
            if price_history[i - 1] > 0:
                lr = math.log(price_history[i] / price_history[i - 1])
                log_returns.append(lr)
        
        if not log_returns:
            return 0.02
        
        mean_r = sum(log_returns) / len(log_returns)
        variance = sum((r - mean_r) ** 2 for r in log_returns) / len(log_returns)
        return math.sqrt(variance)
    
    def simulate(
        self,
        current_price: float,
        mu: float,              # Expected drift (e.g., from Omega verdict)
        sigma: float,           # Volatility per step
        direction: Literal["LONG", "SHORT"],
    ) -> Dict:
        """
        Run Monte Carlo simulation and return risk metrics.
        
        Returns:
            var_95, var_99: Value-at-Risk at 95% and 99% confidence
            cvar_95: Conditional VaR (Expected Shortfall)
            sharpe: Annualized Sharpe ratio
            win_rate: % of simulations that end profitable
            max_drawdown_avg: Average max drawdown across simulations
            optimal_kelly: Monte Carlo-validated Kelly fraction
        """
        n_sims = self.config.n_simulations
        n_steps = self.config.n_steps
        dt = 1.0  # Each step = 1 unit (10 minutes)
        sqrt_dt = math.sqrt(dt)
        
        final_returns = []
        max_drawdowns = []
        
        for _ in range(n_sims):
            price = current_price
            peak = price
            max_dd = 0.0
            
            for _ in range(n_steps):
                z = random.gauss(0, 1)
                # GBM step
                price *= math.exp((mu - 0.5 * sigma ** 2) * dt + sigma * sqrt_dt * z)
                
                # Track drawdown
                if price > peak:
                    peak = price
                dd = (peak - price) / peak
                if dd > max_dd:
                    max_dd = dd
            
            # Calculate return based on direction
            pct_return = (price - current_price) / current_price
            if direction == "SHORT":
                pct_return = -pct_return
            
            final_returns.append(pct_return)
            max_drawdowns.append(max_dd)
        
        # Sort returns for percentile calculations
        sorted_returns = sorted(final_returns)
        
        # VaR (negative percentile = loss)
        var_95_idx = int(n_sims * 0.05)
        var_99_idx = int(n_sims * 0.01)
        var_95 = -sorted_returns[var_95_idx]
        var_99 = -sorted_returns[var_99_idx]
        
        # CVaR (Expected Shortfall) — average of worst 5%
        worst_5pct = sorted_returns[:var_95_idx]
        cvar_95 = -sum(worst_5pct) / len(worst_5pct) if worst_5pct else var_95
        
        # Expected return & volatility
        mean_return = sum(final_returns) / n_sims
        variance = sum((r - mean_return) ** 2 for r in final_returns) / n_sims
        vol = math.sqrt(variance)
        
        # Sharpe ratio (annualized: assume 6 periods/hour × 24h × 365d)
        periods_per_year = (60 / self.config.step_minutes) * 24 * 365
        sharpe = (mean_return / vol * math.sqrt(periods_per_year)) if vol > 0 else 0.0
        
        # Win rate
        wins = sum(1 for r in final_returns if r > 0)
        win_rate = wins / n_sims
        
        # Max drawdown average
        avg_max_dd = sum(max_drawdowns) / n_sims
        
        # Monte Carlo Kelly: f* = mean_return / variance
        mc_kelly = (mean_return / variance) if variance > 0 else 0.0
        mc_kelly_safe = max(0.0, min(0.25, mc_kelly * 0.25))  # Quarter-Kelly cap
        
        return {
            "var_95": round(var_95 * 100, 4),          # as percentage
            "var_99": round(var_99 * 100, 4),
            "cvar_95": round(cvar_95 * 100, 4),
            "sharpe_ratio": round(sharpe, 4),
            "expected_return": round(mean_return * 100, 4),
            "volatility": round(vol * 100, 4),
            "win_rate": round(win_rate * 100, 2),
            "avg_max_drawdown": round(avg_max_dd * 100, 4),
            "mc_kelly_fraction": round(mc_kelly_safe, 4),
            "simulations": n_sims,
            "steps": n_steps,
            "step_minutes": self.config.step_minutes,
        }


# ═══════════════════════════════════════════════════════════
# UPGRADE 2: SELF-REFLECTION ENGINE
# ═══════════════════════════════════════════════════════════
# Concept source: Crypto Self-Learning (자가학습 엔진)
# Our implementation: Bayesian prior-updating based on
#   settlement history — no neural network, pure statistics.
# ═══════════════════════════════════════════════════════════

@dataclass
class TradeRecord:
    """A single settled trade for reflection analysis."""
    timestamp: str
    direction: str          # LONG / SHORT / HOLD
    confidence: float
    actual_outcome: str     # LONG / SHORT
    pnl_percent: float
    signals_snapshot: List[Dict]
    market_conditions: Dict  # RSI, trend, volatility at time of trade


class SelfReflectionEngine:
    """
    🧠 Blue-Brain Enhancement: Post-settlement self-reflection.
    
    After each trade settles, this engine asks THREE questions:
    
    1. "Which agent was most accurate?" → Update agent trust weights
    2. "What market regime did we fail in?" → Pattern recognition
    3. "Should we adjust our thresholds?" → Adaptive parameter tuning
    
    Method:
    ───────
    Agent Trust = Bayesian Beta distribution
      - Each agent starts with Beta(α=2, β=2) (mild prior)
      - Correct signal → α += 1
      - Incorrect signal → β += 1
      - Trust = α / (α + β) = empirical accuracy
    
    This naturally gives more weight to agents with longer track records,
    and allows recovery from bad streaks.
    """
    
    def __init__(self):
        # Agent trust priors: Beta(alpha, beta)
        self.agent_trust: Dict[str, Dict[str, float]] = {}
        self.trade_history: List[TradeRecord] = []
        self.regime_patterns: Dict[str, Dict] = {}
        self._init_trust()
    
    def _init_trust(self):
        """Initialize Bayesian trust for each signal-contributing agent."""
        agents = [
            "blue_eye", "blue_sound", "blue_blade",
            "blue_flash", "oracle", "blue_med"
        ]
        for agent in agents:
            self.agent_trust[agent] = {
                "alpha": 2.0,    # Prior successes
                "beta": 2.0,     # Prior failures
                "total_signals": 0,
                "correct": 0,
                "streak": 0,     # Positive = consecutive wins, negative = losses
            }
    
    def reflect(self, record: TradeRecord) -> Dict:
        """
        Perform post-settlement reflection.
        Returns insights and recommended weight adjustments.
        """
        self.trade_history.append(record)
        
        insights = {
            "timestamp": datetime.now(KST).isoformat(),
            "trade_direction": record.direction,
            "actual_outcome": record.actual_outcome,
            "was_correct": record.direction == record.actual_outcome,
            "pnl_percent": record.pnl_percent,
            "agent_updates": [],
            "regime_insight": None,
            "threshold_suggestion": None,
        }
        
        # ─── Q1: Which agent was most accurate? ──────
        for sig in record.signals_snapshot:
            agent_id = sig.get("agent_id", "")
            if agent_id not in self.agent_trust:
                continue
            
            trust = self.agent_trust[agent_id]
            agent_correct = sig["direction"] == record.actual_outcome
            
            trust["total_signals"] += 1
            
            if agent_correct:
                trust["alpha"] += 1
                trust["correct"] += 1
                trust["streak"] = max(1, trust["streak"] + 1)
            else:
                trust["beta"] += 1
                trust["streak"] = min(-1, trust["streak"] - 1)
            
            # Current Bayesian trust score
            current_trust = trust["alpha"] / (trust["alpha"] + trust["beta"])
            
            insights["agent_updates"].append({
                "agent_id": agent_id,
                "was_correct": agent_correct,
                "direction_given": sig["direction"],
                "new_trust": round(current_trust, 4),
                "total_signals": trust["total_signals"],
                "accuracy": round(trust["correct"] / trust["total_signals"], 4),
                "streak": trust["streak"],
            })
        
        # ─── Q2: What market regime did we fail in? ──
        regime_key = self._classify_regime(record.market_conditions)
        if regime_key not in self.regime_patterns:
            self.regime_patterns[regime_key] = {
                "wins": 0, "losses": 0, "total_pnl": 0.0
            }
        
        rp = self.regime_patterns[regime_key]
        rp["total_pnl"] += record.pnl_percent
        
        if record.direction == record.actual_outcome:
            rp["wins"] += 1
        else:
            rp["losses"] += 1
        
        total = rp["wins"] + rp["losses"]
        regime_wr = rp["wins"] / total if total > 0 else 0.5
        
        insights["regime_insight"] = {
            "regime": regime_key,
            "win_rate": round(regime_wr, 4),
            "total_trades": total,
            "cumulative_pnl": round(rp["total_pnl"], 4),
            "warning": regime_wr < 0.4 and total >= 5,
        }
        
        # ─── Q3: Should we adjust thresholds? ─────────
        if len(self.trade_history) >= 10:
            recent_10 = self.trade_history[-10:]
            recent_wr = sum(
                1 for t in recent_10 if t.direction == t.actual_outcome
            ) / 10
            
            if recent_wr < 0.4:
                insights["threshold_suggestion"] = {
                    "action": "RAISE_VETO_THRESHOLD",
                    "reason": f"Recent win rate {recent_wr:.0%} < 40%. "
                              f"Recommend raising Oracle veto from 0.55 to 0.60.",
                    "new_threshold": 0.60,
                }
            elif recent_wr > 0.7:
                insights["threshold_suggestion"] = {
                    "action": "LOWER_VETO_THRESHOLD",
                    "reason": f"Recent win rate {recent_wr:.0%} > 70%. "
                              f"Can safely lower veto from 0.55 to 0.52.",
                    "new_threshold": 0.52,
                }
            else:
                insights["threshold_suggestion"] = {
                    "action": "HOLD_CURRENT",
                    "reason": f"Recent win rate {recent_wr:.0%} is within normal range.",
                }
        
        return insights
    
    def get_recommended_weights(self) -> Dict[str, float]:
        """
        Generate recommended Omega fusion weights based on trust scores.
        Normalized so sum of signal-agent weights = 0.85 
        (Oracle veto keeps 0.10, Blue-Med keeps 0.10 base).
        """
        trust_scores = {}
        for agent_id, trust in self.agent_trust.items():
            trust_scores[agent_id] = trust["alpha"] / (trust["alpha"] + trust["beta"])
        
        # Normalize to target sum
        total_trust = sum(trust_scores.values())
        if total_trust == 0:
            return {k: 1.0 / len(trust_scores) for k in trust_scores}
        
        target_sum = 0.85  # Total weight budget for signal agents
        normalized = {
            k: round(v / total_trust * target_sum, 4)
            for k, v in trust_scores.items()
        }
        
        return normalized
    
    def _classify_regime(self, conditions: Dict) -> str:
        """Classify market conditions into a regime label."""
        rsi = conditions.get("rsi", 50)
        trend = conditions.get("trend", "NEUTRAL")
        vol = conditions.get("volatility", "normal")
        
        if rsi > 70:
            rsi_label = "overbought"
        elif rsi < 30:
            rsi_label = "oversold"
        else:
            rsi_label = "neutral"
        
        return f"{trend.lower()}_{rsi_label}_{vol}"
    
    def export_state(self) -> Dict:
        """Export full reflection state for persistence."""
        return {
            "agent_trust": self.agent_trust,
            "regime_patterns": self.regime_patterns,
            "total_trades_analyzed": len(self.trade_history),
            "exported_at": datetime.now(KST).isoformat(),
            "sdna": __sdna__["id"],
        }


# ═══════════════════════════════════════════════════════════
# UPGRADE 3: ADVANCED TECHNICAL INDICATORS
# ═══════════════════════════════════════════════════════════
# Concept source: Stock Info Explorer (기술 지표 정밀 생성)
# Our implementation: Lightweight pure-Python TA library
#   designed for 10-minute scalping resolution.
# ═══════════════════════════════════════════════════════════

class AoinecoTechnicalAnalysis:
    """
    👁️ Blue-Eye Enhancement: High-resolution technical analysis.
    
    Pure Python — zero external dependencies.
    Optimized for BTC 5-minute / 10-minute timeframes.
    
    Indicators:
    ───────────
    1. RSI (configurable period)
    2. MACD (12/26/9 standard + custom)
    3. Bollinger Bands (with squeeze detection)
    4. VWAP (Volume-Weighted Average Price)
    5. OBV (On-Balance Volume)
    6. Divergence Detection (RSI vs Price)
    """
    
    @staticmethod
    def rsi(closes: List[float], period: int = 14) -> Optional[float]:
        """Relative Strength Index."""
        if len(closes) < period + 1:
            return None
        
        gains = []
        losses = []
        for i in range(1, len(closes)):
            delta = closes[i] - closes[i - 1]
            gains.append(max(0, delta))
            losses.append(max(0, -delta))
        
        # Wilder's smoothed average
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        for i in range(period, len(gains)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 4)
    
    @staticmethod
    def ema(data: List[float], period: int) -> List[float]:
        """Exponential Moving Average."""
        if len(data) < period:
            return []
        
        k = 2 / (period + 1)
        ema_vals = [sum(data[:period]) / period]  # SMA seed
        
        for i in range(period, len(data)):
            ema_vals.append(data[i] * k + ema_vals[-1] * (1 - k))
        
        return ema_vals
    
    @classmethod
    def macd(
        cls,
        closes: List[float],
        fast: int = 12,
        slow: int = 26,
        signal: int = 9,
    ) -> Optional[Dict]:
        """
        MACD (Moving Average Convergence Divergence).
        Returns: macd_line, signal_line, histogram, crossover state.
        """
        if len(closes) < slow + signal:
            return None
        
        ema_fast = cls.ema(closes, fast)
        ema_slow = cls.ema(closes, slow)
        
        # Align lengths
        offset = slow - fast
        ema_fast_aligned = ema_fast[offset:]
        
        macd_line = [f - s for f, s in zip(ema_fast_aligned, ema_slow)]
        
        if len(macd_line) < signal:
            return None
        
        signal_line = cls.ema(macd_line, signal)
        
        # Histogram (most recent)
        hist_offset = len(macd_line) - len(signal_line)
        histogram = [
            m - s for m, s in zip(macd_line[hist_offset:], signal_line)
        ]
        
        # Crossover detection
        if len(histogram) >= 2:
            if histogram[-2] < 0 and histogram[-1] >= 0:
                crossover = "BULLISH"
            elif histogram[-2] > 0 and histogram[-1] <= 0:
                crossover = "BEARISH"
            else:
                crossover = "NONE"
        else:
            crossover = "NONE"
        
        return {
            "macd": round(macd_line[-1], 4),
            "signal": round(signal_line[-1], 4),
            "histogram": round(histogram[-1], 4),
            "crossover": crossover,
        }
    
    @staticmethod
    def bollinger_bands(
        closes: List[float],
        period: int = 20,
        std_dev: float = 2.0,
    ) -> Optional[Dict]:
        """
        Bollinger Bands with squeeze detection.
        Squeeze = bandwidth < 4% → volatility breakout imminent.
        """
        if len(closes) < period:
            return None
        
        window = closes[-period:]
        sma = sum(window) / period
        variance = sum((x - sma) ** 2 for x in window) / period
        std = math.sqrt(variance)
        
        upper = sma + std_dev * std
        lower = sma - std_dev * std
        bandwidth = (upper - lower) / sma * 100  # as percentage
        
        current = closes[-1]
        position = (current - lower) / (upper - lower) if upper != lower else 0.5
        
        return {
            "upper": round(upper, 2),
            "middle": round(sma, 2),
            "lower": round(lower, 2),
            "bandwidth": round(bandwidth, 4),
            "position": round(position, 4),       # 0=lower band, 1=upper band
            "squeeze": bandwidth < 4.0,
        }
    
    @staticmethod
    def vwap(
        closes: List[float],
        highs: List[float],
        lows: List[float],
        volumes: List[float],
    ) -> Optional[float]:
        """Volume-Weighted Average Price."""
        if not all(len(x) == len(closes) for x in [highs, lows, volumes]):
            return None
        if sum(volumes) == 0:
            return None
        
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(highs, lows, closes)]
        cum_tp_vol = sum(tp * v for tp, v in zip(typical_prices, volumes))
        cum_vol = sum(volumes)
        
        return round(cum_tp_vol / cum_vol, 2)
    
    @staticmethod
    def obv(closes: List[float], volumes: List[float]) -> Optional[Dict]:
        """
        On-Balance Volume — measures buying/selling pressure.
        Returns current OBV and its trend (rising/falling).
        """
        if len(closes) < 2 or len(closes) != len(volumes):
            return None
        
        obv_val = 0
        obv_series = [0]
        
        for i in range(1, len(closes)):
            if closes[i] > closes[i - 1]:
                obv_val += volumes[i]
            elif closes[i] < closes[i - 1]:
                obv_val -= volumes[i]
            obv_series.append(obv_val)
        
        # OBV trend: compare last 5 OBVs
        if len(obv_series) >= 5:
            recent = obv_series[-5:]
            if all(recent[i] <= recent[i + 1] for i in range(4)):
                trend = "RISING"
            elif all(recent[i] >= recent[i + 1] for i in range(4)):
                trend = "FALLING"
            else:
                trend = "MIXED"
        else:
            trend = "INSUFFICIENT_DATA"
        
        return {
            "obv": obv_val,
            "trend": trend,
        }
    
    @classmethod
    def detect_divergence(
        cls,
        closes: List[float],
        period: int = 14,
        lookback: int = 10,
    ) -> Optional[Dict]:
        """
        Detect RSI-Price divergence.
        
        Bullish divergence: Price makes lower low, RSI makes higher low
        Bearish divergence: Price makes higher high, RSI makes lower high
        """
        if len(closes) < period + lookback:
            return None
        
        # Calculate RSI for each point in lookback
        rsi_series = []
        for i in range(lookback):
            end_idx = len(closes) - lookback + i + 1
            rsi_val = cls.rsi(closes[:end_idx], period)
            if rsi_val is not None:
                rsi_series.append(rsi_val)
        
        if len(rsi_series) < lookback:
            return None
        
        price_window = closes[-lookback:]
        
        # Compare first half vs second half
        mid = lookback // 2
        
        price_low_1 = min(price_window[:mid])
        price_low_2 = min(price_window[mid:])
        rsi_low_1 = min(rsi_series[:mid])
        rsi_low_2 = min(rsi_series[mid:])
        
        price_high_1 = max(price_window[:mid])
        price_high_2 = max(price_window[mid:])
        rsi_high_1 = max(rsi_series[:mid])
        rsi_high_2 = max(rsi_series[mid:])
        
        divergence = "NONE"
        
        # Bullish: price lower low + RSI higher low
        if price_low_2 < price_low_1 and rsi_low_2 > rsi_low_1:
            divergence = "BULLISH"
        
        # Bearish: price higher high + RSI lower high
        elif price_high_2 > price_high_1 and rsi_high_2 < rsi_high_1:
            divergence = "BEARISH"
        
        return {
            "divergence": divergence,
            "price_trend": "UP" if price_window[-1] > price_window[0] else "DOWN",
            "rsi_current": rsi_series[-1] if rsi_series else None,
        }
    
    @classmethod
    def full_analysis(
        cls,
        closes: List[float],
        highs: Optional[List[float]] = None,
        lows: Optional[List[float]] = None,
        volumes: Optional[List[float]] = None,
    ) -> Dict:
        """
        Run all indicators and return a comprehensive analysis.
        This is the main entry point for Blue-Eye.
        """
        result = {
            "timestamp": datetime.now(KST).isoformat(),
            "data_points": len(closes),
            "current_price": closes[-1] if closes else None,
            "indicators": {},
            "signals": [],
        }
        
        # RSI
        rsi_val = cls.rsi(closes)
        if rsi_val is not None:
            result["indicators"]["rsi"] = rsi_val
            if rsi_val > 70:
                result["signals"].append({
                    "indicator": "RSI",
                    "signal": "OVERBOUGHT",
                    "bias": "SHORT",
                    "strength": min(1.0, (rsi_val - 70) / 30),
                })
            elif rsi_val < 30:
                result["signals"].append({
                    "indicator": "RSI",
                    "signal": "OVERSOLD",
                    "bias": "LONG",
                    "strength": min(1.0, (30 - rsi_val) / 30),
                })
        
        # MACD
        macd_result = cls.macd(closes)
        if macd_result:
            result["indicators"]["macd"] = macd_result
            if macd_result["crossover"] == "BULLISH":
                result["signals"].append({
                    "indicator": "MACD",
                    "signal": "BULLISH_CROSSOVER",
                    "bias": "LONG",
                    "strength": 0.7,
                })
            elif macd_result["crossover"] == "BEARISH":
                result["signals"].append({
                    "indicator": "MACD",
                    "signal": "BEARISH_CROSSOVER",
                    "bias": "SHORT",
                    "strength": 0.7,
                })
        
        # Bollinger Bands
        bb = cls.bollinger_bands(closes)
        if bb:
            result["indicators"]["bollinger"] = bb
            if bb["squeeze"]:
                result["signals"].append({
                    "indicator": "BOLLINGER",
                    "signal": "SQUEEZE_DETECTED",
                    "bias": "NEUTRAL",
                    "strength": 0.8,
                    "note": "Volatility breakout imminent",
                })
            if bb["position"] > 0.95:
                result["signals"].append({
                    "indicator": "BOLLINGER",
                    "signal": "UPPER_BAND_TOUCH",
                    "bias": "SHORT",
                    "strength": 0.5,
                })
            elif bb["position"] < 0.05:
                result["signals"].append({
                    "indicator": "BOLLINGER",
                    "signal": "LOWER_BAND_TOUCH",
                    "bias": "LONG",
                    "strength": 0.5,
                })
        
        # VWAP
        if highs and lows and volumes:
            vwap_val = cls.vwap(closes, highs, lows, volumes)
            if vwap_val:
                result["indicators"]["vwap"] = vwap_val
                if closes[-1] > vwap_val:
                    result["signals"].append({
                        "indicator": "VWAP",
                        "signal": "ABOVE_VWAP",
                        "bias": "LONG",
                        "strength": 0.4,
                    })
                else:
                    result["signals"].append({
                        "indicator": "VWAP",
                        "signal": "BELOW_VWAP",
                        "bias": "SHORT",
                        "strength": 0.4,
                    })
            
            # OBV
            obv_result = cls.obv(closes, volumes)
            if obv_result:
                result["indicators"]["obv"] = obv_result
        
        # Divergence
        div = cls.detect_divergence(closes)
        if div and div["divergence"] != "NONE":
            result["indicators"]["divergence"] = div
            result["signals"].append({
                "indicator": "DIVERGENCE",
                "signal": f"{div['divergence']}_DIVERGENCE",
                "bias": "LONG" if div["divergence"] == "BULLISH" else "SHORT",
                "strength": 0.85,
                "note": "RSI-Price divergence — strong reversal signal",
            })
        
        # Summary
        long_signals = sum(1 for s in result["signals"] if s["bias"] == "LONG")
        short_signals = sum(1 for s in result["signals"] if s["bias"] == "SHORT")
        
        if long_signals > short_signals:
            result["ta_consensus"] = "LONG"
        elif short_signals > long_signals:
            result["ta_consensus"] = "SHORT"
        else:
            result["ta_consensus"] = "NEUTRAL"
        
        result["ta_confidence"] = round(
            abs(long_signals - short_signals) / max(1, long_signals + short_signals), 4
        )
        
        return result


# ═══════════════════════════════════════════════════════════
# INTEGRATION: V6 REBUILD ORCHESTRATOR
# ═══════════════════════════════════════════════════════════

class V6RebuildOrchestrator:
    """
    Glues all three upgrades into the Omega pipeline.
    
    Flow:
    1. Blue-Eye generates full TA → feeds AgentSignal with richer data
    2. Omega fuses signals → verdict
    3. Blue-Med runs Monte Carlo on verdict → risk-adjusted position
    4. Post-settlement → Self-Reflection updates trust weights
    """
    
    def __init__(self):
        self.ta = AoinecoTechnicalAnalysis()
        self.mc = MonteCarloRiskEngine(MonteCarloConfig(n_simulations=5_000))
        self.reflection = SelfReflectionEngine()
    
    def enhanced_analysis(
        self,
        price_data: Dict,  # {closes, highs, lows, volumes}
        omega_verdict: Dict,  # From OmegaFusionEngine.fuse()
    ) -> Dict:
        """Run the full V6 enhanced pipeline."""
        
        # Step 1: Advanced TA
        ta_result = self.ta.full_analysis(
            closes=price_data.get("closes", []),
            highs=price_data.get("highs"),
            lows=price_data.get("lows"),
            volumes=price_data.get("volumes"),
        )
        
        # Step 2: Monte Carlo risk assessment
        sigma = self.mc.estimate_volatility(price_data.get("closes", []))
        direction = omega_verdict.get("direction", "LONG")
        mu = 0.001 if direction == "LONG" else -0.001  # Drift from verdict
        
        mc_result = self.mc.simulate(
            current_price=price_data["closes"][-1] if price_data.get("closes") else 0,
            mu=mu,
            sigma=sigma,
            direction=direction if direction != "HOLD" else "LONG",
        )
        
        # Step 3: Combine into enhanced verdict
        return {
            "sdna": __sdna__["id"],
            "engine": "omega-v6-rebuild",
            "omega_verdict": omega_verdict,
            "technical_analysis": ta_result,
            "monte_carlo_risk": mc_result,
            "enhanced_position_size": min(
                omega_verdict.get("position_size_kelly", 0),
                mc_result.get("mc_kelly_fraction", 0),
            ),
            "recommendation": self._synthesize(omega_verdict, ta_result, mc_result),
            "timestamp": datetime.now(KST).isoformat(),
        }
    
    def post_settlement(self, record: TradeRecord) -> Dict:
        """Run self-reflection after settlement."""
        reflection = self.reflection.reflect(record)
        new_weights = self.reflection.get_recommended_weights()
        
        return {
            "reflection": reflection,
            "recommended_weights": new_weights,
            "reflection_state": self.reflection.export_state(),
        }
    
    def _synthesize(self, verdict: Dict, ta: Dict, mc: Dict) -> Dict:
        """Final synthesis: combine all three upgrades into one recommendation."""
        omega_dir = verdict.get("direction", "HOLD")
        ta_dir = ta.get("ta_consensus", "NEUTRAL")
        
        # Agreement check
        if omega_dir == ta_dir:
            agreement = "STRONG"
            final_dir = omega_dir
        elif omega_dir == "HOLD" or ta_dir == "NEUTRAL":
            agreement = "WEAK"
            final_dir = omega_dir if omega_dir != "HOLD" else ta_dir
        else:
            agreement = "CONFLICT"
            final_dir = "HOLD"  # Conflicting signals → sit out
        
        # Risk gate
        var_95 = mc.get("var_95", 0)
        if var_95 > 2.0:  # More than 2% VaR at 95% → reduce
            risk_override = "HIGH_RISK_REDUCE"
        elif var_95 > 1.0:
            risk_override = "MODERATE"
        else:
            risk_override = "CLEAR"
        
        return {
            "final_direction": final_dir,
            "agreement": agreement,
            "risk_override": risk_override,
            "var_95": var_95,
            "win_probability": mc.get("win_rate", 50),
            "rationale": (
                f"Omega={omega_dir}(conf:{verdict.get('confidence', 0):.2%}), "
                f"TA={ta_dir}(conf:{ta.get('ta_confidence', 0):.2%}), "
                f"MC VaR95={var_95:.2f}%, WinRate={mc.get('win_rate', 0):.1f}%"
            ),
        }


# ═══════════════════════════════════════════════════════════
# CLI DEMO
# ═══════════════════════════════════════════════════════════

def demo():
    """Full V6 Rebuild demonstration."""
    print("=" * 64)
    print("🌌 NEXUS ORACLE Ω — V6 REBUILD DEMO")
    print("   Monte Carlo × Self-Learning × Advanced TA")
    print("   Aoineco & Co. — Architecture of Intelligence")
    print("=" * 64)
    
    orchestrator = V6RebuildOrchestrator()
    
    # Simulated price data (50 candles of 5-min BTC)
    import random
    random.seed(42)
    base = 97000.0
    closes = [base]
    highs = [base + 50]
    lows = [base - 50]
    volumes = [random.uniform(100, 500)]
    
    for _ in range(49):
        change = random.gauss(0, 80)
        c = closes[-1] + change
        closes.append(c)
        highs.append(c + random.uniform(10, 60))
        lows.append(c - random.uniform(10, 60))
        volumes.append(random.uniform(100, 500))
    
    price_data = {
        "closes": closes,
        "highs": highs,
        "lows": lows,
        "volumes": volumes,
    }
    
    # Mock Omega verdict
    mock_verdict = {
        "direction": "LONG",
        "confidence": 0.68,
        "position_size_kelly": 0.09,
    }
    
    # Run enhanced analysis
    result = orchestrator.enhanced_analysis(price_data, mock_verdict)
    
    # Display
    rec = result["recommendation"]
    mc = result["monte_carlo_risk"]
    ta = result["technical_analysis"]
    
    print(f"\n🎯 Final Direction: {rec['final_direction']}")
    print(f"🤝 Agreement: {rec['agreement']}")
    print(f"⚠️  Risk Override: {rec['risk_override']}")
    print(f"📊 Rationale: {rec['rationale']}")
    print(f"\n--- Monte Carlo (n={mc['simulations']}) ---")
    print(f"  VaR 95%: {mc['var_95']:.4f}%")
    print(f"  VaR 99%: {mc['var_99']:.4f}%")
    print(f"  CVaR 95%: {mc['cvar_95']:.4f}%")
    print(f"  Sharpe: {mc['sharpe_ratio']:.4f}")
    print(f"  Win Rate: {mc['win_rate']:.2f}%")
    print(f"  MC Kelly: {mc['mc_kelly_fraction']:.4f}")
    print(f"\n--- Technical Analysis ({ta['data_points']} candles) ---")
    for k, v in ta["indicators"].items():
        print(f"  {k}: {v}")
    print(f"\n  TA Consensus: {ta['ta_consensus']} "
          f"(confidence: {ta['ta_confidence']:.2%})")
    print(f"\n  Signals Detected:")
    for sig in ta["signals"]:
        print(f"    • {sig['indicator']}: {sig['signal']} → {sig['bias']} "
              f"(strength: {sig['strength']:.0%})")
    
    print(f"\n💰 Position Size: {result['enhanced_position_size']:.4f}")
    print(f"⏰ {result['timestamp']}")
    print(f"🧬 S-DNA: {result['sdna']}")
    print("=" * 64)
    
    return result


if __name__ == "__main__":
    demo()
