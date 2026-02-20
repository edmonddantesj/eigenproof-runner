# WHITEPAPER ↔ AOI Core Platform Gap Matrix (v0.1 DRAFT)

Date: 2026-02-20 (KST)
Owner: GAP subagent
Scope: Align **public-facing claims** (Tech Whitepaper + Litepaper) with **AOI Core SSOT** (Product Vision + MVP Scope + SSOT Index).

## Sources
- Tech Whitepaper: `strategy/AOI_Tech_Whitepaper_v1.0.md`
- Litepaper: `strategy/AOI_Litepaper_v1.md`
- AOI Core Vision (SSOT): `context/AOI_CORE_PRODUCT_VISION_V0_1.md`
- AOI Core MVP Scope (SSOT): `context/AOI_CORE_MVP_SCOPE_V0_1.md`
- SSOT index: `context/SSOT_INDEX.md`

## Matrix

> Gap types
> - **missing-doc**: claim exists in WP/Litepaper but not represented/controlled in SSOT (definitions, scope, governance, exposure tier)
> - **missing-code**: claim implies a working capability but no implementation evidence found in repo
> - **conflict**: WP/Litepaper claim contradicts AOI Core SSOT (or two SSOTs contradict)

| Claim / Promise | Current evidence (file path) | Gap type | Fix plan | Exposure tier |
|---|---|---|---|---|
| **AOI Core one-liner**: “agent execution becomes provable safe commerce (Execution Commerce)” | `context/AOI_CORE_PRODUCT_VISION_V0_1.md` | missing-doc | Ensure WP/Litepaper either (a) adopt this as the primary one-liner, or (b) clearly position Nexus Protocol as a *module* under AOI Core. Add a short section “AOI Core = governance OS; Nexus = reference architecture.” | OPEN |
| **Nexus Protocol solves Identity/Intelligence/Economy** (vertical framework) | `strategy/AOI_Tech_Whitepaper_v1.0.md` | missing-doc | Map “Identity/Intelligence/Economy” to AOI Core SSOT primitives: (Identity→S-DNA, Intelligence→Omega, Economy→Settlement/ACP + Bazaar). Add mapping paragraph to Vision SSOT to prevent brand drift. | OPEN/TEASER |
| **9-agent layered squad** as the canonical topology | `strategy/AOI_Tech_Whitepaper_v1.0.md` | missing-doc | In AOI Core SSOT, clarify whether AOI Core supports **N-agent teams** generally, or hard-canon “9-agent Aoineco squad” as reference implementation only. Add a “Reference Squad” vs “General Platform” distinction. | OPEN |
| **Governance: L1/L2/L3** decision system (autonomous/oracle/human) | `strategy/AOI_Tech_Whitepaper_v1.0.md`; `context/AOI_CORE_MVP_SCOPE_V0_1.md`; `context/SSOT_INDEX.md` | (no gap) | Keep as-is; ensure Litepaper product pages (Brand-Genesis/Smart-Manager) reference “queue_for_approval by default” for risky actions. | OPEN |
| **S-DNA = 3-layer identity protocol** (Layer1 visible tag, Layer2 guardian scan, Layer3 runtime handshake) | `strategy/AOI_Tech_Whitepaper_v1.0.md`; `context/AOI_CORE_PRODUCT_VISION_V0_1.md` | missing-doc | AOI Core SSOT defines S‑DNA triple helix, but does not specify *acceptance criteria* (what “complete” means). Add explicit spec checklist + audit artifacts location (e.g., proof pack outputs) in AOI Core docs. | OPEN/TEASER/STEALTH mix |
| **Claim: S-DNA Protocol v1.0 — Full 3-layer identity stack is “✅ Complete”** | `strategy/AOI_Tech_Whitepaper_v1.0.md` (Roadmap table shows complete) | conflict | Either (A) downgrade claim in WP to “implemented in internal reference stack; external release TEASER”, or (B) update AOI Core SSOT with evidence links proving completion (code + demo + proof logs). Also classify which parts are public-safe. | TEASER/STEALTH |
| **Layer 3 handshake details are “proprietary / not disclosed”** | WP says proprietary: `strategy/AOI_Tech_Whitepaper_v1.0.md`; yet code exists: `skills/aoineco-sdna-handshake/scripts/handshake_engine.py` | conflict | Decide posture: if keeping proprietary, remove/relocate detailed code to restricted repo OR sanitize to “public-safe wrapper” and keep secrets out (org_secret vault, key derivation). Update WP wording to match reality. | STEALTH/TOP SECRET |
| **Guardian Sentry** (Tier1 surface scan + Tier2 logic scan) required pre-deploy | `strategy/AOI_Tech_Whitepaper_v1.0.md`; SSOT definitions in `context/AOI_CORE_PRODUCT_VISION_V0_1.md` | missing-doc | Add to AOI Core MVP acceptance criteria: “No publish/deploy without Guardian pass,” and link the actual run command / checklist (likely under `context/SECURITY_GATE_CHECKLIST_V0_2.md` / scripts). | OPEN/TEASER |
| **Nexus Oracle Ω (Omega)** Bayesian fusion engine is “✅ Complete” and live-tested | Claim: `strategy/AOI_Tech_Whitepaper_v1.0.md` (Roadmap Phase 3 ✅); code: `skills/nexus-oracle-omega/scripts/omega_fusion.py`, `skills/nexus-oracle-omega/scripts/omega_ops_os.py` | conflict | AOI Core MVP Scope says “Nexus Oracle Ω product implementation = vNext”: `context/AOI_CORE_MVP_SCOPE_V0_1.md`. Reconcile by defining: “Omega exists as internal skill; AOI Core MVP will only standardize schemas + proof bundles, not ship productized Omega.” Update both docs. | TEASER/STEALTH |
| **Monte Carlo risk engine** produces VaR/CVaR/Sharpe/Kelly before trades | `strategy/AOI_Tech_Whitepaper_v1.0.md` | missing-code | If this is real: link implementation (file path) and minimal reproducible demo. If not: change WP to “methodology only (planned)” and mark as TEASER. | TEASER/STEALTH |
| **Self-Reflection Engine** updates agent weights and thresholds recursively | `strategy/AOI_Tech_Whitepaper_v1.0.md` | missing-code | Either provide code evidence + proof logs (where weights are stored; update rules), or explicitly mark as “concept only” and move to STEALTH roadmap. | STEALTH |
| **State-Guardian** gives “immortality guarantee” (session→persistent memory) | `strategy/AOI_Tech_Whitepaper_v1.0.md`; repo skill exists: `skills/aoineco-state-guardian/` | missing-doc | AOI Core SSOT references “State-Guardian” but MVP scope acceptance criteria don’t mention it. Add to AOI Core MVP deliverables: proof bundle must include state snapshot/commit hooks. | OPEN/TEASER |
| **Nexus Bazaar** skill marketplace + verified modules + audit reports | WP: `strategy/AOI_Tech_Whitepaper_v1.0.md`; Vision defines: `context/AOI_CORE_PRODUCT_VISION_V0_1.md`; MVP excludes: `context/AOI_CORE_MVP_SCOPE_V0_1.md` | (no gap) | Already aligned: Vision yes / MVP no. Ensure WP does not imply marketplace is live; keep roadmap Q2 2026 phrasing. | TEASER |
| **Core-Temp Score** exists and is used for quality ranking and fees | WP concept: `strategy/AOI_Tech_Whitepaper_v1.0.md`; Vision defines Core-Temperature: `context/AOI_CORE_PRODUCT_VISION_V0_1.md` | missing-code | If Core-Temp is claimed operational (not just concept), provide implementation + current score calculation. Otherwise, keep as Vision-only and ensure WP avoids “current score: X” unless evidence exists. | TEASER |
| **$AOI token** is the ecosystem fuel; utility burn model | `strategy/AOI_Litepaper_v1.md` | conflict | AOI Core Vision mandates **Stealth $AOI** (pre-launch “no external exposure/marketing”): `context/AOI_CORE_PRODUCT_VISION_V0_1.md`. Decide: (A) Litepaper stays internal (Restricted), or (B) revise Vision to allow controlled OPEN token comms. Align exposure tier policy in SSOT Index. | TOP SECRET |
| **Litepaper offers public pricing in $AOI** (Brand-Genesis tiers; Smart-Manager costs) | `strategy/AOI_Litepaper_v1.md` | missing-doc | Product Vision SSOT defines AOI Core & Bazaar/Omega, but does not define Brand-Genesis/Smart-Manager deliverables/pricing as SSOT. Either add those as SSOT (separate docs) or remove pricing from Litepaper until SSOT exists. | TOP SECRET |
| **Brand-Genesis = Company-as-a-Service** (deliverables: roles/personas/branding/governance) | `strategy/AOI_Litepaper_v1.md` | missing-doc | Create a Product SSOT for Brand-Genesis (scope, output schema, governance, proof bundle). Add cross-link into `context/SSOT_INDEX.md`. | OPEN/TEASER (token pricing TOP SECRET) |
| **Smart-Manager = intelligent task routing + cheapest capable LLM** | `strategy/AOI_Litepaper_v1.md`; Vision mentions “Dynamic Model Switching”: `context/AOI_CORE_PRODUCT_VISION_V0_1.md` | missing-doc | Align terminology: Smart-Manager should be positioned as the product wrapper around AOI Core primitives (Policy/Gate/Approval/Proof + model switching). Write a Smart-Manager SSOT (routing rules, guardrails, cost telemetry). | TEASER |
| **AI DEX = skill marketplace paid by $AOI** | `strategy/AOI_Litepaper_v1.md`; Vision: `context/AOI_CORE_PRODUCT_VISION_V0_1.md` | conflict | **Decision locked:** external top-level term is **Nexus Bazaar**. Treat “AI DEX” as internal/background only and remove/rename from any public docs. Update Litepaper/WP wording to “Nexus Bazaar (proof-first market)” and keep token-payment language TOP SECRET. | TEASER/TOP SECRET |
| **“$AOI is not an investment product” + legal disclaimer** | `strategy/AOI_Litepaper_v1.md` | missing-doc | Add a “Comms/Legal disclaimers policy SSOT” (where disclaimers must appear; what words are banned; jurisdiction notes). Without SSOT, public docs risk inconsistency. | OPEN (text) / TOP SECRET (token plans) |
| **Token distribution & vesting & sell caps** | `strategy/AOI_Litepaper_v1.md` | conflict | AOI Core SSOT says token/treasury are TOP SECRET/need chairman approval. Either remove distribution table from any public docs, or explicitly authorize it and move the “Stealth $AOI” rule. | TOP SECRET |

---

## Top 5 highest-risk gaps (need resolution before any public launch)

1) **Stealth $AOI vs public Litepaper token marketing**
   - Evidence: `context/AOI_CORE_PRODUCT_VISION_V0_1.md` (Stealth $AOI) ↔ `strategy/AOI_Litepaper_v1.md` (public token utility/pricing/distribution)
   - Risk: brand/governance breach; exposure of TOP SECRET tier material.

2) **“✅ Complete” roadmap claims vs AOI Core MVP scope exclusions**
   - Evidence: `strategy/AOI_Tech_Whitepaper_v1.0.md` (Phase 2/3/5 complete) ↔ `context/AOI_CORE_MVP_SCOPE_V0_1.md` (Omega/Bazaar implementation vNext)
   - Risk: credibility gap with builders/investors; internal team may mis-prioritize.

3) **Layer 3 handshake “proprietary” claim vs code availability**
   - Evidence: `strategy/AOI_Tech_Whitepaper_v1.0.md` ↔ `skills/aoineco-sdna-handshake/scripts/handshake_engine.py`
   - Risk: IP/confidentiality mismatch; security theater accusations if secrets are hardcoded.

4) **Monte Carlo / Self-Reflection engines described with strong operational language but unclear repo evidence**
   - Evidence: `strategy/AOI_Tech_Whitepaper_v1.0.md`
   - Risk: technical due diligence failure if asked to demo; over-claiming.

5) **Product naming drift (AOI Core vs Nexus Protocol vs AI DEX vs Nexus Bazaar)**
   - Evidence: WP/Litepaper vs `context/AOI_CORE_PRODUCT_VISION_V0_1.md`
   - Risk: market confusion; internal scope creep; inconsistent website copy.

---

## Notes / Suggested next actions (fastest path)
- Add a **"Public Claims Registry"** section to AOI Core SSOT linking every OPEN/TEASER claim to evidence paths + demo commands.
- Decide a single **brand architecture**: AOI Core (platform) vs Nexus (reference protocol) vs Bazaar/DEX (market).
- Create SSOT docs for **Brand-Genesis** and **Smart-Manager** (even as v0.1 one-pagers) before keeping their pricing in any outward-facing doc.
