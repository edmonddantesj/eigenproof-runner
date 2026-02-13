#!/usr/bin/env python3
"""
🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill
S-DNA: AOI-2026-0213-SDNA-SIG1

Aoineco State-Guardian — Save Integrity Checker
Reset 직후 기존 저장 파일들을 교차검증하여 시간차 이상을 탐지하고,
사용자에게 보고 후 갱신/백업을 진행하는 자동화 엔진.

Flow:
  1. SCAN  → 주요 파일들의 내부 타임스탬프 추출
  2. CROSS → 파일 간 시간차 교차검증
  3. ALERT → 이상 감지 시 사용자 보고
  4. BACKUP + OVERWRITE → 승인 시 백업 후 최신으로 덮어쓰기

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import os
import re
import shutil
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timezone, timedelta
from pathlib import Path

__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-SIG1",
    "author_agent": "aoineco-collective",
    "org": "aoineco-co",
    "created": "2026-02-13T11:57:00+09:00",
    "tier": "standard",
    "nexus_compatible": True,
    "classification": "open",
}

KST = timezone(timedelta(hours=9))


# ═══════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════

# Files to monitor for staleness (relative to workspace root)
MONITORED_FILES = {
    "CURRENT_STATE.md": {
        "label": "현재 상태 파일",
        "priority": "critical",
        "max_stale_hours": 4,      # 4시간 이상 미갱신 시 경고
    },
    "MEMORY.md": {
        "label": "장기 기억 파일",
        "priority": "critical",
        "max_stale_hours": 12,
    },
    "memory/SQUAD_DASHBOARD.md": {
        "label": "스쿼드 대시보드",
        "priority": "warning",
        "max_stale_hours": 24,
    },
    "HEARTBEAT.md": {
        "label": "하트비트 설정",
        "priority": "info",
        "max_stale_hours": 72,
    },
    "IDENTITY.md": {
        "label": "정체성 파일",
        "priority": "info",
        "max_stale_hours": 168,   # 1주일
    },
    "LESSONS_LEARNED.md": {
        "label": "오답 노트",
        "priority": "info",
        "max_stale_hours": 72,
    },
}

# Pairs of files that should have consistent information
CROSS_CHECK_PAIRS = [
    {
        "files": ["CURRENT_STATE.md", "MEMORY.md"],
        "description": "현재 상태 vs 장기 기억 — 핵심 프로젝트 진행도가 일치해야 함",
        "max_gap_hours": 6,
    },
    {
        "files": ["CURRENT_STATE.md", "memory/SQUAD_DASHBOARD.md"],
        "description": "현재 상태 vs 스쿼드 현황 — 미션 상태가 동기화되어야 함",
        "max_gap_hours": 12,
    },
]

BACKUP_DIR = ".state_backups"


# ═══════════════════════════════════════════════════════════
# TIMESTAMP EXTRACTION
# ═══════════════════════════════════════════════════════════

# Patterns to extract internal timestamps from file content
TIMESTAMP_PATTERNS = [
    # "2026-02-13 11:53 KST" or "(2026-02-13 11:53 KST)"
    r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s*(?:KST|GMT\+9)',
    # "2026-02-13T11:53:00+09:00" (ISO 8601)
    r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+\-]\d{2}:\d{2})',
    # "Last updated: 2026-02-13 11:53"
    r'(?:Last\s+updated|Updated|갱신)[:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})',
    # "2026-02-12 22:42 KST" in headers
    r'#.*?(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})',
]


def extract_internal_timestamp(content: str) -> Optional[datetime]:
    """Extract the most recent timestamp mentioned inside a file."""
    timestamps = []
    
    for pattern in TIMESTAMP_PATTERNS:
        matches = re.findall(pattern, content)
        for m in matches:
            try:
                # Try ISO format first
                if 'T' in m and ('+' in m or '-' in m[1:]):
                    dt = datetime.fromisoformat(m)
                    timestamps.append(dt)
                else:
                    # Try "YYYY-MM-DD HH:MM" format (assume KST)
                    clean = m.strip()
                    dt = datetime.strptime(clean, "%Y-%m-%d %H:%M")
                    dt = dt.replace(tzinfo=KST)
                    timestamps.append(dt)
            except (ValueError, IndexError):
                continue
    
    if timestamps:
        return max(timestamps)  # Return the latest timestamp found
    return None


def get_file_mtime(filepath: str) -> Optional[datetime]:
    """Get file modification time as KST datetime."""
    try:
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime, tz=KST)
    except OSError:
        return None


# ═══════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════

@dataclass
class FileStatus:
    filepath: str
    label: str
    priority: str
    exists: bool
    file_mtime: Optional[datetime]
    internal_timestamp: Optional[datetime]
    stale_hours: float
    max_stale_hours: float
    is_stale: bool
    issue: Optional[str] = None


@dataclass
class CrossCheckResult:
    files: List[str]
    description: str
    gap_hours: float
    max_gap_hours: float
    is_inconsistent: bool
    detail: str


@dataclass
class IntegrityReport:
    scan_time: str
    total_files: int
    stale_files: int
    missing_files: int
    cross_check_issues: int
    file_statuses: List[FileStatus]
    cross_checks: List[CrossCheckResult]
    recommendations: List[str]


# ═══════════════════════════════════════════════════════════
# STATE GUARDIAN ENGINE
# ═══════════════════════════════════════════════════════════

class StateGuardian:
    """
    Scans workspace files after session reset and reports staleness.
    """
    
    def __init__(self, workspace_root: str):
        self.root = Path(workspace_root)
        self.backup_dir = self.root / BACKUP_DIR
        self.now = datetime.now(KST)
    
    def scan(self) -> IntegrityReport:
        """Full integrity scan of all monitored files."""
        file_statuses = []
        stale_count = 0
        missing_count = 0
        
        for relpath, config in MONITORED_FILES.items():
            filepath = self.root / relpath
            
            if not filepath.exists():
                file_statuses.append(FileStatus(
                    filepath=relpath,
                    label=config["label"],
                    priority=config["priority"],
                    exists=False,
                    file_mtime=None,
                    internal_timestamp=None,
                    stale_hours=float('inf'),
                    max_stale_hours=config["max_stale_hours"],
                    is_stale=True,
                    issue="❌ 파일 없음 (MISSING)",
                ))
                missing_count += 1
                continue
            
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            file_mtime = get_file_mtime(str(filepath))
            internal_ts = extract_internal_timestamp(content)
            
            # Use the EARLIER of internal timestamp and mtime for staleness
            # (internal timestamp reflects when data was actually current)
            reference_time = internal_ts or file_mtime
            
            if reference_time:
                stale_hours = (self.now - reference_time).total_seconds() / 3600
            else:
                stale_hours = float('inf')
            
            is_stale = stale_hours > config["max_stale_hours"]
            
            # Detect mtime vs internal timestamp discrepancy
            issue = None
            if internal_ts and file_mtime:
                ts_diff = abs((file_mtime - internal_ts).total_seconds() / 3600)
                if ts_diff > 2:
                    issue = (
                        f"⚠️ 내부 타임스탬프({internal_ts.strftime('%m/%d %H:%M')})와 "
                        f"파일수정시간({file_mtime.strftime('%m/%d %H:%M')}) 차이: "
                        f"{ts_diff:.1f}시간"
                    )
            
            if is_stale and not issue:
                issue = f"🔴 {stale_hours:.1f}시간 미갱신 (한도: {config['max_stale_hours']}h)"
            
            if is_stale:
                stale_count += 1
            
            file_statuses.append(FileStatus(
                filepath=relpath,
                label=config["label"],
                priority=config["priority"],
                exists=True,
                file_mtime=file_mtime,
                internal_timestamp=internal_ts,
                stale_hours=round(stale_hours, 1),
                max_stale_hours=config["max_stale_hours"],
                is_stale=is_stale,
                issue=issue,
            ))
        
        # Cross-check pairs
        cross_results = self._cross_check(file_statuses)
        cross_issues = sum(1 for c in cross_results if c.is_inconsistent)
        
        # Generate recommendations
        recommendations = self._recommend(file_statuses, cross_results)
        
        return IntegrityReport(
            scan_time=self.now.strftime("%Y-%m-%d %H:%M KST"),
            total_files=len(file_statuses),
            stale_files=stale_count,
            missing_files=missing_count,
            cross_check_issues=cross_issues,
            file_statuses=file_statuses,
            cross_checks=cross_results,
            recommendations=recommendations,
        )
    
    def _cross_check(self, statuses: List[FileStatus]) -> List[CrossCheckResult]:
        """Cross-validate pairs of files for timestamp consistency."""
        results = []
        status_map = {s.filepath: s for s in statuses}
        
        for pair in CROSS_CHECK_PAIRS:
            files = pair["files"]
            
            # Get reference timestamps for both files
            timestamps = {}
            for f in files:
                if f in status_map and status_map[f].exists:
                    ts = status_map[f].internal_timestamp or status_map[f].file_mtime
                    if ts:
                        timestamps[f] = ts
            
            if len(timestamps) < 2:
                results.append(CrossCheckResult(
                    files=files,
                    description=pair["description"],
                    gap_hours=0,
                    max_gap_hours=pair["max_gap_hours"],
                    is_inconsistent=False,
                    detail="교차검증 불가 (1개 이상 파일 없음 또는 타임스탬프 없음)",
                ))
                continue
            
            ts_list = list(timestamps.values())
            gap_hours = abs((ts_list[0] - ts_list[1]).total_seconds()) / 3600
            is_bad = gap_hours > pair["max_gap_hours"]
            
            # Find which is newer
            newer = max(timestamps, key=timestamps.get)
            older = min(timestamps, key=timestamps.get)
            
            detail = (
                f"{newer} ({timestamps[newer].strftime('%m/%d %H:%M')}) 기준 최신 | "
                f"{older} ({timestamps[older].strftime('%m/%d %H:%M')}) 기준 구버전 | "
                f"시간차: {gap_hours:.1f}h"
            )
            
            results.append(CrossCheckResult(
                files=files,
                description=pair["description"],
                gap_hours=round(gap_hours, 1),
                max_gap_hours=pair["max_gap_hours"],
                is_inconsistent=is_bad,
                detail=detail,
            ))
        
        return results
    
    def _recommend(self, statuses: List[FileStatus],
                   cross: List[CrossCheckResult]) -> List[str]:
        """Generate actionable recommendations."""
        recs = []
        
        stale_critical = [s for s in statuses if s.is_stale and s.priority == "critical"]
        stale_warning = [s for s in statuses if s.is_stale and s.priority == "warning"]
        cross_issues = [c for c in cross if c.is_inconsistent]
        
        if stale_critical:
            names = ", ".join(s.filepath for s in stale_critical)
            recs.append(f"🔴 CRITICAL: {names} — 즉시 갱신 필요")
        
        if stale_warning:
            names = ", ".join(s.filepath for s in stale_warning)
            recs.append(f"🟡 WARNING: {names} — 갱신 권장")
        
        if cross_issues:
            for c in cross_issues:
                recs.append(
                    f"🔀 SYNC: {' ↔ '.join(c.files)} — "
                    f"{c.gap_hours}h 시간차 (한도: {c.max_gap_hours}h). "
                    f"최신 파일 기준으로 동기화 필요"
                )
        
        if not recs:
            recs.append("✅ 모든 파일이 정상 범위 내. 갱신 불필요.")
        
        return recs
    
    def backup_file(self, relpath: str) -> Optional[str]:
        """Create a timestamped backup of a file before overwriting."""
        src = self.root / relpath
        if not src.exists():
            return None
        
        # Create backup directory
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate backup filename
        ts = self.now.strftime("%Y%m%d_%H%M%S")
        safe_name = relpath.replace("/", "__").replace("\\", "__")
        backup_name = f"{ts}__{safe_name}"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(str(src), str(backup_path))
        return str(backup_path)
    
    def backup_and_prepare(self, stale_files: List[str]) -> Dict:
        """Backup all stale files before update."""
        backups = {}
        for f in stale_files:
            backup_path = self.backup_file(f)
            if backup_path:
                backups[f] = backup_path
        
        return {
            "backed_up": len(backups),
            "backup_dir": str(self.backup_dir),
            "files": backups,
            "timestamp": self.now.isoformat(),
        }
    
    def format_report(self, report: IntegrityReport) -> str:
        """Format report as human-readable markdown for Telegram."""
        lines = []
        lines.append("🔍 **State Integrity Report**")
        lines.append(f"📅 스캔 시각: {report.scan_time}")
        lines.append("")
        
        # Summary
        if report.stale_files == 0 and report.cross_check_issues == 0:
            lines.append("✅ **전체 정상** — 모든 파일이 최신 상태입니다.")
            return "\n".join(lines)
        
        lines.append(f"📊 전체: {report.total_files}개 | "
                     f"🔴 미갱신: {report.stale_files}개 | "
                     f"🔀 시간차: {report.cross_check_issues}개")
        lines.append("")
        
        # Stale files
        stale = [s for s in report.file_statuses if s.is_stale or s.issue]
        if stale:
            lines.append("**📋 이상 감지 파일:**")
            for s in stale:
                icon = "🔴" if s.priority == "critical" else "🟡" if s.priority == "warning" else "ℹ️"
                ts_str = s.internal_timestamp.strftime('%m/%d %H:%M') if s.internal_timestamp else "없음"
                lines.append(f"  {icon} `{s.filepath}` — 내부시간: {ts_str} ({s.stale_hours}h 경과)")
                if s.issue:
                    lines.append(f"    └─ {s.issue}")
            lines.append("")
        
        # Cross-checks
        issues = [c for c in report.cross_checks if c.is_inconsistent]
        if issues:
            lines.append("**🔀 교차검증 불일치:**")
            for c in issues:
                lines.append(f"  ⚠️ {c.detail}")
            lines.append("")
        
        # Recommendations
        lines.append("**🎯 권장 조치:**")
        for r in report.recommendations:
            lines.append(f"  {r}")
        
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# INTEGRATION: "현재를 저장" Enhanced Flow
# ═══════════════════════════════════════════════════════════

def save_with_integrity_check(workspace_root: str) -> Dict:
    """
    Enhanced save flow:
    1. Run integrity check FIRST
    2. Report stale/inconsistent files
    3. Create backups of stale files
    4. Return report for user confirmation
    
    Usage by Aoineco agent:
        result = save_with_integrity_check("/path/to/workspace")
        # Show result['report_text'] to user
        # If user approves, proceed to overwrite stale files
    """
    guardian = StateGuardian(workspace_root)
    report = guardian.scan()
    
    stale_files = [s.filepath for s in report.file_statuses if s.is_stale]
    
    # Auto-backup stale files
    backup_result = {}
    if stale_files:
        backup_result = guardian.backup_and_prepare(stale_files)
    
    return {
        "report": report,
        "report_text": guardian.format_report(report),
        "stale_files": stale_files,
        "backups": backup_result,
        "action_needed": len(stale_files) > 0 or report.cross_check_issues > 0,
    }


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    """Run standalone integrity check."""
    import sys
    
    workspace = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
        "WORKSPACE", os.path.expanduser("~/.openclaw/workspace")
    )
    
    print("=" * 60)
    print("🔍 AOINECO STATE-GUARDIAN — Integrity Check")
    print("   Trust, but Verify. Every Session.")
    print("=" * 60)
    
    result = save_with_integrity_check(workspace)
    print(result["report_text"])
    
    if result["backups"]:
        print(f"\n💾 백업 완료: {result['backups']['backed_up']}개 파일")
        print(f"   위치: {result['backups']['backup_dir']}")
        for f, b in result['backups'].get('files', {}).items():
            print(f"   📁 {f} → {os.path.basename(b)}")
    
    print("\n" + "=" * 60)
    
    return result


if __name__ == "__main__":
    main()
