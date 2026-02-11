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
    title = "Profitable Meteora DLMM Strategy: Low-Risk Yield Farming"
    summary = "메테오라(Meteora) DLMM을 활용하여 솔라나 기반 밈코인 풀에서 수수료 수익을 극대화하는 저위험 단기 유동성 공급 전략."
    key_points = "1. Pool Filtering (700k+ MC, $1200+ Fee), 2. Single-sided SOL Deposit, 3. Bid Ask Curve Selection, 4. Range Setting (5-10% below resistance)."
    observation = "Alpha Oracle V6의 솔라나 온체인 수익 창출 로직으로 즉시 도입 가능. 특히 'Bid Ask' 커브와 단방향 SOL 예치 로직은 $6 생존 챌린지에서 안정적인 시드 확보와 수수료 수익을 동시에 노릴 수 있는 실전 전술임."

    payload = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "No.": { "rich_text": [{"text": {"content": "88"}}] },
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
        print("✅ No.88 Synced Successfully")
    else:
        print("❌ Sync Failed")
