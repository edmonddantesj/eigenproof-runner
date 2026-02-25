# Triage Report — doc569 (2026-02-25)

Source:
- `/Users/silkroadcat/.openclaw/media/inbound/file_569---79c0d753-d536-47be-b021-a992631b7095.docx`
- Extracted text: `context/ingest/inbound_doc_569_2026-02-25.txt`

## 1) Structure scan (headings / themes)
- “ACP Margin Playbook” — token 비용을 COGS로 보고 마진을 관리하자는 글
- Cost per job가 핵심 지표
- OpenClaw 비용 가시화(/context detail, 로그, Prometheus metrics)
- Model routing이 가장 큰 레버(70–80% 절감)
- Heartbeat 비용 줄이기(간격/모델/cron 대체, 캐시 TTL 정렬)
- 주간 cost review cron 제안

## 2) Value score (0–3)
- Score: **3 (critical / high leverage)**

## 3) Decision
- Escalate to **Full ingest**.

## 4) Why
- AOI Core의 Survival Engine / 비용-수익 엔진 / Dispatch 운영(heartbeat/cron)과 직접 연결.
