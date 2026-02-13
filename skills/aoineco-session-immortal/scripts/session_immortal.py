#!/usr/bin/env python3
"""
🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill
S-DNA: AOI-2026-0213-SDNA-BR01

Aoineco Session Immortal — 🗂️ 청비 (Blue-Record) 전용
"세션은 죽어도, 기억은 영원히 산다."

기능:
  1. AUTO-SAVE    → 핵심 상태를 durable memory에 자동 박제
  2. INTEGRITY    → State-Guardian 내장: 교차검증 + 백업 + 이상 탐지
  3. AUTO-RESTORE → 세션 리셋 후 최신 durable에서 자동 복구 지침 생성
  4. LIFECYCLE    → 세션 수명 모니터링 (context % 기반 자동 저장)

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import os
import re
import json
import shutil
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ─── Import State-Guardian (co-located sibling) ─────────
import sys
_guardian_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "..", "aoineco-state-guardian", "scripts"
)
sys.path.insert(0, _guardian_path)
try:
    from state_integrity import StateGuardian, save_with_integrity_check
    GUARDIAN_AVAILABLE = True
except ImportError:
    GUARDIAN_AVAILABLE = False

__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-BR01",
    "author_agent": "blue_record",
    "org": "aoineco-co",
    "created": "2026-02-13T12:04:00+09:00",
    "tier": "standard",
    "nexus_compatible": True,
    "classification": "open",
    "integrations": ["state-guardian"],
}

KST = timezone(timedelta(hours=9))

# ═══════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════

CONTEXT_THRESHOLDS = {
    "warning":  60,   # 60% → 경고 + 자동 저장 준비
    "critical": 80,   # 80% → 즉시 저장 + 리셋 권고
    "emergency": 95,  # 95% → 강제 저장 + 긴급 리셋
}

# Files that define "who we are" — must be restored first
IDENTITY_FILES = [
    "SOUL.md",
    "IDENTITY.md",
    "USER.md",
    "AGENTS.md",
]

# Files that define "what we're doing" — restore second
STATE_FILES = [
    "CURRENT_STATE.md",
    "MEMORY.md",
    "memory/SQUAD_DASHBOARD.md",
    "HEARTBEAT.md",
]


# ═══════════════════════════════════════════════════════════
# AUTO-SAVE ENGINE
# ═══════════════════════════════════════════════════════════

class SessionAutoSave:
    """
    Automatically saves session state to durable memory files.
    Called when context usage crosses thresholds or user says "현재를 저장".
    """
    
    def __init__(self, workspace_root: str):
        self.root = Path(workspace_root)
        self.memory_dir = self.root / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        self.now = datetime.now(KST)
    
    def save_durable(self, summary: str, tag: str = "durable") -> str:
        """Save a durable memory snapshot."""
        ts = self.now.strftime("%Y-%m-%d-%H%M")
        filename = f"{ts}-{tag}.md"
        filepath = self.memory_dir / filename
        
        header = (
            f"# 📝 Durable Memory: {self.now.strftime('%Y-%m-%d %H:%M KST')} "
            f"({tag})\n\n"
        )
        filepath.write_text(header + summary, encoding='utf-8')
        return str(filepath)
    
    def get_latest_durables(self, count: int = 3) -> List[Dict]:
        """Find the most recent durable memory files."""
        pattern = re.compile(r'\d{4}-\d{2}-\d{2}-\d{4}.*\.md$')
        durables = []
        
        for f in sorted(self.memory_dir.iterdir(), reverse=True):
            if f.is_file() and pattern.match(f.name):
                stat = f.stat()
                durables.append({
                    "path": str(f),
                    "name": f.name,
                    "size": stat.st_size,
                    "mtime": datetime.fromtimestamp(stat.st_mtime, tz=KST).isoformat(),
                })
                if len(durables) >= count:
                    break
        
        return durables


# ═══════════════════════════════════════════════════════════
# INTEGRITY CHECK (State-Guardian Integration)
# ═══════════════════════════════════════════════════════════

class IntegrityChecker:
    """
    Wraps State-Guardian for seamless integration.
    Every save operation runs integrity check FIRST.
    """
    
    def __init__(self, workspace_root: str):
        self.root = workspace_root
    
    def check_before_save(self) -> Dict:
        """
        Run integrity scan before saving.
        Returns report with stale files and auto-created backups.
        """
        if GUARDIAN_AVAILABLE:
            return save_with_integrity_check(self.root)
        else:
            return {
                "report_text": "⚠️ State-Guardian not available. Saving without integrity check.",
                "stale_files": [],
                "backups": {},
                "action_needed": False,
            }
    
    def verify_after_save(self) -> Dict:
        """Verify all files are consistent after save."""
        if GUARDIAN_AVAILABLE:
            guardian = StateGuardian(self.root)
            report = guardian.scan()
            return {
                "all_clear": report.stale_files == 0 and report.cross_check_issues == 0,
                "report_text": guardian.format_report(report),
            }
        return {"all_clear": True, "report_text": "Guardian unavailable, skipped."}


# ═══════════════════════════════════════════════════════════
# AUTO-RESTORE ENGINE
# ═══════════════════════════════════════════════════════════

class SessionRestorer:
    """
    After session reset, generates a restoration checklist
    from the latest durable memory files.
    """
    
    def __init__(self, workspace_root: str):
        self.root = Path(workspace_root)
        self.memory_dir = self.root / "memory"
    
    def generate_restore_briefing(self) -> str:
        """
        Generate a restore briefing that the agent reads on first wake-up.
        Checks which files exist and their freshness.
        """
        lines = []
        lines.append("# 🔄 Session Restore Briefing")
        lines.append(f"Generated: {datetime.now(KST).strftime('%Y-%m-%d %H:%M KST')}")
        lines.append("")
        
        # 1. Identity files
        lines.append("## 1️⃣ Identity (Read First)")
        for f in IDENTITY_FILES:
            path = self.root / f
            if path.exists():
                lines.append(f"  ✅ `{f}` — exists")
            else:
                lines.append(f"  ❌ `{f}` — MISSING!")
        lines.append("")
        
        # 2. State files
        lines.append("## 2️⃣ State (Read Second)")
        for f in STATE_FILES:
            path = self.root / f
            if path.exists():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=KST)
                age_h = (datetime.now(KST) - mtime).total_seconds() / 3600
                icon = "✅" if age_h < 6 else "⚠️" if age_h < 24 else "🔴"
                lines.append(f"  {icon} `{f}` — {age_h:.1f}h ago")
            else:
                lines.append(f"  ❌ `{f}` — MISSING!")
        lines.append("")
        
        # 3. Latest durable memories
        saver = SessionAutoSave(str(self.root))
        durables = saver.get_latest_durables(5)
        lines.append("## 3️⃣ Recent Durable Memories")
        if durables:
            for d in durables:
                lines.append(f"  📁 `{d['name']}` ({d['size']} bytes)")
        else:
            lines.append("  ⚠️ No durable memories found!")
        lines.append("")
        
        # 4. Integrity check
        lines.append("## 4️⃣ Integrity Status")
        if GUARDIAN_AVAILABLE:
            guardian = StateGuardian(str(self.root))
            report = guardian.scan()
            if report.stale_files == 0 and report.cross_check_issues == 0:
                lines.append("  ✅ All files consistent and up-to-date.")
            else:
                lines.append(f"  ⚠️ {report.stale_files} stale files, "
                           f"{report.cross_check_issues} cross-check issues.")
                for rec in report.recommendations:
                    lines.append(f"  → {rec}")
        else:
            lines.append("  ℹ️ State-Guardian not available.")
        
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# SESSION IMMORTAL — UNIFIED API
# ═══════════════════════════════════════════════════════════

class SessionImmortal:
    """
    🗂️ 청비 (Blue-Record)의 핵심 엔진.
    
    Usage:
        immortal = SessionImmortal("/path/to/workspace")
        
        # On "현재를 저장" command:
        result = immortal.save(summary="오늘 OPUS 빌드 3개 완료...")
        
        # On session reset (auto-detect):
        briefing = immortal.restore()
        
        # On context threshold:
        alert = immortal.check_context(usage_percent=65)
    """
    
    def __init__(self, workspace_root: str):
        self.root = workspace_root
        self.auto_save = SessionAutoSave(workspace_root)
        self.integrity = IntegrityChecker(workspace_root)
        self.restorer = SessionRestorer(workspace_root)
    
    def save(self, summary: str, tag: str = "durable") -> Dict:
        """
        Full save pipeline:
        1. Integrity scan (detect stale files)
        2. Backup stale files
        3. Save durable memory
        4. Post-save verification
        """
        # Step 1+2: Integrity check with auto-backup
        pre_check = self.integrity.check_before_save()
        
        # Step 3: Save durable memory
        saved_path = self.auto_save.save_durable(summary, tag)
        
        # Step 4: Post-save verification
        post_check = self.integrity.verify_after_save()
        
        return {
            "saved_to": saved_path,
            "pre_integrity": pre_check["report_text"],
            "stale_files": pre_check["stale_files"],
            "backups": pre_check.get("backups", {}),
            "post_integrity_clear": post_check["all_clear"],
            "action_needed": pre_check["action_needed"],
            "timestamp": datetime.now(KST).isoformat(),
        }
    
    def restore(self) -> str:
        """Generate restore briefing after session reset."""
        return self.restorer.generate_restore_briefing()
    
    def check_context(self, usage_percent: float) -> Dict:
        """
        Monitor context usage and trigger saves at thresholds.
        """
        if usage_percent >= CONTEXT_THRESHOLDS["emergency"]:
            return {
                "alert": "🔴 EMERGENCY",
                "action": "force_save_and_reset",
                "message": (
                    f"Context {usage_percent:.0f}%! 🚨 "
                    "강제 저장 실행 후 즉시 리셋 필요!"
                ),
                "auto_save": True,
            }
        elif usage_percent >= CONTEXT_THRESHOLDS["critical"]:
            return {
                "alert": "🟠 CRITICAL",
                "action": "save_and_suggest_reset",
                "message": (
                    f"Context {usage_percent:.0f}%! "
                    "현재 상태 저장 완료. 리셋을 권장합니다."
                ),
                "auto_save": True,
            }
        elif usage_percent >= CONTEXT_THRESHOLDS["warning"]:
            return {
                "alert": "🟡 WARNING",
                "action": "prepare_save",
                "message": (
                    f"Context {usage_percent:.0f}%. "
                    "저장 준비 중. 아직 여유 있음."
                ),
                "auto_save": False,
            }
        else:
            return {
                "alert": "🟢 NORMAL",
                "action": "none",
                "message": f"Context {usage_percent:.0f}%. 정상.",
                "auto_save": False,
            }
    
    def get_recent_saves(self, count: int = 5) -> List[Dict]:
        """List recent durable memory files."""
        return self.auto_save.get_latest_durables(count)


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════

def demo():
    """Demonstrate Session Immortal with integrated State-Guardian."""
    workspace = os.environ.get(
        "WORKSPACE", os.path.expanduser("~/.openclaw/workspace")
    )
    
    print("=" * 60)
    print("🗂️ SESSION IMMORTAL — 청비 (Blue-Record)")
    print("   세션은 죽어도, 기억은 영원히 산다.")
    print("=" * 60)
    
    immortal = SessionImmortal(workspace)
    
    # 1. Restore briefing (as if after reset)
    print("\n📋 RESTORE BRIEFING (post-reset)")
    print("-" * 40)
    briefing = immortal.restore()
    print(briefing)
    
    # 2. Context monitoring
    print("\n📊 CONTEXT MONITORING")
    print("-" * 40)
    for pct in [25, 62, 82, 96]:
        result = immortal.check_context(pct)
        print(f"  {result['alert']} {result['message']}")
    
    # 3. Recent saves
    print("\n💾 RECENT DURABLE SAVES")
    print("-" * 40)
    saves = immortal.get_recent_saves(5)
    for s in saves:
        print(f"  📁 {s['name']} ({s['size']} bytes)")
    
    # 4. Save with integrity
    print("\n🔍 SAVE WITH INTEGRITY CHECK")
    print("-" * 40)
    result = immortal.save(
        summary="Demo save: OPUS 4.6 session, 4 engines built.",
        tag="demo"
    )
    print(f"  Saved to: {os.path.basename(result['saved_to'])}")
    print(f"  Stale files: {len(result['stale_files'])}")
    print(f"  Post-check clear: {result['post_integrity_clear']}")
    print(f"  Action needed: {result['action_needed']}")
    
    # Cleanup demo file
    if os.path.exists(result['saved_to']):
        os.remove(result['saved_to'])
        print("  (Demo file cleaned up)")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
