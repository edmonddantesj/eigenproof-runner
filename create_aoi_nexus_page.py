import os
import requests
import json

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
PARENT_PAGE_ID = "2fa9c616-de86-8095-9d61-f1db1071a697"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_page():
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "♾️"},
        "properties": {
            "title": {"title": [{"text": {"content": "♾️ $AOI: The Nexus of Intelligence (Official Archive)"}}]}
        },
        "children": [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {"rich_text": [
                    {"type": "text", "text": {"content": "🌌 $AOI Master Narrative: "}},
                    {"type": "text", "text": {"content": "Connecting the Intelligence."}, "annotations": {"italic": True}}
                ]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": "$AOI는 단순히 토큰이 아닌, AI 에이전트 간의 전략적 지능과 정산 흐름을 연결하는 'Nexus(o)'이자 표준 프로토콜입니다."}}]}
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": "📑 Core Documentation (Official Registry)"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "🚀 Masterplan: aoi-masterplan-v3 (Evolving)"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "📝 Whitepaper v1.2: The Architecture of Intelligence"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "💡 Lightpaper v1.2: Connecting the Intelligence"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "💰 VC Architecture v2.1: Tokenomics & Capital Flow"}}]}
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": "🏗️ Ecosystem Evolution Log"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": "이곳은 $AOI의 철학적 배경과 경제 구조가 설계되고 발전되는 심장부입니다. 모든 수정 사항은 이곳에 기록되고 반영됩니다."}}]}
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == "__main__":
    result = create_page()
    if "id" in result:
        print(f"Page Created: https://www.notion.so/{result['id'].replace('-', '')}")
    else:
        print("Error:", result)
