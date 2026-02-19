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


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_commit_or_none() -> str | None:
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=2)
        if r.returncode == 0:
            return r.stdout.strip() or None
    except Exception:
        pass
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Input JSON path")
    ap.add_argument("--outdir", required=True, help="Output directory (mounted volume recommended)")
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

    manifest = {
        "schema": "eigenproof.manifest.v0.1",
        "run_id": f"{data.get('job_id','run')}-{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
        "created_at": utc_now_iso(),
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        "git_commit": git_commit_or_none(),
        "docker_image_digest": os.environ.get("EIGEN_IMAGE_DIGEST") or os.environ.get("DOCKER_IMAGE_DIGEST"),
        },
        "source": {
            "git_commit": git_commit_or_none(),
        },
        "files": [
            {"path": "input.json", "sha256": sha256_file(input_copy)},
            {"path": "output.json", "sha256": sha256_file(output_json)},
        ],
    }

    manifest_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # sha256sum.txt (bundle)
    lines = []
    for rel in ["input.json", "output.json", "manifest.json"]:
        p = outdir / rel
        lines.append(f"{sha256_file(p)}  {rel}")
    sha256sum.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "outdir": str(outdir)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
