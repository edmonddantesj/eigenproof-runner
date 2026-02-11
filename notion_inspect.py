import requests
import json

NOTION_TOKEN = "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"
DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28"
}
res = requests.get(url, headers=headers)
print(json.dumps(res.json(), indent=2, ensure_ascii=False))
