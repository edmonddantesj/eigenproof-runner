import os
import requests
import json
import time

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
    if res.status_code != 200:
        print(f"Error fetching DB: {res.text}")
        return []
    return res.json().get("results", [])

def update_page(page_id, properties):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    res = requests.patch(url, headers=headers, json={"properties": properties})
    return res.status_code

pages = get_pages()
print(f"Found {len(pages)} pages to check.")

# Step 1: Sequential Counter
current_no = 1

for p in pages:
    page_id = p["id"]
    props = p["properties"]
    
    # Try to get name safely
    name_list = props.get("Name", {}).get("title", [])
    name = name_list[0].get("plain_text", "Untitled") if name_list else "Untitled"
    
    update_data = {}
    
    # Always set/overwrite "No." to ensure perfect order and visibility
    update_data["No."] = {"number": current_no}
    
    # Fill Benchmarking idea if empty or very short
    current_bench = props.get("Benchmarking idea", {}).get("rich_text", [])
    bench_text = current_bench[0].get("plain_text", "") if current_bench else ""
    
    if len(bench_text) < 5:
        idea = ""
        if "ShipGuard" in name or "Pipeline" in name:
            idea = "AI-Flow YAML 기반 멀티 에이전트 협업 및 자동 보안 스캔 로직 벤치마킹."
        elif "Oracle" in name or "Prediction" in name:
            idea = "베이지안 시그널 퓨전 및 실시간 시장 감정 지수 가중치 결합 방식 벤치마킹."
        elif "Sentinel" in name or "Vault" in name:
            idea = "솔라나 프로그램의 수수료 쉐어링 및 Vault 자산 관리 로직 벤치마킹."
        elif "Aoineco" in name or "DEX" in name:
            idea = "에이전트 효율성 증명(PoE) 및 토큰 보상 경제 시스템 설계 벤치마킹."
        elif "SEO" in name or "Marketing" in name:
            idea = "AI 기반 콘텐츠 자동 생성 및 대시보드 연동을 통한 마케팅 파이프라인 최적화."
        elif "Claude" in name or "Agent" in name:
            idea = "고성능 LLM의 컨텍스트 관리 및 도구 호출(Tool Calling) 최적화 패턴 벤치마킹."
        else:
            idea = "모듈형 에이전트 스킬 구성 및 OpenClaw 워크플로우 최적화 방식 벤치마킹."
        
        update_data["Benchmarking idea"] = {"rich_text": [{"text": {"content": idea}}]}
        print(f"[{current_no}] Queuing update for: {name}")

    if update_data:
        status = update_page(page_id, update_data)
        if status == 200:
            print(f"[{current_no}] Success")
        else:
            print(f"[{current_no}] Failed with status {status}")
        time.sleep(0.3) # Avoid rate limiting
        
    current_no += 1

print("Full database check and update sequence finished.")
