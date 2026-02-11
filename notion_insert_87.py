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
    title = "Building Algorithmic Traders with Claude Code: 5-Step Workflow"
    summary = "Claude Code를 활용하여 알고리즘 트레이딩 봇을 구축하는 5단계 표준 프로세스 가이드."
    key_points = "1. Strategy & Backtest, 2. Execution Logic, 3. Deploy & Monitor, 4. Optimize & Refine, 5. Performance Report."
    observation = "Alpha Oracle V6와 $6 생존 챌린지의 개발 및 운영 표준 가이드라인으로 채택. 특히 Claude Code를 활용한 백테스팅 코드 생성과 클라우드 배포(Step 3), 그리고 자동 성과 보고서 생성(Step 5) 로직을 우리 시스템에 그대로 이식할 것."

    payload = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "No.": { "rich_text": [{"text": {"content": "87"}}] },
            "Name": { "title": [{"text": {"content": title}}] },
            "등록일": { "date": {"start": today_str} },
            "Category": { "select": {"name": "Trade & Signal"} },
            "Benchmarking Idea": { "rich_text": [{"text": {"content": observation}}] }
        }
    }
    res = requests.post(url, json=payload, headers=headers)
    page_id = res.json().get("id")
    
    if page_id:
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
        print("✅ No.87 Synced Successfully")
    else:
        print("❌ Sync Failed")
