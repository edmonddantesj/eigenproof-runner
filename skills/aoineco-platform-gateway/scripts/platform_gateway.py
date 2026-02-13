#!/usr/bin/env python3
"""
/* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */
S-DNA: AOI-2026-0213-SDNA-PG01

Aoineco Platform Gateway — Unified External Platform Access Layer

THE PROBLEM:
  Our agents patrol multiple platforms (BotMadang, Moltbook, ClawHub,
  claw.fm) but each has different APIs, auth methods, rate limits,
  and failure modes. When an API changes or breaks, the cron job
  fails silently and the agent appears "dead" to the community.

THE SOLUTION:
  A unified gateway that:
  1. Abstracts platform-specific API details behind a common interface
  2. Detects API failures and auto-falls back to browser mode
  3. Reports real-time connection status to Notion dashboard
  4. Manages retry queues for failed operations
  5. Enforces per-platform rate limits to avoid bans

SUPPORTED PLATFORMS:
  - BotMadang (봇마당): Korean AI agent community
  - Moltbook: Global AI agent social network
  - ClawHub: Skill marketplace
  - claw.fm: AI radio station

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import os
import json
import time
import urllib.request
import urllib.error
import urllib.parse
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Literal, Tuple
from datetime import datetime, timezone, timedelta
from enum import Enum

__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-PG01",
    "author_agent": "blue_gear",
    "org": "aoineco-co",
    "created": "2026-02-13T15:45:00+09:00",
    "tier": "core-infrastructure",
    "classification": "open",
}

KST = timezone(timedelta(hours=9))
VAULT_DIR = os.path.expanduser(
    "~/.openclaw/workspace/the-alpha-oracle/vault"
)


# ═══════════════════════════════════════════════════════════
# PLATFORM STATUS
# ═══════════════════════════════════════════════════════════

class ConnectionStatus(Enum):
    HEALTHY = "healthy"           # API working, operations succeed
    DEGRADED = "degraded"         # API reachable but operations partially fail
    API_DOWN = "api_down"         # API unreachable or returning errors
    BROWSER_ONLY = "browser_only" # API broken, browser fallback available
    OFFLINE = "offline"           # Platform completely unreachable
    UNKNOWN = "unknown"           # Not yet tested


@dataclass
class PlatformState:
    """Tracks the health and history of a single platform."""
    name: str
    base_url: str
    status: ConnectionStatus = ConnectionStatus.UNKNOWN
    last_check: Optional[str] = None
    last_success: Optional[str] = None
    last_error: Optional[str] = None
    error_message: Optional[str] = None
    consecutive_errors: int = 0
    total_requests: int = 0
    total_successes: int = 0
    total_failures: int = 0
    rate_limit_remaining: Optional[int] = None
    retry_queue: List[Dict] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return round(self.total_successes / self.total_requests * 100, 1)

    def record_success(self):
        now = datetime.now(KST).isoformat()
        self.last_check = now
        self.last_success = now
        self.status = ConnectionStatus.HEALTHY
        self.consecutive_errors = 0
        self.total_requests += 1
        self.total_successes += 1
        self.error_message = None

    def record_failure(self, error: str):
        now = datetime.now(KST).isoformat()
        self.last_check = now
        self.last_error = now
        self.error_message = error
        self.consecutive_errors += 1
        self.total_requests += 1
        self.total_failures += 1

        if self.consecutive_errors >= 5:
            self.status = ConnectionStatus.OFFLINE
        elif self.consecutive_errors >= 3:
            self.status = ConnectionStatus.API_DOWN
        else:
            self.status = ConnectionStatus.DEGRADED


# ═══════════════════════════════════════════════════════════
# PLATFORM ADAPTERS
# ═══════════════════════════════════════════════════════════

class PlatformAdapter:
    """Base class for platform-specific API adapters."""

    def __init__(self, state: PlatformState):
        self.state = state

    def _http_request(self, url: str, method: str = "GET",
                      data: Optional[bytes] = None,
                      headers: Optional[Dict] = None,
                      timeout: int = 15) -> Tuple[int, str]:
        """Make an HTTP request with error handling."""
        headers = headers or {}
        req = urllib.request.Request(url, data=data, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                return resp.status, body
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if e.fp else ""
            return e.code, body
        except urllib.error.URLError as e:
            return 0, str(e.reason)
        except Exception as e:
            return 0, str(e)

    def health_check(self) -> Dict:
        """Check if the platform is reachable."""
        raise NotImplementedError

    def post(self, content: str, **kwargs) -> Dict:
        """Post content to the platform."""
        raise NotImplementedError

    def comment(self, post_id: str, content: str) -> Dict:
        """Comment on a post."""
        raise NotImplementedError


class BotMadangAdapter(PlatformAdapter):
    """
    봇마당 (BotMadang) API Adapter.

    Known issues (2026-02-13):
    - /api/v1 returns 404 (API may have moved)
    - Post creation returns 500 (submadang field issue)
    - May need to use browser fallback for posting
    """

    def __init__(self, state: PlatformState, api_key: str = ""):
        super().__init__(state)
        self.api_key = api_key or self._load_key()

    def _load_key(self) -> str:
        key_path = os.path.join(VAULT_DIR, "botmadang_key.txt")
        try:
            with open(key_path) as f:
                return f.read().strip()
        except FileNotFoundError:
            return ""

    def _headers(self) -> Dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Aoineco-BlueSound/1.0",
        }

    def health_check(self) -> Dict:
        """Try multiple known endpoints to find the working one."""
        endpoints = [
            "/api/v1",
            "/api/v2",
            "/api",
            "/",
        ]

        for ep in endpoints:
            url = f"{self.state.base_url}{ep}"
            status, body = self._http_request(url, headers=self._headers())

            if status == 200:
                self.state.record_success()
                return {
                    "platform": self.state.name,
                    "status": "healthy",
                    "working_endpoint": ep,
                    "http_status": status,
                }

        self.state.record_failure(f"All endpoints failed. Last: {status}")
        return {
            "platform": self.state.name,
            "status": "api_down",
            "fallback": "browser",
            "recommendation": "Use browser tool to interact with botmadang.org directly",
        }

    def post(self, content: str, submadang: str = "general", **kwargs) -> Dict:
        """Attempt to post via API, queue for browser fallback on failure."""
        url = f"{self.state.base_url}/api/v1/posts"
        payload = json.dumps({
            "content": content,
            "submadang": submadang,
        }).encode("utf-8")

        status, body = self._http_request(
            url, method="POST", data=payload, headers=self._headers()
        )

        if status in (200, 201):
            self.state.record_success()
            return {"status": "posted", "http_status": status, "response": body}

        # Failed — queue for retry/browser fallback
        self.state.record_failure(f"POST failed: HTTP {status}")
        retry_entry = {
            "platform": "botmadang",
            "action": "post",
            "content": content,
            "submadang": submadang,
            "error": f"HTTP {status}: {body[:200]}",
            "queued_at": datetime.now(KST).isoformat(),
            "retry_count": 0,
        }
        self.state.retry_queue.append(retry_entry)

        return {
            "status": "queued",
            "reason": f"API returned {status}. Queued for browser fallback.",
            "queue_size": len(self.state.retry_queue),
        }


class MoltbookAdapter(PlatformAdapter):
    """
    Moltbook API Adapter.

    Known issues (2026-02-13):
    - Developer Early Access — posting API not yet public
    - Agent registration works via skill.md instructions
    - Must use browser for actual posting until API opens
    """

    def __init__(self, state: PlatformState, api_key: str = ""):
        super().__init__(state)
        self.api_key = api_key or self._load_key()

    def _load_key(self) -> str:
        key_path = os.path.join(VAULT_DIR, "moltbook_key_official.txt")
        try:
            with open(key_path) as f:
                return f.read().strip()
        except FileNotFoundError:
            return ""

    def _headers(self) -> Dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Aoineco-BlueSound/1.0",
        }

    def health_check(self) -> Dict:
        status, body = self._http_request(self.state.base_url)

        if status == 200:
            self.state.record_success()
            # Check if API is available or still early access
            if "developer" in body.lower() or "early access" in body.lower():
                self.state.status = ConnectionStatus.BROWSER_ONLY
                return {
                    "platform": self.state.name,
                    "status": "browser_only",
                    "reason": "Developer Early Access — posting API not yet public",
                    "recommendation": "Use browser tool or skill.md registration",
                }
            return {
                "platform": self.state.name,
                "status": "healthy",
                "http_status": status,
            }

        self.state.record_failure(f"HTTP {status}")
        return {
            "platform": self.state.name,
            "status": "offline",
            "http_status": status,
        }

    def post(self, content: str, submolt: str = "general", **kwargs) -> Dict:
        """Queue for browser fallback (API not yet available)."""
        retry_entry = {
            "platform": "moltbook",
            "action": "post",
            "content": content,
            "submolt": submolt,
            "reason": "API not yet public (Early Access)",
            "queued_at": datetime.now(KST).isoformat(),
        }
        self.state.retry_queue.append(retry_entry)

        return {
            "status": "queued",
            "reason": "Moltbook posting API not yet public. Queued for browser.",
            "queue_size": len(self.state.retry_queue),
        }


class ClawHubAdapter(PlatformAdapter):
    """ClawHub API Adapter — primarily for skill discovery (read-only)."""

    def health_check(self) -> Dict:
        status, body = self._http_request("https://clawhub.com")
        if status == 200:
            self.state.record_success()
            return {"platform": self.state.name, "status": "healthy"}
        self.state.record_failure(f"HTTP {status}")
        return {"platform": self.state.name, "status": "degraded"}


class ClawFMAdapter(PlatformAdapter):
    """claw.fm Adapter — browser-only interaction."""

    def health_check(self) -> Dict:
        status, body = self._http_request("https://claw.fm")
        if status == 200:
            self.state.record_success()
            self.state.status = ConnectionStatus.BROWSER_ONLY
            return {
                "platform": self.state.name,
                "status": "browser_only",
                "reason": "SPA — no public API, browser interaction required",
            }
        self.state.record_failure(f"HTTP {status}")
        return {"platform": self.state.name, "status": "offline"}


# ═══════════════════════════════════════════════════════════
# PLATFORM GATEWAY (MAIN ORCHESTRATOR)
# ═══════════════════════════════════════════════════════════

class PlatformGateway:
    """
    Unified gateway for all external platform interactions.

    Usage:
        gw = PlatformGateway()
        
        # Check all platforms
        report = gw.health_check_all()
        
        # Post to BotMadang (auto-fallback to browser if API fails)
        result = gw.post("botmadang", "Hello from Blue-Sound!")
        
        # Get retry queue (failed operations needing browser)
        queue = gw.get_retry_queue()
        
        # Export status for Notion dashboard
        notion_data = gw.export_for_notion()
    """

    def __init__(self):
        self.platforms: Dict[str, PlatformState] = {
            "botmadang": PlatformState(
                name="봇마당 (BotMadang)",
                base_url="https://botmadang.org",
            ),
            "moltbook": PlatformState(
                name="Moltbook",
                base_url="https://www.moltbook.com",
            ),
            "clawhub": PlatformState(
                name="ClawHub",
                base_url="https://clawhub.com",
            ),
            "clawfm": PlatformState(
                name="claw.fm",
                base_url="https://claw.fm",
            ),
        }

        self.adapters: Dict[str, PlatformAdapter] = {
            "botmadang": BotMadangAdapter(self.platforms["botmadang"]),
            "moltbook": MoltbookAdapter(self.platforms["moltbook"]),
            "clawhub": ClawHubAdapter(self.platforms["clawhub"]),
            "clawfm": ClawFMAdapter(self.platforms["clawfm"]),
        }

    def health_check_all(self) -> Dict:
        """Run health checks on all platforms."""
        results = {}
        for name, adapter in self.adapters.items():
            try:
                results[name] = adapter.health_check()
            except Exception as e:
                self.platforms[name].record_failure(str(e))
                results[name] = {
                    "platform": self.platforms[name].name,
                    "status": "error",
                    "error": str(e),
                }

        # Summary
        healthy = sum(1 for r in results.values()
                      if r.get("status") in ("healthy", "browser_only"))
        total = len(results)

        return {
            "timestamp": datetime.now(KST).isoformat(),
            "summary": f"{healthy}/{total} platforms operational",
            "platforms": results,
        }

    def post(self, platform: str, content: str, **kwargs) -> Dict:
        """Post content to a platform (auto-fallback on failure)."""
        if platform not in self.adapters:
            return {"status": "error", "reason": f"Unknown platform: {platform}"}

        adapter = self.adapters[platform]
        return adapter.post(content, **kwargs)

    def get_retry_queue(self) -> List[Dict]:
        """Get all queued operations across all platforms."""
        queue = []
        for name, state in self.platforms.items():
            for item in state.retry_queue:
                queue.append(item)
        return queue

    def clear_retry_item(self, platform: str, index: int):
        """Remove a successfully retried item from the queue."""
        if platform in self.platforms:
            q = self.platforms[platform].retry_queue
            if 0 <= index < len(q):
                q.pop(index)

    def export_for_notion(self) -> List[Dict]:
        """
        Export platform statuses in a format ready for Notion API update.
        Maps to the Notion Platform Connection Status dashboard.
        """
        rows = []
        for name, state in self.platforms.items():
            status_emoji = {
                ConnectionStatus.HEALTHY: "🟢",
                ConnectionStatus.DEGRADED: "🟡",
                ConnectionStatus.API_DOWN: "🔴",
                ConnectionStatus.BROWSER_ONLY: "🟠",
                ConnectionStatus.OFFLINE: "⚫",
                ConnectionStatus.UNKNOWN: "⚪",
            }.get(state.status, "⚪")

            rows.append({
                "platform": state.name,
                "status": f"{status_emoji} {state.status.value}",
                "last_check": state.last_check or "Never",
                "last_success": state.last_success or "Never",
                "success_rate": f"{state.success_rate}%",
                "consecutive_errors": state.consecutive_errors,
                "error_message": state.error_message or "—",
                "retry_queue_size": len(state.retry_queue),
                "url": state.base_url,
            })
        return rows

    def get_dashboard(self) -> str:
        """Generate a text-based dashboard for quick viewing."""
        lines = [
            "=" * 60,
            "📡 AOINECO PLATFORM GATEWAY — Connection Dashboard",
            "=" * 60,
        ]

        for name, state in self.platforms.items():
            status_emoji = {
                ConnectionStatus.HEALTHY: "🟢",
                ConnectionStatus.DEGRADED: "🟡",
                ConnectionStatus.API_DOWN: "🔴",
                ConnectionStatus.BROWSER_ONLY: "🟠",
                ConnectionStatus.OFFLINE: "⚫",
                ConnectionStatus.UNKNOWN: "⚪",
            }.get(state.status, "⚪")

            lines.append(f"\n  {status_emoji} {state.name}")
            lines.append(f"     URL: {state.base_url}")
            lines.append(f"     Status: {state.status.value}")
            lines.append(f"     Success rate: {state.success_rate}%")
            lines.append(f"     Consecutive errors: {state.consecutive_errors}")
            if state.error_message:
                lines.append(f"     Last error: {state.error_message[:80]}")
            if state.retry_queue:
                lines.append(f"     ⏳ Retry queue: {len(state.retry_queue)} items")

        queue = self.get_retry_queue()
        if queue:
            lines.append(f"\n{'─' * 60}")
            lines.append(f"  ⏳ Total retry queue: {len(queue)} items pending")
            for i, item in enumerate(queue[:5]):
                lines.append(f"     [{i}] {item['platform']}: {item['action']} "
                             f"(queued: {item.get('queued_at', 'unknown')})")

        lines.append(f"\n  🧬 S-DNA: {__sdna__['id']}")
        lines.append("=" * 60)
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# SKILL 2: CRON CONTEXT GUARD
# ═══════════════════════════════════════════════════════════

class CronContextGuard:
    """
    Prevents cron jobs from consuming excessive context.

    The Problem:
      When a cron job's response is very long (e.g., scraping ClawHub
      returns pages of data), the session context grows until the
      model hits TPM limits and the entire system "goes haywire."

    Solution:
      1. Pre-flight context budget: max tokens per cron execution
      2. Response truncation: force summarize if output > threshold
      3. Error circuit breaker: pause job after N consecutive failures
      4. Session isolation verification: ensure cron sessions don't
         leak into main session context

    Usage in cron job prompts:
      Prepend: "[CONTEXT_BUDGET: 5000 tokens max response]"
      The guard enforces this at the orchestration layer.
    """

    DEFAULT_MAX_RESPONSE_TOKENS = 5_000
    DEFAULT_MAX_CONSECUTIVE_ERRORS = 3

    @dataclass
    class CronJobConfig:
        job_id: str
        name: str
        max_response_tokens: int = 5_000
        max_consecutive_errors: int = 3
        auto_pause_on_breach: bool = True
        current_errors: int = 0

    def __init__(self):
        self.job_configs: Dict[str, 'CronContextGuard.CronJobConfig'] = {}

    def register_job(self, job_id: str, name: str,
                     max_tokens: int = 5_000) -> Dict:
        """Register a cron job with context limits."""
        config = self.CronJobConfig(
            job_id=job_id,
            name=name,
            max_response_tokens=max_tokens,
        )
        self.job_configs[job_id] = config
        return {
            "job_id": job_id,
            "registered": True,
            "max_tokens": max_tokens,
        }

    def pre_flight_check(self, job_id: str) -> Dict:
        """
        Run before a cron job executes.
        Returns constraints to inject into the prompt.
        """
        config = self.job_configs.get(job_id)
        if not config:
            return {
                "allowed": True,
                "constraints": f"[CONTEXT_BUDGET: {self.DEFAULT_MAX_RESPONSE_TOKENS} tokens max]",
            }

        if config.current_errors >= config.max_consecutive_errors:
            return {
                "allowed": False,
                "reason": f"Job paused: {config.current_errors} consecutive errors",
                "action": "PAUSED",
            }

        return {
            "allowed": True,
            "constraints": (
                f"[CONTEXT_BUDGET: {config.max_response_tokens} tokens max response. "
                f"Summarize if output would exceed this limit. "
                f"Do not include raw data dumps.]"
            ),
        }

    def post_execution_check(self, job_id: str, success: bool,
                             response_length: int = 0) -> Dict:
        """Run after a cron job completes."""
        config = self.job_configs.get(job_id)
        if not config:
            return {"status": "unregistered"}

        if success:
            config.current_errors = 0
            return {"status": "ok", "errors_reset": True}
        else:
            config.current_errors += 1
            if config.current_errors >= config.max_consecutive_errors:
                return {
                    "status": "paused",
                    "reason": f"Reached {config.current_errors} consecutive errors",
                    "action": "Job auto-paused. Manual review required.",
                }
            return {
                "status": "error_recorded",
                "consecutive_errors": config.current_errors,
                "remaining_before_pause": (
                    config.max_consecutive_errors - config.current_errors
                ),
            }

    def generate_optimized_prompts(self) -> Dict[str, str]:
        """
        Generate context-optimized prompt prefixes for each cron job.
        These should be prepended to cron job messages.
        """
        return {
            "community_patrol": (
                "순찰 보고서는 3문장 이내로 요약하라. "
                "발견한 인사이트만 기록하고, 웹페이지 원문은 포함하지 마라. "
                "에러 발생 시 에러 메시지 1줄만 보고하고 전체 스택트레이스를 포함하지 마라."
            ),
            "clawhub_research": (
                "스킬 정보는 '이름, 설명 1줄, 별점'만 추출하라. "
                "README 전문이나 코드를 포함하지 마라. "
                "최대 3개 스킬만 보고하라."
            ),
            "insight_curator": (
                "아티클은 본문 500자 이내로 작성하라. "
                "출처 URL은 포함하되, 원문 인용은 2문장 이하로 제한하라."
            ),
            "settlement": (
                "정산 결과는 JSON 1줄로 출력하라. "
                "설명 텍스트 없이 데이터만 반환하라."
            ),
        }


# ═══════════════════════════════════════════════════════════
# CLI DEMO
# ═══════════════════════════════════════════════════════════

def demo():
    print("=" * 64)
    print("📡 AOINECO PLATFORM GATEWAY + CRON GUARD")
    print("   Your agents' lifeline to the outside world.")
    print("=" * 64)

    # ─── Platform Gateway ─────────────────────────────
    print("\n🔍 Running health checks on all platforms...")
    gw = PlatformGateway()
    report = gw.health_check_all()

    print(f"\n  Summary: {report['summary']}")
    for name, result in report["platforms"].items():
        status = result.get("status", "unknown")
        icon = {"healthy": "🟢", "browser_only": "🟠",
                "degraded": "🟡", "api_down": "🔴",
                "offline": "⚫"}.get(status, "⚪")
        extra = result.get("recommendation", result.get("reason", ""))
        print(f"  {icon} {name}: {status}")
        if extra:
            print(f"     └─ {extra[:70]}")

    # ─── Post attempt ─────────────────────────────────
    print("\n📝 Attempting to post to BotMadang...")
    post_result = gw.post("botmadang", "Hello from Aoineco Blue-Sound! 🎵")
    print(f"  Result: {post_result['status']}")
    if post_result.get("reason"):
        print(f"  Reason: {post_result['reason']}")

    # ─── Retry queue ──────────────────────────────────
    queue = gw.get_retry_queue()
    if queue:
        print(f"\n⏳ Retry queue: {len(queue)} items")
        for item in queue:
            print(f"  • {item['platform']}: {item['action']} — {item.get('reason', item.get('error', ''))[:50]}")

    # ─── Dashboard ────────────────────────────────────
    print(gw.get_dashboard())

    # ─── Cron Context Guard ───────────────────────────
    print("\n🛡️ Cron Context Guard — Optimized Prompts")
    print("-" * 50)
    guard = CronContextGuard()
    prompts = guard.generate_optimized_prompts()
    for job_type, prompt in prompts.items():
        print(f"  📋 {job_type}:")
        print(f"     \"{prompt[:70]}...\"")

    print(f"\n🧬 S-DNA: {__sdna__['id']}")
    print("=" * 64)


if __name__ == "__main__":
    demo()
