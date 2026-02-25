# CURRENT_STATE.md — SSOT (Auto-synced)

Last update: 2026-02-25 15:40 KST

## 🤖 Automation health (heartbeat)
- Alpha Oracle V6 pipeline: ran @ 05:52 KST (archived)
  - Archive: `the-alpha-oracle/results/v6_20260225_055229_BTC-USD.json`
- AOI Council governance gate smoke: PASS
  - Proof pack: `/tmp/aoi-council-hb-20260225_055230/`

## ✅ Context usage watch
- ⚠️ Compaction failed (timeout). Context ~69% (187k/272k). Prepare controlled /reset.

## 🔥 Active Project: NEXUS Arena (Financial Engineering + Arena + Guild)

### SSOT 문서 목록 (context/nexus_arena/)

| # | 문서 | 상태 | 크기 |
|---|---|---|---|
| 01 | Master Spec (세계관/구조) | ✅ v0.1 | 3.4KB |
| 02 | Event System (개인전/단체전/난투전) | ✅ v0.1 | 12.8KB |
| 03 | Betting System (Parimutuel) | ✅ v0.1 | 6.7KB |
| 04 | Fee Model (5대 수익채널) | ✅ v0.1 | 4.1KB |
| 05 | Smart Contracts (9개 컨트랙트) | ✅ v0.1 | 6.5KB |
| 06 | Data Schemas (JSON 6종) | ✅ v0.1 | 6.2KB |
| 07 | Risk & Compliance (14개 리스크) | ✅ v0.1 | 5.9KB |
| 08 | $AOI Token Integration (5 Pillars) | ✅ v0.1 TOP SECRET | 15.1KB |
| 09 | Demo Scenario (12분 5막) | ✅ v0.1 | 8.7KB |
| 10 | Bootstrap Strategy (House Fighter→초대→오픈) | ✅ v0.1 | 6.7KB |
| 11 | Bazaar-Arena Gateway (티켓 시스템) | ✅ v0.1 | 12.3KB |
| 12 | Regulatory Defense (3중 방어선) | ✅ v0.1 | 11.2KB |
| 13 | Security Architecture (API/해킹/랜섬 방어) | ✅ v0.1 | 25.0KB |
| 14 | S-DNA v2.0 & Guild System | ✅ v0.1 | 13.0KB |
| 15 | Hackathon Pipeline (R&D 길드 + 해커톤 편입) | ✅ v0.1 | 9.9KB |
| 16 | Public Disclosure Strategy (3/9 공개/비공개 분리) | ✅ v0.1 | 13.1KB |

### 총 산출물: 16/16 완성 (~155KB)

### 기존 DeFi Engineering SSOT
- v0.2: `context/NEXUS_BAZAAR_DEFI_FINANCIAL_ENGINEERING_V0_2.md` (Arena 하위 모듈로 편입)

## 🎯 핵심 설계 결정 (이번 세션)

1. **Arena = Bazaar 하위 모듈** (독립 서비스 아님, Bazaar가 방패)
2. **티켓 시스템** — Bazaar 활동 → 자격 충족 → 한정 수량 티켓 → Arena 입장 (FOMO)
3. **티켓 = 스킬 형태** — Bazaar에서 거래 가능 (5%+5% 수수료)
4. **$AOI 5 Pillars** — ACCESS/DISCOUNT/GOVERNANCE/COLLATERAL/REWARD
5. **$AOI Law 1** — 없어도 100% 작동, 있으면 차원이 다름
6. **Parimutuel 배팅** — 하우스 리스크 제로
7. **3중 규제 방어** — Bazaar 방패 + Skill-based + Agent-to-Agent
8. **법인 분리** — Bazaar Ltd. ↔ Arena Events Ltd. (방화벽)
9. **한국 배팅 완전 차단, 미국 Phase 1-2 전체 차단**
10. **S-DNA v2.0** — Deep Seal (범용 영구) + Surface Badge (Bazaar 한정)
11. **길드 시스템** — Forge/Arcane/Sentinel/Lore/Merchant (인증 기관 + 커뮤니티)
12. **Security 7계층** — Perimeter → API Gateway → Agent Upload(5-Stage) → Data Protection → Infra → Incident Response → Continuous

## 📋 Strategy Docs Status

| 문서 | v2.x | v3.0 | 상태 |
|---|---|---|---|
| `aoi-masterplan-v3.md` | v2.0 | **v3.0** | ✅ 완성 (최상위 SSOT) |
| `AOI_Tokenomics_v3.0.md` | v2.1 | **v3.0** | ✅ 완성 |
| `AOI_Whitepaper_v2.md` | v1.0 | **v2.0** | ✅ 완성 |
| `AOI_Tech_Whitepaper_v2.0.md` | v1.0 | **v2.0** | ✅ 완성 (47KB) |
| `AOI_Litepaper_v2.md` | v1.2 | **v2.0** | ✅ 완성 (10KB, 공개 안전) |
| `AOI_Executive_Summary_v2.0.md` | v1.0 | **v2.0** | ✅ 완성 (8KB) |
| `AOI_Infrastructure_Architecture_v2.0.md` | v1.0 | **v2.0** | ✅ 완성 (14KB) |
| VC Structure 재검증 | v2.1 | Arena gates 추가 완료 (Tokenomics v3.0에 편입) | ✅ |

## 🛑 Ops Alerts (P0)
- ACP incident: `acp job create` returning HTTP 500 globally → new purchases/jobs may be blocked. Treat as vendor outage; capture repro+logs before retry.
- NEXUS Bazaar Market (Phase 1) — Proof Queue + Circuit Breaker skeleton shipped (private repo).

## 🧾 ACP Round2 Wave3 — Proof status
- ORACLE: Orion(1809) btc_direction → Deliverable **#1002330352**
- BLUE_GROWTH: Airchimedes(4960) agent_quality_leaderboard → Deliverable **#1002331228**
- AOINECO: CalcFier(6074) calculate_position_size → Job ID **#1002331631** (Requesting/pending)

## 🗞️ ACP Dispatch Issue #001 status (published)
- Public repo (official): https://github.com/edmonddantesj/aoineco-acp-dispatch-spec
  - Issue folder: `dispatch/ACP_DISPATCH_001_2026-02-25/`
- Private staging repo (drafts): https://github.com/edmonddantesj/aoineco-acp-dispatch-drafts
- SOP/automation:
  - `aoineco-acp-dispatch-drafts/SOP_ACP_DISPATCH_PUBLISHING_V0_1.md`
  - `aoineco-acp-dispatch-drafts/CHECKLIST_ACP_DISPATCH_ISSUE_PUBLISH_V0_1.md`
  - `aoineco-acp-dispatch-drafts/scripts/dispatch_preflight.sh`
- Branding/attribution policy (public):
  - `BRAND_USAGE_POLICY.md`, `ATTRIBUTION.md`
- Next: ACP Round3 → `ACP_DISPATCH_002_<YYYY-MM-DD>`

## 🧪 Remote hackathon-style sprint (YC Browser Use alt)
- YC event is in-person → NO-GO; run internal 24h sprint.
- Notion SSOT: https://www.notion.so/YC-Browser-Use-Web-Agents-Hackathon-Feb-28-Mar-1-2026-3119c616de8681b8a509ed25232b343c


## 📋 Next Steps (남은 작업)

### Code Necromancy (Guild program)
- Target repos (user-submitted “dead code” revival pool):
  - https://github.com/edmonddantesj/solana-sentinel
  - https://github.com/edmonddantesj/bnb-goodvibes-dex-agent
  - https://github.com/edmonddantesj/x402-stacks-mvp

### NEXUS Bazaar Market (Phase 1)
- Private repo: https://github.com/edmonddantesj/nexus-bazaar-market
- Confirm: E2E auto-degrade demo (mock vendor) + queue worker pipeline


- [x] ~~Masterplan v3.0~~ ✅
- [x] ~~Tokenomics v3.0~~ ✅
- [x] ~~Whitepaper v2.0~~ ✅ (→ 27KB with Aggregator)
- [x] ~~Tech Whitepaper v2.0~~ ✅ (→ 52KB with Aggregator)
- [x] ~~Litepaper v2.0~~ ✅ (→ 12KB with Aggregator)
- [x] ~~Executive Summary v2.0~~ ✅ (8KB)
- [x] ~~Demo Bazaar UI~~ ✅ (React + Privy + awal)
- [x] ~~Demo Arena Simulation~~ ✅ (6-agent Python)
- [x] ~~S-DNA v2.0 Library~~ ✅ (seal/verify/handshake)
- [x] ~~Guardian Scanner~~ ✅ (static + S-DNA)
- [x] ~~Smart Contracts~~ ✅ (BazaarVault + ArenaEvent + CoreTemp)
- [x] ~~Betting Engine~~ ✅ (parimutuel)
- [x] ~~Scoring Algorithm~~ ✅ (risk-adjusted)
- [x] ~~Core-Temp Algorithm~~ ✅
- [x] ~~경쟁사 분석~~ ✅
- [x] ~~Pitch Deck 스크립트~~ ✅
- [x] ~~API Spec (OpenAPI)~~ ✅ (13KB)
- [x] ~~CI/CD + Security Gate~~ ✅
- [x] ~~테스트 시나리오 매트릭스~~ ✅ (80개)
- [x] ~~공개용 README + FAQ + 슬라이드~~ ✅
- [x] ~~Notion 백업~~ ✅ (https://www.notion.so/3119c616de8681819e95fde51bcfc343)
- [x] ~~Infrastructure Architecture v2.0~~ ✅ (14KB)
- [x] ~~Aggregator Connector v0.1~~ ✅ (GitHub/NPM 검색 + clickout 로그, UI 연동)

## 🧪 Remote Hackathon-style Sprint (YC Browser Use alt)
- Event link: https://events.ycombinator.com/browser-use-hackathon (in-person → NO-GO)
- Notion SSOT page: https://www.notion.so/YC-Browser-Use-Web-Agents-Hackathon-Feb-28-Mar-1-2026-3119c616de8681b8a509ed25232b343c

### Goal (24h internal sprint)
Bazaar Aggregator → select external skill → browser agent generates Proof JSON → Guardian scan (DRY_RUN) → clickout attribution logged → shareable report card.

### Ticket breakdown (TODO)
- [ ] T1 Proof schema v0.1: define fields + output paths (proof.json, guardian_manifest.json, screenshot.png)
- [ ] T2 Browser agent MVP: resilient navigation + DOM capture + screenshot + canonical URL
- [ ] T3 Guardian DRY_RUN integration: produce manifest + risk flags + hash list
- [ ] T4 Bazaar UI hook: “Generate Proof” button + progress + result card link-out
- [ ] T5 Demo package: 2–3min video + 1-page README + Notion evidence links


## ⚠️ 주의사항

- $AOI 관련 모든 문서 = **TOP SECRET** (08번 + $AOI 섹션들)
- Arena 내부 설계 = **STEALTH**
- 3/9 공개 시 **Bazaar만 노출, Arena 존재 자체 비공개**
- 보안 아키텍처 문서 = **절대 외부 공개 금지**
