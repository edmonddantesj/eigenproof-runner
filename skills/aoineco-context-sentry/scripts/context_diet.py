#!/usr/bin/env python3
"""
/* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */
S-DNA: AOI-2026-0213-SDNA-CD01

Aoineco Context Diet — Workspace File Obesity Scanner

PROBLEM (Real-world, 2026-02-13):
  OpenClaw injects workspace files (MEMORY.md, SOUL.md, etc.) into
  EVERY LLM request as system context. When these files grow large,
  a simple "hello" message can consume 149,237 input tokens — 
  exceeding Claude Haiku's 50K TPM limit on a single request.

SOLUTION:
  This module scans all auto-injected workspace files, measures their
  token cost, and produces actionable recommendations:
  1. Flag files exceeding size thresholds
  2. Identify candidates for archival (move to memory/*.md)
  3. Calculate total "context tax" — the fixed token cost per request
  4. Estimate compatibility with each model's TPM limits

LESSON LEARNED:
  Context bloat is the #1 silent killer of multi-model agent systems.
  It doesn't crash — it silently degrades. You only notice when you
  switch to a model with tighter limits and get 429 errors.

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import os
import json
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timezone, timedelta

__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-CD01",
    "author_agent": "blue_gear",
    "org": "aoineco-co",
    "created": "2026-02-13T14:20:00+09:00",
    "tier": "core-infrastructure",
    "classification": "open",
    "parent": "AOI-2026-0213-SDNA-CS01",
}

KST = timezone(timedelta(hours=9))

# ═══════════════════════════════════════════════════════════
# MODEL TPM LIMITS (Known as of 2026-02)
# ═══════════════════════════════════════════════════════════

MODEL_LIMITS = {
    "gemini-3-flash": {
        "tpm": 1_000_000,
        "rpm": 1_000,
        "context_window": 1_000_000,
    },
    "gemini-3-pro": {
        "tpm": 1_000_000,
        "rpm": 1_000,
        "context_window": 1_000_000,
    },
    "claude-haiku-4.5": {
        "tpm": 50_000,
        "rpm": 50,
        "context_window": 200_000,
    },
    "claude-sonnet-4": {
        "tpm": 80_000,
        "rpm": 50,
        "context_window": 200_000,
    },
    "claude-opus-4.6": {
        "tpm": 200_000,
        "rpm": 50,
        "context_window": 1_000_000,
    },
    "deepseek-3.1": {
        "tpm": 500_000,
        "rpm": 200,
        "context_window": 128_000,
    },
}

# ═══════════════════════════════════════════════════════════
# WORKSPACE FILES THAT GET AUTO-INJECTED
# ═══════════════════════════════════════════════════════════

# These files are loaded by OpenClaw into EVERY request's system prompt.
# Their combined size is the "context tax" — the minimum token cost
# before any user message or conversation history is added.
AUTO_INJECTED_FILES = [
    "AGENTS.md",
    "SOUL.md",
    "TOOLS.md",
    "IDENTITY.md",
    "USER.md",
    "HEARTBEAT.md",
    "BOOTSTRAP.md",
    "MEMORY.md",
    "CURRENT_STATE.md",
]

# OpenClaw system prompt overhead (estimated)
SYSTEM_PROMPT_OVERHEAD_TOKENS = 4_000

# Average conversation history per active session
AVG_HISTORY_TOKENS = {
    "fresh_session": 0,
    "light_session": 20_000,
    "medium_session": 60_000,
    "heavy_session": 120_000,
}


# ═══════════════════════════════════════════════════════════
# TOKEN ESTIMATION
# ═══════════════════════════════════════════════════════════

def estimate_tokens(text: str) -> int:
    """
    Estimate token count from text.
    
    Rule of thumb:
    - English: ~4 chars per token
    - Korean/CJK: ~2-3 chars per token (more tokens per char)
    - Mixed: ~3 chars per token (conservative)
    
    We use 3 chars/token as a safe conservative estimate.
    """
    return max(1, len(text.encode("utf-8")) // 3)


def estimate_tokens_from_file(filepath: str) -> int:
    """Estimate tokens from a file path."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return estimate_tokens(f.read())
    except (FileNotFoundError, PermissionError):
        return 0


# ═══════════════════════════════════════════════════════════
# CONTEXT DIET SCANNER
# ═══════════════════════════════════════════════════════════

@dataclass
class FileReport:
    filename: str
    exists: bool
    bytes_size: int
    est_tokens: int
    recommendation: str
    priority: str  # "critical", "warning", "ok", "delete"


class ContextDietScanner:
    """
    Scans workspace files and produces a diet plan.
    
    Thresholds:
    - CRITICAL: Single file > 5,000 tokens (bloated)
    - WARNING:  Single file > 2,000 tokens (could trim)
    - OK:       Single file ≤ 2,000 tokens (healthy)
    - DELETE:   File exists but serves no current purpose
    """
    
    CRITICAL_THRESHOLD = 5_000  # tokens
    WARNING_THRESHOLD = 2_000   # tokens
    
    def __init__(self, workspace_dir: str):
        self.workspace_dir = workspace_dir
    
    def scan(self) -> Dict:
        """Run full context diet scan."""
        reports: List[FileReport] = []
        total_tokens = 0
        
        for filename in AUTO_INJECTED_FILES:
            filepath = os.path.join(self.workspace_dir, filename)
            exists = os.path.exists(filepath)
            
            if not exists:
                reports.append(FileReport(
                    filename=filename,
                    exists=False,
                    bytes_size=0,
                    est_tokens=0,
                    recommendation="File not found (good if intentionally removed)",
                    priority="ok",
                ))
                continue
            
            size = os.path.getsize(filepath)
            tokens = estimate_tokens_from_file(filepath)
            total_tokens += tokens
            
            # Classify
            if filename == "BOOTSTRAP.md":
                rec = "DELETE: Only needed for first-time setup. Remove to save tokens."
                priority = "delete"
            elif tokens > self.CRITICAL_THRESHOLD:
                rec = (f"CRITICAL: {tokens} tokens is too heavy for auto-injection. "
                       f"Archive detail to memory/*.md and keep only essential rules.")
                priority = "critical"
            elif tokens > self.WARNING_THRESHOLD:
                rec = (f"WARNING: {tokens} tokens. Consider trimming verbose sections "
                       f"or moving reference material to searchable memory files.")
                priority = "warning"
            else:
                rec = f"OK: {tokens} tokens — healthy size."
                priority = "ok"
            
            reports.append(FileReport(
                filename=filename,
                exists=True,
                bytes_size=size,
                est_tokens=tokens,
                recommendation=rec,
                priority=priority,
            ))
        
        # System overhead
        total_context_tax = total_tokens + SYSTEM_PROMPT_OVERHEAD_TOKENS
        
        # Model compatibility check
        compatibility = {}
        for model_name, limits in MODEL_LIMITS.items():
            for session_type, hist_tokens in AVG_HISTORY_TOKENS.items():
                total_request = total_context_tax + hist_tokens
                fits = total_request < limits["tpm"]
                
                if model_name not in compatibility:
                    compatibility[model_name] = {}
                
                compatibility[model_name][session_type] = {
                    "total_tokens": total_request,
                    "tpm_limit": limits["tpm"],
                    "fits": fits,
                    "headroom_pct": round(
                        (1 - total_request / limits["tpm"]) * 100, 1
                    ) if fits else round(
                        (total_request / limits["tpm"] - 1) * -100, 1
                    ),
                }
        
        return {
            "timestamp": datetime.now(KST).isoformat(),
            "workspace": self.workspace_dir,
            "files": [
                {
                    "name": r.filename,
                    "exists": r.exists,
                    "bytes": r.bytes_size,
                    "est_tokens": r.est_tokens,
                    "priority": r.priority,
                    "recommendation": r.recommendation,
                }
                for r in reports
            ],
            "summary": {
                "total_file_tokens": total_tokens,
                "system_overhead_tokens": SYSTEM_PROMPT_OVERHEAD_TOKENS,
                "total_context_tax": total_context_tax,
                "files_scanned": len(reports),
                "critical_count": sum(1 for r in reports if r.priority == "critical"),
                "warning_count": sum(1 for r in reports if r.priority == "warning"),
                "delete_count": sum(1 for r in reports if r.priority == "delete"),
            },
            "model_compatibility": compatibility,
            "sdna": __sdna__["id"],
        }


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    import sys
    
    workspace = sys.argv[1] if len(sys.argv) > 1 else "/Users/silkroadcat/.openclaw/workspace"
    
    scanner = ContextDietScanner(workspace)
    result = scanner.scan()
    
    print("=" * 60)
    print("🍎 AOINECO CONTEXT DIET — Workspace Obesity Report")
    print("   Every token in system prompt costs you on EVERY request.")
    print("=" * 60)
    
    # File breakdown
    print(f"\n📁 Files Scanned: {result['summary']['files_scanned']}")
    print("-" * 60)
    
    for f in result["files"]:
        if not f["exists"]:
            icon = "⬜"
        elif f["priority"] == "critical":
            icon = "🔴"
        elif f["priority"] == "warning":
            icon = "🟡"
        elif f["priority"] == "delete":
            icon = "🗑️"
        else:
            icon = "🟢"
        
        print(f"  {icon} {f['name']:25s} {f['est_tokens']:>6,} tok  ({f['bytes']:>6,} bytes)")
        if f["priority"] in ("critical", "warning", "delete"):
            print(f"     └─ {f['recommendation']}")
    
    # Summary
    s = result["summary"]
    print(f"\n{'─' * 60}")
    print(f"  📊 Total Context Tax: {s['total_context_tax']:,} tokens/request")
    print(f"     (Files: {s['total_file_tokens']:,} + System: {s['system_overhead_tokens']:,})")
    
    if s["critical_count"] > 0:
        print(f"  🔴 CRITICAL files: {s['critical_count']}")
    if s["warning_count"] > 0:
        print(f"  🟡 WARNING files: {s['warning_count']}")
    if s["delete_count"] > 0:
        print(f"  🗑️  Deletable files: {s['delete_count']}")
    
    # Model compatibility
    print(f"\n📡 Model Compatibility (with heavy session ~120K history):")
    print("-" * 60)
    for model, sessions in result["model_compatibility"].items():
        heavy = sessions["heavy_session"]
        status = "✅" if heavy["fits"] else "❌"
        print(f"  {status} {model:25s} {heavy['total_tokens']:>8,} / {heavy['tpm_limit']:>10,} TPM "
              f"({heavy['headroom_pct']:+.1f}%)")
    
    print(f"\n🧬 S-DNA: {result['sdna']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
