from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class GateFinding:
    rule_id: str
    severity: str  # info|low|med|high
    message: str
    evidence: dict[str, Any] | None = None


DEFAULT_SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("AWS_ACCESS_KEY_ID", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("OPENAI_API_KEY", re.compile(r"sk-[A-Za-z0-9]{20,}")),
]

HEX_0X_64 = re.compile(r"0x[a-fA-F0-9]{64}")

# Heuristic allowlist: tx hashes are also 0x + 64 hex.
# We allow them in documentation contexts, but keep fail-closed elsewhere.
TXHASH_HINTS = {
    "txhash",
    "tx hash",
    "transaction hash",
    "txid",
    "explorer",
    "etherscan",
    "bscscan",
    "basescan",
    "arbiscan",
    "polygonscan",
    "solscan",
}

SENSITIVE_KEYWORDS = {
    "private key",
    "privkey",
    "seed",
    "mnemonic",
    "secret",
    "wallet",
}


def looks_like_doc_txhash(*, line: str, path: Path) -> bool:
    if path.suffix.lower() not in {".md", ".txt"}:
        return False
    l = line.lower()
    return any(h in l for h in TXHASH_HINTS)


def looks_like_secret_context(*, line: str) -> bool:
    l = line.lower()
    return any(k in l for k in SENSITIVE_KEYWORDS)


def scan_repo_snapshot(repo_dir: Path) -> list[GateFinding]:
    findings: list[GateFinding] = []

    lockfiles = ["package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock", "uv.lock", "Cargo.lock"]
    has_lock = any((repo_dir / lf).exists() for lf in lockfiles)
    if not has_lock:
        findings.append(
            GateFinding(
                rule_id="repro.lockfile.missing",
                severity="med",
                message="No common lockfile detected (reproducibility risk).",
                evidence={"checked": lockfiles},
            )
        )

    pkg = repo_dir / "package.json"
    if pkg.exists():
        try:
            j = json.loads(pkg.read_text(encoding="utf-8"))
            scripts = (j.get("scripts") or {})
            suspicious = []
            for name, cmd in scripts.items():
                if isinstance(cmd, str) and any(x in cmd.lower() for x in ["curl ", "wget ", "bash -c", "sh -c", "powershell", "nc "]):
                    suspicious.append({"name": name, "cmd": cmd})
            if suspicious:
                findings.append(
                    GateFinding(
                        rule_id="pkg.scripts.suspicious",
                        severity="high",
                        message="Suspicious package.json scripts detected.",
                        evidence={"scripts": suspicious},
                    )
                )
        except Exception as e:
            findings.append(
                GateFinding(
                    rule_id="pkg.json.parse_error",
                    severity="low",
                    message=f"package.json parse error: {e}",
                )
            )

    max_bytes = 200_000
    text_ext_allow = {".py", ".ts", ".js", ".json", ".md", ".sh", ".yaml", ".yml", ".toml", ".env", ""}

    for p in repo_dir.rglob("*"):
        if not p.is_file():
            continue
        if any(part in {"node_modules", ".git", ".venv", "venv"} for part in p.parts):
            continue
        try:
            if p.stat().st_size > max_bytes:
                continue
        except FileNotFoundError:
            continue

        if p.suffix not in text_ext_allow and p.name not in {".env"}:
            continue

        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        # 1) deterministic secret patterns
        for label, pat in DEFAULT_SECRET_PATTERNS:
            if pat.search(content):
                findings.append(
                    GateFinding(
                        rule_id="secrets.pattern.match",
                        severity="high",
                        message=f"Potential secret detected ({label}) in file {p.relative_to(repo_dir)}.",
                        evidence={"file": str(p.relative_to(repo_dir)), "pattern": label},
                    )
                )

        # 2) 0x64-hex patterns: treat as private key unless clearly a tx hash in docs.
        if HEX_0X_64.search(content):
            rel = str(p.relative_to(repo_dir))
            # scan line-by-line so we can apply context hints
            for i, line in enumerate(content.splitlines(), start=1):
                if not HEX_0X_64.search(line):
                    continue

                # Allow tx hashes in docs when explicitly labeled as such
                if looks_like_doc_txhash(line=line, path=p) and not looks_like_secret_context(line=line):
                    continue

                # If it's a doc but not clearly a tx hash, downgrade to MED (still visible)
                if p.suffix.lower() in {".md", ".txt"} and not looks_like_secret_context(line=line):
                    severity = "med"
                    rule_id = "secrets.hex64.maybe_txhash"
                    pattern = "HEX_0X_64"
                    msg = f"0x64-hex detected in doc; could be txhash or key. Verify context. file={rel}:{i}"
                else:
                    severity = "high"
                    rule_id = "secrets.pattern.match"
                    pattern = "PRIVATE_KEY_HEX"
                    msg = f"Potential secret detected (PRIVATE_KEY_HEX) in file {rel}:{i}."

                findings.append(
                    GateFinding(
                        rule_id=rule_id,
                        severity=severity,
                        message=msg,
                        evidence={"file": rel, "line": i, "pattern": pattern},
                    )
                )

                # don't spam too many lines per file
                if sum(1 for f in findings if (f.evidence or {}).get("file") == rel) >= 5:
                    break

    return findings


def score_findings(findings: list[GateFinding]) -> dict[str, Any]:
    weights = {"info": 0, "low": 10, "med": 25, "high": 60}
    score = 100
    max_sev = "info"
    for f in findings:
        score -= weights.get(f.severity, 10)
        if weights.get(f.severity, 0) > weights.get(max_sev, 0):
            max_sev = f.severity
    score = max(0, min(100, score))

    if max_sev == "high" or score < 60:
        signal = "red"
    elif score < 85:
        signal = "yellow"
    else:
        signal = "green"

    return {"score": score, "signal": signal, "max_severity": max_sev}


def make_report(*, repo: str, commit: str, findings: list[GateFinding]) -> dict[str, Any]:
    scored = score_findings(findings)
    return {
        "schema": "aoi.acp.clawshield_gate.v0.1",
        "created_at": utc_now(),
        "input": {"repo": repo, "commit": commit, "input_digest": sha256_text(f"{repo}@{commit}")},
        "result": scored,
        "findings": [
            {"rule_id": f.rule_id, "severity": f.severity, "message": f.message, "evidence": f.evidence}
            for f in findings
        ],
        "policy": {"green_only_attest": True, "fail_closed": True},
    }
