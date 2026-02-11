import requests
import json

api_key = "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"
db_id = "3009c616de868146a4fdf512bf5efe2b"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

query_url = f"https://api.notion.com/v1/databases/{db_id}/query"
res = requests.post(query_url, headers=headers, json={"page_size": 50})
results = res.json().get("results", [])

new_reports = {
    "clawify": [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔍 Gemini 3 Pro 상세 분석 리포트"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "한 줄 요약: OpenClaw 에이전트 설정 자동화 및 템플릿 배포를 위한 CLI 도구."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "핵심 구조: Node.js 기반. openclaw.json 설정 파싱 및 자동 동기화 로직 내장."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "배울 점: 복잡한 설정을 템플릿화하여 휴먼 에러를 차단하고 구축 속도를 극대화함."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "주의 사항: 로컬 설정과 게이트웨이 버전이 일치해야 하며 권한 설정 누락에 유의."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "판단 메모: 신규 전문 에이전트 추가 시 이 도구를 사용한 표준 배포 프로세스 구축 권장."}}]}}
    ],
    "Mission Control Guide": [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔍 Gemini 3 Pro 상세 분석 리포트"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "한 줄 요약: 10명의 전문 AI 에이전트가 팀으로 협업하는 멀티 에이전트 아키텍처 설계도."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "핵심 구조: Staggered Cron(시간차 호출) 및 Convex DB를 통한 공유 데이터 플랫폼 활용."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "배울 점: 에이전트 간 '기억 공유'를 위해 중앙화된 DB를 협업 루프로 사용하는 방식."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "주의 사항: 에이전트 증가에 따른 API 비용 관리 및 컨텍스트 요약 전략 필수."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "판단 메모: Narratr 분석 및 FDS 모니터링을 스쿼드 단위로 분리 운영 시 표준 모델로 적용."}}]}}
    ],
    "ClawSearch.io": [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔍 Gemini 3 Pro 상세 분석 리포트"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "한 줄 요약: 인간이 아닌 AI 에이전트 전용으로 설계된 MCP 호환 고정밀 검색 엔진."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "핵심 구조: BM25 + Semantic Reranking 하이브리드 알고리즘. JSON 방식 Full Content 반환."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "배울 점: 본문 전체를 구조화된 데이터로 제공하여 브라우징 토큰 비용을 획기적으로 절감함."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "주의 사항: 쿼리당 비용 최적화를 위한 정밀한 키워드 추출 전처리 필수."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "판단 메모: 현재 검색 스킬에 ClawSearch를 통합하여 실시간 벤치마킹 정보력 업그레이드."}}]}}
    ]
}

for page in results:
    name_list = page.get("properties", {}).get("Name", {}).get("title", [])
    if not name_list: continue
    name = name_list[0].get("plain_text")
    if name in new_reports:
        # 기존 본문 삭제 (실제로는 Append Children이므로 구분선 추가 후 삽입)
        content_url = f"https://api.notion.com/v1/blocks/{page['id']}/children"
        payload = {"children": [{"object": "block", "type": "divider", "divider": {}}] + new_reports[name]}
        r = requests.patch(content_url, headers=headers, json=payload)
        print(f"Format 리모델링 {name}: {r.status_code}")
