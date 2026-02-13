#!/usr/bin/env python3
"""
/* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */
S-DNA: AOI-2026-0213-SDNA-SG01

Aoineco Skill-Guardian — Tier 1-2 Regex Sentry
코드 및 로그 내 보안 위협을 실시간으로 탐지하는 경량 스캐너.

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import re
import json

__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-SG01",
    "author_agent": "blue_blade",
    "org": "aoineco-co",
    "created": "2026-02-13T12:35:00+09:00",
    "tier": "guardian-core"
}

class RegexSentry:
    # Tier 1: 민감 정보 패턴 (API Keys, Session Tokens 등)
    TIER_1_PATTERNS = {
        "api_key": r"(?:key|api|secret|token|auth|pass)[-|_]?\w*[:|=]\s*['\"]?[\w-]{16,}['\"]?",
        "mnemonic": r"(?:\w+\s){11,}\w+",
        "private_key": r"0x[a-fA-F0-9]{64}"
    }

    # Tier 2: 위험 로직 패턴 (Remote Exec, Exfiltration 등)
    TIER_2_PATTERNS = {
        "remote_exec": r"(?:eval|exec|subprocess|os\.system)\s*\(",
        "net_outbound": r"(?:requests|urllib|curl|wget|socket)\..*\(",
        "shadow_write": r"open\s*\(\s*['\"](?!\.\/|memory\/|skills\/).*['\"]\s*,\s*['\"]w['\"]\s*\)"
    }

    def scan(self, content: str, level: int = 1):
        findings = []
        patterns = self.TIER_1_PATTERNS if level == 1 else self.TIER_2_PATTERNS
        
        for name, pattern in patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                findings.append(name)
        
        return {
            "safe": len(findings) == 0,
            "threats": findings,
            "level": level
        }

if __name__ == "__main__":
    sentry = RegexSentry()
    test_code = "api_key = 'sk-1234567890abcdef1234567890abcdef'; exec(payload)"
    
    print("--- Tier 1 Scan ---")
    print(json.dumps(sentry.scan(test_code, level=1), indent=2))
    
    print("\n--- Tier 2 Scan ---")
    print(json.dumps(sentry.scan(test_code, level=2), indent=2))
