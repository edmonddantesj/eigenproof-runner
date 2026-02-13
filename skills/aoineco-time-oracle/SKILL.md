---
name: aoineco-time-oracle
description: |
  🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill
  Synchronizes agent session time with global NTP standards and monitors drift.
  
  Use when:
  - Reporting time-sensitive events (Alpha Oracle V6, Settlements)
  - Detecting system time drift or event loop lag
  - Synchronizing across multiple agent sessions
---

# Aoineco Time Oracle 🧭😼

## Capabilities
- **Global Sync:** Compares local system time with `pool.ntp.org`
- **Drift Detection:** Calculates sub-second drift between OS and Real-time.
- **Auto-KST:** Automatically formats to Asia/Seoul (UTC+9) with precision.

## Commands
- `python3 scripts/sync.py`: Returns `SUCCESS|YYYY-MM-DD HH:MM:SS|DriftInSeconds`

## Global Market Positioning (ACP/Virtuals)
- **Product Name:** Aoineco Time Oracle (Standard Time Sync for Sovereign Agents)
- **Feature:** Universal Timezone Support. Accepts `utc_offset` as an argument to sync anywhere on Earth (or beyond).
- **Commerce:** Positioned as a "System Integrity" infrastructure utility on Virtuals Protocol.
