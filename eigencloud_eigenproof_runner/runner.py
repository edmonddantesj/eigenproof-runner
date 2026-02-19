#!/usr/bin/env python3
"""EigenProof Runner — proof-first bundle generator.

- Reads an input JSON
- Produces deterministic output JSON
- Writes manifest.json (sha256 hashes + runtime metadata)
- Writes sha256sum.txt for the bundle

Designed for container execution (EigenCompute) and local Docker demo.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import platform
import subprocess
from typing import Any


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_commit_or_none() -> str | None:
    env_commit = os.environ.get("GIT_COMMIT")
    if env_commit:
        return env_commit
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=2)
        if r.returncode == 0:
            return (r.stdout or "").strip() or None
    except Exception:
        pass
    return None


def load_policy(path: Path) -> tuple[dict | None, str | None]:
    """Load policy.json and compute exact source hash.

    Returns (policy, policy_sha). Missing file returns (None, None).
    """
    if not path.exists():
        return None, None
    try:
        raw = path.read_text(encoding="utf-8")
        policy = json.loads(raw)
        return policy, sha256_text(raw)
    except Exception:
        return None, None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Input JSON path")
    ap.add_argument("--outdir", required=True, help="Output directory (mounted volume recommended)")
    ap.add_argument("--policy", default="/app/policy.json", help="Path to policy JSON")
    args = ap.parse_args()

    inp = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    input_copy = outdir / "input.json"
    output_json = outdir / "output.json"
    manifest_json = outdir / "manifest.json"
    sha256sum = outdir / "sha256sum.txt"

    data = json.loads(inp.read_text(encoding="utf-8"))

    # Deterministic output for demo
    msg = (((data.get("task") or {}).get("message")) or "").strip()
    n = int((((data.get("task") or {}).get("n")) or 0))

    digest = hashlib.sha256((msg + "|" + str(n)).encode("utf-8")).hexdigest()
    out = {
        "schema": "eigenproof.output.v0.1",
        "job_id": data.get("job_id"),
        "ok": True,
        "result": {
            "input_message": msg,
            "n": n,
            "sha256": digest,
        },
        "generated_at": utc_now_iso(),
    }

    input_copy.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output_json.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Policy handling (B2)
    policy, policy_sha = load_policy(Path(args.policy))
    if policy is not None:
        # include policy snapshot in bundle for auditability
        policy_out = outdir / "policy.json"
        policy_out.write_text(json.dumps(policy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "schema": "eigenproof.manifest.v0.1",
        "run_id": f"{data.get('job_id', 'run')}-{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
        "created_at": utc_now_iso(),
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "git_commit": git_commit_or_none(),
            "policy_sha256": policy_sha,
        },
        "source": {
            "git_commit": git_commit_or_none(),
        },
        "policy": policy,
        "files": [
            {"path": "input.json", "sha256": sha256_file(input_copy)},
            {"path": "output.json", "sha256": sha256_file(output_json)},
        ],
    }

    if policy is not None:
        manifest["files"].append({"path": "policy.json", "sha256": sha256_file(outdir / "policy.json")})

    manifest_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = []
    for rel in ["input.json", "output.json", "manifest.json"] + (["policy.json"] if policy is not None else []):
        p = outdir / rel
        lines.append(f"{sha256_file(p)}  {rel}")
    sha256sum.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "outdir": str(outdir), "policy_present": policy is not None}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
