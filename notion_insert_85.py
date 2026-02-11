import requests
import json
from datetime import datetime

NOTION_TOKEN = "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"
DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

def insert_to_notion():
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    today_str = datetime.now().strftime("%Y-%m-%d")
    title = "ERC-8004: Onchain AI Agent Identity Standard"
    summary = "AI 에이전트의 온체인 신원 확인 및 평판 관리를 위한 새로운 ERC-721 기반 표준(Identity Registry)."
    key_points = "Agent Identity NFTs, Reputation Layer, Verification via Metadata, Agentic Payments Infrastructure."
    observation = "Aoineco 요원들을 ERC-8004 표준에 등록하여 '신뢰할 수 있는 에이전트' 브랜딩 선점 가능. 특히 SF Agentic Commerce 해커톤에서 에이전트 간 자율 결제의 신뢰 기반으로 강력하게 어필할 수 있는 핵심 기술 요소임."

    payload = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "No.": { "rich_text": [{"text": {"content": "85"}}] },
            "Name": { "title": [{"text": {"content": title}}] },
            "등록일": { "date": {"start": today_str} },
            "Category": { "select": {"name": "Architecture/Security"} },
            "Benchmarking Idea": { "rich_text": [{"text": {"content": observation}}] }
        }
    }
    res = requests.post(url, json=payload, headers=headers)
    page_id = res.json().get("id")
    
    if page_id:
        # Append inner content
        blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        blocks_payload = {
            "children": [
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": { "rich_text": [{"text": {"content": "🔍 Gemini 3 Pro 상세 분석 리포트"}}] }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": { "rich_text": [{"text": {"content": f"한 줄 요약: {summary}", "link": None}, "annotations": {"bold": True}}] }
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": { "rich_text": [{"text": {"content": "핵심 구성 요소"}}] }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": { "rich_text": [{"text": {"content": key_points}}] }
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": { "rich_text": [{"text": {"content": "판단 메모"}}] }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": { "rich_text": [{"text": {"content": observation}}] }
                }
            ]
        }
        requests.post(blocks_url, json=blocks_payload, headers=headers)
        return True
    return False

if __name__ == "__main__":
    if insert_to_notion():
        print("✅ No.85 Synced Successfully")
    else:
        print("❌ Sync Failed")
