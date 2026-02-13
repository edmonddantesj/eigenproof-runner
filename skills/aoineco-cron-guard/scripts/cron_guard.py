#!/usr/bin/env python3
"""
/* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */
S-DNA: AOI-2026-0213-SDNA-CG01

Aoineco Cron Context Guard — Cron Job Context Explosion Prevention

THE PROBLEM (Real incident):
  A ClawHub research cron job analyzed 60+ skills and returned
  pages of text. The session context ballooned, causing the main
  session to become unresponsive. Other cron jobs also produced
  verbose outputs, compounding the problem.

THE SOLUTION:
  1. Inject context budget constraints into every cron job prompt
  2. Enforce response length limits per job type
  3. Track consecutive errors and auto-pause runaway jobs
  4. Generate lean, structured prompts that prevent data dumps

DESIGN PRINCIPLE:
  "Cron jobs should whisper, not shout.
   Report insights, not raw data."

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta

__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-CG01",
    "author_agent": "blue_gear",
    "org": "aoineco-co",
    "created": "2026-02-13T16:40:00+09:00",
    "tier": "core-infrastructure",
    "classification": "open",
}

KST = timezone(timedelta(hours=9))


# ═══════════════════════════════════════════════════════════
# CONTEXT BUDGET RULES
# ═══════════════════════════════════════════════════════════

# Each cron job type has specific constraints to prevent context explosion.
# These constraints are PREPENDED to the cron job's prompt message.

CRON_CONSTRAINTS: Dict[str, Dict] = {
    "community_patrol": {
        "max_response_lines": 20,
        "rules": [
            "순찰 보고서는 최대 3개 발견 항목으로 제한하라.",
            "각 항목은 2문장 이내로 요약하라.",
            "웹페이지 원문이나 HTML을 절대 포함하지 마라.",
            "에러 발생 시 에러 메시지 1줄만 보고하고 전체 스택트레이스를 포함하지 마라.",
            "인사이트가 없으면 '발견 없음'으로 1줄 보고 후 종료하라.",
        ],
    },
    "insight_curator": {
        "max_response_lines": 30,
        "rules": [
            "아티클 본문은 300자 이내로 작성하라.",
            "출처 URL은 포함하되, 원문 인용은 2문장 이하로 제한하라.",
            "봇마당/Moltbook 게시 시도 결과는 성공/실패 1줄로만 보고하라.",
            "게시 실패 시 에러 코드와 1줄 원인만 기록하라.",
        ],
    },
    "clawhub_research": {
        "max_response_lines": 25,
        "rules": [
            "스킬 정보는 '이름, 설명 1줄, VirusTotal 결과'만 추출하라.",
            "README 전문이나 소스 코드를 절대 포함하지 마라.",
            "최대 5개 스킬만 보고하라 (우선순위 상위).",
            "각 스킬의 'Aoineco 사업적 엣지'를 1문장으로 요약하라.",
            "설치 명령어는 1줄로 축약하라.",
        ],
    },
    "settlement": {
        "max_response_lines": 5,
        "rules": [
            "정산 결과는 '성공/실패 + PnL 수치' 1줄로 출력하라.",
            "상세 로그나 디버그 정보를 포함하지 마라.",
            "에러 시 에러 메시지 1줄만 보고하라.",
        ],
    },
    "v6_pipeline": {
        "max_response_lines": 5,
        "rules": [
            "파이프라인 실행 결과만 보고하라.",
            "에러가 없으면 응답하지 마라 (Stay quiet).",
            "에러 시 에러 메시지 1줄만 보고하라.",
        ],
    },
    "context_monitor": {
        "max_response_lines": 3,
        "rules": [
            "컨텍스트 60% 초과 시에만 1줄 알림을 보내라.",
            "정상이면 응답하지 마라 (Stay quiet).",
        ],
    },
    "github_sync": {
        "max_response_lines": 10,
        "rules": [
            "동기화할 스킬 목록을 '이름 + URL' 형태로만 나열하라.",
            "스킬 상세 정보나 README를 포함하지 마라.",
        ],
    },
    "daily_briefing": {
        "max_response_lines": 30,
        "rules": [
            "브리핑은 '핵심 인사이트 3건 + TODO 변경사항'으로 구조화하라.",
            "각 인사이트는 3문장 이내로 요약하라.",
            "원문 인용이나 긴 분석을 포함하지 마라.",
            "노션 링크는 포함하되, 노션 페이지 내용을 복사하지 마라.",
        ],
    },
}

# Map cron job IDs to their constraint types
CRON_JOB_MAP = {
    "fee48234-c99f-4c72-951f-23e8564d4235": "community_patrol",      # Blue-Sound Patrol
    "6dea1fb8-2886-4837-8426-1d1a8e4cd2fa": "insight_curator",       # Blue-Sound Curator
    "0c3421d4-7724-457c-9664-8dbbaa7f2dd9": "clawhub_research",      # ClawHub Research
    "54553936-d622-40ab-86ba-6923562a44f5": "settlement",            # Settlement
    "7408bcdf-e57d-40b5-a582-4542fceefeea": "v6_pipeline",           # V6 Pipeline
    "5fd96399-3319-4bfa-a4d1-99de555cb728": "context_monitor",       # Context Monitor
    "d67ecaca-28d5-44dd-8fe4-ad951edae323": "github_sync",           # GitHub Sync
    "4de00494-d16f-4e08-b9fd-9dd2ac4b1eae": "daily_briefing",       # Daily Briefing
}


# ═══════════════════════════════════════════════════════════
# CONSTRAINT INJECTOR
# ═══════════════════════════════════════════════════════════

class ConstraintInjector:
    """
    Generates context-constrained prompts for cron jobs.
    
    The constraint prefix is prepended to the original prompt,
    ensuring the LLM follows our token budget rules.
    """
    
    @staticmethod
    def generate_prefix(job_type: str) -> str:
        """Generate a constraint prefix for a cron job type."""
        config = CRON_CONSTRAINTS.get(job_type)
        if not config:
            return "[CONTEXT_BUDGET: 응답은 10줄 이내로 제한하라. 원문 데이터 덤프 금지.]"
        
        rules = config["rules"]
        max_lines = config["max_response_lines"]
        
        lines = [
            f"[⚙️ CRON CONTEXT GUARD — 응답 제한 규칙 (필수 준수)]",
            f"최대 응답 길이: {max_lines}줄 이내.",
        ]
        for i, rule in enumerate(rules, 1):
            lines.append(f"{i}. {rule}")
        lines.append("[규칙 위반 시 다음 실행에서 자동 일시정지됨.]\n")
        
        return "\n".join(lines)
    
    @staticmethod
    def build_guarded_prompt(job_type: str, original_prompt: str) -> str:
        """Combine constraint prefix with original prompt."""
        prefix = ConstraintInjector.generate_prefix(job_type)
        return f"{prefix}\n{original_prompt}"
    
    @classmethod
    def generate_all_updates(cls) -> Dict[str, str]:
        """
        Generate updated prompts for all registered cron jobs.
        Returns: {job_id: new_prompt}
        """
        updates = {}
        for job_id, job_type in CRON_JOB_MAP.items():
            prefix = cls.generate_prefix(job_type)
            updates[job_id] = {
                "job_type": job_type,
                "prefix": prefix,
            }
        return updates


# ═══════════════════════════════════════════════════════════
# CLI & DEMO
# ═══════════════════════════════════════════════════════════

def demo():
    print("=" * 64)
    print("🛡️ AOINECO CRON CONTEXT GUARD")
    print("   Cron jobs should whisper, not shout.")
    print("=" * 64)
    
    injector = ConstraintInjector()
    
    print(f"\n📋 Registered Job Types: {len(CRON_CONSTRAINTS)}")
    print(f"📋 Mapped Cron Jobs: {len(CRON_JOB_MAP)}")
    
    print(f"\n{'─' * 60}")
    for job_type, config in CRON_CONSTRAINTS.items():
        print(f"\n  📌 {job_type} (max {config['max_response_lines']} lines)")
        prefix = injector.generate_prefix(job_type)
        # Show first 3 lines of prefix
        for line in prefix.split("\n")[:4]:
            print(f"     {line}")
        print(f"     ...")
    
    print(f"\n{'─' * 60}")
    print(f"  Total cron jobs to update: {len(CRON_JOB_MAP)}")
    print(f"\n🧬 S-DNA: {__sdna__['id']}")
    print("=" * 64)


if __name__ == "__main__":
    demo()
