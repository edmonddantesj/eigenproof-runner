import requests
import json

NOTION_TOKEN = "secret_6d4c38132f50094cac7d9178f33019a25d8f896adcecbc9b"
DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

def query_database():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            print(f"Total entries found: {len(results)}")
            for i, page in enumerate(results[:5]):
                props = page.get("properties", {})
                name = props.get("Name", {}).get("title", [{}])[0].get("plain_text", "No Title")
                no = props.get("No.", {}).get("number", "N/A")
                date = props.get("Date", {}).get("date", {}).get("start", "N/A")
                print(f"[{i+1}] No.{no} | {date} | {name}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    query_database()
