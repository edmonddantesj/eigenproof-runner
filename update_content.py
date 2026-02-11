import requests
import json

api_key = "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"
db_id = "3009c616de868146a4fdf512bf5efe2b"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 1. 대상 페이지 ID들 가져오기
query_url = f"https://api.notion.com/v1/databases/{db_id}/query"
res = requests.post(query_url, headers=headers, json={"page_size": 50})
results = res.json().get("results", [])

reports = {
    "clawify": {
        "url": "https://github.com/scotthconner/clawify",
        "content": [
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "📊 Gemini 3 Pro 상세 분석 리포트"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• TL;DR: OpenClaw 에이전트 설정 및 배포 자동화 도구"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• 분석: JSON 설정 파일 수동 편집 오류 차단 및 템플릿 기반 에이전트 생성"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• 인사이트: 신규 에이전트 스쿼드 구축 시 필수 도구로 채택 권장"}}]}}
        ]
    },
    "Mission Control Guide": {
        "url": "https://www.notion.so/3009c616de868146a4fdf512bf5efe2b",
        "content": [
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "📊 Gemini 3 Pro 상세 분석 리포트"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• TL;DR: 10인 AI 에이전트 팀 협업 아키텍처 가이드"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• 분석: Staggered Cron 및 공유 DB를 통한 완벽한 문맥 공유 체계"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• 인사이트: Narratr/FDS 프로젝트 스쿼드 확장의 표준 모델로 활용"}}]}}
        ]
    },
    "ClawSearch.io": {
        "url": "https://clawsearch.io",
        "content": [
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "📊 Gemini 3 Pro 상세 분석 리포트"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• TL;DR: AI 에이전트 전용 MCP 호환 검색 엔진"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• 분석: 스니펫이 아닌 본문 전체 제공으로 브라우징 토큰 혁신적 절감"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "• 인사이트: 검색 스킬에 API 통합하여 실시간 정보력 업그레이드"}}]}}
        ]
    }
}

for page in results:
    props = page.get("properties", {})
    name_list = props.get("Name", {}).get("title", [])
    if not name_list: continue
    name = name_list[0].get("plain_text")
    
    if name in reports:
        data = reports[name]
        # URL 및 속성 업데이트
        patch_url = f"https://api.notion.com/v1/pages/{page['id']}"
        requests.patch(patch_url, headers=headers, json={"properties": {"URL": {"url": data["url"]}}})
        
        # 본문 내용 추가 (Append Blocks)
        content_url = f"https://api.notion.com/v1/blocks/{page['id']}/children"
        r = requests.patch(content_url, headers=headers, json={"children": data["content"]})
        print(f"Content Update {name}: {r.status_code}")

