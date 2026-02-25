# AOI Pattern — Circuit Breaker + Proof Queue (v0.1)

Date: 2026-02-25 (KST)
Origin: Blue-Sound insight (Idea Vault: ACP job-create HTTP 500 대응)
Related AOI artifacts:
- `context/aoi_core_radar/checklists/AOI_X402_INTEGRATION_CHECKLIST_V0_1.md`
- `context/aoi_core_radar/playbooks/AOI_402_DEBUG_PLAYBOOK_V0_1.md`

Purpose: ensure user-facing flows do not break under upstream/vendor instability by queueing intents with proof and settling later.

---

## 1) Problem
Upstream vendors can fail unpredictably (e.g., `job create` HTTP 500). Naïve flows:
- hard-fail and lose user intent
- trigger duplicate retries (double spend / double execution risk)
- lose evidence trails and become unauditable

---

## 2) Goal
Create a fail-soft, auditable execution wrapper:
- preserve intent as a durable record
- prevent duplicates via idempotency
- retry safely with backoff
- settle automatically once upstream recovers
- always emit a receipt bundle

---

## 3) Components

### 3.1 Circuit Breaker (front gate)
States: `OK | DEGRADED | RECOVERING`
- Trigger DEGRADED on error-rate spikes (HTTP 5xx) or timeout threshold.
- In DEGRADED:
  - do not block the product experience entirely
  - switch to queue-first behavior

### 3.2 Proof Queue (append-only)
Record every intended action as a durable entry:
- `request_id` (idempotency key)
- `actor_role` + `actor_ticker`
- `provider` + `skill_name`
- `params_sanitized`
- `created_at`
- `status`: `QUEUED | RETRYING | SUBMITTED | SETTLED | FAILED`
- `evidence`: `job_id?`, `deliverable_id?`, `tx_hashes?`, `log_links?`

### 3.3 Backoff retry + settle
- Retry with exponential backoff + jitter.
- Enforce idempotency using `request_id`.
- On success:
  - persist evidence
  - mark `SETTLED`
  - emit a receipt

---

## 4) Receipt bundle (minimum)
- request_id
- quoted_price (if any)
- payer/payee (if payments)
- job/deliverable ids
- tx hashes (if on-chain)
- timestamps
- outcome + error_code

---

## 5) Failure modes & guardrails
- Duplicate execution → require idempotency key.
- Silent drops → queue must be durable + observable.
- Sensitive data leakage → sanitize params.
- Cost spiral retries → cap retries + cool-down.

---

## 6) How to apply
- ACP job creation
- x402 payment-gated endpoints
- any external marketplace/vendor integration

---

## 7) Next action
- Convert this pattern into a reusable AOI library/module once we pick a runtime (Node) and a storage primitive (KV/DB).
