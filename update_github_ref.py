import os
import requests
import json

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    res = requests.post(url, headers=headers)
    return res.json().get("results", [])

def update_page(page_id, properties):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    res = requests.patch(url, headers=headers, json={"properties": properties})
    return res.json()

pages = get_pages()
# Find the highest No. to increment
max_no = 0
for p in pages:
    no_val = p["properties"].get("No.", {}).get("number", 0)
    if no_val and no_val > max_no:
        max_no = no_val

print(f"Current Max No.: {max_no}")

for p in pages:
    page_id = p["id"]
    props = p["properties"]
    name = props.get("Name", {}).get("title", [{}])[0].get("plain_text", "Unknown")
    
    update_props = {}
    
    # Fill "No." if empty
    if not props.get("No.", {}).get("number"):
        max_no += 1
        update_props["No."] = {"number": max_no}
        print(f"Filling No. {max_no} for {name}")

    # Fill "Benchmarking idea" if empty
    bench_prop = props.get("Benchmarking idea", {}).get("rich_text", [])
    if not bench_prop:
        # Context-aware benchmarking ideas based on name
        idea = ""
        if "ShipGuard" in name:
            idea = "AI-Flow YAML 기반 멀티 에이전트 협업 및 자동 보안 스캔 로직 벤치마킹."
        elif "Alpha Oracle" in name:
            idea = "베이지안 시그널 퓨전 및 실시간 시장 감정 지수 가중치 결합 방식 벤치마킹."
        elif "Sentinel" in name:
            idea = "솔라나 프로그램의 수수료 쉐어링 및 Vault 자산 관리 로직 벤치마킹."
        elif "Aoineco" in name:
            idea = "에이전트 효율성 증명(PoE) 및 토큰 보상 경제 시스템 설계 벤치마킹."
        else:
            idea = "모듈형 에이전트 스킬 구성 및 OpenClaw 워크플로우 최적화 방식 벤치마킹."
            
        update_props["Benchmarking idea"] = {"rich_text": [{"text": {"content": idea}}]}
        print(f"Filling Benchmarking idea for {name}")

    if update_props:
        update_page(page_id, update_props)

