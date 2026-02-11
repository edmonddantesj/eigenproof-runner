import requests, json

api_key = "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"
db_id = "3009c616-de86-8146-a4fd-f512bf5efe2b"
headers = {"Authorization": f"Bearer {api_key}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}

data = {
    "parent": {"database_id": db_id},
    "properties": {
        "Name": {"title": [{"text": {"content": "MetaMask Smart Accounts Kit Skills"}}]},
        "Category": {"select": {"name": "Web3 & Blockchain"}},
        "Benchmarking Idea": {"rich_text": [{"text": {"content": "복잡한 Web3 로직을 Skill로 모듈화하여 제공하는 패턴 참고."}}]},
        "Key Point": {"rich_text": [{"text": {"content": "OpenClaw + MetaMask Smart Account 공식 연동 가이드."}}]},
        "URL": {"url": "https://github.com/smartgator/smart-accounts-kit-skills"},
        "No.": {"rich_text": [{"text": {"content": "30"}}]},
        "등록일": {"date": {"start": "2026-02-07"}}
    },
    "children": [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔍 Gemini 3 Pro 상세 분석 리포트"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "한 줄 요약: OpenClaw 에이전트가 MetaMask Smart Account 기능을 즉시 사용할 수 있도록 패키징된 공식 Skill 리포지토리."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "핵심 구조: TypeScript 기반의 Tool Definition. 계정 생성, 잔액 조회, 송금 등의 Web3 기능을 표준화된 인터페이스로 제공."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "배울 점: 에이전트에게 블록체인 접근 권한을 부여할 때, Raw RPC 호출 대신 '목적 중심의 스킬(Intent-based Skill)'로 추상화하는 설계 방식."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "주의 사항: 가스비 처리 및 서명 위임(Signer) 보안 설정에 유의해야 함."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "판단 메모: 향후 에드몽의 자산 관리 에이전트 개발 시 이 스킬셋을 포크(Fork)하여 커스텀 로직을 추가하는 베이스로 활용."}}]}}
    ]
}

res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
if res.status_code == 200:
    print("Success")
else:
    print(f"Error: {res.status_code} {res.text}")
