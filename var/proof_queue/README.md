# AOI Proof Queue (local) — v0.1

This folder is the Phase-1 local implementation target for the AOI Circuit Breaker + Proof Queue pattern.

Files:
- `queue.jsonl` — append-only intent log (1 JSON object per line)
- `state.json` — circuit breaker state (OK/DEGRADED/RECOVERING)

Validation:
```bash
scripts/aoi_proof_queue_preflight.sh var/proof_queue/queue.jsonl
```

Notes:
- Store sanitized params only (no secrets).
- Use `request_id` as idempotency key to prevent duplicates.
