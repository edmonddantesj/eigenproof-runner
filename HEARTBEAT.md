# HEARTBEAT.md

## 🤖 Context Care & Auto-State Sync
- **Trigger:** context usage >= 60% (via 📊 session_status)
- **Action:**
  1. Immediately update `CURRENT_STATE.md` with the latest summary.
  2. Alert user: "⚠️ Context usage at 60%. Current state synced. Preparing for reset."
  3. Suggest or initiate `/reset` to maintain performance.

## 🕒 The Alpha Oracle V3 Simulation (Hourly)
- **Action:** Run `python3 the-alpha-oracle/engine/sim_engine_v3.py` every hour (or during heartbeats).
- **Goal:** Accumulate BTC prediction data, calculate win rates, and refine logic via Aoineco squad debates.

## 🕒 Periodic Checks
- Check `TODO List` in `CURRENT_STATE.md` twice a day.
- Monitor active blockers.
- (Self-Improvement) Search GitHub/Moltbook for new prediction strategies or Alpha Oracle mentions.
