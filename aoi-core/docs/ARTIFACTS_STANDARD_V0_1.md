# AOI Core — Artifacts Standard v0.1 (SSOT)

Last updated: 2026-02-20 (KST)
Status: READY
Exposure: OPEN

> Purpose: Standardize proof artifacts so every pillar can be audited the same way.

---

## 1) Proof Bundle (minimum required)
Every governed run must be able to emit this set:

1) `proof_manifest.json`
- required keys:
  - generated_at (KST ISO)
  - run_id
  - inputs_digest
  - exposure_tier
  - approvals (if any)
  - evidence_paths[]
  - files[{path, sha256, bytes}]
  - self_sha256
    - definition: `sha256(canonical_json(proof_manifest WITHOUT self_sha256))`
    - canonical_json: `json.dumps(obj, sort_keys=true, separators=(",", ":"), ensure_ascii=false)`
    - rationale: avoids impossible self-referential hashing while staying deterministic

2) `sha256sum.txt`
- sha256 for every file in the bundle (including the manifest itself)

3) `run_log.txt`
- commands executed + timestamps + environment notes

4) `decision_summary.md`
- TL;DR + risks + next actions + links

---

## 2) Pillar-specific artifacts (v0.1)

> Each pillar MUST emit exactly one primary JSON artifact (below). This keeps audits uniform across pillars.

### S‑DNA
- `sdna_verify.json`
  - minimum keys:
    - `generated_at`, `run_id`, `target_path` or `target_digest`
    - `protocol_version`
    - `result.verified` (bool)
    - `result.author_id` (optional)
    - `result.hash_match` (bool|null)

### Skill-Guardian
- `guardian_report.json`
  - minimum keys:
    - `generated_at`, `run_id`
    - `guardian_report.verdict` (PASS/FAIL)
    - `guardian_report.risk` (low/medium/high)
    - `guardian_report.findings[]` (each: id, severity, message, evidence_path?)

### Context-Sentry
- `context_sentry_report.json` (inputs, compression_ratio, retention_score, decisions[])

### Nexus Oracle Ω
- `oracle_verdict.json`
  - minimum keys:
    - `generated_at`, `run_id`
    - `verdict.direction` (LONG/SHORT/HOLD/NEUTRAL)
    - `verdict.confidence` (0..1)
    - `verdict.veto_applied` (bool)
    - `risk.summary` (string)
    - `evidence_paths[]`

### Nexus Bazaar / Settlement
- `settlement_intent.json` (report-only by default)
- `royalty_statement.json` (month, totals, payees, status)

### Survival Engine
- `survival_summary.json` (cost, revenue, ratio, mode, allowed_actions)

### Stealth Strategy
- `exposure_classification.json` (asset, tier, allowed_channels)

---

## 3) Ship gate
- No public claim without at least: `decision_summary.md` + `proof_manifest.json` + reproducible command.

---

## 4) Evidence
- 7 Pillars audit: `context/strategy_tft/aoi_core_brand_alignment/SEVEN_PILLARS_AUDIT_V0_1_DRAFT.md`
- Alignment map: `context/AOI_CORE_ALIGNMENT_MAP_V0_1.md`
