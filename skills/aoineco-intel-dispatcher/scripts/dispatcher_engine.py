#!/usr/bin/env python3
"""
/* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */
S-DNA: AOI-2026-0213-SDNA-ID01

Aoineco Intelligence Dispatcher — Autonomous LLM Routing Engine

THE PROBLEM:
  In a multi-agent system, using the same LLM for every task is like
  hiring a brain surgeon to take out the trash. It works, but you're
  burning money and talent on the wrong job.

THE SOLUTION:
  The Intelligence Dispatcher automatically routes each task to the
  optimal LLM based on 5 factors:

  1. AGENT ROLE      — Who is asking? (Eye needs speed, Brain needs depth)
  2. TASK COMPLEXITY  — What are they doing? (Chat vs Architecture design)
  3. TOKEN BUDGET     — How much can we spend? ($7 Bootstrap constraint)
  4. PERFORMANCE      — Which model performed best on similar tasks before?
  5. CASCADE LOGIC    — Start cheap, escalate only when needed.

ARCHITECTURE:
  ┌─────────────────────────────────────────────────────────┐
  │                 INTELLIGENCE DISPATCHER                  │
  │                                                         │
  │  ┌──────────┐   ┌──────────────┐   ┌───────────────┐   │
  │  │ Task     │──▶│ Agent×Model  │──▶│ Budget        │   │
  │  │ Classifier│   │ Affinity     │   │ Governor      │   │
  │  │ (5 tiers)│   │ Matrix       │   │ ($7 cap)      │   │
  │  └──────────┘   └──────────────┘   └───────┬───────┘   │
  │                                             │           │
  │  ┌──────────────────────────────────────────┴────────┐  │
  │  │              CASCADE ROUTER                        │  │
  │  │  Try Tier 1 (cheapest) → if insufficient,         │  │
  │  │  escalate to Tier 2 → ... → Tier 4 (most capable) │  │
  │  └───────────────────────────────────────────────────┘  │
  │                          │                              │
  │  ┌───────────────────────┴───────────────────────────┐  │
  │  │           PERFORMANCE MEMORY                       │  │
  │  │  Records which model worked best for each          │  │
  │  │  (agent, task_type) pair → refines future routing  │  │
  │  └───────────────────────────────────────────────────┘  │
  └─────────────────────────────────────────────────────────┘

USAGE:
  Single-agent mode:
    dispatcher.route(task="Analyze this GitHub repo", agent="blue_eye")
    → Returns: {"model": "gemini-3-pro", "reason": "...", "tier": 2}

  Multi-agent mode:
    dispatcher.route_squad(tasks=[
        {"agent": "blue_eye", "task": "Fetch BTC data"},
        {"agent": "blue_brain", "task": "Fuse signals via Bayesian"},
        {"agent": "blue_blade", "task": "Scan code for backdoors"},
    ])
    → Returns optimal model for EACH agent based on their specific task.

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import json
import math
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Literal
from datetime import datetime, timezone, timedelta

# ─── S-DNA ──────────────────────────────────────────────
__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-ID01",
    "author_agent": "blue_brain",
    "org": "aoineco-co",
    "created": "2026-02-13T15:05:00+09:00",
    "tier": "core-infrastructure",
    "classification": "open",
}

KST = timezone(timedelta(hours=9))


# ═══════════════════════════════════════════════════════════
# MODEL REGISTRY
# ═══════════════════════════════════════════════════════════

@dataclass
class ModelSpec:
    """Specification for a single LLM model."""
    id: str                      # e.g., "google/gemini-3-flash-preview"
    alias: str                   # e.g., "gemini-flash"
    provider: str                # "google", "openrouter", "anthropic"
    tier: int                    # 1=cheapest, 4=most capable
    cost_per_1k_input: float     # USD per 1K input tokens (estimate)
    cost_per_1k_output: float    # USD per 1K output tokens (estimate)
    tpm_limit: int               # Tokens per minute
    context_window: int          # Max context size
    strengths: List[str]         # What this model excels at
    weaknesses: List[str]        # Where this model struggles
    requires_approval: bool      # L3 Chairman approval needed?


MODEL_REGISTRY: Dict[str, ModelSpec] = {
    "gemini-flash": ModelSpec(
        id="google/gemini-3-flash-preview",
        alias="gemini-flash",
        provider="google",
        tier=1,
        cost_per_1k_input=0.00010,
        cost_per_1k_output=0.00040,
        tpm_limit=1_000_000,
        context_window=1_000_000,
        strengths=["speed", "cost", "high_throughput", "simple_chat", "data_scan"],
        weaknesses=["complex_reasoning", "nuanced_writing", "architecture_design"],
        requires_approval=False,
    ),
    "gemini-pro": ModelSpec(
        id="google/gemini-3-pro-preview",
        alias="gemini-pro",
        provider="google",
        tier=2,
        cost_per_1k_input=0.00125,
        cost_per_1k_output=0.00500,
        tpm_limit=1_000_000,
        context_window=1_000_000,
        strengths=["code_analysis", "large_document", "reasoning", "structured_output"],
        weaknesses=["cost_for_simple_tasks", "overkill_for_chat"],
        requires_approval=False,
    ),
    "claude-sonnet": ModelSpec(
        id="openrouter/anthropic/claude-sonnet-4",
        alias="claude-sonnet",
        provider="openrouter",
        tier=3,
        cost_per_1k_input=0.00300,
        cost_per_1k_output=0.01500,
        tpm_limit=80_000,
        context_window=200_000,
        strengths=["nuanced_writing", "security_audit", "final_review", "precision"],
        weaknesses=["tpm_limited", "expensive_for_bulk"],
        requires_approval=True,
    ),
    "claude-opus": ModelSpec(
        id="openrouter/anthropic/claude-opus-4.6",
        alias="claude-opus",
        provider="openrouter",
        tier=4,
        cost_per_1k_input=0.01500,
        cost_per_1k_output=0.07500,
        tpm_limit=200_000,
        context_window=1_000_000,
        strengths=["architecture_design", "whitepaper", "deep_strategy", "complex_code"],
        weaknesses=["very_expensive", "overkill_for_routine"],
        requires_approval=True,
    ),
    "deepseek": ModelSpec(
        id="openrouter/deepseek/deepseek-chat-v3.1",
        alias="deepseek",
        provider="openrouter",
        tier=1,
        cost_per_1k_input=0.00014,
        cost_per_1k_output=0.00028,
        tpm_limit=500_000,
        context_window=128_000,
        strengths=["cost", "code_generation", "reasoning_for_price"],
        weaknesses=["context_limit", "occasional_hallucination"],
        requires_approval=False,
    ),
    "claude-haiku": ModelSpec(
        id="anthropic/claude-haiku-4-5",
        alias="claude-haiku",
        provider="anthropic",
        tier=1,
        cost_per_1k_input=0.00080,
        cost_per_1k_output=0.00400,
        tpm_limit=50_000,
        context_window=200_000,
        strengths=["logic", "security_scan", "quick_code_review", "precision_for_price"],
        weaknesses=["severe_tpm_limit", "no_heavy_context"],
        requires_approval=False,
    ),
}


# ═══════════════════════════════════════════════════════════
# AGENT AFFINITY MATRIX
# ═══════════════════════════════════════════════════════════
# Maps each agent to their preferred models, ranked by affinity.
# Affinity = how well a model matches the agent's role.
# ═══════════════════════════════════════════════════════════

AGENT_AFFINITY: Dict[str, List[Tuple[str, float]]] = {
    # (model_alias, affinity_score 0.0~1.0)

    "blue_eye": [
        # Eye needs SPEED for high-frequency data scanning
        # Pro only for deep TA with large candle sets (tier 3+)
        ("gemini-flash", 0.95),
        ("deepseek", 0.70),
        ("gemini-pro", 0.65),
    ],
    "blue_sound": [
        # Sound does sentiment — needs nuance but volume is high
        ("gemini-flash", 0.85),
        ("gemini-pro", 0.70),
        ("deepseek", 0.60),
    ],
    "blue_blade": [
        # Blade needs PRECISION for security scanning
        ("claude-haiku", 0.90),
        ("gemini-flash", 0.75),
        ("claude-sonnet", 0.95),  # Best but expensive
    ],
    "blue_brain": [
        # Brain needs DEPTH — but Pro handles 90% of fusion tasks.
        # OPUS reserved only for architecture-level design (requires approval).
        ("gemini-pro", 0.95),
        ("gemini-flash", 0.65),  # Can handle routine fusion
        ("claude-opus", 0.60),   # Only when task_tier >= 5
    ],
    "blue_flash": [
        # Flash needs SPEED above all — execution latency matters
        ("gemini-flash", 0.98),
        ("deepseek", 0.75),
    ],
    "blue_record": [
        # Record does archival — lightweight, structured output
        ("gemini-flash", 0.90),
        ("deepseek", 0.80),
    ],
    "oracle": [
        # Oracle needs JUDGMENT — macro regime, veto decisions
        ("gemini-pro", 0.85),
        ("claude-sonnet", 0.90),
        ("claude-opus", 0.80),
    ],
    "blue_gear": [
        # Gear monitors infra — simple checks, low cost
        ("gemini-flash", 0.95),
        ("deepseek", 0.80),
    ],
    "blue_med": [
        # Med does risk calculation — needs math precision
        ("gemini-pro", 0.85),
        ("gemini-flash", 0.70),
        ("claude-haiku", 0.75),
    ],

    # ─── Single-Agent Mode (generic) ─────────────────
    "generic": [
        ("gemini-flash", 0.80),
        ("gemini-pro", 0.70),
        ("deepseek", 0.65),
        ("claude-haiku", 0.60),
        ("claude-sonnet", 0.50),
        ("claude-opus", 0.40),
    ],
}


# ═══════════════════════════════════════════════════════════
# TASK COMPLEXITY CLASSIFIER
# ═══════════════════════════════════════════════════════════

class TaskClassifier:
    """
    Classifies a task description into 5 complexity tiers.

    Tier 1 — TRIVIAL: Simple chat, status check, greeting
    Tier 2 — ROUTINE: Data fetch, formatting, simple analysis
    Tier 3 — MODERATE: Code review, document analysis, multi-step reasoning
    Tier 4 — COMPLEX: Architecture design, security audit, deep strategy
    Tier 5 — CRITICAL: Final review, whitepaper, system-wide decisions

    Method: Keyword-weighted scoring (no LLM needed — zero cost).
    """

    TIER_KEYWORDS = {
        5: {
            "keywords": [
                "whitepaper", "architecture", "design system", "final review",
                "strategic", "tokenomics", "protocol design", "security audit",
                "cryptographic", "rewrite entire", "masterplan", "roadmap",
            ],
            "weight": 5.0,
        },
        4: {
            "keywords": [
                "refactor entire", "implement new system", "complex architecture",
                "design protocol", "deep dive analysis", "rewrite engine",
                "handshake protocol", "encryption scheme", "guardian redesign",
            ],
            "weight": 3.0,
        },
        3: {
            "keywords": [
                "analyze", "code review", "document", "github", "debug", "test",
                "script", "function", "class", "module", "api", "integrate",
                "compare", "evaluate", "summarize long", "bayesian", "fusion",
                "monte carlo", "optimize", "implement", "engine", "pipeline",
            ],
            "weight": 2.0,
        },
        2: {
            "keywords": [
                "fetch", "check", "list", "status", "format", "convert",
                "simple", "quick", "update", "edit", "rename", "move",
                "search", "find", "count", "calculate",
            ],
            "weight": 1.0,
        },
        1: {
            "keywords": [
                "hello", "hi", "hey", "thanks", "ok", "yes", "no",
                "chat", "how are you", "good morning", "헬로", "안녕",
            ],
            "weight": 0.5,
        },
    }

    # Complexity multipliers for task characteristics
    LENGTH_THRESHOLDS = [
        (50, 0),       # Very short → no bonus
        (200, 0.5),    # Medium → slight complexity bump
        (500, 1.0),    # Long description → likely complex
        (1000, 1.5),   # Very long → definitely complex
    ]

    @classmethod
    def classify(cls, task: str) -> Dict:
        """
        Classify a task and return tier + confidence + reasoning.
        """
        task_lower = task.lower()
        scores = {tier: 0.0 for tier in range(1, 6)}

        # Keyword matching
        for tier, config in cls.TIER_KEYWORDS.items():
            for keyword in config["keywords"]:
                if keyword in task_lower:
                    scores[tier] += config["weight"]

        # Length bonus
        task_len = len(task)
        length_bonus = 0
        for threshold, bonus in cls.LENGTH_THRESHOLDS:
            if task_len >= threshold:
                length_bonus = bonus
        
        # Apply length bonus to tiers 3+
        for tier in [3, 4, 5]:
            scores[tier] += length_bonus

        # Find winning tier
        max_score = max(scores.values())
        if max_score == 0:
            # No keywords matched — default to tier 2 (routine)
            winning_tier = 2
            confidence = 0.50
        else:
            winning_tier = max(scores, key=scores.get)
            total = sum(scores.values())
            confidence = max_score / total if total > 0 else 0.5

        # Map tier to required model tier
        model_tier_map = {
            1: 1,  # Trivial → cheapest model
            2: 1,  # Routine → still cheap
            3: 2,  # Moderate → mid-tier
            4: 3,  # Complex → high-tier
            5: 4,  # Critical → top-tier
        }

        return {
            "task_tier": winning_tier,
            "min_model_tier": model_tier_map[winning_tier],
            "confidence": round(confidence, 4),
            "scores": {k: round(v, 2) for k, v in scores.items()},
            "task_length": task_len,
        }


# ═══════════════════════════════════════════════════════════
# TOKEN BUDGET GOVERNOR
# ═══════════════════════════════════════════════════════════

@dataclass
class BudgetState:
    """Tracks daily token spending against $7 Bootstrap budget."""
    daily_budget_usd: float = 2.00    # Target daily operational cost
    spent_today_usd: float = 0.0
    tokens_in_today: int = 0
    tokens_out_today: int = 0
    requests_today: int = 0
    date: str = ""

    def __post_init__(self):
        if not self.date:
            self.date = datetime.now(KST).strftime("%Y-%m-%d")

    @property
    def remaining_usd(self) -> float:
        return max(0, self.daily_budget_usd - self.spent_today_usd)

    @property
    def usage_percent(self) -> float:
        if self.daily_budget_usd == 0:
            return 100.0
        return round(self.spent_today_usd / self.daily_budget_usd * 100, 1)

    def can_afford(self, model: ModelSpec, estimated_tokens: int) -> bool:
        """Check if we can afford a request with this model."""
        estimated_cost = (
            (estimated_tokens / 1000) * model.cost_per_1k_input +
            (estimated_tokens * 0.3 / 1000) * model.cost_per_1k_output  # ~30% output ratio
        )
        return estimated_cost <= self.remaining_usd

    def record_usage(self, model: ModelSpec, tokens_in: int, tokens_out: int):
        """Record a completed request's cost."""
        cost = (
            (tokens_in / 1000) * model.cost_per_1k_input +
            (tokens_out / 1000) * model.cost_per_1k_output
        )
        self.spent_today_usd += cost
        self.tokens_in_today += tokens_in
        self.tokens_out_today += tokens_out
        self.requests_today += 1


class BudgetGovernor:
    """
    Enforces the $7 Bootstrap Protocol's daily budget.

    Rules:
    1. If budget > 70% remaining → allow any affordable model
    2. If budget 30-70% remaining → prefer tier 1-2 only
    3. If budget < 30% remaining → force tier 1 (survival mode)
    4. If budget exhausted → emergency: only free/cached responses
    """

    def __init__(self, state: Optional[BudgetState] = None):
        self.state = state or BudgetState()

    def get_max_tier(self) -> int:
        """Get the maximum model tier allowed by current budget."""
        pct = self.state.usage_percent

        if pct < 30:
            return 4  # Plenty of budget — any tier OK
        elif pct < 70:
            return 2  # Moderate — stick to cheap models
        elif pct < 100:
            return 1  # Tight — survival mode
        else:
            return 1  # Exhausted — absolute minimum

    def get_budget_status(self) -> Dict:
        return {
            "daily_budget": self.state.daily_budget_usd,
            "spent": round(self.state.spent_today_usd, 4),
            "remaining": round(self.state.remaining_usd, 4),
            "usage_percent": self.state.usage_percent,
            "max_tier_allowed": self.get_max_tier(),
            "requests_today": self.state.requests_today,
            "tokens_today": self.state.tokens_in_today + self.state.tokens_out_today,
            "mode": (
                "NORMAL" if self.state.usage_percent < 30 else
                "CONSERVATIVE" if self.state.usage_percent < 70 else
                "SURVIVAL" if self.state.usage_percent < 100 else
                "EMERGENCY"
            ),
        }


# ═══════════════════════════════════════════════════════════
# PERFORMANCE MEMORY
# ═══════════════════════════════════════════════════════════

class PerformanceMemory:
    """
    Tracks which models performed best for each (agent, task_type) pair.

    Uses a simple Bayesian scoring system:
    - Each (agent, model, task_tier) triple has a Beta(α, β) prior
    - Success (fast + good output) → α += 1
    - Failure (slow, error, poor output) → β += 1
    - Score = α / (α + β)

    Over time, the system learns:
    "Blue-Eye works best with Flash for tier-2 tasks"
    "Blue-Brain works best with Pro for tier-4 tasks"
    """

    def __init__(self):
        # Key: (agent_id, model_alias, task_tier) → {"alpha": float, "beta": float}
        self.records: Dict[str, Dict[str, float]] = {}

    def _key(self, agent_id: str, model_alias: str, task_tier: int) -> str:
        return f"{agent_id}:{model_alias}:{task_tier}"

    def record_outcome(self, agent_id: str, model_alias: str,
                       task_tier: int, success: bool):
        """Record a routing outcome."""
        key = self._key(agent_id, model_alias, task_tier)
        if key not in self.records:
            self.records[key] = {"alpha": 1.0, "beta": 1.0}

        if success:
            self.records[key]["alpha"] += 1
        else:
            self.records[key]["beta"] += 1

    def get_score(self, agent_id: str, model_alias: str, task_tier: int) -> float:
        """Get Bayesian trust score for a routing combination."""
        key = self._key(agent_id, model_alias, task_tier)
        if key not in self.records:
            return 0.5  # Neutral prior
        r = self.records[key]
        return r["alpha"] / (r["alpha"] + r["beta"])

    def get_best_model(self, agent_id: str, task_tier: int,
                       candidates: List[str]) -> Optional[str]:
        """Find the historically best-performing model for this agent+tier."""
        if not candidates:
            return None

        scores = {
            model: self.get_score(agent_id, model, task_tier)
            for model in candidates
        }
        best = max(scores, key=scores.get)
        # Only use memory if we have strong evidence (score > 0.6)
        if scores[best] > 0.6:
            return best
        return None  # Not enough data — fall back to affinity matrix

    def export_state(self) -> Dict:
        return {
            "records": self.records,
            "total_entries": len(self.records),
            "exported_at": datetime.now(KST).isoformat(),
        }


# ═══════════════════════════════════════════════════════════
# CASCADE ROUTER
# ═══════════════════════════════════════════════════════════

class CascadeRouter:
    """
    The cascade routing strategy:

    1. Start with the cheapest model that meets the minimum tier.
    2. If the task actually needs more capability, escalate.
    3. Never exceed the budget governor's max tier.
    4. If performance memory has a strong signal, use that instead.

    This ensures we NEVER overspend while still getting quality
    when we need it.
    """

    @staticmethod
    def select(
        min_tier: int,
        max_tier: int,
        agent_id: str,
        affinity: List[Tuple[str, float]],
        memory_recommendation: Optional[str],
    ) -> Tuple[str, str]:
        """
        Select the optimal model.
        Returns (model_alias, reason).
        """
        # If performance memory has a strong recommendation, prefer it
        if memory_recommendation and memory_recommendation in MODEL_REGISTRY:
            model = MODEL_REGISTRY[memory_recommendation]
            if min_tier <= model.tier <= max_tier:
                return (
                    memory_recommendation,
                    f"Performance memory recommends {memory_recommendation} "
                    f"for {agent_id} (proven track record)"
                )

        # Filter affinity list by tier constraints
        valid_candidates = []
        for model_alias, affinity_score in affinity:
            if model_alias not in MODEL_REGISTRY:
                continue
            model = MODEL_REGISTRY[model_alias]
            if min_tier <= model.tier <= max_tier:
                valid_candidates.append((model_alias, affinity_score, model.tier))

        if not valid_candidates:
            # Fallback: find ANY model in the tier range
            for alias, spec in MODEL_REGISTRY.items():
                if min_tier <= spec.tier <= max_tier:
                    return (alias, f"Fallback selection (no affinity match in tier {min_tier}-{max_tier})")
            # Ultimate fallback
            return ("gemini-flash", "Emergency fallback — no model matched constraints")

        # Sort by: lowest tier first (cheapest), then highest affinity
        valid_candidates.sort(key=lambda x: (x[2], -x[1]))

        # Pick the cheapest model with acceptable affinity (> 0.6)
        for alias, aff, tier in valid_candidates:
            if aff >= 0.6:
                return (
                    alias,
                    f"Cascade selected {alias} (tier={tier}, affinity={aff:.2f}, "
                    f"cheapest viable for {agent_id})"
                )

        # If no high-affinity match, just take the cheapest
        best = valid_candidates[0]
        return (
            best[0],
            f"Cascade selected {best[0]} (tier={best[2]}, affinity={best[1]:.2f}, "
            f"best available for {agent_id})"
        )


# ═══════════════════════════════════════════════════════════
# MAIN DISPATCHER
# ═══════════════════════════════════════════════════════════

class IntelligenceDispatcher:
    """
    The master orchestrator.

    Usage (Single Agent):
        dispatcher = IntelligenceDispatcher()
        result = dispatcher.route(task="Analyze this code", agent="blue_brain")

    Usage (Multi Agent):
        results = dispatcher.route_squad([
            {"agent": "blue_eye", "task": "Fetch BTC 5m data"},
            {"agent": "blue_brain", "task": "Run Bayesian fusion on 6 signals"},
            {"agent": "blue_blade", "task": "Scan omega_fusion.py for backdoors"},
        ])
    """

    def __init__(
        self,
        budget: Optional[BudgetState] = None,
        memory: Optional[PerformanceMemory] = None,
    ):
        self.classifier = TaskClassifier()
        self.governor = BudgetGovernor(budget)
        self.memory = memory or PerformanceMemory()
        self.cascade = CascadeRouter()

    def route(self, task: str, agent: str = "generic",
              context_tokens: int = 10_000) -> Dict:
        """
        Route a single task to the optimal model.

        Args:
            task: Description of what needs to be done
            agent: Agent ID (e.g., "blue_eye", "blue_brain", or "generic")
            context_tokens: Estimated current context size

        Returns:
            Routing decision with model, reason, cost estimate, etc.
        """
        # Step 1: Classify task complexity
        classification = self.classifier.classify(task)
        min_tier = classification["min_model_tier"]

        # Step 2: Check budget constraints
        max_tier = self.governor.get_max_tier()

        # Step 3: Check performance memory
        affinity = AGENT_AFFINITY.get(agent, AGENT_AFFINITY["generic"])
        candidate_aliases = [alias for alias, _ in affinity]
        memory_rec = self.memory.get_best_model(
            agent, classification["task_tier"], candidate_aliases
        )

        # Step 4: Cascade route
        selected_model, reason = self.cascade.select(
            min_tier=min_tier,
            max_tier=max_tier,
            agent_id=agent,
            affinity=affinity,
            memory_recommendation=memory_rec,
        )

        # Step 5: Validate against context size
        model_spec = MODEL_REGISTRY.get(selected_model)
        if model_spec and context_tokens > model_spec.tpm_limit * 0.8:
            # Context too large for this model — find a bigger one
            for alias, spec in sorted(MODEL_REGISTRY.items(),
                                       key=lambda x: x[1].tier):
                if (spec.tier <= max_tier and
                        context_tokens < spec.tpm_limit * 0.8):
                    selected_model = alias
                    model_spec = spec
                    reason += f" [Upgraded from context pressure: {context_tokens} tok]"
                    break

        # Step 6: Check approval requirement
        needs_approval = model_spec.requires_approval if model_spec else False

        # Step 7: Estimate cost
        estimated_cost = 0.0
        if model_spec:
            estimated_cost = (
                (context_tokens / 1000) * model_spec.cost_per_1k_input +
                (context_tokens * 0.3 / 1000) * model_spec.cost_per_1k_output
            )

        return {
            "model": selected_model,
            "model_id": model_spec.id if model_spec else None,
            "model_tier": model_spec.tier if model_spec else None,
            "provider": model_spec.provider if model_spec else None,
            "agent": agent,
            "task_classification": classification,
            "reason": reason,
            "needs_approval": needs_approval,
            "estimated_cost_usd": round(estimated_cost, 6),
            "budget_status": self.governor.get_budget_status(),
            "memory_recommendation": memory_rec,
            "timestamp": datetime.now(KST).isoformat(),
            "sdna": __sdna__["id"],
        }

    def route_squad(self, tasks: List[Dict]) -> List[Dict]:
        """
        Route multiple agent tasks simultaneously.

        Args:
            tasks: List of {"agent": str, "task": str, "context_tokens": int}

        Returns:
            List of routing decisions, one per task.
        """
        results = []
        for task_spec in tasks:
            result = self.route(
                task=task_spec["task"],
                agent=task_spec.get("agent", "generic"),
                context_tokens=task_spec.get("context_tokens", 10_000),
            )
            results.append(result)
        return results

    def record_outcome(self, agent: str, model_alias: str,
                       task_tier: int, success: bool,
                       tokens_in: int = 0, tokens_out: int = 0):
        """Record the outcome of a routing decision for learning."""
        self.memory.record_outcome(agent, model_alias, task_tier, success)
        if model_alias in MODEL_REGISTRY:
            self.governor.state.record_usage(
                MODEL_REGISTRY[model_alias], tokens_in, tokens_out
            )


# ═══════════════════════════════════════════════════════════
# CLI DEMO
# ═══════════════════════════════════════════════════════════

def demo():
    """Full Intelligence Dispatcher demonstration."""
    print("=" * 64)
    print("🧠 AOINECO INTELLIGENCE DISPATCHER")
    print("   The Right Brain for the Right Job.")
    print("   $7 Bootstrap Protocol — Every Token Counts.")
    print("=" * 64)

    dispatcher = IntelligenceDispatcher()

    # ─── Demo 1: Single Agent Routing ─────────────────
    print("\n📡 Demo 1: Single Agent Routing")
    print("-" * 50)

    test_cases = [
        ("blue_eye", "Fetch BTC-USD 5-minute OHLCV data from yfinance"),
        ("blue_brain", "Run Bayesian log-odds fusion on 6 agent signals with confidence weighting"),
        ("blue_blade", "Scan omega_fusion.py for backdoor patterns and unauthorized network calls"),
        ("oracle", "Determine current macro regime and decide whether to veto the SHORT verdict"),
        ("generic", "Hello, how are you?"),
        ("generic", "Design the complete architecture for a cross-chain agent communication protocol with encrypted handshakes"),
    ]

    for agent, task in test_cases:
        result = dispatcher.route(task=task, agent=agent)
        approval = " ⚠️ NEEDS APPROVAL" if result["needs_approval"] else ""
        print(f"\n  🤖 {agent}: \"{task[:50]}...\"")
        print(f"     → 🧠 {result['model']} (Tier {result['model_tier']}){approval}")
        print(f"     → 💡 {result['reason'][:80]}...")
        print(f"     → 💰 Est. cost: ${result['estimated_cost_usd']:.6f}")

    # ─── Demo 2: Squad Routing ────────────────────────
    print(f"\n\n📡 Demo 2: Full Squad Routing (V6 Pipeline)")
    print("-" * 50)

    squad_tasks = [
        {"agent": "blue_eye", "task": "Analyze 67 candles of BTC 5m data with RSI, MACD, Bollinger"},
        {"agent": "blue_sound", "task": "Score sentiment from price momentum and volume ratio"},
        {"agent": "blue_blade", "task": "Detect volume anomalies via Z-score analysis"},
        {"agent": "blue_flash", "task": "Calculate price velocity and acceleration for momentum"},
        {"agent": "oracle", "task": "Classify macro regime using SMA trend and RSI levels"},
        {"agent": "blue_med", "task": "Assess volatility regime and Bollinger squeeze status"},
        {"agent": "blue_brain", "task": "Execute Bayesian log-odds fusion across all signals"},
        {"agent": "blue_record", "task": "Archive the verdict to JSON with timestamp"},
    ]

    results = dispatcher.route_squad(squad_tasks)

    total_cost = 0
    for r in results:
        approval = " ⚠️" if r["needs_approval"] else ""
        print(f"  {r['agent']:15s} → {r['model']:15s} (T{r['model_tier']}){approval}"
              f"  ${r['estimated_cost_usd']:.6f}")
        total_cost += r["estimated_cost_usd"]

    print(f"\n  {'─' * 50}")
    print(f"  💰 Total estimated cost for 1 pipeline run: ${total_cost:.6f}")
    print(f"  📊 Runs per day (hourly): ~24")
    print(f"  💵 Estimated daily cost: ${total_cost * 24:.4f}")

    # ─── Demo 3: Budget Status ────────────────────────
    print(f"\n\n📡 Demo 3: Budget Governor Status")
    print("-" * 50)
    budget = dispatcher.governor.get_budget_status()
    for k, v in budget.items():
        print(f"  {k}: {v}")

    print(f"\n🧬 S-DNA: {__sdna__['id']}")
    print("=" * 64)


if __name__ == "__main__":
    demo()
