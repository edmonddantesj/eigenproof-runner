import requests
import json
from datetime import datetime

NOTION_TOKEN = "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"
DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

def query_database():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    payload = {
        "sorts": [{"property": "등록일", "direction": "descending"}], # Sort by date to find latest human entries
        "page_size": 100
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json().get("results", [])
    except:
        return []

def update_page_no(page_id, new_no):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    payload = {
        "properties": {
            "No.": { "rich_text": [{"text": {"content": str(new_no)}}] }
        }
    }
    res = requests.patch(url, json=payload, headers=headers)
    return res.status_code

if __name__ == "__main__":
    results = query_database()
    
    # 1. Existing numbers finding
    existing_nos = []
    for page in results:
        no_prop = page["properties"].get("No.", {}).get("rich_text", [])
        if no_prop:
            try:
                val = int(no_prop[0]["plain_text"])
                # Ignore the 1-7 we just added wrongly
                name = page["properties"]["Name"]["title"][0]["plain_text"]
                if val < 10 and ("Whale" in name or "2026 Skills" in name or "Flywheel" in name):
                    continue
                existing_nos.append(val)
            except:
                pass
    
    start_no = max(existing_nos) + 1 if existing_nos else 1
    print(f"Starting from No.{start_no}")

    # 2. Re-insert or Update our 7 insights with correct numbering
    insights = [
        "Polymarket Whale Autopsy Guide",
        "The Only AI Skills that Matter in 2026",
        "10 AI Agents Printing Money in 2026",
        "Emotional Weather Algorithm: Agent Bio-Rhythm",
        "$6 Survival Challenge Action Plan",
        "Aoineco & Co. Autonomous Growth Flywheel",
        "Hackathon Hunting Roadmap: Beyond Solana"
    ]
    
    updated_count = 0
    for page in results:
        name_prop = page["properties"]["Name"]["title"]
        if name_prop:
            name = name_prop[0]["plain_text"]
            if name in insights:
                idx = insights.index(name)
                new_num = start_no + idx
                status = update_page_no(page["id"], new_num)
                print(f"Updated '{name}' to No.{new_num}: {status}")
                updated_count += 1
    
    print(f"Total updated: {updated_count}")
