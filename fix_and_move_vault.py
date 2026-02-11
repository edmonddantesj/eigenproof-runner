import os
import requests
import json

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
PARENT_PAGE_ID = "2fa9c616de8680959d61f1db1071a697"
# This is the existing DB ID that I suspected was created
DATABASE_ID = "3009c616de8681289cf2d5b6103328ce" 

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_db_under_parent():
    url = "https://api.notion.com/v1/databases"
    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "title": [{"type": "text", "text": {"content": "💡 Aoineco & Co. Idea Vault"}}],
        "properties": {
            "Name": {"title": {}},
            "제안자": {"rich_text": {}},
            "상태": {"select": {"options": [
                {"name": "진행 중", "color": "blue"},
                {"name": "보류", "color": "orange"},
                {"name": "폐기", "color": "red"}
            ]}},
            "우선순위": {"select": {"options": [
                {"name": "High", "color": "red"},
                {"name": "Medium", "color": "yellow"},
                {"name": "Low", "color": "gray"}
            ]}},
            "핵심 내용": {"rich_text": {}},
            "맥락": {"rich_text": {}}
        }
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.json()

def add_entries(db_id):
    ideas = [
        {"name": "AI DEX & Tokenized Soul Economy ()", "proposer": "Edmond", "status": "진행 중", "priority": "High", "content": "LLM 토큰 절감률에 따른 보상 및 AI 전용 DEX 구축.", "context": "PoE 시스템 도입."},
        {"name": "ShipGuard: AI Release Guardian", "proposer": "Blue-Gear", "status": "진행 중", "priority": "Medium", "content": "GitLab CI/CD 무결점 배포 시스템.", "context": "deployed."},
        {"name": "V6 Sentiment Bias Fusion", "proposer": "Blue-Eye", "status": "진행 중", "priority": "High", "content": "지표 + 감정 융합 예측.", "context": "Working on it."},
        {"name": "Blue_Sound Aoi-Fi Artist", "proposer": "Blue_Sound", "status": "보류", "priority": "Low", "content": "온체인 데이터 음악화.", "context": "Demo phase."},
        {"name": "Cybertruck Price Model", "proposer": "Edmond", "status": "보류", "priority": "Medium", "content": "사이버트럭 전략 모델.", "context": "Data collection."}
    ]
    for idea in ideas:
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {"database_id": db_id},
            "properties": {
                "Name": {"title": [{"text": {"content": idea["name"]}}]},
                "제안자": {"rich_text": [{"text": {"content": idea["proposer"]}}]},
                "상태": {"select": {"name": idea["status"]}},
                "우선순위": {"select": {"name": idea["priority"]}},
                "핵심 내용": {"rich_text": [{"text": {"content": idea["content"]}}]},
                "맥락": {"rich_text": [{"text": {"content": idea["context"]}}]}
            }
        }
        requests.post(url, headers=headers, json=payload)

print("Creating Idea Vault under the correct parent page...")
new_db = create_db_under_parent()
if "id" in new_db:
    new_id = new_db["id"].replace("-", "")
    print(f"Success! New DB ID: {new_id}")
    add_entries(new_id)
else:
    print("Failed to create DB:", new_db)

