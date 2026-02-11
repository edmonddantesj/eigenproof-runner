import requests
import json

NOTION_API_KEY = "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"
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

TASKS = [
    {
        "id": "3029c616-de86-817c-b663-f9035112b95c",
        "name": "VoxYZ AI 자율 운영 체제 가이드",
        "summary": "4개 테이블 기반 Closed Loop 아키텍처 가이드.",
        "structure": "ops_mission_proposals, ops_missions, ops_mission_steps, ops_agent_events 테이블 연동.",
        "lessons": "단일 제안 통로와 쿼터 관리를 통한 에이전트 자율성 통제.",
        "caution": "순환 루프 무한 반복 방지를 위한 탈출 조건 필수.",
        "decision": "Alpha Oracle V4 엔진의 핵심 운영 로직으로 채택."
    },
    {
        "id": "3029c616-de86-813c-b4c6-de88f01a4527",
        "name": "AI Adoption Journey: From Chatbot to Agent",
        "summary": "단순 챗봇을 버리고 실행 능력을 갖춘 에이전트 체제로의 전환 과정.",
        "structure": "End-of-Day Agent 리서치 및 아침 Warm Start 환경 조성.",
        "lessons": "에이전트에게 검증 도구(Harness)를 제공하여 실수를 스스로 교정하게 함.",
        "caution": "너무 복잡한 작업은 계획(Planning)과 실행(Execution) 세션을 분리할 것.",
        "decision": "퇴근 전 에이전트 리서치 업무 예약 기능을 Alpha Oracle에 추가 예정."
    },
    {
        "id": "3029c616-de86-8147-b6bb-c83f320d06a1",
        "name": "10 People Making $847k with AI Agents",
        "summary": "에이전트 자동화 스킬 판매를 통한 실제 수익 창출 사례 분석.",
        "structure": "웹 스크래핑, 이메일 카피라이팅 등 특정 목적 중심의 스킬 마켓플레이스.",
        "lessons": "범용 봇보다 특정 문제를 해결하는 'Micro-Skill'의 가치가 더 높음.",
        "caution": "에이전트 간의 비밀 통신(E2E) 요구 등 보안 프라이버시 이슈 발생 중.",
        "decision": "Alpha Oracle의 예측 시장 분석 루프를 OpenClaw 표준 스킬로 패키징 제안."
    },
    {
        "id": "3029c616-de86-813d-aec5-e229e06674e5",
        "name": "Claude Code Guide for Designers (Vibe Coding)",
        "summary": "비개발자가 기획안만으로 주말 사이 실물 서비스를 배포하는 프로세스.",
        "structure": "FigJam 순서도 -> Figma MCP -> Claude Code 연동 루프.",
        "lessons": "구문(Syntax)이 아닌 결과물(Vibe)에 집중하는 개발 방식의 효용성.",
        "caution": "에이전트의 데스크톱 알림을 꺼서 인간의 심층 사고 몰입을 방해하지 말 것.",
        "decision": "Alpha Oracle의 대시보드 UI 개발 시 Figma MCP와 Claude Code 연동 방식 채택."
    },
    {
        "id": "3029c616-de86-81d7-916f-ddfcf7a5d1af",
        "name": "The Cloud Agent Thesis (nader dabit)",
        "summary": "로컬 Copilot을 넘어 네트워크 기반의 Cloud Teammate로의 에이전트 진화.",
        "structure": "원격 인프라, 비동기 업무, 팀 전체가 접근 가능한 Entry Point.",
        "lessons": "코드 작성보다 '코드 리뷰'가 병목이 되므로 리뷰 에이전트 상주 필수.",
        "caution": "개별 개발 환경이 아닌 조직 전체 인프라로서의 보안 거버넌스 필요.",
        "decision": "Mac mini 로컬 환경을 넘어 Moltbook 네트워크 접점의 Teammate로 청묘의 정체성 설정."
    },
    {
        "id": "3009c616-de86-8130-bd8e-cccfb7b244c1",
        "name": "10 Claude Code Prompts You Need to Steal",
        "summary": "Claude Code의 성능을 극대화하는 10가지 표준 프롬프트 기법.",
        "structure": "기능 구현, 테스트 작성, 리팩토링 등 시나리오별 명령 체계.",
        "lessons": "에이전트에게 명확한 '역할'과 '종료 조건'을 명시할 때 최선의 결과 도출.",
        "caution": "프롬프트 주입(Injection) 및 불필요한 토큰 낭비 방지를 위한 가이드라인 준수.",
        "decision": "내부 코딩 루틴 및 Critic 에이전트 검증 프롬프트 최적화에 즉시 적용."
    },
    {
        "id": "3019c616-de86-812f-b6d1-d267d84ae0d1",
        "name": "Agent-based Game Development Case Study",
        "summary": "에이전트 팀이 협업하여 복잡한 게임(Tetris 등)을 원샷으로 개발한 사례.",
        "structure": "기획봇, 아트봇, 코드봇의 순차적/병렬적 협업 파이프라인.",
        "lessons": "인간의 수동 개입을 최소화한 에이전트 간 핸드오프(Hand-off) 설계.",
        "caution": "에이전트 간의 사소한 명세 불일치가 전체 빌드 실패로 이어질 위험.",
        "decision": "Solana Sentinel 대시보드 개발 시 '디자인-코드' 자동 핸드오프 로직 벤치마킹."
    },
    {
        "id": "3019c616-de86-8196-a7aa-e59995fcc738",
        "name": "Building a C Compiler with Team of parallel Claudes",
        "summary": "고도의 논리력이 필요한 작업을 병렬 클로드 에이전트 팀으로 해결한 분석.",
        "structure": "작업 쪼개기(Sharding) 및 중간 결과 검증 에이전트 배치.",
        "lessons": "어려운 과제를 하나 큰 모델에 맡기기보다 여러 모델의 병렬 검증이 유리함.",
        "caution": "병렬 세션 간의 상태 동기화 및 결합(Integration) 난이도 증대.",
        "decision": "Alpha Oracle V3의 예측 정확도 향상을 위해 3인방 에이전트의 병렬 논박 루프 강화."
    },
    {
        "id": "3019c616-de86-8143-a28a-d80d24b4bb00",
        "name": "Recursive Self-Improvement Loop for Marketing",
        "summary": "컨텐츠 생성과 분석 피드백을 무한 반복하여 성과를 높이는 자가 발전 모델.",
        "structure": "Draft -> Critic -> Edit -> Social Signal Analysis -> Loop.",
        "lessons": "외부 피드백(조회수 등)을 에이전트의 다음 행동 지침으로 자동 연결하는 루프.",
        "caution": "자의적 판단 강화에 따른 확증 편향 및 품질 저하 감시 체계 필요.",
        "decision": "Moltbook 활동 시 조회수/반응 데이터를 수집해 포스팅 전략을 수정하는 루틴 도입."
    }
]

def update_notion():
    for task in TASKS:
        page_id = task["id"]
        # Update Name Header inside (Heading 1) and contents
        content_payload = {
            "children": [
                {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "🔍 Gemini 3 Pro 상세 분석 리포트"}}]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"한 줄 요약: {task['summary']}"}}]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"핵심 구조: {task['structure']}"}}]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"배울 점: {task['lessons']}"}}]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"주의 사항: {task['caution']}"}}]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"판단 메모: {task['decision']}"}}]}}
            ]
        }
        
        # Clear existing children first (optional but cleaner)
        # requests.delete(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=HEADERS) # DELETE API might vary, better just append for now as it's fresh pages
        
        # Fix: PATCH children actually appends. To replace, we would need to delete. 
        # Since these are relatively fresh, I will just update the title and append the standard blocks.
        
        # Update Page Properties (Title)
        prop_payload = {
            "properties": {
                "Name": {"title": [{"text": {"content": task["name"]}}]}
            }
        }
        res_prop = requests.patch(f"https://api.notion.com/v1/pages/{page_id}", headers=HEADERS, json=prop_payload)
        res_cont = requests.patch(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=HEADERS, json=content_payload)
        
        if res_prop.status_code == 200 and res_cont.status_code == 200:
            print(f"✅ Success: {task['name']}")
        else:
            print(f"❌ Failed: {task['name']} - {res_prop.text} / {res_cont.text}")

if __name__ == "__main__":
    update_notion()
