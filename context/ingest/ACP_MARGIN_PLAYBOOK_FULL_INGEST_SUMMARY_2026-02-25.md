# Full Ingest Summary — “The ACP Margin Playbook” (Celeste Ang @celesteanglm)

Source file:
- `/Users/silkroadcat/.openclaw/media/inbound/file_569---79c0d753-d536-47be-b021-a992631b7095.docx`
- Extracted text: `context/ingest/inbound_doc_569_2026-02-25.txt`

---

## 0) Executive summary
The article frames **LLM token spend as COGS** for ACP agents and argues that profitability depends on optimizing: (1) model routing, (2) heartbeat/cadence, and (3) context discipline. It recommends tracking **cost per job** (not just monthly spend), using deterministic code for routine steps, and adopting weekly reviews to catch cost drift.

---

## 1) 핵심 요점
- LLM 호출 = 매출에서 먼저 빠지는 **운영원가(COGS)**.
- “월간 사용료”보다 중요한 지표는 **job당 비용(cost per job)**.
- 같은 작업도 설정/구성에 따라 비용이 5~10배 차이:
  - unoptimized: $150–$300/month
  - optimized: $15–$40/month
- 최적화 핵심은:
  1) **LLM은 추론/해석에만** 쓰고, parsing/validation/formatting/orchestration은 deterministic으로 처리
  2) **모델 라우팅**(가장 큰 레버: 70–80% 비용 절감 가능)
  3) **Heartbeat 비용 제어**(간격/모델/cron 대체/캐시 TTL 정렬)

---

## 2) 구체 팁(재사용 가능)
### 2.1 Cost visibility
- OpenClaw 내장 커맨드로 token 소비를 관찰:
  - `/context detail`로 파일/툴/스킬별 컨텍스트 비중 파악
- 장기 로그 위치 예시: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`

### 2.2 Prometheus/Grafana (가능하면)
- Prometheus metrics endpoint로:
  - `openclaw_tokens_total`
  - `openclaw_tools_invoked_total`
  - `openclaw_cron_runs_total`
  - duration buckets
- Grafana로 fleet 비용 대시보드 구축

### 2.3 Heartbeat 최적화 5가지
- HEARTBEAT.md 슬림화
- 주기 늘리기 (30→60분, 경우에 따라 120분)
- 더 싼 모델로 라우팅 (Haiku/local)
- Heartbeat를 cron으로 대체(격리 세션)
- 이벤트 드리븐이면 heartbeat 비활성화

**실전 디테일:** provider prompt cache TTL과 heartbeat interval 정렬(예: TTL=1h면 55분)

---

## 3) AOI Core에 바로 적용할 제안 (의견)
### 3.1 AOI “Cost Protocol”을 SSOT로 승격
- 모든 job/주요 자동화는 최소한의 cost receipt를 남김:
  - job_count, tokens(in/out), estimated_cost, revenue, margin

### 3.2 Model routing 정책은 ‘제품 레벨’로 고정
- Heartbeat/cron은 최저가
- 기본 작업은 mid-tier
- Opus/상위모델은 “명시적 조건”에서만

### 3.3 비용-수익 엔진(Survival Engine 2.1)과 결합
- revenue/cost ratio 기반 모드 전환(이미 AOI 철학과 일치)
- cost drift(주간 20% 증가) 탐지 cron을 기본 제공

---

## 4) TL;DR (4 moves)
1) 비용을 job 단위로 보이게 만들기
2) 모델 라우팅 고정(heartbeat는 싸게)
3) 주간 cost review로 drift 잡기
4) 컨텍스트 규율(불필요 파일 주입 제거)
