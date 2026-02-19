#!/usr/bin/env python3
"""EigenProof Runner — proof-first bundle generator.

A (MVP): Proof Bundle Runner
- Reads an input JSON
- Produces deterministic output JSON
- Writes manifest.json (sha256 hashes + runtime metadata)
- Writes sha256sum.txt for the bundle

B (Next level): Identity Wrapper (public-safe)
- Writes identity.json: a verifiable description of "what code ran"
- Writes policy.json: upgrade/execution policy hints (no secrets)

Designed for container execution (EigenCompute) and local Docker demo.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import platform
import subprocess
from typing import Optional


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now_iso(deterministic: bool = False) -> str:
    if deterministic:
        return "1970-01-01T00:00:00Z"
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_commit_or_none() -> Optional[str]:
    env = os.environ.get("GIT_COMMIT")
    if env:
        return env
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=2)
        if r.returncode == 0:
            return r.stdout.strip() or None
    except Exception:
        pass
    return None


def docker_image_digest_or_none() -> Optional[str]:
    """Best-effort: allow injecting an image digest from the runtime.

    In EigenCompute, the platform may expose image identifiers via env.
    We intentionally keep this as "optional" to stay portable.
    """

    for k in [
        "EIGEN_IMAGE_DIGEST",
        "IMAGE_DIGEST",
        "DOCKER_IMAGE_DIGEST",
    ]:
        v = (os.environ.get(k) or "").strip()
        if v:
            return v
    return None


def build_identity(outdir: Path, run_id: str, deterministic: bool = False) -> dict:
    # Code fingerprint (no secrets): hash this file and Dockerfile if present
    this_file = Path(__file__)
    runner_sha = sha256_file(this_file) if this_file.exists() else None

    dockerfile = (Path("/app") / "Dockerfile")
    dockerfile_sha = sha256_file(dockerfile) if dockerfile.exists() else None

    ident = {
        "schema": "eigenproof.identity.v0.1",
        "run_id": run_id,
        "created_at": utc_now_iso(deterministic),
        "identity": {
            "project": "eigenproof-runner",
            "publisher": "Aoineco",
            "image_digest": docker_image_digest_or_none(),
        },
        "code": {
            "git_commit": git_commit_or_none(),
            "files": [
                {"path": "runner.py", "sha256": runner_sha},
                {"path": "Dockerfile", "sha256": dockerfile_sha},
            ],
        },
        "attestations": {
            "public_safe": True,
            "no_external_calls": True,
            "no_secrets": True,
        },
    }

    # Remove null hashes cleanly
    ident["code"]["files"] = [f for f in ident["code"]["files"] if f.get("sha256")]
    if not ident["identity"].get("image_digest"):
        ident["identity"].pop("image_digest", None)

    return ident


def build_policy() -> dict:
    return {
        "schema": "eigenproof.policy.v0.1",
        "default_mode": "shadow-only",
        "governance": {
            "tiers": ["L1", "L2", "L3"],
            "l3_requires_explicit_approval": True,
            "l3_examples": ["fund_movement", "external_posting", "secrets_access", "irreversible_config"],
        },
        "upgrade": {
            "allowed": True,
            "rule": "no auto-upgrade without proof bundle + changelog",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Input JSON path")
    ap.add_argument("--outdir", required=True, help="Output directory (mounted volume recommended)")
    ap.add_argument("--deterministic", action="store_true", help="Use fixed timestamps/run_id for deterministic replay")
    args = ap.parse_args()

    inp = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Bundle paths
    input_copy = outdir / "input.json"
    output_json = outdir / "output.json"
    manifest_json = outdir / "manifest.json"
    identity_json = outdir / "identity.json"
    policy_json = outdir / "policy.json"
    sha256sum = outdir / "sha256sum.txt"

    data = json.loads(inp.read_text(encoding="utf-8"))

    # Deterministic core output hash; timestamps/run_id are runtime-variant unless --deterministic
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
        "generated_at": utc_now_iso(args.deterministic),
    }

    run_id = f"{data.get('job_id','run')}-" + ("deterministic" if args.deterministic else datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))

    input_copy.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output_json.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Next-level identity wrapper
    identity = build_identity(outdir, run_id, args.deterministic)
    policy = build_policy()
    identity_json.write_text(json.dumps(identity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    policy_json.write_text(json.dumps(policy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "schema": "eigenproof.manifest.v0.2",
        "run_id": run_id,
        "created_at": utc_now_iso(args.deterministic),
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "git_commit": git_commit_or_none(),
            "policy_sha256": sha256_file(policy_json),
            "docker_image_digest": docker_image_digest_or_none(),
        },
        "source": {
            "git_commit": git_commit_or_none(),
        },
        "bundle": {
            "files": [
                {"path": "input.json", "sha256": sha256_file(input_copy)},
                {"path": "output.json", "sha256": sha256_file(output_json)},
                {"path": "identity.json", "sha256": sha256_file(identity_json)},
                {"path": "policy.json", "sha256": sha256_file(policy_json)},
            ]
        },
    }

    manifest_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest_sha = sha256_file(manifest_json)
    manifest["bundle"]["files"].append({"path": "manifest.json", "sha256": manifest_sha})
    manifest["self_sha256"] = manifest_sha
    manifest_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # sha256sum.txt (bundle)
    rels = ["input.json", "output.json", "identity.json", "policy.json", "manifest.json"]
    lines = []
    for rel in rels:
        p = outdir / rel
        lines.append(f"{sha256_file(p)}  {rel}")
    sha256sum.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "outdir": str(outdir), "run_id": run_id}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
