#!/usr/bin/env python3
"""AOI Proof Queue validator (v0.1)

Validates JSONL entries against the AOI proof queue schema.

Usage:
  python3 scripts/aoi_proof_queue_validate.py --schema context/aoi_core_radar/patterns/AOI_PROOF_QUEUE_SCHEMA_V0_1.json --jsonl /path/to/queue.jsonl

Notes:
- Uses only stdlib for portability (light validation + required fields + patterns).
- This is a preflight guard, not a full JSON-Schema engine.
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

HEX40 = re.compile(r"^0x[a-fA-F0-9]{40}$")
HEX64 = re.compile(r"^0x[a-fA-F0-9]{64}$")

ALLOWED_STATUS = {"QUEUED", "RETRYING", "SUBMITTED", "SETTLED", "FAILED"}


def is_iso_dt(s: str) -> bool:
    try:
        # Accept Z by replacing with +00:00
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        datetime.fromisoformat(s)
        return True
    except Exception:
        return False


def validate_entry(obj: dict) -> list[str]:
    errs: list[str] = []

    def req(path: str):
        cur = obj
        for part in path.split('.'):
            if not isinstance(cur, dict) or part not in cur:
                errs.append(f"missing:{path}")
                return None
            cur = cur[part]
        return cur

    schema = req("schema")
    if schema != "aoineco.aoi.proof_queue.entry.v0.1":
        errs.append("schema:invalid")

    rid = req("request_id")
    if not isinstance(rid, str) or len(rid) < 8:
        errs.append("request_id:invalid")

    created_at = req("created_at")
    if not isinstance(created_at, str) or not is_iso_dt(created_at):
        errs.append("created_at:invalid")

    status = req("status")
    if status not in ALLOWED_STATUS:
        errs.append("status:invalid")

    actor_role = req("actor.role")
    if not isinstance(actor_role, str) or not actor_role:
        errs.append("actor.role:invalid")

    # optional actor.wallet
    wallet = obj.get("actor", {}).get("wallet")
    if wallet is not None and wallet != "" and not HEX40.match(str(wallet)):
        errs.append("actor.wallet:invalid")

    provider = req("target.provider")
    skill = req("target.skill_name")
    if not isinstance(provider, str) or not provider:
        errs.append("target.provider:invalid")
    if not isinstance(skill, str) or not skill:
        errs.append("target.skill_name:invalid")

    params = req("params_sanitized")
    if not isinstance(params, dict):
        errs.append("params_sanitized:invalid")

    # evidence tx hashes
    txs = obj.get("evidence", {}).get("tx_hashes")
    if txs is not None:
        if not isinstance(txs, list):
            errs.append("evidence.tx_hashes:invalid")
        else:
            for t in txs:
                if t is None:
                    continue
                if not HEX64.match(str(t)):
                    errs.append("evidence.tx_hashes:invalid_item")
                    break

    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--jsonl", required=True)
    args = ap.parse_args()

    schema_path = Path(args.schema)
    jsonl_path = Path(args.jsonl)

    if not schema_path.exists():
        raise SystemExit(f"schema not found: {schema_path}")
    if not jsonl_path.exists():
        raise SystemExit(f"jsonl not found: {jsonl_path}")

    # schema file is not parsed for logic (stdlib validator) — but we ensure it exists.
    _ = schema_path.read_text(encoding="utf-8")

    bad = 0
    total = 0
    for i, line in enumerate(jsonl_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        total += 1
        try:
            obj = json.loads(line)
        except Exception as e:
            bad += 1
            print(f"line {i}: invalid_json: {e}")
            continue

        if not isinstance(obj, dict):
            bad += 1
            print(f"line {i}: not_object")
            continue

        errs = validate_entry(obj)
        if errs:
            bad += 1
            print(f"line {i}: " + ",".join(errs))

    if bad:
        print(f"FAIL: {bad}/{total} invalid")
        raise SystemExit(1)

    print(f"PASS: {total} entries")


if __name__ == "__main__":
    main()
