import os
import requests
import json
from datetime import datetime

# Notion API Configuration
NOTION_TOKEN = "secret_6d4c38132f50094cac7d9178f33019a25d8f896adcecbc9b" # Using user's confirmed pattern
DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

def add_insight_to_notion(title, content, tags=[]):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Generate Date and Placeholder for No.
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    payload = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "Name": {
                "title": [
                    { "text": { "content": title } }
                ]
            },
            "Date": {
                "date": { "start": today_str }
            },
            "Tags": {
                "multi_select": [{"name": tag} for tag in tags]
            }
            # No. is usually an Auto-increment property in Notion DB, 
            # If it's a manual number field, we might need to query the max count first.
        },
        "children": [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{ "type": "text", "text": { "content": "🔍 Insight Report" } }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{ "type": "text", "text": { "content": content } }]
                }
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ Created: {title} on {today_str}")
            return response.json()
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

# Update MEMORY.md to reflect this new standard
