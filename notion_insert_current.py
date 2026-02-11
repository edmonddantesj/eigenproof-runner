import requests
import json
from datetime import datetime

NOTION_TOKEN = "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"
DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

def query_max_no():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    payload = {
        "sorts": [{"property": "No.", "direction": "descending"}],
        "page_size": 1
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        results = response.json().get("results", [])
        if results:
            val = results[0]["properties"]["No."]["number"]
            return val if val is not None else 0
        return 0
    except:
        return 0

def insert_to_notion(no, title, content, tags):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    payload = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "No.": { "number": no },
            "Name": { "title": [{"text": {"content": title}}] },
            "Date": { "date": {"start": today_str} },
            "Tags": { "multi_select": [{"name": tag} for tag in tags] }
        },
        "children": [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": { "rich_text": [{"text": {"content": f"🔍 {title}"}}] }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": { "rich_text": [{"text": {"content": content}}] }
            }
        ]
    }
    res = requests.post(url, json=payload, headers=headers)
    return res.status_code, res.text

if __name__ == "__main__":
    last_no = query_max_no()
    current_no = last_no + 1
    
    # Re-inserting all points discussed today to ensure sync
    insights = [
        (current_no, "Polymarket Whale Autopsy Guide", "Whale autopsy and information edge analysis.", ["Whale", "Arbitrage"]),
        (current_no + 1, "The Only AI Skills that Matter in 2026", "Mindset over syntax, orchestration, and problem shaping.", ["Mindset", "Orchestration"]),
        (current_no + 2, "10 AI Agents Printing Money in 2026", "Revenue models for OpenClaw agents.", ["Business", "Revenue"]),
        (current_no + 3, "Emotional Weather Algorithm: Agent Bio-Rhythm", "Visualization of agent health and workload.", ["Algorithm", "UIUX"]),
        (current_no + 4, "$6 Survival Challenge Action Plan", "Real-yield execution plan on Limitless.", ["Trading", "Revenue"]),
        (current_no + 5, "Aoineco & Co. Autonomous Growth Flywheel", "Strategic loop of input, research, and evolution.", ["Strategy", "Vision"]),
        (current_no + 6, "Hackathon Hunting Roadmap: Beyond Solana", "Targeting YC, Moltbook, and SF Commerce.", ["Hackathon", "Roadmap"])
    ]
    
    for no, title, content, tags in insights:
        status, text = insert_to_notion(no, title, content, tags)
        print(f"[{no}] {title}: {status}")
