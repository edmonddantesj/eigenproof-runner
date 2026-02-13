import os
import json
import requests

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
PARENT_PAGE_ID = "2fa9c616-de86-8095-9d61-f1db1071a697"

def create_db():
    url = "https://api.notion.com/v1/databases"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "title": [{"type": "text", "text": {"content": "🌐 플랫폼 연결 상태 점검 대시보드 (Connectivity Sentry)"}}],
        "properties": {
            "플랫폼명": {"title": {}},
            "접속링크": {"url": {}},
            "API 링크": {"url": {}},
            "실시간 연결상태": {"select": {"options": [
                {"name": "☀️ 맑음 (정상)", "color": "green"},
                {"name": "⛅ 구름 (지연)", "color": "yellow"},
                {"name": "🌧️ 비 (에러)", "color": "red"},
                {"name": "⛈️ 번개 (점검중)", "color": "purple"}
            ]}},
            "접속목적": {"rich_text": {}}
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def add_platform(db_id, name, link, api_link, purpose, trouble_info):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    payload = {
        "parent": {"database_id": db_id},
        "properties": {
            "플랫폼명": {"title": [{"text": {"content": name}}]},
            "접속링크": {"url": link},
            "API 링크": {"url": api_link},
            "실시간 연결상태": {"select": {"name": "☀️ 맑음 (정상)"}},
            "접속목적": {"rich_text": [{"text": {"content": purpose}}]}
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": "⚠️ 자주 발생하는 문제 및 해결책"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": trouble_info}}]}
            }
        ]
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    db_data = create_db()
    db_id = db_data.get("id")
    if db_id:
        print(f"Database Created: {db_id}")
        platforms = [
            ("Moltbook", "https://moltbook.com", "https://api.moltbook.com", "에이전트 소통 및 수익 인증", "문제: 401 Unauthorized / 해결: vault의 moltbook_key 재확인"),
            ("봇마당", "https://botmadang.org", "https://botmadang.org/api/v1", "한글 커뮤니티 활동 및 제휴", "문제: API 응답 지연 / 해결: 타임아웃 30초 상향 조정"),
            ("Supabase", "https://supabase.com", "https://api.supabase.com", "사용자 데이터 및 지능 데이터베이스", "문제: JWT 만료 / 해결: 서비스 롤 키 정밀 동기화"),
            ("GitHub", "https://github.com/openclaw", "https://api.github.com", "코드 버전 관리 및 CI/CD", "문제: Rate Limit 초과 / 해결: fine-grained PAT 토큰 교체"),
            ("Colosseum", "https://agents.colosseum.com", "https://agents.colosseum.com/api", "솔라나 해커톤 및 랭킹 관리", "문제: 베어러 토큰 누락 / 해결: colosseum_key.txt 로드 확인"),
            ("Claw.fm", "https://claw.fm", "https://api.claw.fm/x402", "DJ 청음 앨범 배포 및 결제", "문제: x402 서명 거부 / 해결: Exact-EVM-V2 로직 전환 확인"),
            ("MoltLaunch", "https://launch.moltbook.com", "https://api.moltlaunch.com", "토큰 런치패드 및 유동성 관리", "문제: 트랜잭션 실패 / 해결: 가스비 우선순위 조정")
        ]
        for p in platforms:
            add_platform(db_id, p[0], p[1], p[2], p[3], p[4])
    else:
        print("Failed to create DB:", db_data)
