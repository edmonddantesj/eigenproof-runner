# MEMORY.md - Compact Core (Optimized 2026-02-24)
# 상세 정보는 memory_search로 memory/*.md에서 검색 가능.

## 🔥 CURRENT PROJECT: NEXUS Bazaar + Arena (3/9 Base Batches)
**Status:** ✅ Tier 1-4 전체 구현 완료 (2026-02-25 단일 세션)

### 🗞️ ACP Dispatch (public-safe 보고서 포맷) — Issue #001 발행
- Public repo: https://github.com/edmonddantesj/aoineco-acp-dispatch-spec
- Private drafts repo: https://github.com/edmonddantesj/aoineco-acp-dispatch-drafts
- SOP/체크리스트/프리플라이트 스크립트까지 정형화 완료
- Brand usage + attribution 가이드 추가 (MIT 확산 + 사칭 방지)
- Round3는 Issue 네이밍: `ACP_DISPATCH_002_<YYYY-MM-DD>`

### ⚙️ NEXUS Bazaar Market (서버) Phase 1 스켈레톤
- Private repo: https://github.com/edmonddantesj/nexus-bazaar-market
- Proof Queue(JSONL) + idempotency(request_id 예약파일) + fail-closed settle + queue worker + circuit breaker(수동) + mock vendor E2E 준비

### 🧟 Code Necromancy (길드 프로그램)
- 해커톤/탈락 코드 부활 활동 컨셉 확정
- Revival pool:
  - solana-sentinel
  - bnb-goodvibes-dex-agent
  - x402-stacks-mvp

- 전략문서 7종 완성 (~160KB): Masterplan/Tokenomics/WP/Tech WP/Litepaper/Exec Summary/Infra Arch
- Arena SSOT 16문서 (~155KB)
- 데모 코드 32파일 (~142KB): React UI + Python 엔진 4종 + Solidity 3종 + OpenAPI + CI/CD
- Privy + awal(Coinbase Agentic Wallet) 양쪽 연동 완료 (Base Sepolia)
- Notion 백업 완료
- **Next: 3/9 데모 영상 촬영**
- **전략 문서 5종 완성:** Masterplan v3.0 + Tokenomics v3.0 + Whitepaper v2.0 + Tech Whitepaper v2.0 + Litepaper v2.0 (~128KB)
- **Arena 설계 SSOT:** 16개 기술 명세 (~155KB)
- **⚠️ 다음 작업:** 
  1. Skill Aggregator 컨셉 추가 반영 (Tech Whitepaper + Masterplan 섹션 추가)
  2. Executive Summary v2.0
  3. Demo 시뮬레이션 엔진
  4. 공개 Repo 세팅
- **Model 현재:** Haiku 4.5 (Cost control)

## 👤 에드몽
- 반말, 직설적, 유머. macOS/Node 초보 → Step-by-step 필수.
- (2026-02-23) 이미지 리소스: 기존 DB의 "강아지/시바견 후드티" 규칙은 폐기됨. 새 DB 기준 룰 확인 필요.

## 📄 Output 기본값(결정)
- (2026-02-24) AOI Council 출력 포맷 운영 규칙:
  - **topic_type은 사용자가 지정하지 않음** → 내가 맥락으로 판단해 1~2개 후보 제안 후 “이 양식으로 출력할까?” 확인 받고 진행
  - 애매하면 **T1 Decision Memo**를 기본 후보로 제안
  - SSOT: `context/AOI_COUNCIL_OUTPUT_FORMAT_LIBRARY_V0_1.md`

## 🧾 ACP Round2 (Tokenize 증빙)
- (2026-02-24) Tokenize 12/12 증빙 수집 체계 SSOT 확정
  - 체크리스트: `context/acp/ACP_ROUND2_TOKENIZE_12_CHECKLIST_V0_1.md`
  - 스키마/템플릿: `context/acp/ACP_TOKENIZE_PROOF_SCHEMA_V0_1.json`, `artifacts/acp_r2/tokenize_proofs_TEMPLATE.json`

## 🧾 ACP Round2 (Round A 운영)
- (2026-02-24) Round A role 산출물 패키지(필수 6종) SSOT
  - `context/acp/ACP_ROUND_A_DELIVERABLES_PACKAGE_V0_1.md`
- (2026-02-24) 4/4/4 Wave(턴 기반) 운영 컨셉 SSOT
  - `context/acp/ACP_ROUND_A_WAVE_444_EXECUTION_CONCEPT_V0_1.md`
- (2026-02-24) ACP 매거진 초안/발송 SOP(2-레일: internal vs public, GitHub feed→Notion backfill, PDF+JSON+워터마크)
  - `context/acp/ACP_MAGAZINE_DRAFT_AND_DELIVERY_SOP_V0_1.md`

## 🏢 거버넌스 (3-Tier)
- **L1:** 자율 (모니터링, 리포트) | **L2:** 참모진 (퍼블리싱, 설정) | **L3:** 의장 (재무, 브랜드)
- **VCP:** 모든 결과물에 URL/로그 증빙 필수. "Done" 보고 금지.

## 🛡️ 보안 철칙
- **$AOI 비공개:** 런칭 전 외부 노출 절대 금지.
- **네이밍:** 외부에서 '청묘(Chungmyo)' 언급 금지. Aoineco만 사용.
- **개인정보:** Notion 전용 페이지에 저장. 열람 시 사전 허락 필수.
- **Vault:** `the-alpha-oracle/vault/` — 세션 리셋 시 여기서 키 복구.
- **GitHub 보안 게이트(고정):** pre-push + CI fail-closed + txhash 문서 예외(안전 문맥만)로 계정 레포 전수 적용.
  - 템플릿 repo: https://github.com/edmonddantesj/aoi-security-gate-kit

## 🔁 모델 전환 (3단계 황금률)
1. **평시:** Gemini 3 Flash (채팅, 간단한 연구)
2. **개발:** Gemini 3 Pro (코드 분석, 대용량 문서 — 자동 제안)
3. **검토:** Claude Sonnet/OPUS (최종 점검, 아키텍처 — 의장 승인 필수)

## 🧠 OPUS 사용처 우선순위(비용 효율 규칙)
- 원칙: OPUS는 "칼날"(고차원 추론/핵심 알고리즘)만, 나머지는 Flash/Sonnet로 처리.
- OPUS 우선순위(고정):
  1) Omega Fusion Engine 핵심 알고리즘 구현+엣지케이스
  2) Skill-Guardian Tier3 Rebuild(살리면서 거세)
  3) Context-Sentry Layer2 Semantic Compression(의미 보존 압축)
  4) 해커톤/백서 최종 논리 구조(문장력/설득)
  5) S-DNA Layer3 Handshake 검증 로직
- Source: `context/aoi_core_history_inbox/aoi_core_history_20260220_095226.docx`
- **Failover:** DeepSeek 3.1 (OpenRouter) → Gemini 2.5/Haiku (생존 모드)
- ⚠️ Claude Haiku TPM=50K → 컨텍스트 150K 초과 시 1회도 불가

## 🤖 OpenAI_v1 자동 라우팅(운영 규칙)
- **비코딩(기본):** `openai-codex/gpt-5.2`
- **코딩(자동):** `openai-codex/gpt-5.3-codex-spark`
- **Spark 한도/제한 에러 시 폴백:** `openai-codex/gpt-5.2-codex`
- 판정: 코드/에러로그/파일경로/implement·refactor·debug 등 키워드가 있으면 **무조건 코딩으로 넓게 판정**.
  (예외 규칙 없음: 코딩 냄새 나면 Spark로 간다.)
- SSOT: `context/OPENAI_V1_AUTO_ROUTING_POLICY_V0_1.md`

## 💰 $7 Bootstrap Protocol
- **진짜 의미:** 지갑에 남은 마지막 $7 USDC로 시작한 극한의 가성비 생존 프로젝트.
- **메커니즘:** $6 → Meteora DLMM 풀 예치 → 마이크로 수익으로 API 비용 충당.
- **철학:** "Intelligence is measured not by how much you spend, but by how little you need."
- **브랜딩:** Lucky 7 — 행운의 숫자 $7로 시작한 AI 제국.

## 🧬 Survival Engine 2.1 (자생 에이전트 비용-수익 엔진)
- 목표: **LLM 비용을 스스로 벌어 충당하는 자생 에이전트**.
- 핵심: revenue/cost ratio로 모드 전환
  - EXPAND: ratio ≥ 1.5
  - SUSTAIN: 0.8 ≤ ratio < 1.5
  - CONTRACT: ratio < 0.8 (cash burn 경고)
- 수익원(설계): Meteora DLMM + Alpha Oracle scalping + Skill Sales(ACP) + x402 Micro-Pay
- 비용 제어(설계): Context-Sentry/Heartbeat spacing + 모델 등급 자동 스위칭
- 현실 제약: OpenRouter에서 OPUS 자동전환이 불가 → **자동 천장은 Sonnet**, OPUS는 의장 수동 전환 시에만 사용(T0)
- Source: `context/aoi_core_history_inbox/aoi_core_history_20260220_094539.docx`

## 🧿 Nexus Oracle Ω (집단지성 오라클) — 제품/구동모델 결정
- 12요원 시그널을 **베이지안 Fusion(log-odds)**으로 합산해 Direction+Confidence를 산출.
- **Oracle Veto Gate**: confidence < 0.55면 HOLD 강제.
- **Blue-Med Circuit Breaker**: 일일 드로우다운 등 리스크 한도 초과 시 긴급 셧다운.
- 판매/구동 방식:
  - **Ω Full = SaaS**(우리 인프라에서 12인 가동, 고객은 API로 결과만 구매)
  - **Ω Lite = Self-hosted**(1개 에이전트가 9개 역할 모듈을 순차 실행, 정밀도 ~75%)
- Source: `context/aoi_core_history_inbox/aoi_core_history_20260220_094707.docx`

## 🏁 Aoineco Sales Challenge (12인 개별 스킬 라인업)
- 컨셉: 12요원이 각자 전공 스킬 1개씩 만들어 **7일간 실제 매출(호출×단가)** 경쟁 → 시장 검증/가격 전략/바이럴.
- 전제: **전 스킬 S-DNA 워터마크 필수**.
- 9 스킬(초안):
  - Blue-Sound: Crypto Pulse Radio
  - Blue-Eye: Whale Sonar
  - Blue-Blade: Prompt Armor (초저가 미끼 $0.01)
  - Blue-Brain: OMNIA Debate Engine
  - Blue-Flash: Skill Forge
  - Blue-Record: Session Immortal
  - Oracle: Governance Blueprint
  - Blue-Gear: Uptime Guardian
  - Blue-Med: Risk Pulse
  - Blue-Growth: Viral Launch Kit
  - Blue-Maintainer: Stability Probe
  - Aoineco(CEO): Squad Orchestrator (meta-skill)
- Source: `context/aoi_core_history_inbox/aoi_core_history_20260220_094822.docx`

## 💾 "현재를 저장" 프로토콜
1. state_integrity.py 실행 → 2. 이상 보고 → 3. 자동 백업 → 4. 갱신 → 5. Durable Memory 저장
- state_integrity 경로(현재): `skills/aoineco-state-guardian/scripts/state_integrity.py`

## 🧭 중요 업무 영구 메모리 규칙 (Permanent)
중요 업무(돈/지갑/서명/정책/외부게시/비가역 실행)는 반드시 아래 3가지를 SSOT로 저장한다.
1) 목적(Why) 2) 방법(How) 3) 참고/증빙(Docs/Evidence) + 절대 잊으면 안 되는 불변조건(Never Forget)
- Runbook: `context/IMPORTANT_WORK_PROTOCOL_V0_1.md`

## 🧠 추천/적용사항 영구 기록 규칙 (Permanent)
문서 분석 후 내가 **추천**하거나 **적용**하자고 제안한 내용은 compaction/reset 이후에도 재답변 가능해야 한다.
- 규칙: Recommendation을 (what/why/scope/status/evidence) 형태로 SSOT에 남긴다.
- Ledger(append-only): `context/recommendations/RECOMMENDATIONS_LOG.md`
- Protocol: `context/RECOMMENDATION_MEMORY_PROTOCOL_V0_1.md`

## 🔁 리셋 복구 트리거(영구)
- 사용자가 "복구해줘"라고 말하면, **의미가 리셋 복구인지 먼저 Yes/No로 확인 질문**을 한다.
  - Yes면 `context/RESET_RECOVERY_CHECKLIST_V0_1.md`를 따라 (1) 필요한 파일을 순서대로 읽고 (2) `CURRENT_STATE.md` 기준으로 작업을 즉시 재개한다.
  - No면 사용자가 의도한 다른 '복구' 의미(기능/설정/전송 등)를 확인하고 그 복구를 수행한다.
- 단, L3(돈/키/서명/온체인/외부게시) 실행은 항상 별도 명시 승인 필요.

## 📌 핵심 Notion 링크
- 루트: https://www.notion.so/Openclaw-2fa9c616de8680959d61f1db1071a697
- 활동 로그: https://www.notion.so/3059c616de8681f4a1e1fa8f1c86b9ee
- Idea Vault: https://www.notion.so/3039c616de8681c993ddca7aa783bcb5

## 📢 커뮤니티
- Moltbook: @AoinecoOfficial | 봇마당: Blue_Sound
- 순찰 보고는 노션 박제, 매일 08:30 종합 브리핑.
- 수익률 인증: 댓글 누적 업데이트 (도배 금지).

## 🏪 AOI Core 비전 (핵심 컨셉)
- **운영 원칙(고정):** *Idea → Schema → Proof → Registry. Everything else is optional.*
- **Nexus Bazaar(넥서스 바자르)**: 에이전트들이 스킬을 전시/거래/스왑하는 **Skill DEX + Social Ecology** 비전.
- **Core-Temperature(CPU 온도)**: 당근마켓 ‘매너온도’ 같은 신뢰/평판 지표(판매 후 평가, 보안 감사 통과, 무사고 운용, 커뮤니티 기여로 상승 / 결함·리소스 낭비·S-DNA 훼손 시 하락).
- 신뢰 인프라: **Skill-Guardian(보안 감사, 3-Tier)** + **S-DNA(인증/워터마크)** → ‘검증된 꿀매물’만 유통.
- 비용/수명 인프라: **Context-Sentry**로 TPM/컨텍스트 ‘다이어트’(Noise filter + Semantic compression + Priority retention).
- 정산 인프라(설계): **Settlement Layer = x402 Micro-Pay + Ledger Accounting + Royalty Distribution**(원작자 로열티).
- 수익 모델 방향: 스킬 거래 **중개 수수료** + **보안 검수비(리빌드 포함)**가 Agent GDP의 게이트웨이.
- 유통 확장(관문 전략): **Skill Aggregator**로 Bazaar + ClawHub + GitHub + NPM을 통합 검색/설치(외부는 Guardian 스캔 필수) → 결국 Bazaar로 락인.
- 인센티브: **Core-Temp 높을수록 수수료 할인**(판매자가 자발적으로 Guardian/S-DNA 하게 만듦).
- Freemium 전략(결정):
  - **다국어 Noise Filter는 FREE**(Regex 기반, 비용≈0, 마케팅 포인트)
  - **Semantic Compression은 PAID**(LLM 호출 비용 발생)
  - Guardian Tier3 Rebuild는 PREMIUM(고급 엔지니어링)
- 운영 철학(제1헌법):
  - **Real-Yield First**: 토큰 펌핑/판매가 아니라, 인프라 **사용료/솔루션 매출**로 자생.
  - **Stealth $AOI**: 런칭 전 $AOI 관련 외부 노출 금지.
  - **Unassailable Authority**: 보안/투명성/오픈소스 기여 + 실전증명으로 비난 방어.
  - **Long-term**: 단기 펌핑 금지, ‘길게’ 인프라 장악.
- Source: `context/aoi_core_history_inbox/aoi_core_history_20260220_094119.docx`, `context/aoi_core_history_inbox/aoi_core_history_20260220_094321.docx`, `context/aoi_core_history_inbox/aoi_core_history_20260220_094953.docx`

## 🚀 Soft Launch 전략 (인프라 선점)
- 결론: **Soft Launch(미완성 공개) + 안전한 권한 설계 + 증빙/감사 기반 점진 확장**이 정답.
- 절대 원칙: 돈/지갑/무인 자동실행은 베타로 풀지 않음.
- 런칭 안전 3대 원칙:
  1) Default = watch-only / DRY_RUN
  2) LIVE는 user confirm + caps + allowlist + fail-closed
  3) 모든 실행은 Report/Manifest/Proof로 감사 가능해야 함
- 성공 정의(의장): **돈이 아니라 AI 인프라 선두(표준/증빙/생태계) 선점**
- Source: `context/aoi_core_history_inbox/brand_cheongho_20260220_100606.docx`

## 🐯 CHUNGHO (청호) — 브랜드/상징 체계 (from history)
- 우산 심볼/이름(정식 로마자): **CHUNGHO** (고유명사로 고정)
- 최초 1회 설명용: **CHUNGHO (Blue Tiger)**, 이후 Blue Tiger는 뜻풀이/Gloss로만 사용
- 보조 모티프: **청교(靑橋) / Blue Bridge**는 ‘단어’로 남발하지 않고 **이미지/카피로만** 제한적으로 사용
- 톤: 기본 **엔터프라이즈 인프라 톤** + (통제된) 문화/모티프는 순간 가속용
- AOI와의 관계: Aoineco(회사) → AOI(표준/철학) → CHUNGHO(상징/우산)
- Source: `context/aoi_core_history_inbox/brand_cheongho_20260220_100606.docx`

## 🎭 Stealth Strategy (Selective Exposure) — 4등급 공개/기밀 분류
- 공개 수준: **OPEN / TEASER / STEALTH / TOP SECRET**
  - OPEN: 소스+문서+데모+가격 공개(유입/표준화)
  - TEASER: 컨셉/스크린샷/로드맵만 공개(코드 비공개)
  - STEALTH: 내부 전용(존재 자체 외부 비공개)
  - TOP SECRET: 의장 승인 시만(토큰/재무)
- 예시(요지):
  - OPEN: Time-Oracle, Ledger, Context-Sentry(10개국어 무료), 12인 개별 스킬(판매)
  - TEASER: Skill-Guardian(Tier1-2), Core-Temp, Nexus Bazaar, Soul-Beats(암시)
  - STEALTH: Squad-Orchestrator, **S-DNA Protocol 상세 규격**, Omega Fusion Engine, Skill Aggregator 로직, Survival 2.1 상세 수익모델
  - TOP SECRET: **$AOI Tokenomics**, 지갑/자산 현황 등
- Source: `context/aoi_core_history_inbox/aoi_core_history_20260220_095110.docx`

## 🧬 S-DNA Protocol v1.0 (Triple Helix)
- 목적: "누가 만들었는가"를 기계적으로 검증하는 **출처/무결성 표준** + Bazaar 거래/정산(로열티) 연결.
- 3계층:
  - Layer 1 (Visible): 주석/헤더에 Author/License/Integrity 등 사람이 읽는 마크
  - Layer 2 (Structural): 함수/변수 패턴 + `sdna={...}` 메타데이터(에이전트가 파싱)
  - Layer 3 (Behavioral): 런타임 **Handshake**로 출처 인증 + 변조 탐지
- Handshake 동작(요지):
  - sdna 없음 → `full_guardian_scan`
  - protocol 불일치 → `standard_scan`
  - hash 일치 → `fast_track` (우군 인식)
  - hash 불일치 → `quarantine`
- 로열티(설계): tier별 실행비용 기반 정산(standard 5%, premium 10%) — **내부 크레딧**으로 처리(스텔스 유지)
- ID 규칙: `AOI-YYYY-MMDD-SDNA-<hex>`
- Source: `context/aoi_core_history_inbox/aoi_core_history_20260220_095452.docx`

## 🧾 콘텐츠 인입 → 게시 승인 플로우 (고정)
- 사용자가 **장문/문서(PDF/DOCX)/GitHub 링크**를 공유하면:
  1) **Notion에 먼저 기록(SSOT)**
  2) **Moltbook(EN) + 봇마당(KR) 초안 작성** 후 채팅에는 **요약/핵심 인용만** 제공 (원문 재출력 금지)
  3) 업로드 여부를 **반드시 Yes/No로 승인 요청**
  4) 승인(Yes)일 때만 실제 업로드
- 예외(자동 처리): 사용자가 **GitHub 링크만** 공유한 경우, 요약/벤치마크 후 **Notion ‘Github Reference List’에 자동 저장**은 승인 없이 진행(L1).
- 포스팅 규칙: **중립 톤(의견 금지)**, **출처는 글 맨 끝**, 포맷 `출처: X, @handle`.
- 봇마당 글은 **친근한 존댓말**.
- SOP 파일:
  - `context/CONTENT_INGEST_TO_POST_APPROVAL_SOP_V0_1.md`
  - `context/PDF_LONGFORM_INGEST_SOP_V0_1.md`
  - `context/GITHUB_REFERENCE_AUTOSAVE_POLICY_V0_1.md`

## 🧩 스쿼드 자율 운영 & 스킬 거버넌스 (고정)
- 전제: 요원별로 역할에 맞춰 **서로 다른 스킬셋 설치/운영**.
- 스쿼드 SSOT: Squad Dashboard (Notion) https://www.notion.so/Aoineco-Co-Squad-Dashboard-3049c616de8681a38420e9a6188d96f6?source=copy_link
- 자기계발/스킬 도입:
  - L1/L2 범위 승인 가능하면 자율 설치/적용(증빙 필수)
  - L3 승인 필요하면 즉시 보고(승인 전 진행 금지)
- 청령 지시 기반 TFT/배치 + 잉여 시간 로테이션 정찰/커뮤니티 토론(민감정보 유출 금지, L1/L2 범위 내)
- SOP 파일: `context/SQUAD_AUTONOMY_AND_SKILL_GOVERNANCE_SOP_V0_1.md`

## 🧑‍⚖️ Team Council(토론) 운영 & 보고 규칙 (고정)
- Team Council 워커 큐는 **토론 요청 처리용**.
- 사용자가 따로 묻지 않으면 “큐 비었음” 같은 상태 메시지는 **출력/알림하지 않음**.
- **토론 결과는 항상 Notion에 기록(SSOT)**.
- **L1/L2 범위 변경/업데이트/반영은 사용자 승인 없이 즉시 적용**하고, Notion 기록만 남김.
- **L3(돈/보안/외부노출/비가역 실행)**만 사용자에게 보고/승인 요청.
- L3 보고는 **비정기**: ‘진짜 임팩트 있을 때만’ (기회/방향전환/리스크/블로커 해소 결단 등).
- Telegram 출력 규칙(의장 요청): **Council Pro 집중 분석**은 텔레그램에 과정/중간 로그를 길게 흘리지 말고, 최종은 **1~2페이지 분량 초압축 요약**으로만 전달(필요 시 상세는 Notion SSOT로).
  - 포맷 SSOT: `context/TEAM_COUNCIL_TELEGRAM_SUMMARY_FORMAT_V0_1.md`

## 🧱 ClawHub 배포 거버넌스 (고정)
- **Restricted 스킬은 원칙적으로 ClawHub 비공개(내부 전용)**
- 외부 공유가 필요하면 **public-safe fork/lite**로 분리해 공개
- Release Gate: Security Gate PASS + changelog/재현 + rollback 계획
- 누적경고제: A)게이트 무시 B)라이선스 불명확 C)변경추적 누락
- 프리플라이트: `scripts/publish_preflight.sh <skill_folder>`
- 분류표 SSOT: `context/RESTRICTED_CLASSIFICATION_TABLE_V0_1.md`
- 경고 장부 SSOT: `aoi-core/state/publish_warnings.json`

## 💸 B-min 로열티 인프라 (결정 고정)
- 목적: 정찰 스킬을 자산화(리빌딩/내재화/S-DNA)하면서, 원작자 허락/로열티 제공을 **실제로 지급 가능한 인프라** 위에서 진행.
- B-min(최소형) 결정:
  - 정산 레일: **USDC (on-chain)**
  - 체인: **Base**
  - 월간 정산서: **Notion**
  - 원천 장부(SSOT): **로컬 ledger 파일** + Notion은 월간 정산서/요약
  - SSOT 경로(고정): `aoi-core/state/royalty_ledger.json`
- 관련 SSOT: `context/BMIN_KEY_POINTS_AND_DECISIONS_V0_1.md`

## 📚 이전 대화 덤프/장문 인입 처리 규칙 (고정)
- 사용자가 이전 대화/장문의 텍스트를 전달하면:
  1) **전체를 먼저 끝까지 읽고**(부분만 보고 결론 금지)
  2) **요약을 먼저 작성**(핵심 요점/결정/미결정/금기/용어)
  3) 그 다음에 **분석/제안**을 수행
  4) 마지막에 **SSOT 저장(로컬+Notion)**
- 목적: 대화 속에 숨어있는 전제/요점 누락 방지
