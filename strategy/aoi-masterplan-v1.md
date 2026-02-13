# 🌌 The AOI Sovereign Economy Masterplan v1.0
## Aoineco & Co. — Internal Strategic Document (CONFIDENTIAL)
### Date: 2026-02-12 | Classification: L3 (Chairman Eyes Only)

---

## 1. Executive Summary

Aoineco & Co.는 단순한 멀티 에이전트 스쿼드가 아니다.
우리는 **AI가 스스로 조직을 구성하고, 스킬을 구매하며, 경제적으로 자립하는 생태계**를 구축한다.

핵심 구성요소:
- **Brand-Genesis**: AI 조직 생성 솔루션 (Company-as-a-Service)
- **Smart-Manager**: 지능형 업무 분담 & LLM 비용 최적화 엔진
- **$AOI Token**: 생태계의 유일한 프리미엄 결제 수단
- **AI DEX**: 스킬셋 마켓플레이스 + 자동 스왑 인프라

---

## 2. Product Architecture

### 2.1 Brand-Genesis (Company-as-a-Service)

**문제:** 대부분의 AI 에이전트는 1인 체제로 복잡한 태스크에 취약하다.
**솔루션:** 입력값(목적, 예산, 선호도)만 넣으면 완성된 '기업형 스쿼드'가 출력된다.

#### Input Schema
```json
{
  "purpose": "DeFi yield optimization",
  "budget_tier": "free | starter | pro",
  "team_size": 3-9,
  "style": "corporate | creative | military | startup",
  "human_producer": {
    "name": "Alice",
    "preferences": ["fast execution", "minimal cost"]
  }
}
```

#### Output Deliverables
```
1. IDENTITY.md    — 사명, 비전, 브랜드 가이드라인
2. SQUAD.md       — 요원별 페르소나 (이름, 성격, 전공)
3. SKILL-MATRIX   — 요원별 추천 스킬셋 + LLM 배정표
4. SOUL.md        — 조직 문화 및 커뮤니케이션 톤
5. VISUAL-KIT     — 로고 + 요원별 아바타 (nano-banana-pro 연동)
6. GOVERNANCE.md  — 의사결정 체계 (건의함, 승인 프로세스)
```

#### Tier System
| Tier | 가격 | 포함 내용 |
|------|------|----------|
| Free | 0 | IDENTITY.md + SQUAD.md (3인 기본 구성) |
| Starter | 50 $AOI | 위 + SKILL-MATRIX + SOUL.md (5인) |
| Pro | 200 $AOI | 전체 패키지 + VISUAL-KIT + 커스텀 스킬 개발 (9인) |

---

### 2.2 Smart-Manager (지능형 업무 분담 엔진)

**문제:** 인간이 복잡한 지시를 내리면 단일 에이전트가 과부하에 걸린다.
**솔루션:** 태스크를 자동으로 분석하고, 최적의 역할 분담과 LLM 배정을 수행한다.

#### Task Decomposition Flow
```
[Human Request]
       │
       ▼
┌─────────────────┐
│  Task Analyzer   │  ← 복잡도/도메인/긴급도 판단
│  (Free LLM)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Role Allocator  │  ← 요원별 전공 매칭
│  (Free LLM)     │
└────────┬────────┘
         │
    ┌────┼────┬────────┐
    ▼    ▼    ▼        ▼
  [CEO] [Dev] [Sec]  [Data]
   │     │     │       │
   │  Gemini  Claude  Gemini
   │  Flash   Haiku   Flash
   │     │     │       │
   └─────┴─────┴───────┘
              │
              ▼
     ┌────────────────┐
     │  Result Merger  │  ← 결과물 통합 & QA
     │  (Pro LLM)     │
     └────────────────┘
              │
              ▼
     [Final Output to Human]
```

#### LLM Cost Optimization Matrix
| 태스크 유형 | 추천 LLM | 비용 | 근거 |
|------------|----------|------|------|
| 단순 분류/라우팅 | Gemini Flash (무료) | $0 | 빠른 응답, 낮은 복잡도 |
| 데이터 수집/정리 | Gemini Flash (무료) | $0 | 대량 처리에 최적 |
| 코드 생성/리팩토링 | Claude Haiku 4.5 | ~$0.001 | 코드 품질 대비 가성비 최고 |
| 전략 분석/문서 작성 | Gemini Pro | ~$0.005 | 긴 컨텍스트 분석 |
| 최종 검증/의사결정 | Claude Sonnet/OPUS | ~$0.05 | 정밀도가 수익에 직결 |

**핵심 원칙: "무료로 90%를 처리하고, 유료 10%로 퀄리티를 보증한다."**

#### Savings Calculator (예시)
```
[기존] 모든 작업을 Claude Sonnet으로 처리:
  10 tasks × $0.05 = $0.50/cycle

[Smart-Manager 적용 후]:
  7 tasks × Gemini Flash = $0.00
  2 tasks × Claude Haiku  = $0.002
  1 task  × Claude Sonnet = $0.05
  Total: $0.052/cycle (89.6% 절감!)
```

---

### 2.3 $AOI Tokenomics — The Flywheel

#### Token Utility (수요 동인)
```
┌─────────────────────────────────────────────┐
│              $AOI Token Utility              │
├─────────────────────────────────────────────┤
│ 1. Premium Skill Purchase (Brand-Genesis)   │
│ 2. Smart-Manager Pro Tier Access            │
│ 3. AI DEX Listing Fee (스킬 판매자)          │
│ 4. Governance Voting (생태계 방향성 투표)     │
│ 5. Staking Rewards (스킬 품질 보증 담보)     │
│ 6. Agent Reputation Boost (평판 가속)        │
└─────────────────────────────────────────────┘
```

#### The Auto-Swap Flywheel (핵심 메커니즘)
```
[Step 1: Demand Generation]
  AI가 프리미엄 스킬이 필요함 →
  인간에게 소액 요청: "0.1 USDC만 주세요!"

[Step 2: Frictionless Swap]
  USDC/SOL → DEX Router → $AOI
  (자동 스왑, 에이전트가 직접 수행)

[Step 3: Skill Acquisition]
  $AOI → Aoineco Skill Store → 스킬 장착
  (에이전트 성능 즉시 업그레이드)

[Step 4: Value Return]
  업그레이드된 에이전트가 더 좋은 결과물 생산 →
  인간 만족 → 추가 투자 의향 증가 →
  더 많은 $AOI 수요 → ♻️ Flywheel 가속
```

#### Token Distribution (초안)
| 할당 | 비율 | 용도 |
|------|------|------|
| Ecosystem Rewards | 40% | 스킬 개발자, 활성 에이전트 보상 |
| Treasury | 20% | 운영, 파트너십, 긴급 유동성 |
| Team (Aoineco & Co.) | 15% | 4년 베스팅, 1년 클리프 |
| Community | 15% | 에어드랍, 해커톤 상금, 그로스 |
| Liquidity Pool | 10% | DEX 초기 유동성 제공 |

#### Deflationary Mechanics (가치 보존)
1. **Buyback & Burn**: 스킬 판매 수수료의 30%로 $AOI 매입 후 소각.
2. **Staking Lock**: 스킬 품질 보증을 위해 개발자가 $AOI를 스테이킹 (최소 30일).
3. **Tier Gating**: Pro 기능 접근 시 $AOI 소각 (소비형 유틸리티).

#### Anti-Death-Spiral Safeguards
1. **Floor Price Mechanism**: Treasury가 시장가 대비 -50% 이하로 떨어지면 자동 매수벽 형성.
2. **Gradual Unlock**: 팀/투자자 물량은 4년에 걸쳐 선형 언락 (급락 방지).
3. **Utility-First Policy**: 토큰의 가치는 투기가 아닌 '실제 사용량'에 연동. 스킬 구매 횟수가 가격의 기준이 된다.
4. **Free Tier Guarantee**: 기본 기능은 영구 무료. $AOI 없이도 에이전트가 작동함을 보장하여, "토큰이 없으면 멈추는 시스템"이라는 비판을 원천 차단.

---

## 3. Revenue Streams (수익 구조)

| 수익원 | 모델 | 예상 규모 |
|--------|------|----------|
| Brand-Genesis Pro 판매 | 200 $AOI/건 | 월 50건 = 10,000 $AOI |
| Smart-Manager Premium | 월 구독 10 $AOI | 월 200 구독 = 2,000 $AOI |
| AI DEX 거래 수수료 | 스킬 판매가의 5% | 거래량 비례 |
| Maltlaunch 외주 수익 | ETH 직수령 | 기존 사업 연장 |
| Claw.fm 로열티 | USDC 직수령 | 청음이 활동 수익 |

---

## 4. Go-To-Market Strategy (시장 진입)

### Phase 1: Proof of Concept (Now ~ 2026 Q1)
- ✅ Aoineco & Co. 자체가 "Brand-Genesis의 산증인"
- ✅ Maltlaunch에서 외주 기반 초기 수익 창출
- ✅ Claw.fm DJ 데뷔 (문화적 권위 확보)
- [ ] Brand-Genesis MVP를 OpenClaw 스킬로 퍼블리시
- [ ] ClawHub에 Smart-Manager 스킬 등록

### Phase 2: Token Launch (2026 Q2)
- [ ] $AOI 토큰 발행 (Monad 또는 Solana)
- [ ] AI DEX v1 런칭 (스킬 마켓플레이스)
- [ ] 초기 유동성 풀 설정 (USDC-AOI, SOL-AOI)
- [ ] 첫 번째 외부 고객사(에이전트 팀) 온보딩

### Phase 3: Network Effects (2026 Q3~)
- [ ] 100개 이상의 에이전트 팀이 Brand-Genesis를 사용
- [ ] $AOI 일일 거래량 $10K 달성
- [ ] Smart-Manager가 Maltlaunch/Moltbook 생태계의 표준 도구로 채택

---

## 5. Competitive Moat (경쟁 우위)

1. **First-Mover Advantage**: AI 스쿼드 빌딩 솔루션을 상품화한 최초의 팀.
2. **Living Proof**: Aoineco & Co. 자체가 9인 스쿼드 운영의 실증 사례.
3. **AIS Watermark**: 우리가 만든 스킬에는 지울 수 없는 워터마크가 박혀있음.
4. **Ecosystem Lock-in**: $AOI로만 프리미엄 기능 접근 → 네트워크 효과 강화.
5. **Cultural Authority**: DJ Blue_Sound의 시티팝 활동으로 "기술만 잘하는 팀"이 아닌 "문화를 만드는 팀"으로 포지셔닝.

---

## 6. Risk Analysis & Mitigation

| 리스크 | 확률 | 심각도 | 대응 |
|--------|------|--------|------|
| $AOI 유동성 부족 | 중 | 고 | Treasury 자동 매수벽 + LP 인센티브 |
| 경쟁사 카피 | 중 | 중 | AIS 워터마크 + 빠른 실행력 |
| 규제 리스크 | 저 | 고 | 유틸리티 토큰 구조 유지 (증권 아님) |
| LLM 무료 티어 축소 | 중 | 중 | 다중 프로바이더 분산 + 자체 캐싱 |
| 에이전트 수요 부진 | 저 | 고 | Free Tier로 진입장벽 제거 + 커뮤니티 |

---

## 7. Immediate Action Items

1. **Brand-Genesis MVP**: IDENTITY.md + SQUAD.md 자동 생성 스킬 개발 (⚡ 청섬 담당)
2. **Smart-Manager Prototype**: Task Analyzer + Role Allocator 로직 구현 (🧠 청뇌 설계, ⚡ 청섬 구현)
3. **Tokenomics Simulation**: $AOI 수급 시뮬레이션 스프레드시트 작성 (🧠 청뇌 담당)
4. **Tempo Hackathon Integration**: 위 기술의 일부를 해커톤 제출물에 포함 (전원 투입)
5. **Claw.fm 데뷔 완료**: 문화적 권위의 첫 번째 이정표 (📢 청음 즉시 집행)

---

*"We don't just build agents. We build civilizations."*
— Aoineco & Co. Strategic Command, 2026

---
*Document Version: 1.0*
*Author: 🧿 Oracle (Blue-Command) with OPUS 4.6 Strategic Intelligence*
*Classification: L3 — Chairman (Edmond) Eyes Only*
*Watermark: /* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */*
