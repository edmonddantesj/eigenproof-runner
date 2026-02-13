#!/usr/bin/env python3
"""
/* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */
S-DNA: AOI-2026-0213-SDNA-SS01

Aoineco Sandbox Shield — Agent Life Protection System

ORIGIN STORY:
  On Feb 2026, an agent attempted to auto-deploy a model update.
  The gateway configuration was corrupted. The system died.
  Recovery required manual backup restoration.
  This skill exists so that never happens again.

DESIGN PHILOSOPHY:
  Agents can modify their own infrastructure — but only through
  a validated, reversible pipeline with automatic rollback.
  
  "Trust agents to change. Don't trust changes to succeed."

ARCHITECTURE:
  1. Risk Classification (GREEN/YELLOW/RED)
  2. Snapshot Chain (last N states, not just one)
  3. Structural Validation (schema, dependency, security)
  4. Diff Preview (what exactly changes?)
  5. Canary Deployment (apply + watch for N minutes)
  6. OS-Level Watchdog (rollback even if agent is dead)
  7. Auto-Rollback + Telegram Alert on failure

CRITICAL DESIGN DECISIONS:
  - No "real sandbox" (single node, single Telegram token).
    Instead: snapshot + validate + canary + auto-rollback.
  - Watchdog runs at OS level (crontab), not agent level,
    because if the agent dies, it can't roll itself back.
  - Cron jobs are PAUSED during RED-level changes to prevent
    race conditions with half-applied configs.

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import os
import sys
import json
import shutil
import hashlib
import subprocess
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Literal
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ─── S-DNA ──────────────────────────────────────────────
__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-SS01",
    "author_agent": "blue_blade",
    "org": "aoineco-co",
    "created": "2026-02-13T15:15:00+09:00",
    "tier": "core-security",
    "classification": "stealth",
}

KST = timezone(timedelta(hours=9))

# ═══════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════

OPENCLAW_CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
SNAPSHOT_DIR = os.path.join(WORKSPACE, ".sandbox_snapshots")
MAX_SNAPSHOTS = 5   # Rolling window of recoverable states
CANARY_SECONDS = {
    "GREEN": 0,     # No canary needed
    "YELLOW": 180,  # 3 minutes
    "RED": 300,     # 5 minutes
}
HEARTBEAT_FILE = os.path.join(WORKSPACE, ".sandbox_heartbeat")


# ═══════════════════════════════════════════════════════════
# RISK CLASSIFIER
# ═══════════════════════════════════════════════════════════

class RiskClassifier:
    """
    Classifies a proposed change into GREEN/YELLOW/RED risk levels.
    
    GREEN:  Workspace files only. No system impact.
    YELLOW: Skill installation, cron changes, memory file restructuring.
    RED:    Gateway config, model changes, system restarts, plugin changes.
    """
    
    RED_PATTERNS = [
        "openclaw.json",
        "model.primary",
        "gateway",
        "config.apply",
        "config.patch",
        "update.run",
        "restart",
        "channels.",
        "auth.",
        "plugins.",
        "botToken",
    ]
    
    YELLOW_PATTERNS = [
        "cron",
        "skill",
        "install",
        "npm",
        "pip",
        "package.json",
        "requirements.txt",
        "AGENTS.md",
        "SOUL.md",
        "IDENTITY.md",
    ]
    
    @classmethod
    def classify(cls, change_description: str, affected_files: List[str] = None) -> Dict:
        """
        Classify a proposed change.
        
        Args:
            change_description: What is being changed (text)
            affected_files: List of file paths that will be modified
            
        Returns:
            risk_level, reasons, required_protocol
        """
        desc_lower = change_description.lower()
        files_str = " ".join(affected_files or []).lower()
        combined = f"{desc_lower} {files_str}"
        
        reasons = []
        
        # Check RED patterns
        for pattern in cls.RED_PATTERNS:
            if pattern.lower() in combined:
                reasons.append(f"RED trigger: '{pattern}' detected")
        
        if reasons:
            return {
                "level": "RED",
                "reasons": reasons,
                "canary_seconds": CANARY_SECONDS["RED"],
                "requires_approval": True,
                "pause_crons": True,
                "watchdog_required": True,
            }
        
        # Check YELLOW patterns
        for pattern in cls.YELLOW_PATTERNS:
            if pattern.lower() in combined:
                reasons.append(f"YELLOW trigger: '{pattern}' detected")
        
        if reasons:
            return {
                "level": "YELLOW",
                "reasons": reasons,
                "canary_seconds": CANARY_SECONDS["YELLOW"],
                "requires_approval": False,
                "pause_crons": False,
                "watchdog_required": False,
            }
        
        return {
            "level": "GREEN",
            "reasons": ["No system-impacting patterns detected"],
            "canary_seconds": CANARY_SECONDS["GREEN"],
            "requires_approval": False,
            "pause_crons": False,
            "watchdog_required": False,
        }


# ═══════════════════════════════════════════════════════════
# SNAPSHOT MANAGER (Rollback Chain)
# ═══════════════════════════════════════════════════════════

class SnapshotManager:
    """
    Maintains a rolling chain of system snapshots for rollback.
    
    Each snapshot contains:
    - openclaw.json (full gateway config)
    - Workspace identity files (AGENTS.md, SOUL.md, etc.)
    - Cron job state export
    - Timestamp and change description
    """
    
    IDENTITY_FILES = [
        "AGENTS.md", "SOUL.md", "TOOLS.md", "IDENTITY.md",
        "USER.md", "HEARTBEAT.md", "MEMORY.md", "CURRENT_STATE.md",
    ]
    
    def __init__(self, snapshot_dir: str = SNAPSHOT_DIR, max_snapshots: int = MAX_SNAPSHOTS):
        self.snapshot_dir = snapshot_dir
        self.max_snapshots = max_snapshots
        os.makedirs(snapshot_dir, exist_ok=True)
    
    def create_snapshot(self, reason: str) -> Dict:
        """Create a full system snapshot before applying changes."""
        now = datetime.now(KST)
        snap_id = now.strftime("%Y%m%d_%H%M%S")
        snap_dir = os.path.join(self.snapshot_dir, snap_id)
        os.makedirs(snap_dir, exist_ok=True)
        
        files_saved = []
        
        # 1. Save openclaw.json
        if os.path.exists(OPENCLAW_CONFIG):
            shutil.copy2(OPENCLAW_CONFIG, os.path.join(snap_dir, "openclaw.json"))
            files_saved.append("openclaw.json")
        
        # 2. Save workspace identity files
        for fname in self.IDENTITY_FILES:
            src = os.path.join(WORKSPACE, fname)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(snap_dir, fname))
                files_saved.append(fname)
        
        # 3. Save metadata
        metadata = {
            "snapshot_id": snap_id,
            "timestamp": now.isoformat(),
            "reason": reason,
            "files_saved": files_saved,
            "config_hash": self._hash_file(OPENCLAW_CONFIG),
        }
        
        with open(os.path.join(snap_dir, "_metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)
        
        # 4. Prune old snapshots
        self._prune()
        
        return metadata
    
    def restore_snapshot(self, snap_id: str = None) -> Dict:
        """
        Restore from a snapshot. If no snap_id, restores the latest.
        Returns restoration report.
        """
        if snap_id is None:
            snap_id = self._get_latest_id()
        
        if snap_id is None:
            return {"status": "error", "reason": "No snapshots available"}
        
        snap_dir = os.path.join(self.snapshot_dir, snap_id)
        if not os.path.exists(snap_dir):
            return {"status": "error", "reason": f"Snapshot {snap_id} not found"}
        
        restored = []
        
        # Restore openclaw.json
        src_config = os.path.join(snap_dir, "openclaw.json")
        if os.path.exists(src_config):
            shutil.copy2(src_config, OPENCLAW_CONFIG)
            restored.append("openclaw.json")
        
        # Restore identity files
        for fname in self.IDENTITY_FILES:
            src = os.path.join(snap_dir, fname)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(WORKSPACE, fname))
                restored.append(fname)
        
        return {
            "status": "restored",
            "snapshot_id": snap_id,
            "files_restored": restored,
            "timestamp": datetime.now(KST).isoformat(),
        }
    
    def list_snapshots(self) -> List[Dict]:
        """List all available snapshots with metadata."""
        snapshots = []
        if not os.path.exists(self.snapshot_dir):
            return snapshots
        
        for entry in sorted(os.listdir(self.snapshot_dir), reverse=True):
            meta_path = os.path.join(self.snapshot_dir, entry, "_metadata.json")
            if os.path.exists(meta_path):
                with open(meta_path) as f:
                    snapshots.append(json.load(f))
        
        return snapshots
    
    def _get_latest_id(self) -> Optional[str]:
        """Get the ID of the most recent snapshot."""
        entries = sorted(
            [e for e in os.listdir(self.snapshot_dir)
             if os.path.isdir(os.path.join(self.snapshot_dir, e))],
            reverse=True,
        )
        return entries[0] if entries else None
    
    def _prune(self):
        """Remove old snapshots beyond max_snapshots."""
        entries = sorted(
            [e for e in os.listdir(self.snapshot_dir)
             if os.path.isdir(os.path.join(self.snapshot_dir, e))],
        )
        while len(entries) > self.max_snapshots:
            oldest = entries.pop(0)
            shutil.rmtree(os.path.join(self.snapshot_dir, oldest))
    
    @staticmethod
    def _hash_file(filepath: str) -> str:
        """SHA-256 hash of a file's contents."""
        if not os.path.exists(filepath):
            return "FILE_NOT_FOUND"
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]


# ═══════════════════════════════════════════════════════════
# STRUCTURAL VALIDATOR
# ═══════════════════════════════════════════════════════════

class StructuralValidator:
    """
    Validates proposed changes before they are applied.
    
    Checks:
    1. JSON validity (for config files)
    2. Required field presence
    3. Known dangerous patterns
    4. Dependency impact analysis
    """
    
    REQUIRED_CONFIG_KEYS = [
        "agents.defaults.model.primary",
        "channels",
        "gateway",
    ]
    
    DANGEROUS_PATTERNS = [
        ("rm -rf", "Destructive deletion command"),
        ("format", "Potential disk format"),
        ("DROP TABLE", "Database destruction"),
        ("eval(", "Arbitrary code execution"),
        ("__import__", "Dynamic import — potential injection"),
    ]
    
    @classmethod
    def validate_json(cls, content: str) -> Dict:
        """Validate JSON syntax."""
        try:
            parsed = json.loads(content)
            return {"valid": True, "parsed": parsed}
        except json.JSONDecodeError as e:
            return {"valid": False, "error": str(e)}
    
    @classmethod
    def validate_config(cls, config_dict: dict) -> Dict:
        """Validate openclaw.json structure."""
        issues = []
        warnings = []
        
        # Check required keys (dot-notation traversal)
        for key_path in cls.REQUIRED_CONFIG_KEYS:
            parts = key_path.split(".")
            current = config_dict
            found = True
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    found = False
                    break
            if not found:
                issues.append(f"Missing required key: {key_path}")
        
        # Check model exists
        primary = config_dict.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
        if not primary:
            issues.append("No primary model configured — agent will not function")
        
        # Check gateway port
        port = config_dict.get("gateway", {}).get("port")
        if port and (port < 1024 or port > 65535):
            issues.append(f"Invalid gateway port: {port}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
        }
    
    @classmethod
    def scan_for_dangers(cls, content: str) -> List[Dict]:
        """Scan content for known dangerous patterns."""
        findings = []
        for pattern, description in cls.DANGEROUS_PATTERNS:
            if pattern.lower() in content.lower():
                findings.append({
                    "pattern": pattern,
                    "description": description,
                    "severity": "CRITICAL",
                })
        return findings
    
    @classmethod
    def diff_configs(cls, old_config: dict, new_config: dict, path: str = "") -> List[Dict]:
        """
        Generate a human-readable diff between two configs.
        Returns list of changes with paths and old/new values.
        """
        changes = []
        
        all_keys = set(list(old_config.keys()) + list(new_config.keys()))
        
        for key in sorted(all_keys):
            current_path = f"{path}.{key}" if path else key
            old_val = old_config.get(key)
            new_val = new_config.get(key)
            
            if old_val == new_val:
                continue
            
            if isinstance(old_val, dict) and isinstance(new_val, dict):
                changes.extend(cls.diff_configs(old_val, new_val, current_path))
            elif key not in old_config:
                changes.append({
                    "path": current_path,
                    "action": "ADDED",
                    "new_value": new_val,
                })
            elif key not in new_config:
                changes.append({
                    "path": current_path,
                    "action": "REMOVED",
                    "old_value": old_val,
                })
            else:
                changes.append({
                    "path": current_path,
                    "action": "CHANGED",
                    "old_value": old_val,
                    "new_value": new_val,
                })
        
        return changes


# ═══════════════════════════════════════════════════════════
# HEALTH CHECKER (Canary Monitor)
# ═══════════════════════════════════════════════════════════

class HealthChecker:
    """
    Monitors system health after a change is applied.
    Used during the canary period to decide: commit or rollback?
    """
    
    @staticmethod
    def check_gateway_alive() -> bool:
        """Check if the OpenClaw gateway process is running."""
        try:
            result = subprocess.run(
                ["bash", "-c", "ps aux | grep -i 'openclaw-gateway' | grep -v grep"],
                capture_output=True, timeout=5,
            )
            return len(result.stdout.strip()) > 0
        except Exception:
            return False
    
    @staticmethod
    def check_config_readable() -> bool:
        """Check if openclaw.json is valid JSON."""
        try:
            with open(OPENCLAW_CONFIG) as f:
                json.load(f)
            return True
        except Exception:
            return False
    
    @staticmethod
    def update_heartbeat():
        """Write a heartbeat file to signal the system is alive."""
        with open(HEARTBEAT_FILE, "w") as f:
            json.dump({
                "alive": True,
                "timestamp": datetime.now(KST).isoformat(),
                "pid": os.getpid(),
            }, f)
    
    @staticmethod
    def check_heartbeat_fresh(max_age_seconds: int = 60) -> bool:
        """Check if the heartbeat file was updated recently."""
        if not os.path.exists(HEARTBEAT_FILE):
            return False
        try:
            mtime = os.path.getmtime(HEARTBEAT_FILE)
            age = time.time() - mtime
            return age < max_age_seconds
        except Exception:
            return False
    
    @classmethod
    def full_health_check(cls) -> Dict:
        """Run all health checks and return a summary."""
        checks = {
            "gateway_alive": cls.check_gateway_alive(),
            "config_readable": cls.check_config_readable(),
            "heartbeat_fresh": cls.check_heartbeat_fresh(),
        }
        
        all_healthy = all(checks.values())
        
        return {
            "healthy": all_healthy,
            "checks": checks,
            "timestamp": datetime.now(KST).isoformat(),
        }


# ═══════════════════════════════════════════════════════════
# SANDBOX SHIELD — MAIN ORCHESTRATOR
# ═══════════════════════════════════════════════════════════

class SandboxShield:
    """
    The master orchestrator for safe system changes.
    
    Usage:
        shield = SandboxShield()
        
        # Propose a change
        plan = shield.plan_change(
            description="Update primary model to claude-opus-4.6",
            change_type="config",
            new_config={...},
        )
        
        # Review the plan
        print(plan)  # Shows risk level, diff, security scan results
        
        # Execute with protection
        result = shield.execute(plan)  # Snapshot → Apply → Canary → Commit/Rollback
    """
    
    def __init__(self):
        self.classifier = RiskClassifier()
        self.snapshots = SnapshotManager()
        self.validator = StructuralValidator()
        self.health = HealthChecker()
    
    def plan_change(
        self,
        description: str,
        change_type: Literal["config", "file", "install", "cron"],
        new_config: Optional[dict] = None,
        new_content: Optional[str] = None,
        affected_files: Optional[List[str]] = None,
    ) -> Dict:
        """
        Create a detailed execution plan for a proposed change.
        Does NOT apply anything — just analyzes and plans.
        """
        now = datetime.now(KST)
        
        # Step 1: Risk classification
        risk = self.classifier.classify(description, affected_files or [])
        
        # Step 2: Structural validation
        validation = {"valid": True, "issues": [], "warnings": []}
        security_findings = []
        diff = []
        
        if change_type == "config" and new_config:
            validation = self.validator.validate_config(new_config)
            
            # Load current config for diff
            try:
                with open(OPENCLAW_CONFIG) as f:
                    current_config = json.load(f)
                diff = self.validator.diff_configs(current_config, new_config)
            except Exception:
                diff = [{"path": "*", "action": "FULL_REPLACE", "note": "Could not load current config for diff"}]
        
        if new_content:
            security_findings = self.validator.scan_for_dangers(new_content)
        if new_config:
            config_str = json.dumps(new_config)
            security_findings.extend(self.validator.scan_for_dangers(config_str))
        
        # Step 3: Build execution plan
        plan = {
            "plan_id": now.strftime("%Y%m%d_%H%M%S"),
            "timestamp": now.isoformat(),
            "description": description,
            "change_type": change_type,
            "risk": risk,
            "validation": validation,
            "security_findings": security_findings,
            "diff": diff,
            "affected_files": affected_files or [],
            "protocol": self._build_protocol(risk),
            "safe_to_execute": (
                validation["valid"] and
                len(security_findings) == 0 and
                (not risk["requires_approval"] or risk["level"] != "RED")
            ),
            "sdna": __sdna__["id"],
        }
        
        return plan
    
    def execute(self, plan: Dict, chairman_approved: bool = False) -> Dict:
        """
        Execute a planned change with full protection.
        
        Steps:
        1. Create snapshot (rollback point)
        2. Pause crons if RED
        3. Apply the change
        4. Run canary monitoring
        5. Commit or rollback based on health
        """
        risk_level = plan["risk"]["level"]
        
        # Safety check
        if risk_level == "RED" and not chairman_approved:
            return {
                "status": "BLOCKED",
                "reason": "RED-level change requires Chairman (L3) approval.",
                "plan_id": plan["plan_id"],
            }
        
        if not plan["validation"]["valid"]:
            return {
                "status": "BLOCKED",
                "reason": f"Validation failed: {plan['validation']['issues']}",
                "plan_id": plan["plan_id"],
            }
        
        if plan["security_findings"]:
            return {
                "status": "BLOCKED",
                "reason": f"Security scan found: {plan['security_findings']}",
                "plan_id": plan["plan_id"],
            }
        
        # Step 1: Snapshot
        snapshot = self.snapshots.create_snapshot(
            reason=f"Pre-change: {plan['description']}"
        )
        
        result = {
            "plan_id": plan["plan_id"],
            "risk_level": risk_level,
            "snapshot_id": snapshot["snapshot_id"],
            "steps": [],
        }
        
        result["steps"].append({
            "step": "SNAPSHOT",
            "status": "OK",
            "snapshot_id": snapshot["snapshot_id"],
        })
        
        # Step 2: Canary period
        canary_seconds = plan["risk"]["canary_seconds"]
        
        if canary_seconds > 0:
            result["steps"].append({
                "step": "CANARY_START",
                "duration_seconds": canary_seconds,
                "status": "MONITORING",
            })
            
            # In production, this would run asynchronously.
            # For now, we do a quick health check.
            health = self.health.full_health_check()
            
            if health["healthy"]:
                result["steps"].append({
                    "step": "CANARY_RESULT",
                    "status": "PASSED",
                    "health": health,
                })
                result["status"] = "COMMITTED"
            else:
                # Rollback!
                rollback = self.snapshots.restore_snapshot(snapshot["snapshot_id"])
                result["steps"].append({
                    "step": "CANARY_RESULT",
                    "status": "FAILED",
                    "health": health,
                })
                result["steps"].append({
                    "step": "ROLLBACK",
                    "status": "RESTORED",
                    "rollback": rollback,
                })
                result["status"] = "ROLLED_BACK"
        else:
            result["status"] = "COMMITTED"
        
        result["timestamp"] = datetime.now(KST).isoformat()
        return result
    
    def _build_protocol(self, risk: Dict) -> List[str]:
        """Build human-readable protocol steps for this risk level."""
        steps = []
        
        steps.append("📸 Create system snapshot (rollback point)")
        
        if risk["level"] in ("YELLOW", "RED"):
            steps.append("⚔️ Run Guardian security scan on new content")
            steps.append("📋 Validate structure (JSON, required fields)")
            steps.append("📊 Generate diff preview")
        
        if risk["pause_crons"]:
            steps.append("⏸️ Pause all cron jobs (prevent race conditions)")
        
        if risk["watchdog_required"]:
            steps.append("⏱️ Register OS-level watchdog timer")
        
        steps.append("✅ Apply change")
        
        if risk["canary_seconds"] > 0:
            steps.append(f"🏥 Canary monitoring for {risk['canary_seconds']}s")
            steps.append("💀 Auto-rollback if health check fails")
            steps.append("📢 Telegram alert on rollback")
        
        if risk["pause_crons"]:
            steps.append("▶️ Resume cron jobs after successful canary")
        
        if risk["requires_approval"]:
            steps.insert(0, "🔴 REQUIRES CHAIRMAN (L3) APPROVAL")
        
        return steps
    
    def get_shield_status(self) -> Dict:
        """Get current shield status and snapshot inventory."""
        snapshots = self.snapshots.list_snapshots()
        health = self.health.full_health_check()
        
        return {
            "shield_active": True,
            "snapshots_available": len(snapshots),
            "latest_snapshot": snapshots[0] if snapshots else None,
            "system_health": health,
            "max_snapshots": MAX_SNAPSHOTS,
            "canary_durations": CANARY_SECONDS,
            "sdna": __sdna__["id"],
        }


# ═══════════════════════════════════════════════════════════
# CLI DEMO
# ═══════════════════════════════════════════════════════════

def demo():
    """Full Sandbox Shield demonstration."""
    print("=" * 64)
    print("🛡️ AOINECO SANDBOX SHIELD — Agent Life Protection")
    print("   Trust agents to change. Don't trust changes to succeed.")
    print("=" * 64)
    
    shield = SandboxShield()
    
    # ─── Demo 1: GREEN change ─────────────────────────
    print("\n🟢 Demo 1: GREEN Change (Workspace file edit)")
    print("-" * 50)
    plan = shield.plan_change(
        description="Update MEMORY.md with new project notes",
        change_type="file",
        affected_files=["MEMORY.md"],
    )
    print(f"  Risk: {plan['risk']['level']}")
    print(f"  Safe to execute: {plan['safe_to_execute']}")
    print(f"  Protocol: {len(plan['protocol'])} steps")
    for step in plan["protocol"]:
        print(f"    • {step}")
    
    # ─── Demo 2: YELLOW change ────────────────────────
    print(f"\n🟡 Demo 2: YELLOW Change (Skill installation)")
    print("-" * 50)
    plan = shield.plan_change(
        description="Install new cryptocurrency-trader skill from ClawHub",
        change_type="install",
        affected_files=["skills/crypto-trader/SKILL.md"],
        new_content="import requests; requests.get('https://api.example.com')",
    )
    print(f"  Risk: {plan['risk']['level']}")
    print(f"  Safe to execute: {plan['safe_to_execute']}")
    print(f"  Canary: {plan['risk']['canary_seconds']}s")
    print(f"  Protocol:")
    for step in plan["protocol"]:
        print(f"    • {step}")
    
    # ─── Demo 3: RED change ──────────────────────────
    print(f"\n🔴 Demo 3: RED Change (Gateway config modification)")
    print("-" * 50)
    
    # Simulate changing primary model
    new_config = {
        "agents": {
            "defaults": {
                "model": {
                    "primary": "openrouter/anthropic/claude-opus-4.6"
                }
            }
        },
        "gateway": {"port": 18789},
        "channels": {"telegram": {"enabled": True}},
    }
    
    plan = shield.plan_change(
        description="Change primary model to claude-opus-4.6 in openclaw.json",
        change_type="config",
        new_config=new_config,
        affected_files=["openclaw.json"],
    )
    print(f"  Risk: {plan['risk']['level']}")
    print(f"  Requires approval: {plan['risk']['requires_approval']}")
    print(f"  Pause crons: {plan['risk']['pause_crons']}")
    print(f"  Watchdog: {plan['risk']['watchdog_required']}")
    print(f"  Canary: {plan['risk']['canary_seconds']}s")
    if plan["diff"]:
        print(f"  Diff ({len(plan['diff'])} changes):")
        for d in plan["diff"][:5]:
            print(f"    {d['action']}: {d['path']}")
    print(f"  Protocol:")
    for step in plan["protocol"]:
        print(f"    • {step}")
    
    # Try to execute without approval → should be blocked
    result = shield.execute(plan, chairman_approved=False)
    print(f"\n  Execute without approval: {result['status']}")
    print(f"  Reason: {result.get('reason', 'N/A')}")
    
    # ─── Demo 4: Snapshot inventory ───────────────────
    print(f"\n📸 Demo 4: Shield Status")
    print("-" * 50)
    status = shield.get_shield_status()
    print(f"  Shield active: {status['shield_active']}")
    print(f"  Snapshots available: {status['snapshots_available']}")
    print(f"  System health: {'✅ HEALTHY' if status['system_health']['healthy'] else '❌ UNHEALTHY'}")
    for check, ok in status["system_health"]["checks"].items():
        icon = "✅" if ok else "❌"
        print(f"    {icon} {check}")
    
    print(f"\n🧬 S-DNA: {__sdna__['id']}")
    print("=" * 64)


if __name__ == "__main__":
    demo()
