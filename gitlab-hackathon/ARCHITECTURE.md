# 🏆 GitLab AI Hackathon - Aoineco & Co. 아키텍처 설계서

> **총상금:** $65,000 | **팀:** Aoineco & Co. | **설계일:** 2026-02-10

---

## 📋 목차
1. [해커톤 분석 & 전략](#해커톤-분석--전략)
2. [에이전트 컨셉 3가지](#에이전트-컨셉-3가지)
3. [최종 추천안: ShipGuard](#최종-추천안-shipguard)
4. [구현 로드맵 (1주 스프린트)](#구현-로드맵)
5. [상금 전략](#상금-전략)

---

## 해커톤 분석 & 전략

### 심사 기준 해부
| 기준 | 가중치 | 우승 전략 |
|------|--------|-----------|
| 기술 구현 | ★★★★★ | Flow YAML + Multi-agent + Trigger 3종 모두 활용 |
| 디자인/사용성 | ★★★★ | 원클릭 설치, 자동 트리거 (사용자 개입 최소화) |
| 잠재적 영향력 | ★★★★ | 모든 GitLab 팀이 겪는 보편적 고통 해결 |
| 아이디어 창의성 | ★★★★ | 기존에 없는 "AI Paradox" 병목 해결 |

### 핵심 플랫폼 역량 (우리가 반드시 써야 할 것)
- **Custom Agent**: 시스템 프롬프트 + Tools 조합으로 전문 에이전트 생성
- **Custom Flow (YAML v1)**: 멀티 에이전트 오케스트레이션, `ambient` 환경
- **Triggers**: `mention`, `assign`, `assign_reviewer` 3가지 이벤트 트리거
- **Agent Tools**: 50+ GitLab API 도구 (이슈, MR, 파이프라인, 보안스캔 등)
- **Environment Variables**: `AI_FLOW_CONTEXT`, `AI_FLOW_INPUT`, `AI_FLOW_EVENT`

### 추가 상금 타겟
| 카테고리 상 | 상금 | 전략 |
|------------|------|------|
| Anthropic 대상 | $10,000 | 기본 모델이 Anthropic → 자동 적격 |
| Google Cloud 대상 | $10,000 | GCP MCP 서버 연동 추가 |
| Green Agent | $3,000 | 파이프라인 에너지 효율 측정 모듈 포함 |

---

## 에이전트 컨셉 3가지

---

### 🛡️ 컨셉 A: **ShipGuard** — Release Readiness Guardian
> "배포 전 모든 것을 자동으로 점검하는 릴리즈 가디언"

#### 문제 정의 (Pain Point)
- MR이 merge되어도 배포 준비가 안 됨 (테스트 부족, 보안 취약점, 문서 미비, CHANGELOG 누락)
- 릴리즈 매니저가 수동으로 체크리스트를 돌리는 데 2-4시간 소요
- "AI가 코드는 빨리 짜는데, 배포까지의 병목은 여전하다" = **AI Paradox의 정수**

#### 솔루션
MR이 생성/업데이트되면 자동으로 5단계 릴리즈 준비도 점검을 수행하는 멀티 에이전트 플로우:

1. **🔍 Code Quality Agent** — 코드 품질/패턴 위반 검출
2. **🛡️ Security Agent** — 취약점 스캔 결과 분석 + 자동 이슈 생성
3. **📝 Documentation Agent** — API/README 변경사항 자동 반영 확인
4. **📋 Compliance Agent** — CHANGELOG, 라이선스, 컨벤션 준수 확인
5. **📊 Summary Agent** — 종합 릴리즈 준비도 리포트 (✅/⚠️/❌ 대시보드)

#### 기술 아키텍처
```yaml
version: "v1"
environment: ambient

components:
  - name: "code_quality_reviewer"
    type: AgentComponent
    prompt_id: "shipguard_quality"
    inputs: ["context:goal", "context:project_id"]
    toolset:
      - "get_merge_request"
      - "list_merge_request_diffs"
      - "get_repository_file"
      - "grep"
      - "find_files"
      - "create_merge_request_note"
    ui_log_events: ["on_agent_final_answer", "on_tool_execution_success"]

  - name: "security_analyzer"
    type: AgentComponent
    prompt_id: "shipguard_security"
    inputs:
      - from: "context:goal"
        as: "user_goal"
      - from: "context:project_id"
        as: "project_id"
      - from: "context:code_quality_reviewer.final_answer"
        as: "quality_findings"
    toolset:
      - "list_vulnerabilities"
      - "get_vulnerability_details"
      - "get_pipeline_failing_jobs"
      - "get_job_logs"
      - "create_vulnerability_issue"
      - "create_issue"
    ui_log_events: ["on_agent_final_answer"]

  - name: "documentation_checker"
    type: AgentComponent
    prompt_id: "shipguard_docs"
    inputs:
      - from: "context:goal"
        as: "user_goal"
      - from: "context:project_id"
        as: "project_id"
    toolset:
      - "list_merge_request_diffs"
      - "get_repository_file"
      - "find_files"
      - "grep"
      - "blob_search"
    ui_log_events: ["on_agent_final_answer"]

  - name: "compliance_checker"
    type: AgentComponent
    prompt_id: "shipguard_compliance"
    inputs:
      - from: "context:goal"
        as: "user_goal"
      - from: "context:project_id"
        as: "project_id"
    toolset:
      - "get_repository_file"
      - "list_merge_request_diffs"
      - "grep"
      - "list_commits"
      - "get_commit"
    ui_log_events: ["on_agent_final_answer"]

  - name: "release_summary"
    type: AgentComponent
    prompt_id: "shipguard_summary"
    inputs:
      - from: "context:goal"
        as: "user_goal"
      - from: "context:project_id"
        as: "project_id"
      - from: "context:code_quality_reviewer.final_answer"
        as: "quality_report"
      - from: "context:security_analyzer.final_answer"
        as: "security_report"
      - from: "context:documentation_checker.final_answer"
        as: "docs_report"
      - from: "context:compliance_checker.final_answer"
        as: "compliance_report"
    toolset:
      - "create_merge_request_note"
      - "create_issue_note"
      - "update_merge_request"
    ui_log_events: ["on_agent_final_answer"]

routers:
  - from: "code_quality_reviewer"
    to: "security_analyzer"
  - from: "security_analyzer"
    to: "documentation_checker"
  - from: "documentation_checker"
    to: "compliance_checker"
  - from: "compliance_checker"
    to: "release_summary"
  - from: "release_summary"
    to: "end"

flow:
  entry_point: "code_quality_reviewer"
```

#### Trigger 설정
- **mention**: `@shipguard check this MR`
- **assign_reviewer**: MR에 ShipGuard를 리뷰어로 지정 → 자동 실행
- **assign**: 이슈에 ShipGuard 할당 → 릴리즈 체크리스트 생성

#### 경쟁 우위
- 5개 에이전트의 오케스트레이션 → "기술 구현" 최고점
- 모든 팀이 겪는 릴리즈 병목 해결 → "잠재적 영향력" 최고점
- 리뷰어로 지정만 하면 끝 → "사용성" 최고점

---

### 🔄 컨셉 B: **PipelineHealer** — Self-Healing CI/CD Agent
> "실패한 파이프라인을 자동으로 진단하고 고치는 에이전트"

#### 문제 정의
- CI/CD 파이프라인 실패 시 로그 분석에 30분~2시간 소요
- Flaky test, dependency 충돌, 환경 설정 오류 등 반복적 실패
- 기존 "Fix Pipeline" 플로우는 1회성 → 패턴 학습/예방 없음

#### 솔루션
파이프라인 실패 시 자동 트리거되어 진단 → 수정 → 재실행하는 자가치유 플로우:

1. **🔬 Diagnostician Agent** — 실패 로그 분석 + 근본 원인 분류
2. **🔧 Fixer Agent** — 원인별 자동 수정 (config 패치, dependency 업데이트)
3. **🧪 Validator Agent** — 수정 후 dry-run 검증
4. **📈 Reporter Agent** — 실패 패턴 트렌드 리포트 + 예방 권고

#### 기술 아키텍처
```yaml
version: "v1"
environment: ambient

components:
  - name: "diagnostician"
    type: AgentComponent
    prompt_id: "healer_diagnose"
    inputs: ["context:goal", "context:project_id"]
    toolset:
      - "get_pipeline_errors"
      - "get_pipeline_failing_jobs"
      - "get_job_logs"
      - "get_merge_request"
      - "get_repository_file"
      - "grep"
    ui_log_events: ["on_agent_final_answer"]

  - name: "fixer"
    type: AgentComponent
    prompt_id: "healer_fix"
    inputs:
      - from: "context:goal"
        as: "user_goal"
      - from: "context:project_id"
        as: "project_id"
      - from: "context:diagnostician.final_answer"
        as: "diagnosis"
    toolset:
      - "get_repository_file"
      - "edit_file"
      - "create_file_with_contents"
      - "create_commit"
      - "create_merge_request"
      - "ci_linter"
    ui_log_events: ["on_agent_final_answer", "on_tool_execution_success"]

  - name: "validator"
    type: AgentComponent
    prompt_id: "healer_validate"
    inputs:
      - from: "context:project_id"
        as: "project_id"
      - from: "context:fixer.final_answer"
        as: "fix_result"
    toolset:
      - "ci_linter"
      - "get_repository_file"
      - "run_tests"
    ui_log_events: ["on_agent_final_answer"]

  - name: "reporter"
    type: AgentComponent
    prompt_id: "healer_report"
    inputs:
      - from: "context:goal"
        as: "user_goal"
      - from: "context:project_id"
        as: "project_id"
      - from: "context:diagnostician.final_answer"
        as: "diagnosis"
      - from: "context:fixer.final_answer"
        as: "fix_result"
      - from: "context:validator.final_answer"
        as: "validation_result"
    toolset:
      - "create_issue_note"
      - "create_merge_request_note"
      - "create_issue"
    ui_log_events: ["on_agent_final_answer"]

routers:
  - from: "diagnostician"
    to: "fixer"
  - from: "fixer"
    to: "validator"
  - from: "validator"
    to: "reporter"
  - from: "reporter"
    to: "end"

flow:
  entry_point: "diagnostician"
```

#### 경쟁 우위
- 기존 Fix Pipeline 확장 → GitLab이 좋아할 방향성
- Green Agent 상($3,000) 동시 타겟: 불필요한 재실행 방지 = 에너지 절약

---

### 🎯 컨셉 C: **IssueAlchemist** — Issue-to-Production Orchestrator
> "이슈 하나가 자동으로 구현, 테스트, 리뷰, 배포까지"

#### 문제 정의
- 이슈 → 브랜치 → 코드 → MR → 리뷰 → 머지의 전체 사이클이 수동
- 잘 정의된 이슈(버그 픽스, 단순 기능)도 개발자가 직접 모든 단계를 수행
- "AI Paradox": AI가 코드를 짜도 나머지 프로세스는 사람이 해야 함

#### 솔루션
이슈에 `@issue-alchemist`를 멘션하면 6단계 자동화 파이프라인 실행:

1. **📋 Planner Agent** — 이슈 분석 + 구현 계획 수립 + 태스크 분할
2. **💻 Developer Agent** — 코드 구현 + 파일 생성/수정 + 커밋
3. **🧪 Tester Agent** — 단위 테스트 자동 생성 + 실행
4. **🔍 Reviewer Agent** — 코드 리뷰 + 개선 사항 적용
5. **📝 Documenter Agent** — CHANGELOG + API 문서 업데이트
6. **🚀 Deployer Agent** — MR 생성 + 라벨링 + 머지 준비도 확인

#### 기술 아키텍처
```yaml
version: "v1"
environment: ambient

components:
  - name: "planner"
    type: AgentComponent
    prompt_id: "alchemist_plan"
    inputs: ["context:goal", "context:project_id"]
    toolset:
      - "get_issue"
      - "list_issues"
      - "get_repository_file"
      - "list_repository_tree"
      - "find_files"
      - "grep"
      - "create_issue_note"
    ui_log_events: ["on_agent_final_answer"]

  - name: "developer"
    type: AgentComponent
    prompt_id: "alchemist_develop"
    inputs:
      - from: "context:goal"
        as: "user_goal"
      - from: "context:project_id"
        as: "project_id"
      - from: "context:planner.final_answer"
        as: "implementation_plan"
    toolset:
      - "get_repository_file"
      - "list_repository_tree"
      - "find_files"
      - "create_file_with_contents"
      - "edit_file"
      - "run_git_command"
      - "create_commit"
    ui_log_events: ["on_agent_final_answer", "on_tool_execution_success"]

  - name: "tester"
    type: AgentComponent
    prompt_id: "alchemist_test"
    inputs:
      - from: "context:project_id"
        as: "project_id"
      - from: "context:developer.final_answer"
        as: "dev_output"
    toolset:
      - "get_repository_file"
      - "find_files"
      - "create_file_with_contents"
      - "run_tests"
      - "create_commit"
    ui_log_events: ["on_agent_final_answer"]

  - name: "reviewer"
    type: AgentComponent
    prompt_id: "alchemist_review"
    inputs:
      - from: "context:project_id"
        as: "project_id"
      - from: "context:developer.final_answer"
        as: "dev_output"
      - from: "context:tester.final_answer"
        as: "test_output"
    toolset:
      - "build_review_merge_request_context"
      - "get_repository_file"
      - "edit_file"
      - "create_commit"
    ui_log_events: ["on_agent_final_answer"]

  - name: "documenter"
    type: AgentComponent
    prompt_id: "alchemist_document"
    inputs:
      - from: "context:project_id"
        as: "project_id"
      - from: "context:developer.final_answer"
        as: "dev_output"
    toolset:
      - "get_repository_file"
      - "find_files"
      - "edit_file"
      - "create_file_with_contents"
      - "create_commit"
    ui_log_events: ["on_agent_final_answer"]

  - name: "deployer"
    type: AgentComponent
    prompt_id: "alchemist_deploy"
    inputs:
      - from: "context:goal"
        as: "user_goal"
      - from: "context:project_id"
        as: "project_id"
      - from: "context:planner.final_answer"
        as: "plan"
      - from: "context:reviewer.final_answer"
        as: "review_result"
      - from: "context:tester.final_answer"
        as: "test_result"
    toolset:
      - "create_merge_request"
      - "update_merge_request"
      - "create_issue_note"
      - "update_issue"
    ui_log_events: ["on_agent_final_answer"]

routers:
  - from: "planner"
    to: "developer"
  - from: "developer"
    to: "tester"
  - from: "tester"
    to: "reviewer"
  - from: "reviewer"
    to: "documenter"
  - from: "documenter"
    to: "deployer"
  - from: "deployer"
    to: "end"

flow:
  entry_point: "planner"
```

#### 경쟁 우위
- 6개 에이전트 → 가장 화려한 데모
- 하지만 기존 "Developer Flow"와 차별화 부족 위험

---

## 최종 추천안: ShipGuard 🛡️

### 왜 ShipGuard인가?

| 비교 항목 | ShipGuard | PipelineHealer | IssueAlchemist |
|-----------|-----------|----------------|----------------|
| 차별성 | ★★★★★ 릴리즈 가디언 없음 | ★★★ Fix Pipeline 확장 | ★★ Developer Flow 유사 |
| 구현 난이도 | ★★★ 중간 (안정적) | ★★★★ 높음 (런타임 필요) | ★★★★★ 매우 높음 |
| 데모 임팩트 | ★★★★★ 대시보드 + 결과 | ★★★★ Before/After | ★★★★ End-to-End |
| 영향력 | ★★★★★ 모든 팀 보편적 | ★★★★ DevOps 팀 한정 | ★★★★ 개발팀 한정 |
| 심사위원 어필 | ★★★★★ "AI Paradox" 정조준 | ★★★★ 기술적 인상적 | ★★★ 이미 존재하는 느낌 |
| 1주 내 완성 | ★★★★★ 가능 | ★★★ 위험 | ★★ 어려움 |

### ShipGuard가 최적인 이유

1. **"AI Paradox" 직격**: 해커톤이 명시적으로 원하는 "planning, security, compliance, deployments" 병목 해결
2. **독창성**: "릴리즈 준비도 자동 점검" 에이전트는 현존하지 않음
3. **멀티 에이전트 오케스트레이션**: 5개 에이전트 → 기술 인상도 극대화
4. **데모 스토리텔링**: "이 MR 배포해도 될까?" → 1분 후 종합 리포트 → 3분 데모 완벽
5. **추가 상금 적격**:
   - Anthropic ($10,000): 기본 모델 사용으로 자동 적격
   - Green Agent ($3,000): "불필요한 배포 롤백 방지 = 컴퓨팅 자원 절약" 스토리

---

## 구현 로드맵

### 1주 스프린트 (7일)

#### Day 1-2: 기반 구축
- [ ] GitLab AI Hackathon 그룹 접근 신청 & 프로젝트 생성
- [ ] 프로젝트 구조 설정 (README, LICENSE, .gitlab-ci.yml)
- [ ] Custom Agent 1개 생성: "ShipGuard Summary Agent" (가장 단순한 것부터)
  - System prompt 작성
  - Tools 선택: `get_merge_request`, `create_merge_request_note`
  - 테스트: MR에 멘션하여 기본 동작 확인
- [ ] Flow YAML 스켈레톤 작성 (1개 에이전트만으로 end-to-end 테스트)

#### Day 3-4: 멀티 에이전트 플로우 구축
- [ ] 5개 에이전트 시스템 프롬프트 작성
  - `shipguard_quality`: 코드 품질 전문가 프롬프트
  - `shipguard_security`: 보안 분석 전문가 프롬프트
  - `shipguard_docs`: 문서화 전문가 프롬프트
  - `shipguard_compliance`: 컴플라이언스 전문가 프롬프트
  - `shipguard_summary`: 종합 리포트 생성 프롬프트
- [ ] Flow YAML 완성: 5개 에이전트 순차 실행 + 라우팅
- [ ] Trigger 3종 설정: mention, assign, assign_reviewer
- [ ] 테스트 MR 생성하여 전체 플로우 실행 테스트

#### Day 5: 품질 & 부가 상
- [ ] 출력 포맷 최적화: 마크다운 대시보드 형식
  ```
  ## 🛡️ ShipGuard Release Readiness Report
  
  | Check | Status | Details |
  |-------|--------|---------|
  | Code Quality | ✅ Pass | No critical issues |
  | Security | ⚠️ Warning | 2 medium vulnerabilities |
  | Documentation | ❌ Fail | API docs not updated |
  | Compliance | ✅ Pass | CHANGELOG updated |
  
  **Overall: ⚠️ NOT READY — 1 blocker, 1 warning**
  ```
- [ ] Green Agent 모듈 추가: 파이프라인 실행 횟수 추적 + 에너지 절약 통계
- [ ] 에러 핸들링 강화 (빈 MR, 접근 권한 없음 등)

#### Day 6: 데모 & 문서
- [ ] 데모 시나리오 스크립트 작성 (3분):
  1. (0:00-0:30) 문제 소개: "릴리즈 전 수동 체크에 4시간 소요"
  2. (0:30-1:00) ShipGuard 설치/설정 (원클릭)
  3. (1:00-2:00) 라이브 데모: MR에 @shipguard 멘션 → 자동 실행
  4. (2:00-2:40) 결과: 종합 리포트 생성, 보안 이슈 자동 생성
  5. (2:40-3:00) 임팩트: "4시간 → 5분, 모든 MR에 일관된 품질"
- [ ] 데모 영상 녹화 (YouTube 업로드)
- [ ] README.md 최종 완성
- [ ] CONTRIBUTING.md 작성

#### Day 7: 제출
- [ ] Devpost 제출물 작성
  - 프로젝트 URL
  - 텍스트 설명
  - 데모 영상 링크
- [ ] 최종 코드 정리 + 라이선스 확인 (MIT)
- [ ] 제출!

---

## 상금 전략

### 타겟 상금 (현실적)
| 상 | 금액 | ShipGuard 적격도 |
|----|------|-----------------|
| Grand Prize | $15,000 | ★★★★★ AI Paradox 직격 |
| Most Technically Impressive | $5,000 | ★★★★★ 5-agent orchestration |
| Most Impactful | $5,000 | ★★★★★ 모든 팀 적용 가능 |
| Easiest to Use | $5,000 | ★★★★★ @멘션만 하면 끝 |
| GitLab & Anthropic Grand Prize | $10,000 | ★★★★★ 기본 모델 사용 |
| Green Agent | $3,000 | ★★★★ 불필요한 배포 방지 |

**최대 가능 상금: $43,000** (Grand + Anthropic + Green)

---

## 프로젝트 구조

```
shipguard/
├── README.md                          # 프로젝트 설명
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # 기여 가이드
├── .gitlab-ci.yml                     # CI/CD 파이프라인
├── .gitlab/
│   └── duo/
│       └── flows/
│           └── shipguard.yaml         # Main Flow 설정
├── docs/
│   ├── architecture.md                # 아키텍처 문서
│   ├── setup-guide.md                 # 설치 가이드
│   └── demo-script.md                # 데모 스크립트
├── agents/
│   ├── quality-reviewer.md            # 코드 품질 에이전트 프롬프트
│   ├── security-analyzer.md           # 보안 분석 에이전트 프롬프트
│   ├── documentation-checker.md       # 문서 검증 에이전트 프롬프트
│   ├── compliance-checker.md          # 컴플라이언스 에이전트 프롬프트
│   └── release-summarizer.md          # 릴리즈 요약 에이전트 프롬프트
├── examples/
│   ├── sample-mr/                     # 테스트용 샘플 MR
│   └── sample-reports/                # 예제 리포트 출력
└── AGENTS.md                          # GitLab Duo 커스터마이제이션
```
