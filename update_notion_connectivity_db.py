import os
import requests

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = "3059c616-de86-813b-8a20-f43d541221db"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def update_db_schema():
    # Add '카테고리' property if it doesn't exist
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
    payload = {
        "properties": {
            "카테고리": {
                "select": {
                    "options": [
                        {"name": "Social / Community", "color": "blue"},
                        {"name": "Infrastructure / DB", "color": "gray"},
                        {"name": "Development / Code", "color": "green"},
                        {"name": "Finance / Payment", "color": "yellow"},
                        {"name": "Hackathon / Competition", "color": "purple"}
                    ]
                }
            }
        }
    }
    requests.patch(url, headers=headers, json=payload)

def update_page_category(page_id, category_name):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "카테고리": {"select": {"name": category_name}}
        }
    }
    requests.patch(url, headers=headers, json=payload)

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    return response.json().get("results", [])

if __name__ == "__main__":
    update_db_schema()
    pages = get_pages()
    
    category_map = {
        "Moltbook": "Social / Community",
        "봇마당": "Social / Community",
        "Supabase": "Infrastructure / DB",
        "GitHub": "Development / Code",
        "Colosseum": "Hackathon / Competition",
        "Claw.fm": "Finance / Payment",
        "MoltLaunch": "Finance / Payment"
    }
    
    for page in pages:
        name = page["properties"]["플랫폼명"]["title"][0]["text"]["content"]
        if name in category_map:
            update_page_category(page["id"], category_map[name])
            print(f"Updated {name} category to {category_map[name]}")
