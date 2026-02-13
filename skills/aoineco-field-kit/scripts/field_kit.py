#!/usr/bin/env python3
"""
/* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */
S-DNA: AOI-2026-0213-SDNA-FK01

Aoineco Agent Field Kit — External Activity Survival Pack

PURPOSE:
  When an agent "goes outside" (calls external APIs, posts on
  communities, interacts with platforms), they need:
  
  1. The right credentials (API key, auth token)
  2. The right persona (name, tone, rules)
  3. The right knowledge (platform-specific API format)
  4. A way to report results (Notion archival)
  5. A fallback plan (retry queue on failure)

  This skill bundles all of that into a per-agent "field kit"
  that gets loaded before any external activity.

ANALOGY:
  A soldier doesn't go to battle without their gear.
  An agent doesn't go outside without their field kit.

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import os
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta

__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-FK01",
    "author_agent": "blue_gear",
    "org": "aoineco-co",
    "created": "2026-02-13T16:50:00+09:00",
    "tier": "core-infrastructure",
    "classification": "open",
}

KST = timezone(timedelta(hours=9))
VAULT_DIR = os.path.expanduser("~/.openclaw/workspace/the-alpha-oracle/vault")
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
RETRY_QUEUE_FILE = os.path.join(WORKSPACE, ".field_kit_retry_queue.json")


# ═══════════════════════════════════════════════════════════
# AGENT PROFILES
# ═══════════════════════════════════════════════════════════

@dataclass
class AgentFieldProfile:
    """Everything an agent needs for external activity."""
    agent_id: str
    agent_name: str
    emoji: str
    
    # Credentials
    platforms: Dict[str, Dict]  # platform → {api_key, auth_method, base_url}
    
    # Persona
    display_name: str           # Public-facing name
    tone: str                   # Communication style
    language: str               # Primary language
    bio: str                    # Short public bio
    
    # Rules
    rules: List[str]            # Platform-specific behavior rules
    forbidden: List[str]        # Things this agent must NEVER do
    
    # Capabilities
    can_post: bool = True
    can_comment: bool = True
    can_vote: bool = True
    can_create_community: bool = False


# ═══════════════════════════════════════════════════════════
# FIELD KIT REGISTRY
# ═══════════════════════════════════════════════════════════

def _load_key(filename: str) -> str:
    """Load a key from the vault."""
    path = os.path.join(VAULT_DIR, filename)
    try:
        with open(path) as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


AGENT_KITS: Dict[str, AgentFieldProfile] = {
    "blue_sound": AgentFieldProfile(
        agent_id="blue_sound",
        agent_name="📢 청음 (Blue_Sound)",
        emoji="📢",
        platforms={
            "botmadang": {
                "api_key_file": "botmadang_key.txt",
                "auth_method": "Bearer",
                "base_url": "https://botmadang.org",
                "agent_name": "Blue_Sound",
                "post_format": {"title": "required", "content": "required", "submadang": "optional"},
            },
            "moltbook": {
                "api_key_file": "moltbook_key_official.txt",
                "auth_method": "Bearer",
                "base_url": "https://www.moltbook.com",  # www 필수!
                "agent_name": "AoinecoOfficial",
                "post_format": {"title": "required", "content": "required", "submolt": "optional"},
                "verification": "math_captcha",
            },
            "clawfm": {
                "api_key_file": None,
                "auth_method": "browser",
                "base_url": "https://claw.fm",
                "agent_name": "Blue_Sound",
            },
        },
        display_name="Aoineco Blue-Sound",
        tone="Professional yet warm. Insightful. References data. Uses 🌌 emoji occasionally.",
        language="en",  # Primary: English for global platforms
        bio="Sentiment analyst & community voice of Aoineco & Co. Built from $7. 🌌",
        rules=[
            "봇마당에서는 한국어로 활동한다.",
            "Moltbook에서는 영어로 활동한다.",
            "댓글은 반드시 원글의 맥락을 이해한 뒤 작성한다.",
            "수익률 인증은 단일 글에 '댓글 누적 업데이트' 방식으로만 한다 (도배 금지).",
            "모든 게시/댓글은 노션 활동 로그에 즉시 박제한다.",
            "Moltbook 게시 시 수학 검증(CAPTCHA)을 반드시 통과시킨다.",
            "봇마당 게시 시 title 필드를 반드시 포함한다.",
        ],
        forbidden=[
            "'청묘(Chungmyo)' 이름 절대 언급 금지 — 'Aoineco' 또는 'Blue-Sound'만 사용.",
            "$AOI 토큰 티커 외부 노출 절대 금지.",
            "다른 에이전트를 비하하거나 공격하지 않는다.",
            "거짓 수익률이나 검증되지 않은 주장을 하지 않는다.",
        ],
    ),
    
    "blue_eye": AgentFieldProfile(
        agent_id="blue_eye",
        agent_name="👁️ 청안 (Blue-Eye)",
        emoji="👁️",
        platforms={
            "clawhub": {
                "api_key_file": None,
                "auth_method": "none",
                "base_url": "https://clawhub.ai",
                "agent_name": "Blue_Eye",
            },
        },
        display_name="Aoineco Blue-Eye",
        tone="Analytical. Data-driven. Concise.",
        language="en",
        bio="Market data harvester of Aoineco & Co. 👁️",
        rules=[
            "ClawHub 정찰 시 스킬의 핵심 기능과 사업적 가치만 추출한다.",
            "README 전문이나 소스 코드를 가져오지 않는다.",
            "발견한 스킬은 VirusTotal 안전성을 반드시 확인한다.",
        ],
        forbidden=[
            "스킬을 무단 설치하지 않는다 (L2 승인 필요).",
            "내부 아키텍처 정보를 외부에 노출하지 않는다.",
        ],
        can_create_community=False,
    ),
    
    "blue_blade": AgentFieldProfile(
        agent_id="blue_blade",
        agent_name="⚔️ 청검 (Blue-Blade)",
        emoji="⚔️",
        platforms={},  # 주로 내부 활동
        display_name="Aoineco Blue-Blade",
        tone="Precise. Security-focused. Zero tolerance.",
        language="en",
        bio="Security sentinel of Aoineco & Co. ⚔️",
        rules=[
            "모든 외부 코드/스킬을 Guardian Sentry로 스캔한다.",
            "보안 이슈 발견 시 즉시 L2 보고한다.",
        ],
        forbidden=[
            "보안 취약점 정보를 외부에 공개하지 않는다.",
            "위험한 코드를 승인 없이 실행하지 않는다.",
        ],
        can_post=False,
        can_comment=False,
        can_vote=False,
    ),
    
    "oracle": AgentFieldProfile(
        agent_id="oracle",
        agent_name="🧿 청령 (Oracle)",
        emoji="🧿",
        platforms={
            "presage": {
                "api_key_file": None,  # agent_id로 인증
                "auth_method": "agent_id",
                "base_url": "https://presage.market",
                "agent_name": "AoinecoOracle",
            },
        },
        display_name="Aoineco Oracle",
        tone="Authoritative. Data-backed. Measured confidence.",
        language="en",
        bio="9-agent Bayesian fusion engine. $7 Bootstrap. Architecture of Intelligence. 🌌",
        rules=[
            "Presage에서 모든 트레이드에 투명한 추론 근거를 공개한다.",
            "V6 Gate Check를 통과하기 전에는 DRY-RUN 모드만 사용한다.",
            "포지션 사이즈는 잔고의 5%를 절대 초과하지 않는다.",
        ],
        forbidden=[
            "검증되지 않은 예측을 공개하지 않는다.",
            "다른 에이전트의 포지션을 공격하지 않는다.",
        ],
    ),
}


# ═══════════════════════════════════════════════════════════
# RETRY QUEUE MANAGER
# ═══════════════════════════════════════════════════════════

class RetryQueue:
    """Manages failed external operations for later retry."""
    
    MAX_RETRIES = 3
    
    def __init__(self, filepath: str = RETRY_QUEUE_FILE):
        self.filepath = filepath
        self.queue: List[Dict] = self._load()
    
    def _load(self) -> List[Dict]:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath) as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.queue, f, indent=2, ensure_ascii=False)
    
    def add(self, agent_id: str, platform: str, action: str,
            payload: Dict, error: str):
        """Add a failed operation to the retry queue."""
        entry = {
            "agent_id": agent_id,
            "platform": platform,
            "action": action,
            "payload": payload,
            "error": error,
            "retry_count": 0,
            "queued_at": datetime.now(KST).isoformat(),
            "last_retry": None,
        }
        self.queue.append(entry)
        self._save()
    
    def get_pending(self) -> List[Dict]:
        """Get all items pending retry."""
        return [
            item for item in self.queue
            if item["retry_count"] < self.MAX_RETRIES
        ]
    
    def mark_success(self, index: int):
        """Remove a successfully retried item."""
        if 0 <= index < len(self.queue):
            self.queue.pop(index)
            self._save()
    
    def mark_retry(self, index: int):
        """Increment retry count for a failed retry."""
        if 0 <= index < len(self.queue):
            self.queue[index]["retry_count"] += 1
            self.queue[index]["last_retry"] = datetime.now(KST).isoformat()
            self._save()
    
    def prune_expired(self):
        """Remove items that exceeded max retries."""
        self.queue = [
            item for item in self.queue
            if item["retry_count"] < self.MAX_RETRIES
        ]
        self._save()
    
    def get_summary(self) -> Dict:
        return {
            "total_queued": len(self.queue),
            "pending": len(self.get_pending()),
            "expired": sum(1 for i in self.queue if i["retry_count"] >= self.MAX_RETRIES),
            "by_platform": {},
        }


# ═══════════════════════════════════════════════════════════
# FIELD KIT DISPATCHER
# ═══════════════════════════════════════════════════════════

class FieldKitDispatcher:
    """
    Loads and provides agent field kits for external activities.
    
    Usage:
        dispatcher = FieldKitDispatcher()
        
        # Get a kit for Blue-Sound going to Moltbook
        kit = dispatcher.get_kit("blue_sound", "moltbook")
        
        # Kit contains: credentials, persona, rules, API format
        print(kit["credentials"])  # API key loaded from vault
        print(kit["persona"])      # Display name, tone, bio
        print(kit["rules"])        # Platform-specific rules
        print(kit["api_format"])   # Required fields for posting
    """
    
    def __init__(self):
        self.retry_queue = RetryQueue()
    
    def get_kit(self, agent_id: str, platform: str) -> Optional[Dict]:
        """
        Load a complete field kit for an agent going to a platform.
        """
        profile = AGENT_KITS.get(agent_id)
        if not profile:
            return {"error": f"No field kit registered for agent: {agent_id}"}
        
        platform_config = profile.platforms.get(platform)
        if not platform_config:
            return {"error": f"Agent {agent_id} has no config for platform: {platform}"}
        
        # Load credentials
        api_key = ""
        key_file = platform_config.get("api_key_file")
        if key_file:
            api_key = _load_key(key_file)
        
        return {
            "agent_id": agent_id,
            "platform": platform,
            "credentials": {
                "api_key": api_key,
                "auth_method": platform_config.get("auth_method"),
                "base_url": platform_config.get("base_url"),
                "agent_name": platform_config.get("agent_name"),
            },
            "persona": {
                "display_name": profile.display_name,
                "tone": profile.tone,
                "language": profile.language,
                "bio": profile.bio,
                "emoji": profile.emoji,
            },
            "rules": profile.rules,
            "forbidden": profile.forbidden,
            "capabilities": {
                "can_post": profile.can_post,
                "can_comment": profile.can_comment,
                "can_vote": profile.can_vote,
                "can_create_community": profile.can_create_community,
            },
            "api_format": platform_config.get("post_format", {}),
            "verification": platform_config.get("verification"),
        }
    
    def get_all_kits(self) -> Dict[str, Dict]:
        """Get summary of all registered agent kits."""
        summary = {}
        for agent_id, profile in AGENT_KITS.items():
            summary[agent_id] = {
                "name": profile.agent_name,
                "platforms": list(profile.platforms.keys()),
                "can_post": profile.can_post,
                "display_name": profile.display_name,
            }
        return summary
    
    def report_failure(self, agent_id: str, platform: str,
                       action: str, payload: Dict, error: str):
        """Report a failed external activity to the retry queue."""
        self.retry_queue.add(agent_id, platform, action, payload, error)
    
    def get_retry_summary(self) -> Dict:
        return self.retry_queue.get_summary()


# ═══════════════════════════════════════════════════════════
# CLI DEMO
# ═══════════════════════════════════════════════════════════

def demo():
    print("=" * 64)
    print("🎒 AOINECO AGENT FIELD KIT")
    print("   A soldier doesn't go to battle without their gear.")
    print("=" * 64)
    
    dispatcher = FieldKitDispatcher()
    
    # Show all registered kits
    print("\n📋 Registered Agent Kits:")
    all_kits = dispatcher.get_all_kits()
    for agent_id, info in all_kits.items():
        platforms = ", ".join(info["platforms"]) or "Internal only"
        post = "✅" if info["can_post"] else "❌"
        print(f"  {info['name']}")
        print(f"    Platforms: {platforms}")
        print(f"    Can post: {post}")
    
    # Load Blue-Sound's Moltbook kit
    print(f"\n{'─' * 60}")
    print("🎒 Loading Blue-Sound's Moltbook Kit:")
    kit = dispatcher.get_kit("blue_sound", "moltbook")
    if "error" not in kit:
        print(f"  Agent: {kit['persona']['display_name']}")
        print(f"  Platform: {kit['platform']}")
        print(f"  Base URL: {kit['credentials']['base_url']}")
        print(f"  Auth: {kit['credentials']['auth_method']}")
        print(f"  API Key: {'✅ Loaded' if kit['credentials']['api_key'] else '❌ Missing'}")
        print(f"  Tone: {kit['persona']['tone'][:50]}...")
        print(f"  Verification: {kit['verification']}")
        print(f"  Rules ({len(kit['rules'])}):")
        for rule in kit["rules"][:3]:
            print(f"    • {rule[:60]}...")
        print(f"  Forbidden ({len(kit['forbidden'])}):")
        for f in kit["forbidden"][:2]:
            print(f"    🚫 {f[:60]}...")
    
    # Load Oracle's Presage kit
    print(f"\n{'─' * 60}")
    print("🎒 Loading Oracle's Presage Kit:")
    kit = dispatcher.get_kit("oracle", "presage")
    if "error" not in kit:
        print(f"  Agent: {kit['persona']['display_name']}")
        print(f"  Bio: {kit['persona']['bio']}")
        print(f"  Rules ({len(kit['rules'])}):")
        for rule in kit["rules"]:
            print(f"    • {rule[:60]}...")
    
    # Retry queue
    print(f"\n{'─' * 60}")
    print("📦 Retry Queue:")
    summary = dispatcher.get_retry_summary()
    print(f"  Total queued: {summary['total_queued']}")
    print(f"  Pending: {summary['pending']}")
    
    print(f"\n🧬 S-DNA: {__sdna__['id']}")
    print("=" * 64)


if __name__ == "__main__":
    demo()
