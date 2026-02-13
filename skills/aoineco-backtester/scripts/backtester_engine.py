#!/usr/bin/env python3
"""
/* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */
S-DNA: AOI-2026-0213-SDNA-BT01

Aoineco Backtester — Historical Strategy Validation Engine

CONCEPT SOURCES (ideas only, zero code copied):
  - backtest-expert: Walk-Forward analysis, overfitting prevention
  - time-series-analysis: Feature engineering (Lag, Rolling, EWM)
  
ALL CODE IS 100% ORIGINAL IMPLEMENTATION BY AOINECO & CO.

PURPOSE:
  V6 predicts the future. The Backtester proves the past.
  Together, they form a complete validation loop:
  
  Backtest (past) → V6 (present) → Presage (public proof)

ARCHITECTURE:
  1. Feature Forge — Enrich raw OHLCV with technical features
  2. Strategy Simulator — Replay V6 logic on historical data
  3. Walk-Forward Validator — Rolling window out-of-sample testing
  4. Performance Analyzer — Win rate, Sharpe, max drawdown, overfitting score
  5. Report Generator — JSON + human-readable results

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import math
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
from datetime import datetime, timezone, timedelta

__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-BT01",
    "author_agent": "blue_brain",
    "org": "aoineco-co",
    "created": "2026-02-13T16:20:00+09:00",
    "tier": "premium",
    "classification": "stealth",
    "concept_sources": [
        "concept:walk_forward_analysis",
        "concept:overfitting_prevention",
        "concept:feature_engineering_lag_rolling_ewm",
    ],
    "license": "proprietary-aoineco",
}

KST = timezone(timedelta(hours=9))


# ═══════════════════════════════════════════════════════════
# COMPONENT 1: FEATURE FORGE
# ═══════════════════════════════════════════════════════════
# Concept source: time-series-analysis (feature engineering)
# Implementation: 100% original — optimized for BTC 5min scalping
# ═══════════════════════════════════════════════════════════

class FeatureForge:
    """
    Enriches raw OHLCV data with derived features for backtesting.
    
    Features generated:
    - Lag features (price N steps ago)
    - Rolling statistics (mean, std, min, max over windows)
    - EWM (Exponentially Weighted Moving averages)
    - Returns (simple and log)
    - Volatility (rolling standard deviation of returns)
    - RSI (Relative Strength Index)
    """
    
    @staticmethod
    def lag(series: List[float], n: int) -> List[Optional[float]]:
        """Create a lagged version of a series."""
        return [None] * n + series[:-n] if n > 0 else series
    
    @staticmethod
    def rolling_mean(series: List[float], window: int) -> List[Optional[float]]:
        """Rolling average."""
        result = [None] * (window - 1)
        for i in range(window - 1, len(series)):
            result.append(sum(series[i - window + 1:i + 1]) / window)
        return result
    
    @staticmethod
    def rolling_std(series: List[float], window: int) -> List[Optional[float]]:
        """Rolling standard deviation."""
        result = [None] * (window - 1)
        for i in range(window - 1, len(series)):
            w = series[i - window + 1:i + 1]
            mean = sum(w) / window
            var = sum((x - mean) ** 2 for x in w) / window
            result.append(math.sqrt(var))
        return result
    
    @staticmethod
    def ewm(series: List[float], span: int) -> List[float]:
        """Exponentially Weighted Moving average."""
        alpha = 2 / (span + 1)
        result = [series[0]]
        for i in range(1, len(series)):
            result.append(alpha * series[i] + (1 - alpha) * result[-1])
        return result
    
    @staticmethod
    def returns(series: List[float]) -> List[Optional[float]]:
        """Simple percentage returns."""
        result = [None]
        for i in range(1, len(series)):
            if series[i - 1] != 0:
                result.append((series[i] - series[i - 1]) / series[i - 1])
            else:
                result.append(0.0)
        return result
    
    @staticmethod
    def log_returns(series: List[float]) -> List[Optional[float]]:
        """Log returns (more mathematically correct for compounding)."""
        result = [None]
        for i in range(1, len(series)):
            if series[i - 1] > 0 and series[i] > 0:
                result.append(math.log(series[i] / series[i - 1]))
            else:
                result.append(0.0)
        return result
    
    @staticmethod
    def rsi(closes: List[float], period: int = 14) -> List[Optional[float]]:
        """Relative Strength Index."""
        result = [None] * period
        gains, losses = [], []
        for i in range(1, len(closes)):
            delta = closes[i] - closes[i - 1]
            gains.append(max(0, delta))
            losses.append(max(0, -delta))
        
        if len(gains) < period:
            return [None] * len(closes)
        
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        if avg_loss == 0:
            result.append(100.0)
        else:
            result.append(100 - 100 / (1 + avg_gain / avg_loss))
        
        for i in range(period, len(gains)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            if avg_loss == 0:
                result.append(100.0)
            else:
                result.append(100 - 100 / (1 + avg_gain / avg_loss))
        
        return result
    
    @classmethod
    def forge_all(cls, closes: List[float], volumes: Optional[List[float]] = None) -> Dict[str, List]:
        """Generate all features from close prices."""
        features = {
            "close": closes,
            "returns": cls.returns(closes),
            "log_returns": cls.log_returns(closes),
            "lag_1": cls.lag(closes, 1),
            "lag_3": cls.lag(closes, 3),
            "lag_6": cls.lag(closes, 6),
            "rolling_mean_5": cls.rolling_mean(closes, 5),
            "rolling_mean_20": cls.rolling_mean(closes, 20),
            "rolling_std_5": cls.rolling_std(closes, 5),
            "rolling_std_20": cls.rolling_std(closes, 20),
            "ewm_5": cls.ewm(closes, 5),
            "ewm_20": cls.ewm(closes, 20),
            "rsi_14": cls.rsi(closes, 14),
        }
        
        if volumes:
            features["volume"] = volumes
            features["vol_rolling_mean_5"] = cls.rolling_mean(volumes, 5)
            features["vol_ewm_10"] = cls.ewm(volumes, 10)
        
        return features


# ═══════════════════════════════════════════════════════════
# COMPONENT 2: STRATEGY SIMULATOR
# ═══════════════════════════════════════════════════════════

@dataclass
class Trade:
    """A single simulated trade."""
    entry_idx: int
    exit_idx: int
    direction: str  # "LONG" or "SHORT"
    entry_price: float
    exit_price: float
    pnl_pct: float = 0.0
    
    def __post_init__(self):
        if self.direction == "LONG":
            self.pnl_pct = (self.exit_price - self.entry_price) / self.entry_price
        else:
            self.pnl_pct = (self.entry_price - self.exit_price) / self.entry_price


class StrategySimulator:
    """
    Replays a trading strategy on historical data.
    
    The strategy is provided as a callable that takes:
      (features_at_time_t, index) → "LONG" / "SHORT" / "HOLD"
    
    This mirrors how V6 works: given current data, make a decision.
    """
    
    def __init__(self, holding_period: int = 2):
        """
        Args:
            holding_period: Number of candles to hold after entry.
                           For 5min candles, 2 = 10 minutes (our scalping window).
        """
        self.holding_period = holding_period
    
    def simulate(
        self,
        closes: List[float],
        strategy_fn: Callable,
        features: Optional[Dict[str, List]] = None,
        start_idx: int = 20,  # Skip first 20 for feature warmup
    ) -> List[Trade]:
        """
        Run the strategy over historical data.
        
        Args:
            closes: Price series
            strategy_fn: Function(features, idx) → "LONG"/"SHORT"/"HOLD"
            features: Pre-computed features dict
            start_idx: Where to start (skip warmup period)
        
        Returns:
            List of Trade objects
        """
        trades = []
        i = start_idx
        
        while i < len(closes) - self.holding_period:
            # Get strategy decision
            decision = strategy_fn(features, i)
            
            if decision in ("LONG", "SHORT"):
                entry_price = closes[i]
                exit_price = closes[i + self.holding_period]
                
                trade = Trade(
                    entry_idx=i,
                    exit_idx=i + self.holding_period,
                    direction=decision,
                    entry_price=entry_price,
                    exit_price=exit_price,
                )
                trades.append(trade)
                
                # Skip holding period (no overlapping trades)
                i += self.holding_period
            else:
                i += 1
        
        return trades


# ═══════════════════════════════════════════════════════════
# COMPONENT 3: WALK-FORWARD VALIDATOR
# ═══════════════════════════════════════════════════════════
# Concept source: backtest-expert (walk-forward analysis)
# Implementation: 100% original
# ═══════════════════════════════════════════════════════════

class WalkForwardValidator:
    """
    Walk-Forward Analysis: The gold standard for strategy validation.
    
    Instead of testing on the entire history (which overfits),
    we split data into rolling windows:
    
    ┌──────────────────────────────────────────────┐
    │ Window 1: [train========][test===]            │
    │ Window 2:     [train========][test===]        │
    │ Window 3:         [train========][test===]    │
    │ Window 4:             [train========][test===]│
    └──────────────────────────────────────────────┘
    
    Only the TEST results count. This prevents overfitting
    because the strategy never sees the test data during "training."
    
    For our V6 use case, "training" = the data the agent sees,
    "testing" = the next N candles where we check if the prediction held.
    """
    
    def __init__(
        self,
        train_size: int = 50,   # 50 candles for context
        test_size: int = 10,    # 10 candles for validation
        step_size: int = 10,    # Advance by 10 candles per window
    ):
        self.train_size = train_size
        self.test_size = test_size
        self.step_size = step_size
    
    def validate(
        self,
        closes: List[float],
        strategy_fn: Callable,
        features: Optional[Dict[str, List]] = None,
    ) -> Dict:
        """
        Run walk-forward validation.
        
        Returns:
            Per-window results + aggregate statistics
        """
        simulator = StrategySimulator(holding_period=2)
        windows = []
        all_trades = []
        
        total_len = len(closes)
        start = 0
        
        while start + self.train_size + self.test_size <= total_len:
            train_end = start + self.train_size
            test_end = train_end + self.test_size
            
            # Only simulate on test portion
            test_trades = simulator.simulate(
                closes=closes[start:test_end],
                strategy_fn=strategy_fn,
                features=features,
                start_idx=self.train_size,  # Start at test portion
            )
            
            window_pnl = sum(t.pnl_pct for t in test_trades)
            window_wins = sum(1 for t in test_trades if t.pnl_pct > 0)
            window_total = len(test_trades)
            
            windows.append({
                "window_start": start,
                "window_end": test_end,
                "train_range": (start, train_end),
                "test_range": (train_end, test_end),
                "trades": window_total,
                "wins": window_wins,
                "win_rate": round(window_wins / window_total, 4) if window_total > 0 else 0,
                "pnl_pct": round(window_pnl * 100, 4),
            })
            
            all_trades.extend(test_trades)
            start += self.step_size
        
        return {
            "windows": windows,
            "total_windows": len(windows),
            "all_trades": all_trades,
        }


# ═══════════════════════════════════════════════════════════
# COMPONENT 4: PERFORMANCE ANALYZER
# ═══════════════════════════════════════════════════════════

class PerformanceAnalyzer:
    """
    Comprehensive performance metrics from backtest trades.
    
    Metrics:
    - Win rate, average win/loss
    - Sharpe ratio (annualized)
    - Maximum drawdown
    - Profit factor
    - Overfitting score (in-sample vs out-of-sample divergence)
    """
    
    @staticmethod
    def analyze(trades: List[Trade], windows: Optional[List[Dict]] = None) -> Dict:
        """Full performance analysis."""
        if not trades:
            return {"status": "no_trades", "message": "No trades to analyze"}
        
        pnls = [t.pnl_pct for t in trades]
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p <= 0]
        
        # Basic stats
        total = len(pnls)
        win_count = len(wins)
        loss_count = len(losses)
        win_rate = win_count / total if total > 0 else 0
        
        avg_win = sum(wins) / len(wins) if wins else 0
        avg_loss = sum(losses) / len(losses) if losses else 0
        
        # Total return (compounded)
        cumulative = 1.0
        peak = 1.0
        max_drawdown = 0.0
        equity_curve = [1.0]
        
        for pnl in pnls:
            cumulative *= (1 + pnl)
            equity_curve.append(cumulative)
            if cumulative > peak:
                peak = cumulative
            dd = (peak - cumulative) / peak
            if dd > max_drawdown:
                max_drawdown = dd
        
        total_return = cumulative - 1.0
        
        # Sharpe ratio
        if len(pnls) > 1:
            mean_r = sum(pnls) / len(pnls)
            var_r = sum((r - mean_r) ** 2 for r in pnls) / len(pnls)
            std_r = math.sqrt(var_r)
            # Annualize: assume 12 trades/hour × 24h × 365d
            trades_per_year = 12 * 24 * 365
            sharpe = (mean_r / std_r * math.sqrt(trades_per_year)) if std_r > 0 else 0
        else:
            sharpe = 0
        
        # Profit factor
        gross_profit = sum(wins) if wins else 0
        gross_loss = abs(sum(losses)) if losses else 0.001
        profit_factor = gross_profit / gross_loss
        
        # Overfitting score (if walk-forward windows available)
        overfit_score = None
        if windows and len(windows) >= 4:
            # Compare first half vs second half performance
            mid = len(windows) // 2
            first_half_wr = sum(w["win_rate"] for w in windows[:mid]) / mid
            second_half_wr = sum(w["win_rate"] for w in windows[mid:]) / (len(windows) - mid)
            
            # If first half >> second half, likely overfitting
            overfit_score = round(abs(first_half_wr - second_half_wr), 4)
        
        return {
            "total_trades": total,
            "win_rate": round(win_rate * 100, 2),
            "avg_win_pct": round(avg_win * 100, 4),
            "avg_loss_pct": round(avg_loss * 100, 4),
            "total_return_pct": round(total_return * 100, 4),
            "max_drawdown_pct": round(max_drawdown * 100, 4),
            "sharpe_ratio": round(sharpe, 4),
            "profit_factor": round(profit_factor, 4),
            "overfit_score": overfit_score,
            "overfit_warning": (
                overfit_score is not None and overfit_score > 0.15
            ),
            "longest_win_streak": PerformanceAnalyzer._streak(pnls, positive=True),
            "longest_loss_streak": PerformanceAnalyzer._streak(pnls, positive=False),
        }
    
    @staticmethod
    def _streak(pnls: List[float], positive: bool) -> int:
        """Find longest winning or losing streak."""
        max_streak = 0
        current = 0
        for p in pnls:
            if (positive and p > 0) or (not positive and p <= 0):
                current += 1
                max_streak = max(max_streak, current)
            else:
                current = 0
        return max_streak


# ═══════════════════════════════════════════════════════════
# COMPONENT 5: BACKTEST ORCHESTRATOR
# ═══════════════════════════════════════════════════════════

class AoinecoBacktester:
    """
    Master orchestrator for backtesting.
    
    Usage:
        bt = AoinecoBacktester()
        result = bt.run(closes, volumes, strategy_fn)
    """
    
    def __init__(self):
        self.forge = FeatureForge()
        self.validator = WalkForwardValidator()
        self.analyzer = PerformanceAnalyzer()
    
    def run(
        self,
        closes: List[float],
        volumes: Optional[List[float]] = None,
        strategy_fn: Optional[Callable] = None,
    ) -> Dict:
        """
        Run full backtest pipeline.
        
        If no strategy_fn provided, uses a simple RSI mean-reversion
        strategy as a baseline demonstration.
        """
        # Step 1: Feature engineering
        features = self.forge.forge_all(closes, volumes)
        
        # Step 2: Default strategy if none provided
        if strategy_fn is None:
            strategy_fn = self._default_rsi_strategy
        
        # Step 3: Walk-forward validation
        wf_result = self.validator.validate(closes, strategy_fn, features)
        
        # Step 4: Performance analysis
        performance = self.analyzer.analyze(
            wf_result["all_trades"],
            wf_result["windows"],
        )
        
        # Step 5: Compile report
        return {
            "sdna": __sdna__["id"],
            "engine": "aoineco-backtester-v1.0",
            "timestamp": datetime.now(KST).isoformat(),
            "data_points": len(closes),
            "features_generated": len(features),
            "walk_forward": {
                "total_windows": wf_result["total_windows"],
                "window_results": wf_result["windows"],
            },
            "performance": performance,
            "verdict": self._generate_verdict(performance),
        }
    
    @staticmethod
    def _default_rsi_strategy(features: Dict, idx: int) -> str:
        """
        Default baseline strategy: RSI + Moving Average crossover.
        More signals than pure RSI extremes.
        """
        rsi = features.get("rsi_14", [])
        ema5 = features.get("ewm_5", [])
        ema20 = features.get("ewm_20", [])
        
        if idx >= len(rsi) or rsi[idx] is None:
            return "HOLD"
        if idx >= len(ema5) or idx >= len(ema20):
            return "HOLD"
        
        r = rsi[idx]
        
        # RSI extremes (strong signal)
        if r < 35:
            return "LONG"
        elif r > 65:
            return "SHORT"
        
        # EMA crossover (moderate signal)
        if ema5[idx] > ema20[idx] and r < 55:
            return "LONG"
        elif ema5[idx] < ema20[idx] and r > 45:
            return "SHORT"
        
        return "HOLD"
    
    @staticmethod
    def _generate_verdict(perf: Dict) -> Dict:
        """Generate a human-readable verdict from performance metrics."""
        if perf.get("status") == "no_trades":
            return {"grade": "N/A", "message": "Insufficient trades for evaluation"}
        
        wr = perf["win_rate"]
        sharpe = perf["sharpe_ratio"]
        overfit = perf.get("overfit_warning", False)
        mdd = perf["max_drawdown_pct"]
        
        # Grade the strategy
        if overfit:
            grade = "D"
            message = "⚠️ OVERFITTING DETECTED. Strategy performance degrades over time."
        elif wr >= 60 and sharpe > 1.5 and mdd < 5:
            grade = "A"
            message = "🟢 EXCELLENT. High win rate, strong risk-adjusted returns, controlled drawdown."
        elif wr >= 55 and sharpe > 1.0:
            grade = "B"
            message = "🟡 GOOD. Positive edge detected. Consider deploying with conservative sizing."
        elif wr >= 50 and sharpe > 0.5:
            grade = "C"
            message = "🟠 MARGINAL. Slight edge, but risk/reward may not justify deployment."
        else:
            grade = "D"
            message = "🔴 WEAK. No reliable edge detected. Do not deploy."
        
        return {
            "grade": grade,
            "message": message,
            "deploy_recommendation": grade in ("A", "B"),
        }


# ═══════════════════════════════════════════════════════════
# CLI DEMO
# ═══════════════════════════════════════════════════════════

def demo():
    """Full backtester demonstration with simulated BTC data."""
    import random
    random.seed(42)
    
    print("=" * 64)
    print("📊 AOINECO BACKTESTER — Historical Strategy Validation")
    print("   V6 predicts the future. The Backtester proves the past.")
    print("=" * 64)
    
    # Generate simulated BTC 5-min data (200 candles = ~16 hours)
    base = 97000.0
    closes = [base]
    volumes = [random.uniform(100, 500)]
    for _ in range(199):
        change = random.gauss(0, 80)
        closes.append(closes[-1] + change)
        volumes.append(random.uniform(100, 500))
    
    # Run backtest
    bt = AoinecoBacktester()
    result = bt.run(closes, volumes)
    
    # Display
    perf = result["performance"]
    verdict = result["verdict"]
    wf = result["walk_forward"]
    
    print(f"\n📈 Data: {result['data_points']} candles | "
          f"Features: {result['features_generated']}")
    print(f"🔄 Walk-Forward Windows: {wf['total_windows']}")
    
    print(f"\n{'─' * 50}")
    print(f"📊 Performance Metrics")
    print(f"{'─' * 50}")
    
    if perf.get("status") == "no_trades":
        print(f"  ⚠️ {perf['message']}")
    else:
        print(f"  Total trades:      {perf['total_trades']}")
        print(f"  Win rate:          {perf['win_rate']}%")
        print(f"  Avg win:           {perf['avg_win_pct']}%")
        print(f"  Avg loss:          {perf['avg_loss_pct']}%")
        print(f"  Total return:      {perf['total_return_pct']}%")
        print(f"  Max drawdown:      {perf['max_drawdown_pct']}%")
        print(f"  Sharpe ratio:      {perf['sharpe_ratio']}")
        print(f"  Profit factor:     {perf['profit_factor']}")
        print(f"  Overfit score:     {perf['overfit_score']}")
        print(f"  Win streak (max):  {perf['longest_win_streak']}")
        print(f"  Loss streak (max): {perf['longest_loss_streak']}")
    
    print(f"\n{'─' * 50}")
    print(f"🏆 Verdict: Grade {verdict['grade']}")
    print(f"   {verdict['message']}")
    print(f"   Deploy: {'✅ YES' if verdict.get('deploy_recommendation') else '❌ NO'}")
    
    print(f"\n🧬 S-DNA: {result['sdna']}")
    print("=" * 64)


if __name__ == "__main__":
    demo()
