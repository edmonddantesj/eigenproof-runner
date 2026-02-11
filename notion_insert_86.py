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
    title = "Where Polymarket Still Misprices Reality: Event-Driven Strategies"
    summary = "폴리마켓과 같은 예측 시장에서 '가격 예측'이 아닌 '결과 값 산정(Pricing Outcomes)'에 집중하는 이벤트 기반 트레이딩 시스템 구축 가이드."
    key_points = "Event-Driven Trading, Bayesian Updating, Market-Implied Probability, Fractional Kelly Sizing, Classification Models."
    observation = "Alpha Oracle V6의 핵심 엔진 로직으로 즉시 편입 가능. 특히 '베이지안 업데이트'를 통한 실시간 확률 재산정 로직과 시장 임플라이드 확률과의 괴리율을 이용한 진입 타점 설정은 우리 시스템의 수익성을 극대화할 핵심 병기임."

    payload = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "No.": { "rich_text": [{"text": {"content": "86"}}] },
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
        print("✅ No.86 Synced Successfully")
    else:
        print("❌ Sync Failed")
