# EXPOSURE TIER MATRIX v0.1 (SSOT)

Last updated: 2026-02-20 (KST)
Status: READY (SSOT-grade)
Owner: Edmond (PO)

> Purpose: Enforce selective exposure across AOI ecosystem assets.
> Tiers: **OPEN / TEASER / STEALTH / TOP SECRET**
> Rule: If uncertain → classify higher (more restrictive).

---

## 0) Global constraints (hard)
- **Stealth $AOI**: tokenomics/treasury/wallets/distribution/pricing in $AOI are **TOP SECRET** unless Edmond explicitly approves otherwise.
- No alpha/profit guarantees in any tier.
- Any money/wallet/on-chain signing automation is L3 → **never auto**.

---

## 1) Tier definitions

### OPEN (public)
- Allowed: definitions, principles, architecture language, proof-first operations, governance model, demos that contain **no secrets**.
- Required: evidence path(s) + reproducible command(s) when claiming capability.

### TEASER (hint)
- Allowed: screenshots, high-level roadmaps, module names, limited capability statements.
- Disallowed: full specs, parameters, keys, wallet details, internal ops thresholds.

### STEALTH (internal-only existence)
- Allowed: detailed protocol specs, parameterization, internal runbooks, sensitive implementation details.
- Disallowed: publishing outside internal team channels.

### TOP SECRET (chair approval only)
- Allowed: tokenomics, treasury, wallets, private keys/seed phrases, sensitive financial flows, any irreversible on-chain execution plans.

---

## 2) Asset → Tier mapping (current)

> Rule of thumb: If a reviewer can reproduce it from the repo without secrets, it can be OPEN/TEASER. Anything involving tokenomics/treasury/wallet ops is TOP SECRET.

### 2.1 Brand / Naming / Motifs
- AOI definition (one-liner, principles): **OPEN**
- AOI Core (Policy→Gate→Approval→Proof language): **OPEN**
- CHUNGHO naming rules (CHUNGHO (Blue Tiger) first mention, 이후 CHUNGHO only): **OPEN**
- CHUNGHO deeper lore/ritual narratives: **STEALTH**
- Blue Bridge/청교 textual usage: **OPEN (1-line accent max)**; deeper philosophy: **STEALTH**

### 2.2 7 Pillars
- Pillar names + plain-English/KR definitions: **OPEN**
- Pillar artifact list (what proof files exist): **OPEN**
- Pillar internal parameters (S‑DNA handshake messages, Ω fusion coefficients, survival revenue internals): **STEALTH**

### 2.3 S‑DNA
- Layer1/2 public-safe spec + verification outputs: **OPEN/TEASER**
- Layer3 handshake details (message formats, secrets, salts, derivations): **STEALTH**

### 2.4 Skill-Guardian / Security Gate
- Tier1/2 definitions + report schema: **OPEN/TEASER**
- Tier3 rebuild playbooks + internal signatures: **STEALTH**

### 2.5 Settlement / x402 / Royalty
- Ledger schema + statement generator (report-only): **OPEN/TEASER**
- Live payout automation + routing rules: **STEALTH**
- Wallet addresses, balances, treasury: **TOP SECRET**

### 2.6 Litepaper / Whitepaper
- Tech Whitepaper high-level architecture claims: **OPEN/TEASER** (must map to SSOT)
- Litepaper token utility/pricing/distribution: **TOP SECRET** (default)

### 2.7 Concrete repo/document classification (fast list)
- `context/strategy_tft/aoi_core_brand_alignment/BRAND_SYSTEM_SSOT_V0_2_DRAFT.md`: **OPEN** (rules) / **STEALTH** (lore)
- `context/NAMING_MAPPING_TABLE_V0_1.md`: **OPEN**
- `context/EXPOSURE_TIER_MATRIX_V0_1.md`: **OPEN**
- `aoi-core/docs/ARTIFACTS_STANDARD_V0_1.md`: **OPEN**
- `context/PILLARS_PUBLIC_SAFE_MESSAGE_BLOCKS_V0_1.md`: **OPEN/TEASER**
- `context/PUBLIC_CLAIMS_REGISTRY_V0_1.md`: **OPEN/TEASER**
- Bazaar demos (registry/search/UI): **TEASER**
  - `context/proof_samples/nexus_bazaar_registry_v0_1/`
  - `context/ui/bazaar/index.html`
- Private internal demo packaging repo: **STEALTH**
  - https://github.com/edmonddantesj/nexus-bazaar-private
- Any file containing seeds/keys/wallet addresses/balances: **TOP SECRET**

---

## 3) Publishing enforcement (ship gate)
Before any public post / ClawHub publish / repo release:
- [ ] Classify doc/module: OPEN/TEASER/STEALTH/TOP SECRET
- [ ] If TEASER+: ensure no secrets are present (paths, keys, internal params)
- [ ] If claim implies capability: link to evidence path + repro command
- [ ] Pass Security Gate / Guardian checklist

---

## 4) Evidence
- Alignment map: `context/AOI_CORE_ALIGNMENT_MAP_V0_1.md`
- Brand SSOTs:
  - `context/strategy_tft/aoi_core_brand_alignment/BRAND_SYSTEM_SSOT_V0_2_DRAFT.md`
  - `context/BRAND_AOI_CHUNGHO_SSOT_V0_1.md`
- Gap matrix: `context/strategy_tft/aoi_core_brand_alignment/WHITEPAPER_PLATFORM_GAP_MATRIX_V0_1_DRAFT.md`
