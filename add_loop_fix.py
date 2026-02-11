import requests, json

api_key = "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"
db_id = "3009c616-de86-8146-a4fd-f512bf5efe2b"
headers = {"Authorization": f"Bearer {api_key}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}

data = {
    "parent": {"database_id": db_id},
    "properties": {
        "Name": {"title": [{"text": {"content": "OpenClaw Gateway Restart Loop Fix"}}]},
        "Category": {"select": {"name": "Architecture/Security"}},
        "Benchmarking Idea": {"rich_text": [{"text": {"content": "게이트웨이 무한 재시작 현상의 원인 분석 및 환경 변수 기반 해결책."}}]},
        "Key Point": {"rich_text": [{"text": {"content": "OPENCLAW_DISABLE_RELOAD=1 설정으로 Self-triggering Loop 차단."}}]},
        "URL": {"url": "https://docs.openclaw.ai/troubleshooting"},
        "No.": {"rich_text": [{"text": {"content": "31"}}]},
        "등록일": {"date": {"start": "2026-02-07"}}
    },
    "children": [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔍 Gemini 3 Pro 상세 분석 리포트"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "한 줄 요약: OpenClaw Gateway가 자신의 런타임 상태 변경(lastTouchedAt 등)을 설정 변경으로 오인하여 무한 재시작하는 버그와 해결법."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "핵심 구조: LaunchAgent 환경 변수에 OPENCLAW_DISABLE_RELOAD=1 및 DISABLE_CONFIG_WATCH=1 추가."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "배울 점: Watcher 로직 구현 시 '정적 설정'과 '동적 상태' 파일 경로를 명확히 분리해야 루프를 방지할 수 있음."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "주의 사항: 이 설정을 적용하면 openclaw.json을 수정해도 자동 재시작되지 않으므로, 설정 변경 시 수동으로 재시작(launchctl kickstart)해야 함."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "판단 메모: 향후 안정적인 24/7 운영을 위해 이 환경 변수 설정을 기본값으로 유지."}}]}}
    ]
}

res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
if res.status_code == 200:
    print("Loop Fix added.")
else:
    print(f"Error: {res.status_code} {res.text}")
