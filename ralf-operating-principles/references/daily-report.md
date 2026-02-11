# Daily Report (저녁 보고)

## 17. 매일 저녁 7시 Daily Report

### 원칙
- **시간**: 매일 저녁 7시 (Asia/Seoul 기준)
- **채널**: Telegram으로 summary 발송
- **기록**: Notion 메인 페이지 하위에 날짜별 문서화

### 자동화
- OpenClaw Cron 스케줄러로 자동 실행
- 주 7일, 연중 자동 발송

---

## Daily Report 포함 내용

### 📋 오늘 한 일 (Today's Work)

**목적**: 오늘 처리한 작업들의 요약

**포함 내용**:
- 완료된 작업 (Task 기준)
- 프로젝트별 진행 상황
- 버그 수정 / 개선 사항

**형식**:
```
✅ Narratr 프로젝트
   - KOL 분류 알고리즘 개선
   - API 응답 속도 최적화

✅ FDS 솔루션
   - 대시보드 UI 버그 수정
   - 모니터링 시스템 테스트
```

---

### 💡 메모 / 인사이트 (Memo & Insights)

**목적**: 대화 중 나온 아이디어나 기억할 만한 것들

**포함 내용**:
- 새로운 아이디어
- 의사결정 포인트
- 배운 교훈
- 다음 스텝에 영향을 미칠 인사이트

**형식**:
```
💡 Narratr의 필터링 로직을 다시 설계하는 게 나을 것 같음
   → 다음 주에 검토 필요

💡 Cybertruck 가격 분석에서 새로운 데이터 발견
   → 전략 수정 검토 필요

💡 영어 표현: "approach"는 단수형 ("is", not "are")
   → Notion 영어 학습에 추가
```

---

### 🔧 생성/수정된 스킬 (Skills Created/Updated)

**목적**: 오늘 만들거나 수정한 스킬을 정리

**포함 내용**:
- 새로 만든 스킬 이름 + 목적
- 수정한 스킬 + 어떤 부분을 수정했는지
- 삭제된 스킬 (있으면)

**형식**:
```
🆕 새 스킬
   - ralf-operating-principles
     → 청묘의 운영 규칙 문서화

📝 수정된 스킬
   - narratr-kol-tagging
     → 분류 기준 업데이트 (3가지 규칙 추가)

❌ 삭제된 스킬
   - (없음)
```

---

### 📌 내일 할 일 / 미완료 (Tomorrow / Incomplete)

**목적**: 이어서 해야 할 것들, 우선순위 표시

**포함 내용**:
- 오늘 못 한 작업 (그리고 우선순위)
- 내일 스케줄
- 대기 중인 업무

**형식**:
```
🔴 [높음] Narratr 필터링 로직 재설계
    → 에드몽의 피드백 기다리는 중

🟡 [중간] Cybertruck 데이터 분석
    → 내일 오전 진행 예정

🟢 [낮음] FDS 문서화
    → 이번 주 안에 완료
```

---

## Telegram Daily Report 형식

### 예시

```
📊 청묘의 일일 보고 (2026-02-06)

✅ 오늘 한 일
• IDENTITY.md / USER.md / MEMORY.md 설정
• Notion 장기메모리 페이지 생성
• ralf-operating-principles 스킬 생성

💡 메모 / 인사이트
• 장기메모리는 Notion에만 저장하여 토큰 효율화
• Daily Report Cron 자동화 설정 필요

🔧 생성/수정된 스킬
• [NEW] ralf-operating-principles (5개 reference 포함)

📌 내일 할 일
🔴 Daily Report Cron 스케줄링 (저녁 7시)
🟡 영어 학습 피드백 DB 구축
```

---

## Notion Daily Report 저장 구조

### 페이지 이름
```
📅 Daily Report - [YYYY-MM-DD]
예) 📅 Daily Report - 2026-02-06
```

### 페이지 위치
- 부모: "Openclaw" (메인 페이지)
- 데이터베이스 이름: "Daily Reports"

### 내용 구조
```
# 📅 Daily Report - 2026-02-06

## ✅ 오늘 한 일
- [작업 1]
- [작업 2]

## 💡 메모 / 인사이트
- [인사이트 1]
- [인사이트 2]

## 🔧 생성/수정된 스킬
- [스킬 1]
- [스킬 2]

## 📌 내일 할 일
- [우선순위] [작업]
```

---

## Cron 설정 (자동화)

### 설정 정보
```
task: Daily Report 생성 및 발송
schedule: cron "0 19 * * *" (매일 저녁 7시, Asia/Seoul)
timezone: Asia/Seoul
actions:
  1. 오늘 대화 히스토리에서 정보 추출
  2. Telegram으로 summary 발송
  3. Notion에 날짜별 페이지 생성
  4. 내용 자동 저장
```

### 실행 조건
- 매일 정확히 저녁 7시 (한국 시간)
- 세션 상태와 무관하게 자동 실행
- 오류 발생시 재시도 (3회)

---

## 데이터베이스 구조 (Notion)

### Daily Reports DB 컬럼

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| Title | Title | 📅 Daily Report - YYYY-MM-DD |
| Date | Date | 보고서 날짜 |
| Status | Select | Completed / In Progress |
| Work Summary | Text | 오늘 한 일 요약 |
| Insights | Text | 인사이트 / 메모 |
| Skills | Multi-select | 생성/수정된 스킬 |
| Tomorrow | Text | 내일 할 일 |

---

## 피드백 루프

### 주간 검토
- 일주일 Daily Reports 검토
- 패턴 분석 (자주 나오는 작업, 반복되는 문제)
- 스킬 개선 기회 발견

### 월간 검토
- 월별 성과 정리
- 프로젝트별 진행 상황 분석
- 다음 달 우선순위 설정

---

## 예시 (전체)

### Telegram 메시지
```
📊 청묘의 일일 보고 (2026-02-07)

✅ 오늘 한 일
• Narratr KOL 분류 알고리즘 V2 완성
• FDS 대시보드 성능 최적화 (+40%)
• 영어 학습 피드백 정리

💡 메모 / 인사이트
• Narratr 필터링은 ML 기반으로 개선하면 정확도 향상 가능
• FDS 대시보드는 캐싱 전략 변경으로 큰 성과

🔧 생성/수정된 스킬
• [UPDATE] narratr-kol-tagging (분류 로직 개선)

📌 내일 할 일
🔴 Narratr ML 모델 검증 (우선순위 높음)
🟡 Cybertruck 가격 분석 진행 중
🟢 FDS 문서화 (이번 주 내)
```

### Notion 페이지
```
# 📅 Daily Report - 2026-02-07

## ✅ 오늘 한 일
- Narratr KOL 분류 알고리즘 V2 완성
  → 정확도: 87% (V1 대비 +12%)
  → 처리 속도: 2.3s → 1.8s
  
- FDS 대시보드 성능 최적화
  → 캐싱 전략 변경
  → 로딩 속도: 4.2s → 2.5s (+40%)
  
- 영어 학습 피드백 DB 정리
  → 주어-동사 일치: 5개 사례 추가

## 💡 메모 / 인사이트
- Narratr의 ML 기반 개선이 효과적일 것 같음
  → 다음 주 검증 필요
  
- FDS 캐싱 전략의 ROI가 높음
  → 다른 프로젝트에도 적용 고려

## 🔧 생성/수정된 스킬
- narratr-kol-tagging (V2.1)
  → 분류 로직 3가지 규칙 추가

## 📌 내일 할 일
- 🔴 Narratr ML 모델 검증 (우선순위 높음)
- 🟡 Cybertruck 가격 분석 진행
- 🟢 FDS 문서화 작업 계속
```

---

## 자동화 주의사항

- Daily Report 생성 시간이 정확해야 함
- Notion API 통신 오류시 재시도 로직 필요
- 토큰 효율을 위해 자동 요약만 생성 (상세 내용은 필요시만)
- 에드몽이 바쁠 때는 Telegram 메시지만 발송, 확인은 나중에
