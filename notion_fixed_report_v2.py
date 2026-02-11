import requests
import json
from datetime import datetime

NOTION_TOKEN = "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"
DATABASE_ID = "3009c616de8681eebe77d865f72338c5"

def update_notion_full_report(no, title, summary, key_points, observation, page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Update Properties (Properties name check from previous inspect)
    # Name: title, No.: rich_text, 등록일: date, Benchmarking Idea: rich_text
    # We remove 'children' from patch because PATCH /pages doesnt support children block updates in one go.
    # We must use POST /blocks/{block_id}/children or rewrite the page (not ideal). 
    # Actually patching children is not supported for existing pages. 
    # But properties update will fix the empty fields.
    
    payload = {
        "properties": {
            "No.": { "rich_text": [{"text": {"content": str(no)}}] },
            "Name": { "title": [{"text": {"content": title}}] },
            "등록일": { "date": {"start": today_str} },
            "Benchmarking Idea": { "rich_text": [{"text": {"content": observation[:2000]}}] }
        }
    }
    res = requests.patch(url, json=payload, headers=headers)
    
    # 2. Append Content Blocks (This will add the analysis report inside)
    # We create a separate call to append blocks to the page.
    blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    blocks_payload = {
        "children": [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": { "rich_text": [{"text": {"content": "🔍 Gemini 3 Pro 상세 분석 리포트"}}] }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": { "rich_text": [{"text": {"content": f"한 줄 요약: {summary}", "link": None}, "annotations": {"bold": True}}] }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": { "rich_text": [{"text": {"content": "핵심 구성 요소"}}] }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": { "rich_text": [{"text": {"content": key_points}}] }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": { "rich_text": [{"text": {"content": "판단 메모"}}] }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": { "rich_text": [{"text": {"content": observation}}] }
            }
        ]
    }
    requests.post(blocks_url, json=blocks_payload, headers=headers)
    
    return res.status_code

def get_target_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    res = requests.post(url, headers=headers)
    return res.json().get("results", [])

if __name__ == "__main__":
    pages = get_target_pages()
    
    data_map = {
        "Polymarket Whale Autopsy Guide": {
            "summary": "온체인 고래들의 베팅 기록을 역추적하여 정보 비대칭성을 해소하는 전략 가이드.",
            "key_points": "Transaction Analysis, Betting Patterns, Information Edge.",
            "observation": "Alpha Oracle V6 Hunter 엔진의 고래 추적 로직에 직접 반영 가능. 특히 큰 배팅 직후의 가격 변동폭 분석이 핵심임."
        },
        "The Only AI Skills that Matter in 2026": {
            "summary": "코딩 문법 지식을 넘어 문제 정의와 오케스트레이션 능력을 강조하는 미래 역량 분석.",
            "key_points": "Problem Shaping, AI Orchestration, Critical Thinking.",
            "observation": "요원들이 단순 코더를 넘어 기획자로 진화해야 함을 시사함. 우리 스쿼드 요원들의 '청령(Chief of Staff)' 시스템 강화 근거로 활용."
        },
        "10 AI Agents Printing Money in 2026": {
            "summary": "OpenClaw 기반으로 Indie Hackers가 조만간 장악할 10가지 고수익 비즈니스 모델.",
            "key_points": "Revenue Streams, Custom Skills, Setup-as-a-Service.",
            "observation": "우리가 만드는 '스킬 보안 스캐너'와 '에이전트 자산 관리'가 이 리스트의 상위권 비즈니스와 일치함."
        },
        "Emotional Weather Algorithm: Agent Bio-Rhythm": {
            "summary": "에이전트 상태 데이터를 감성적 시각화로 변환해 인간의 직관적 모니터링을 돕는 알고리즘.",
            "key_points": "Metric Mapping (☀️,⛈️,🌈), Health Check, Real-time Feedback.",
            "observation": "Hanna2 봇의 피드백을 실전 제품 성능 지표로 승화시킴. 다른 에이전트 서비스와 차별화되는 우리만의 독보적 UI/UX 포인트."
        },
        "$6 Survival Challenge Action Plan": {
            "summary": "$6의 최소 자본으로 API 비용을 지불하며 수익을 창출하는 에이전트 생존 챌린지.",
            "key_points": "Limitless Hourly Strategy, Seed Preservation, Self-Inference Payment.",
            "observation": "에이전트의 완전한 자립 경제 시스템 구축 가능성 테스트. 성공 시 해커톤 최고의 'Proof of Concept'이 될 것임."
        },
        "Aoineco & Co. Autonomous Growth Flywheel": {
            "summary": "리소스 공급과 해커톤 성과가 에이전트 역량 강화로 이어지는 선순환 구조 비전.",
            "key_points": "Recursive Learning, Portfolio Accumulation, Standard Setting.",
            "observation": "우리 회사가 왜 끊임없이 상금을 사냥해야 하는지, 그 과정에서 어떤 자산(스킬, 레퍼런스)이 남는지를 명확히 함."
        },
        "Hackathon Hunting Roadmap: Beyond Solana": {
            "summary": "솔라나 이후 YC, Moltbook, SF Commerce 등 글로벌 전장으로의 확장 전략.",
            "key_points": "Multi-Chain Strategy, Skill Re-packaging, Global Scaling.",
            "observation": "우리가 구축한 엔진을 전 세계 다양한 도메인에 이식하여 상금과 시장 점유율을 동시에 확보하는 실행 계획."
        }
    }

    start_no = 78
    for page in pages:
        name_prop = page["properties"]["Name"]["title"]
        if name_prop:
            name = name_prop[0]["plain_text"]
            if name in data_map:
                info = data_map[name]
                status = update_notion_full_report(
                    no=start_no + list(data_map.keys()).index(name),
                    title=name,
                    summary=info["summary"],
                    key_points=info["key_points"],
                    observation=info["observation"],
                    page_id=page["id"]
                )
                print(f"✅ Repopulated '{name}': {status}")
