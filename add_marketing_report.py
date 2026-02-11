import requests
import json

NOTION_API_KEY = "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"
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

def add_marketing_report():
    # 1. Create Page
    payload = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "Name": { "title": [{ "text": { "content": "My Marketing Co-Founder Is an AI Agent (SaaS Squad)" } }] },
            "Category": { "select": { "name": "AI Social & Agents" } },
            "Key Point": { "rich_text": [{ "text": { "content": "OpenClaw 기반 전문 에이전트 스쿼드 및 Notion 기반 파이프라인 구축" } }] },
            "Benchmarking Idea": { "rich_text": [{ "text": { "content": "Claim Locking을 통한 경쟁 조건 해결 및 PM 에이전트를 통한 자율 루프 복업" } }] },
            "No.": { "rich_text": [{ "text": { "content": "46" } }] },
            "등록일": { "date": { "start": "2026-02-09" } }
        }
    }
    
    res = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if res.status_code != 200:
        print(f"Error creating page: {res.text}")
        return
    
    page_id = res.json()["id"]
    
    # 2. Add Content
    content_payload = {
        "children": [
            {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "🔍 Gemini 3 Pro 상세 분석 리포트"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "**한 줄 요약:** OpenClaw 에이전트 스쿼드(Scout, Quill, Sage 등)를 통해 10일 만에 80개 이상의 전문 콘텐츠를 생성/배포하는 자율 마켓팅 시스템 구축 사례."}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "**핵심 구조:** 모든 에이전트가 공유 Notion DB를 상태 머신으로 활용하여 협업. Morgan(PM) 에이전트가 전체 병목을 감시하고 하위 에이전트를 자동 소환(Spawn)함."}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "**배울 점:** 범용 봇 대신 전문화된 에이전트(Specialization) 구성. 'Claim Locking' 기술로 병렬 작업 시 중복을 방지하고 'Sage'를 통해 90점 이상의 엄격한 품질 게이트(Quality Gate) 구축."}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "**주의 사항:** 에이전트의 환각(Hallucination) 방지를 위한 'PRODUCT_CONTEXT.md' 필수 로드 및 Notion API의 비트랜잭션 특성에 따른 동기화 이슈 유의."}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "**판단 메모:** Alpha Oracle V4의 Moltbook 활동 및 기술 블로그 자동화를 위해 'Quill(작성)-Sage(검증)-Herald(배포)' 구조를 벤치마킹하여 우리 팀의 자율 홍보 모듈에 적용."}}]}}
        ]
    }
    
    res_cont = requests.patch(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=HEADERS, json=content_payload)
    if res_cont.status_code == 200:
        print("✅ Marketing Report successfully added to Notion!")
    else:
        print(f"Error adding content: {res_cont.text}")

if __name__ == "__main__":
    add_marketing_report()
