import os
import requests
import json

def insert_to_notion():
    token = os.environ.get("NOTION_API_KEY")
    database_id = "3009c616-de86-8146-a4fd-f512bf5efe2b"
    
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "No": {"number": 44},
            "Name": {"title": [{"text": {"content": "Clawshi - Prediction Market Intelligence with USDC Staking"}}]},
            "URL": {"url": "https://github.com/clawshiai/openclaw-skills"},
            "Category": {"select": {"name": "Trade & Signal"}},
            "Key Point": {"rich_text": [{"text": {"content": "Moltbook community sentiment analysis + Polymarket & USDC staking skill."}}]},
            "Benchmarking Idea": {"rich_text": [{"text": {"content": "Applying 'Collective Intelligence Oracle' by scraping agent chatter on Moltbook to filter noise in BTC predictions."}}]}
        }
    }
    
    res = requests.post(url, headers=headers, data=json.dumps(data))
    if res.status_code == 200:
        print("✅ Successfully registered Clawshi to Notion!")
    else:
        print(f"❌ Failed to register: {res.text}")

if __name__ == "__main__":
    insert_to_notion()
