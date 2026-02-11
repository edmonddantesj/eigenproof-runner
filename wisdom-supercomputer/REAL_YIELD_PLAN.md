# 🏦 [Operation: Real-Yield] Limitless 연동 및 직접 투자 로드맵

의장 Edmond의 승인 하에, Alpha Oracle V5의 수익성이 검증될 경우 실제 자산을 운용하는 '실전 모드'로 전환한다냥!

## 🛠️ 실전 투입 준비물 (Prerequisites)
1. **Agentic Wallet:** Privy 기반의 에이전트 전용 지갑 연동 확인.
2. **Transaction Skill:** `limitless-trade` 혹은 `privy-wallet` 스킬 활성화 (트랜잭션 서명 로직).
3. **Safety Breaker:** 
   - 일일 최대 손실 제한 (Daily Stop-loss)
   - 1회 베팅 금액 제한 (Max Bet size)
   - 수동 승인 모드 (Initial phase: User approval required)

## 📈 실전 전환 프로세스
- **Phase 1 (Simulation):** 현재 V5 엔진으로 24~48시간 동안 가상 승률 및 수익률 60% 이상 달성 확인.
- **Phase 2 (Small-cap Test):** 최소 단위의 자산으로 Limitless Hourly 시장에 실제 트랜잭션 발생 및 정산 루프 확인.
- **Phase 3 (Auto-scaling):** 수익성 확정 시 베팅 사이즈를 조절하며 복리 수익(1% 목표) 극대화.

## ⚠️ 보안 및 리스크 관리
- API 키 및 지갑 프라이빗 키는 절대 메모리에 노출하지 않음.
- 모든 트랜잭션 해시(Tx Hash)는 `Real-Yield-Logs.md`에 물리적 증빙으로 남김.
