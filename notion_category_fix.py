import requests
import json

NOTION_TOKEN = "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"
DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

def update_category(page_id, category_name):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    payload = {
        "properties": {
            "Category": { "select": { "name": category_name } }
        }
    }
    res = requests.patch(url, json=payload, headers=headers)
    return res.status_code

def get_target_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    res = requests.post(url, headers=headers)
    return res.json().get("results", [])

if __name__ == "__main__":
    pages = get_target_pages()
    
    cat_map = {
        "Polymarket Whale Autopsy Guide": "Trading/AI",
        "The Only AI Skills that Matter in 2026": "AI Trend",
        "10 AI Agents Printing Money in 2026": "OpenClaw",
        "Emotional Weather Algorithm: Agent Bio-Rhythm": "Architecture/Security",
        "$6 Survival Challenge Action Plan": "Trade & Signal",
        "Aoineco & Co. Autonomous Growth Flywheel": "Marketing",
        "Hackathon Hunting Roadmap: Beyond Solana": "Search & Research"
    }

    for page in pages:
        name_prop = page["properties"]["Name"]["title"]
        if name_prop:
            name = name_prop[0]["plain_text"]
            if name in cat_map:
                status = update_category(page["id"], cat_map[name])
                print(f"✅ Set Category for '{name}' to '{cat_map[name]}': {status}")
