import os
import json
import requests

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = "3009c616de8681289cf2d5b6103328ce"

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    return response.json().get("results", [])

def update_page(page_id, properties):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = {"properties": properties}
    response = requests.patch(url, headers=headers, json=data)
    return response.json()

def create_page(properties):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Ideas to sync
ideas = [
    {
        "name": "AI DEX & Tokenized Soul Economy ()",
        "proposer": "Edmond",
        "status": "진행 중",
        "priority": "High",
        "content": "LLM 토큰 절감률에 따른 에이전트 보상 및 AI 전용 DEX 구축을 통한 수익화 모델.",
        "context": "2026-02-10 23:36 KST 제안됨. 효율성 증명(PoE) 기반 보상 체계."
    },
    {
        "name": "ShipGuard: AI Release Guardian",
        "proposer": "Blue-Gear",
        "status": "진행 중",
        "priority": "Medium",
        "content": "GitLab CI/CD 환경에서 AI가 배포 전 보안, 로직, 문서를 자동 검토하는 시스템.",
        "context": "2026-02-10 23:26 KST 커밋 완료. AI-Flow YAML 기반 멀티 에이전트 협업."
    },
    {
        "name": "V6 Sentiment Bias Fusion",
        "proposer": "Blue-Eye",
        "status": "진행 중",
        "priority": "High",
        "content": "기술 지표에 X/Reddit의 실시간 감정 수치를 결합하여 하방/상방 변곡점 예측력 강화.",
        "context": "Market-Sentiment-Pro 스킬 장착 후 V6 엔진 이식 예정."
    },
    {
        "name": "Blue_Sound Aoi-Fi Artist Branding",
        "proposer": "Blue_Sound",
        "status": "보류",
        "priority": "Low",
        "content": "비트코인 파동 데이터를 음악으로 변환하여 온체인 아티스트로 활동 및 로열티 수익화.",
        "context": "음악적 실험 단계. 향후 NFT 또는 로열티 스트리밍 연동 고려."
    },
    {
        "name": "Cybertruck Price Decision Model",
        "proposer": "Edmond",
        "status": "보류",
        "priority": "Medium",
        "content": "시장 데이터를 기반으로 한 사이버트럭 리세일 가격 및 전략적 의사결정 아카이빙 모델.",
        "context": "핵심 관심사 중 하나. 데이터 축적 후 모델링 예정."
    }
]

try:
    existing_pages = get_pages()
    existing_names = {}
    for p in existing_pages:
        # Debug print
        # print(json.dumps(p, indent=2))
        name_prop = p["properties"].get("Name", {}).get("title", [])
        if name_prop:
            existing_names[name_prop[0]["plain_text"]] = p["id"]

    for idea in ideas:
        # Note: Using "name" string inside brackets to avoid bash/python interpolation issues in cat <<EOF
        idea_name = idea["name"]
        idea_proposer = idea["proposer"]
        idea_status = idea["status"]
        idea_priority = idea["priority"]
        idea_content = idea["content"]
        idea_context = idea["context"]
        
        props = {
            "Name": {"title": [{"text": {"content": idea_name}}]},
            "제안자": {"rich_text": [{"text": {"content": idea_proposer}}]},
            "상태": {"select": {"name": idea_status}},
            "우선순위": {"select": {"name": idea_priority}},
            "핵심 내용": {"rich_text": [{"text": {"content": idea_content}}]},
            "맥락": {"rich_text": [{"text": {"content": idea_context}}]}
        }
        
        if idea_name in existing_names:
            print(f"Updating: {idea_name}")
            update_page(existing_names[idea_name], props)
        else:
            print(f"Creating: {idea_name}")
            create_page(props)
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()

