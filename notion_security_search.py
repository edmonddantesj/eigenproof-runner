import requests
import json

NOTION_TOKEN = "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"
DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

def search_security():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    # Search for "Security" or "Wallet" in any rich_text or title
    payload = {
        "filter": {
            "or": [
                { "property": "Name", "title": { "contains": "Security" } },
                { "property": "Name", "title": { "contains": "Wallet" } },
                { "property": "Name", "title": { "contains": "보안" } },
                { "property": "Name", "title": { "contains": "지갑" } },
                { "property": "Benchmarking Idea", "rich_text": { "contains": "보안" } }
            ]
        }
    }
    res = requests.post(url, json=payload, headers=headers)
    results = res.json().get("results", [])
    
    findings = []
    for page in results:
        props = page.get("properties", {})
        no = props.get("No.", {}).get("rich_text", [{}])[0].get("plain_text", "N/A")
        name = props.get("Name", {}).get("title", [{}])[0].get("plain_text", "Untitled")
        idea = props.get("Benchmarking Idea", {}).get("rich_text", [{}])[0].get("plain_text", "")
        findings.append(f"No.{no}: {name}\n- Idea: {idea}")
    
    return findings

if __name__ == "__main__":
    findings = search_security()
    if findings:
        print("\n".join(findings))
    else:
        print("No specific security insights found in Notion.")
