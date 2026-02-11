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

updates = {
    "clawify": {
        "Category": "AI Infra & Skills",
        "Benchmarking Idea": "OpenClaw 에이전트 설정 자동화 및 템플릿 배포 워크플로우 벤치마킹.",
        "Key Point": "에이전트 스쿼드 구축 시 openclaw.json 수동 설정 최소화 및 배포 동기화 안정성 확보.",
        "No.": "23"
    },
    "Mission Control Guide": {
        "Category": "AI Social & Agents",
        "Benchmarking Idea": "10인 에이전트 협업 체계(Staggered Cron) 및 공유 뇌(Shared Brain) 구축 기법.",
        "Key Point": "멀티 에이전트 세션 독립성 확보 및 효율적 리소스 관리(비용 절감) 전략.",
        "No.": "24"
    },
    "ClawSearch.io": {
        "Category": "AI Infra & Skills",
        "Benchmarking Idea": "AI 에이전트 네이티브 검색 엔진(MCP 호환) 도입 및 본문 검색 고도화.",
        "Key Point": "No Snippets, Full Content 제공으로 에이전트 브라우징 비용 절감 및 신뢰도 점수 기반 검색.",
        "No.": "25"
    }
}

for page in results:
    props = page.get("properties", {})
    name_list = props.get("Name", {}).get("title", [])
    if not name_list: continue
    name = name_list[0].get("plain_text")
    
    if name in updates:
        data = updates[name]
        patch_url = f"https://api.notion.com/v1/pages/{page['id']}"
        payload = {
            "properties": {
                "Category": {"select": {"name": data["Category"]}},
                "Benchmarking Idea": {"rich_text": [{"text": {"content": data["Benchmarking Idea"]}}]},
                "Key Point": {"rich_text": [{"text": {"content": data["Key Point"]}}]},
                "No.": {"rich_text": [{"text": {"content": data["No."]}}]},
                "등록일": {"date": {"start": "2026-02-07"}}
            }
        }
        r = requests.patch(patch_url, headers=headers, json=payload)
        print(f"Update {name}: {r.status_code}")

