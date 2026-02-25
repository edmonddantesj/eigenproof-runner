# Triage Summary (10 lines) — AI Trading System Pipeline (doc570)

1) 문서는 “AI 트레이딩”을 챗봇 예측이 아니라 **파이프라인 시스템**으로 정의함.
2) 7단계: Data → Ideas → AI structuring → strategy code → backtest → paper trade → live.
3) 가장 중요한 기반은 Stage 1 데이터 수집(OHLCV/오더북/펀딩/온체인/매크로/센티/상관).
4) 설계 철학: **Garbage in, garbage out** — 데이터 품질이 상한을 결정.
5) 데이터는 멀티소스 수집 후 정규화/저장(Time-series DB) + 이상탐지/알림.
6) AI는 Stage 2에서 “예언”이 아니라 **가설 기반 트레이드 아이디어(근거/리스크/무효화 조건 포함)**를 구조화.
7) Stage 3에서 아이디어를 규칙/조건으로 형식화해 코드 생성 가능한 형태로 변환.
8) 백테스트(과거) → 페이퍼(실시간) → 라이브(실자금)로 단계적 검증.
9) 운영에 필요한 도구 예: CCXT, Glassnode/FRED, 센티 API, 스케줄러(cron/agent).
10) AOI 연결점: 우리가 만든 **Proof/Receipt/Queue/Circuit Breaker**는 Stage 6~7(실행) 안정화 레일로 바로 붙일 수 있음.

SSOT:
- Raw: `context/ingest/inbound_doc_570_2026-02-25.txt`
- Triage report: `context/ingest/INGEST_TRIAGE_REPORT_doc570_2026-02-25.md`
