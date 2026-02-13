import os
import requests

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
PARENT_PAGE_ID = "3059c616de8681879c51ca4a6b3eb8cb"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_sub_page(title, content):
    url = "https://api.notion.com/v1/pages"
    paragraphs = content.split('\n')
    children = []
    for p in paragraphs[:80]:
        if p.strip():
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": p[:2000]}}]}
            })

    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "properties": {
            "title": {"title": [{"text": {"content": title}}]}
        },
        "children": children
    }
    return requests.post(url, headers=headers, json=payload).json()

if __name__ == "__main__":
    files = [
        ("🌌 Masterplan v2.0", "strategy/aoi-masterplan-v2.md"),
        ("💰 VC Architecture & Tokenomics v2.1", "strategy/AOI_Tokenomics_v2.1_VC_Structure.md")
    ]
    for title, path in files:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                result = create_sub_page(title, content)
                if "id" in result:
                    print(f"Synced {title} to Notion.")
                else:
                    print(f"Error syncing {title}: {result}")
