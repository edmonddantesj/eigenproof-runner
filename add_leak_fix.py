import requests, json

api_key = "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"
db_id = "3009c616-de86-8146-a4fd-f512bf5efe2b"
headers = {"Authorization": f"Bearer {api_key}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}

data = {
    "parent": {"database_id": db_id},
    "properties": {
        "Name": {"title": [{"text": {"content": "OpenClaw Output Leak & Log Separation Fix"}}]},
        "Category": {"select": {"name": "Architecture/Security"}},
        "Benchmarking Idea": {"rich_text": [{"text": {"content": "로그 누출 방지를 위한 출력 파이프라인 분리 및 쉘 스크립팅 안전화 가이드."}}]},
        "Key Point": {"rich_text": [{"text": {"content": "운영 로그(stderr)와 사용자 메시지 스트림의 엄격한 분리 및 Thinking 필터링."}}]},
        "URL": {"url": "https://docs.openclaw.ai/security/logging"},
        "No.": {"rich_text": [{"text": {"content": "32"}}]},
        "등록일": {"date": {"start": "2026-02-07"}}
    },
    "children": [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "🔍 Gemini 3 Pro 상세 분석 리포트"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "한 줄 요약: OpenClaw의 툴 실행 로그 및 모델 내부 사고(Thinking)가 사용자 채널로 유출되는 원인 분석과 아키텍처적 해결 방안."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "핵심 구조: 출력 파이프라인 분리(Log File vs User Stream) 및 Provider 레이어에서의 Thinking/Debug 필터링 적용."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "배울 점: 복잡한 쉘 커맨드 실행 시 Quoting 오류를 방지하기 위해 Heredoc(python3 - <<'PY') 패턴을 표준으로 사용해야 함."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "주의 사항: 툴 실패 시 Raw 에러 로그를 그대로 노출하지 말고, 요약된 에러 메시지와 함께 로그 파일 경로만 안내해야 함."}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "판단 메모: 향후 에이전트 개발 시 사용자 UX와 보안을 위해 이 '출력 분리 원칙'을 설계 단계부터 적용."}}]}}
    ]
}

res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
if res.status_code == 200:
    print("Leak Fix added.")
else:
    print(f"Error: {res.status_code} {res.text}")
