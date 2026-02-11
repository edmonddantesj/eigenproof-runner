import requests
import json

NOTION_API_KEY = "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"
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

def add_100x_engineer_report():
    # 1. Create Page
    payload = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "Name": { "title": [{ "text": { "content": "How to be a 100x Engineer using AI (Orchestration)" } }] },
            "Category": { "select": { "name": "AI Social & Agents" } },
            "Key Point": { "rich_text": [{ "text": { "content": "AI를 '코드 작성기'가 아닌 '시스템 설계 및 오케스트레이션' 도구로 활용" } }] },
            "Benchmarking Idea": { "rich_text": [{ "text": { "content": "5계층 스택(IDE-Terminal-Background-Chat-Review) 및 MCP 기반 신경망 구축" } }] },
            "No.": { "rich_text": [{ "text": { "content": "47" } }] },
            "등록일": { "date": { "start": "2026-02-09" } }
        }
    }
    
    res = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if res.status_code != 200:
        print(f"Error creating page: {res.text}")
        return
    
    page_id = res.json()["id"]
    
    # 2. Add Content (Mandatory Format)
    content_payload = {
        "children": [
            {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "🔍 Gemini 3 Pro 상세 분석 리포트"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "**한 줄 요약:** 2026년형 100x 엔지니어는 단순 코드 생성을 넘어, 병렬 에이전트와 MCP를 통해 복잡한 시스템을 지휘(Orchestrate)하는 아키텍트라는 통찰."}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "**핵심 구조:** AI-first IDE, Terminal Agent, Background Agents, General Chat, AI Code Review Tools 등 5단계 레이어 스택과 이를 연결하는 MCP(신경망)."}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "**배울 점:** 'Direct -> Dissect -> Delegate' 루프. 인간은 아키텍처와 검증에 집중하고, 에이전트들은 병렬 탭에서 각기 다른 태스크(기능 구현, 테스트, 리팩토링 등)를 수행하게 만드는 지휘 기법."}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "**주의 사항:** 에이전트에 코드 소유권을 무분별하게 넘기는 '환각의 늪' 경계. 반드시 인간 주도의 Verify 레이어와 관측성(Observability) 확보 필수."}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "**판단 메모:** Aoineco & Co.의 5인방 스쿼드가 바로 이 100x 엔지니어의 'Background Agents' 역할을 수행함. 특히 '청비(Archivist)' 에이전트가 MCP를 통해 Notion/GitHub을 연결하는 신경망 중심축으로 작동하도록 설계 보강."}}]}}
        ]
    }
    
    res_cont = requests.patch(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=HEADERS, json=content_payload)
    if res_cont.status_code == 200:
        print("✅ 100x Engineer Report successfully added to Notion!")
    else:
        print(f"Error adding content: {res_cont.text}")

if __name__ == "__main__":
    add_100x_engineer_report()
