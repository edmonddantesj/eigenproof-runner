import requests
import json
from datetime import datetime

NOTION_TOKEN = "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"
DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

def insert_to_notion(no, title, content, tags):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Correcting property names based on inspect result:
    # Name (title), No. (rich_text!), 등록일 (date), Key Point (rich_text)
    payload = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "No.": { "rich_text": [{"text": {"content": str(no)}}] },
            "Name": { "title": [{"text": {"content": title}}] },
            "등록일": { "date": {"start": today_str} },
            "Key Point": { "rich_text": [{"text": {"content": content[:2000]}}] }
        }
    }
    res = requests.post(url, json=payload, headers=headers)
    return res.status_code, res.text

if __name__ == "__main__":
    insights = [
        (1, "Polymarket Whale Autopsy Guide", "Whale autopsy and information edge analysis.", ["Whale", "Arbitrage"]),
        (2, "The Only AI Skills that Matter in 2026", "Mindset over syntax, orchestration, and problem shaping.", ["Mindset", "Orchestration"]),
        (3, "10 AI Agents Printing Money in 2026", "Revenue models for OpenClaw agents.", ["Business", "Revenue"]),
        (4, "Emotional Weather Algorithm: Agent Bio-Rhythm", "Visualization of agent health and workload.", ["Algorithm", "UIUX"]),
        (5, "$6 Survival Challenge Action Plan", "Real-yield execution plan on Limitless.", ["Trading", "Revenue"]),
        (6, "Aoineco & Co. Autonomous Growth Flywheel", "Strategic loop of input, research, and evolution.", ["Strategy", "Vision"]),
        (7, "Hackathon Hunting Roadmap: Beyond Solana", "Targeting YC, Moltbook, and SF Commerce.", ["Hackathon", "Roadmap"])
    ]
    
    for no, title, content, tags in insights:
        status, text = insert_to_notion(no, title, content, tags)
        print(f"[{no}] {title}: {status}")
