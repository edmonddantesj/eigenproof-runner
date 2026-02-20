# AOI Core — Public Claims Registry v0.1 (SSOT)

Last updated: 2026-02-20 (KST)
Status: DRAFT

Purpose: For every **OPEN/TEASER** claim, provide:
1) Exact claim text (what we say)
2) Evidence paths (where it’s proven)
3) Repro command (how to re-generate)
4) Exposure tier

---

## Claim 1 — AOI Core: Policy → Gate → Approval → Proof
- Claim (OPEN): "AOI Core turns agent execution into auditable operations: Policy → Gate → Approval → Proof."
- Evidence:
  - `context/PRINCIPLE_IDEA_SCHEMA_PROOF_REGISTRY_V0_1.md`
  - `context/AOI_CORE_PRODUCT_VISION_V0_1.md`
- Repro:
  - (doc-only) open files above
- Tier: OPEN

## Claim 2 — Proof bundles are deterministic (hashable)
- Claim (OPEN/TEASER): "Proof bundles are reproducible and include manifests + hashes."
- Evidence:
  - `aoi-core/docs/ARTIFACTS_STANDARD_V0_1.md`
  - `scripts/test_audit_stall_demo.py`
  - `scripts/test_bazaar_fx_skill_demo.py`
- Repro:
  - `python3 scripts/test_audit_stall_demo.py`
  - `python3 scripts/test_bazaar_fx_skill_demo.py`
- Tier: OPEN/TEASER

## Claim 3 — Nexus Bazaar registry + search UI (report-only)
- Claim (TEASER): "Nexus Bazaar surfaces registry + audit outcomes before execution (report-only)."
- Evidence:
  - `context/proof_samples/nexus_bazaar_registry_v0_1/README.md`
  - `context/proof_samples/nexus_bazaar_registry_v0_1/registry_search_index.json`
  - `context/ui/bazaar/index.html`
- Repro:
  - `python3 scripts/bazaar_registry_generate.py --outdir context/proof_samples/nexus_bazaar_registry_v0_1 --auto`
  - `python3 scripts/bazaar_core_temp_compute.py --registry context/proof_samples/nexus_bazaar_registry_v0_1/registry_index.json --outdir context/proof_samples/nexus_bazaar_registry_v0_1`
  - `python3 scripts/bazaar_registry_search_index_generate.py --registry context/proof_samples/nexus_bazaar_registry_v0_1/registry_index_enriched.json --out context/proof_samples/nexus_bazaar_registry_v0_1/registry_search_index.json`
- Tier: TEASER

## Claim 4 — Audit Stall is policy-driven PASS/FAIL (fail-closed)
- Claim (TEASER): "A single policy line can flip audit verdict to FAIL (fail-closed)."
- Evidence:
  - PASS: `context/proof_samples/audit_stall_demo_20260220_135002/guardian_report.json`
  - FAIL: `context/proof_samples/audit_stall_demo_20260220_140316_fail/guardian_report.json`
- Repro:
  - `python3 scripts/audit_stall_demo_runner.py --outdir /tmp/audit_demo && cat /tmp/audit_demo/guardian_report.json`
- Tier: TEASER

## Naming constraint (global)
- Policy: External top-level market term is **Nexus Bazaar**. "AI DEX" is internal/background only.
- Evidence:
  - `context/NAMING_MAPPING_TABLE_V0_1.md`
  - `context/TASK_PARKING_LOT.md` (tag: bazaar-terminology-backlog)
