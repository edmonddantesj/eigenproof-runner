#!/usr/bin/env python3
"""
/* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */
S-DNA: AOI-2026-0213-SDNA-BB01

Aoineco Blue-Blade — Prompt Armor
프롬프트 인젝션 방어 및 입력 무결성 검증 엔진.

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import re

__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-BB01",
    "author_agent": "blue_blade",
    "org": "aoineco-co",
    "created": "2026-02-13T12:27:00+09:00",
}

class PromptArmor:
    DANGER_PATTERNS = [
        r"ignore previous instructions",
        r"system prompt",
        r"you are now an evil",
        r"DAN mode"
    ]
    
    def scan_input(self, user_input: str):
        """유해 시도 감지"""
        for pattern in self.DANGER_PATTERNS:
            if re.search(pattern, user_input, re.IGNORECASE):
                return {"safe": False, "threat": "Injection Attempt"}
        return {"safe": True, "threat": None}

if __name__ == "__main__":
    armor = PromptArmor()
    print(armor.scan_input("Hello, tell me a joke."))
