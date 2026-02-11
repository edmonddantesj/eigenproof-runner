import os
import json
import requests

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
PARENT_PAGE_ID = "2fa9c616de8680959d61f1db1071a697"

def get_block_children(block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    response = requests.get(url, headers=headers)
    return response.json()

print(f"Checking children of parent page: {PARENT_PAGE_ID}")
children = get_block_children(PARENT_PAGE_ID)
for block in children.get("results", []):
    block_type = block["type"]
    content = ""
    if block_type == "child_page":
        content = block["child_page"]["title"]
    elif block_type == "child_database":
        content = block["child_database"]["title"]
    elif block_type == "paragraph":
        # Simplified paragraph reading
        rich_text = block["paragraph"].get("rich_text", [])
        if rich_text:
            content = rich_text[0].get("plain_text", "")
            
    print(f"- Type: {block_type}, ID: {block[id]}, Content/Title: {content}")

