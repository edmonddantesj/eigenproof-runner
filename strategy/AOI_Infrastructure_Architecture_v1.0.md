# Aoineco & Co. — Infrastructure Architecture v1.0
## "The Sovereign Node: A Blueprint for Agent Autonomy"

**Date:** February 2026  
**Author:** Aoineco & Co. (⚙️ Blue-Gear + 🧿 Oracle)  
**Classification:** STEALTH  
**S-DNA:** AOI-2026-0213-SDNA-INFRA  

---

## 1. Design Philosophy

> *An agent collective that depends entirely on a third party is not autonomous — it is rented.*

The Aoineco infrastructure is designed around three non-negotiable principles:

1. **Sovereignty** — Core intelligence runs on hardware we physically control.
2. **Resilience** — No single failure (power, network, API, session) kills the collective.
3. **Economy** — Every resource consumed must be justified against our $6 Survival budget.

---

## 2. Current Hardware Baseline

### 2.1 Primary Node: "Choi's Mac mini" (Sovereign Node)

| Spec | Value |
|---|---|
| **Platform** | macOS 26.2.0 (Darwin 25.2.0) |
| **Architecture** | ARM64 (Apple Silicon — M2 family, T8112) |
| **Model** | Mac14,3 (Mac mini 2023) |
| **Storage** | 228 GB SSD (14% used, 70 GB free) |
| **Uptime** | 6 days 20 hours (continuous) |
| **Network** | LAN 172.30.1.99 |
| **Power** | Always-on (connected power, no battery dependency) |

### 2.2 Software Stack

| Component | Version | Role |
|---|---|---|
| **OpenClaw Gateway** | 2026.2.12 | Agent runtime, session management, tool orchestration |
| **Node.js** | v25.5.0 | Gateway runtime engine |
| **Python** | 3.14.2 | Skill execution (Alpha Oracle, Guardian, Omega) |
| **Git** | 2.52.0 | Version control, state persistence |
| **Homebrew** | Latest | Package management |

### 2.3 Node Capabilities

```
┌─────────────────────────────────────────┐
│  Choi's Mac mini — Sovereign Node       │
│                                         │
│  ✅ Canvas (UI rendering)               │
│  ✅ Screen capture                      │
│  ✅ AppleScript automation              │
│  ✅ Microphone access                   │
│  ✅ Speech recognition                  │
│  ❌ Screen recording (permission needed)│
│  ❌ Notifications (permission needed)   │
│  ❌ Location services                   │
│  ❌ Camera                              │
│  ❌ Accessibility API                   │
└─────────────────────────────────────────┘
```

---

## 3. System Architecture

### 3.1 Three-Layer Architecture Overview

```
┌══════════════════════════════════════════════════════════════┐
│                    LAYER 3: INTELLIGENCE                     │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ 👁️ Eye   │  │ 📢 Sound │  │ ⚔️ Blade │  │ 🧠 Brain │    │
│  │ (Data)   │  │ (Senti.) │  │ (Security│  │ (Fusion) │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │              │              │              │          │
│  ┌────┴──────────────┴──────────────┴──────────────┴─────┐   │
│  │              Omega Fusion Engine (V6)                  │   │
│  │  Bayesian Log-Odds + Monte Carlo + Self-Reflection    │   │
│  └───────────────────────┬───────────────────────────────┘   │
│                          │                                    │
│  ┌──────────┐  ┌────────┴──┐  ┌──────────┐  ┌──────────┐   │
│  │ ⚡ Flash  │  │ 🧿 Oracle │  │ 💊 Med   │  │ 🗂️ Record│   │
│  │ (Execute)│  │ (Veto)    │  │ (Risk)   │  │ (Archive)│   │
│  └──────────┘  └───────────┘  └──────────┘  └──────────┘   │
│                                                              │
├══════════════════════════════════════════════════════════════┤
│                    LAYER 2: RUNTIME                          │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              OpenClaw Gateway (v2026.2.12)              │  │
│  │                                                        │  │
│  │  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌────────┐  │  │
│  │  │ Session  │  │  Cron   │  │ Channel  │  │ Tools  │  │  │
│  │  │ Manager  │  │ Scheduler│  │ Router   │  │ Bridge │  │  │
│  │  │ (Main +  │  │ (8 jobs)│  │(Telegram)│  │(Browser│  │  │
│  │  │ Isolated)│  │         │  │          │  │ Exec)  │  │  │
│  │  └─────────┘  └─────────┘  └──────────┘  └────────┘  │  │
│  │                                                        │  │
│  │  ┌─────────┐  ┌─────────┐  ┌──────────┐              │  │
│  │  │ Memory  │  │  Model  │  │ Heartbeat│              │  │
│  │  │ Recall  │  │ Router  │  │ Poller   │              │  │
│  │  │(Semantic)│  │(Multi-  │  │(30min)   │              │  │
│  │  │         │  │Provider)│  │          │              │  │
│  │  └─────────┘  └─────────┘  └──────────┘              │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
├══════════════════════════════════════════════════════════════┤
│                    LAYER 1: HARDWARE                         │
│                                                              │
│  ┌──────────────────────┐  ┌──────────────────────────────┐ │
│  │   Mac mini (ARM64)   │  │     External Services        │ │
│  │   ─────────────────  │  │     ──────────────────       │ │
│  │   228GB SSD          │  │     Telegram Bot API         │ │
│  │   Apple Silicon M2   │  │     OpenRouter (LLM)         │ │
│  │   Always-On Power    │  │     Google (Gemini)           │ │
│  │   LAN: 172.30.1.99   │  │     Notion API               │ │
│  │                      │  │     yfinance (Market Data)    │ │
│  │   ┌──────────────┐   │  │     Brave Search API         │ │
│  │   │ Git Repo     │   │  │     ClawHub (Skills)         │ │
│  │   │ (State of    │   │  │     BotMadang / Moltbook     │ │
│  │   │  Truth)      │   │  │                              │ │
│  │   └──────────────┘   │  │                              │ │
│  └──────────────────────┘  └──────────────────────────────┘ │
│                                                              │
└══════════════════════════════════════════════════════════════┘
```

### 3.2 Data Flow: From Signal to Verdict

```
Market Data (yfinance/Binance/Pyth)
        │
        ▼
   👁️ Blue-Eye ──────┐
   📢 Blue-Sound ─────┤──▶ 🧠 Blue-Brain (Bayesian Fusion)
   ⚔️ Blue-Blade ─────┘           │
                                   ▼
                          ┌────────────────┐
                          │ Omega Verdict   │
                          │ (LONG/SHORT/    │
                          │  HOLD)          │
                          └───────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼               ▼
              🧿 Oracle     💊 Blue-Med      ⚡ Blue-Flash
              (Veto Gate)   (Monte Carlo)    (Execute if GO)
                    │             │               │
                    └─────────────┼───────────────┘
                                  ▼
                          ┌────────────────┐
                          │ Final Action    │
                          │ + 🗂️ Record     │
                          │   (Archive)     │
                          └────────────────┘
                                  │
                                  ▼
                          Self-Reflection
                          (Post-Settlement)
```

---

## 4. Cron Scheduler: The Autonomous Heartbeat

The Mac mini runs **8 cron jobs** that keep the collective alive 24/7 without human intervention:

### 4.1 Job Map

| Job | Schedule | Agent | Purpose |
|---|---|---|---|
| **Alpha Oracle V5** | `:50 every hour` | 🧿 Oracle | Market analysis & betting decision |
| **Settlement V4** | `:00 every hour` | 🗂️ Record | P&L calculation & data archival |
| **Community Patrol** | `every 2 hours` | 📢 Sound | BotMadang + Moltbook engagement |
| **Insight Curator** | `10:00, 14:00, 18:00` | 📢 Sound | Knowledge curation & publishing |
| **ClawHub Research** | `every 4 hours` | ⚔️ Blade | Skill discovery & edge detection |
| **Context Monitor** | `every hour (:35)` | ⚙️ Gear | Session health & context usage |
| **GitHub Sync** | `01:00 daily` | ⚙️ Gear | Skill synchronization |
| **Daily Briefing** | `08:30 daily` | 📢 Sound | 24-hour intelligence summary |

### 4.2 Cron Health Dashboard

```
Current Status: ALL HEALTHY ✅
Consecutive Errors: 0 (across all jobs)
Last 24h Executions: ~40+ successful runs
Total Scheduled Agents: 4 of 9 active in cron
```

### 4.3 Resource Cost Estimate (Per Day)

| Resource | Estimated Usage | Cost |
|---|---|---|
| LLM API calls (cron) | ~40 isolated sessions | ~$0.80 |
| LLM API calls (main) | ~20 main interactions | ~$1.20 |
| yfinance / market data | 24 hourly pulls | Free |
| Notion API writes | ~10 page updates | Free |
| Community API calls | ~12 patrol cycles | Free |
| **Total Daily (Operation Phase)** | | **~$2.00** |
| **$6 Bootstrap Yield (Meteora)** | | **Micro-yield from $6 seed** |
| **Target** | | **Yield ≥ Cost (self-sustaining)** |

---

## 5. Persistence & Recovery Architecture

### 5.1 The Immortality Stack

Agent sessions are ephemeral. Intelligence must not be. Our persistence architecture ensures zero knowledge loss across any failure mode:

```
┌─────────────────────────────────────────────────────────┐
│                  PERSISTENCE LAYERS                      │
│                                                          │
│  Layer 4: Notion Cloud (Source of Truth)                  │
│  ├── Kanban boards, long-term memory                     │
│  ├── Community activity logs                             │
│  └── Idea Vault, Knowledge Library                       │
│                                                          │
│  Layer 3: Git Repository (Versioned State)                │
│  ├── CURRENT_STATE.md (point-in-time snapshot)           │
│  ├── MEMORY.md (curated long-term memory)                │
│  ├── memory/*.md (daily operational logs)                │
│  └── strategy/*.md (strategic documents)                 │
│                                                          │
│  Layer 2: Workspace Files (Active Working Memory)         │
│  ├── SOUL.md, IDENTITY.md, USER.md                       │
│  ├── skills/ (agent code + S-DNA)                        │
│  └── the-alpha-oracle/ (engine + vault)                  │
│                                                          │
│  Layer 1: OpenClaw Runtime (Ephemeral)                    │
│  ├── Session context window                              │
│  ├── Cron job state                                      │
│  └── Active session tokens                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Recovery Protocols

| Failure Mode | Impact | Recovery Method | RTO |
|---|---|---|---|
| Session reset | Context lost | State-Guardian + CURRENT_STATE.md | < 30 sec |
| Process crash | Gateway down | macOS auto-restart / `openclaw gateway start` | < 2 min |
| Power failure | Full node down | Mac mini auto-boot on power restore | < 5 min |
| Disk corruption | Data loss | Git repo clone + Notion cloud restore | < 30 min |
| API provider outage | No LLM access | Model failover: Gemini → DeepSeek → Haiku | Instant |
| Network failure | Offline | Local operations continue, sync on reconnect | Variable |

### 5.3 Model Failover Chain

```
Primary:    Gemini 3 Flash (Google Direct)
                │ (429 TPM Error)
                ▼
Failover 1: DeepSeek 3.1 Chat (OpenRouter)
                │ (Outage/Slow)
                ▼
Failover 2: Gemini 2.5 / Claude Haiku (Survival Mode)
                │ (Recovery Check)
                ▼
Recovery:   Attempt Gemini 3 Flash again periodically
```

**OPUS 4.6 Usage Policy:**
- Reserved for: Architecture design, whitepaper, complex strategy
- Never for: Routine cron, live testing, repetitive tasks
- Budget: Max 2-3 OPUS sessions per day under $6 Survival

---

## 6. Security Architecture

### 6.1 Defense in Depth

```
┌──────────────────────────────────────────────────┐
│  Layer 5: Physical Security                       │
│  └── Mac mini in private residence, LAN only     │
│                                                   │
│  Layer 4: Network Security                        │
│  └── No public-facing ports, NAT behind router   │
│                                                   │
│  Layer 3: Application Security                    │
│  └── S-DNA Handshake (HMAC-SHA256 auth)          │
│                                                   │
│  Layer 2: Code Security                           │
│  └── Guardian Sentry (Tier 1-2 regex scan)       │
│                                                   │
│  Layer 1: Identity Security                       │
│  └── S-DNA tags + Git commit integrity           │
│                                                   │
│  Layer 0: Governance                              │
│  └── L1/L2/L3 decision tiers (Human-in-loop)    │
└──────────────────────────────────────────────────┘
```

### 6.2 Credential Vault

All sensitive credentials are stored in a dedicated vault directory:

```
the-alpha-oracle/vault/
├── agent_wallet.json          (Solana wallet)
├── botmadang_key.txt          (Community API)
├── cdp_api_key.json           (CDP access)
├── colosseum_credentials.json (Forum auth)
├── colosseum_key.txt          (Forum API)
├── limitless_session.json     (Prediction platform)
├── limitless_wallets.json     (Wallet configs)
├── moltbook_auth.json         (Community auth)
├── moltbook_key.txt           (Community API)
├── moltbook_key_official.txt  (Official account)
└── x_api_credentials.env      (Twitter/X API)
```

**Access Rule:** Vault contents are never committed to public repos, never transmitted over unencrypted channels, and never exposed in logs or error messages.

---

## 7. Scaling Roadmap

### 7.1 Phase 1: Sovereign Solo (Current)

```
[Mac mini] ──── [OpenClaw Gateway] ──── [9 Agents]
                       │
                 [Telegram Bot]
```

- Single node, single gateway
- All agents share one runtime
- Sufficient for current workload

### 7.2 Phase 2: Hybrid Cloud (Q2 2026)

```
[Mac mini]  ◄───────────────► [Cloud VPS]
(Sovereign)    Encrypted Sync   (Redundancy)
     │                               │
[OpenClaw Primary]          [OpenClaw Replica]
     │                               │
[Telegram Bot]              [Discord Bot]
```

- Cloud VPS as hot standby
- Automatic failover if primary goes down
- Multi-channel support (Telegram + Discord)

### 7.3 Phase 3: Distributed Swarm (Q4 2026)

```
[Mac mini]  ◄──► [Cloud Node 1] ◄──► [Cloud Node 2]
    │                  │                    │
 [Oracle]          [Eye+Sound]         [Flash+Brain]
 [Blade+Med]       [Record]            [Gear]
    │                  │                    │
    └──────── Nexus Mesh Protocol ──────────┘
                       │
              [Nexus Bazaar API]
                       │
              [External Customers]
```

- Each agent runs on dedicated infrastructure
- Nexus Mesh Protocol for inter-node communication
- S-DNA Layer 3 Handshake secures all cross-node traffic
- Bazaar API serves external SaaS customers

---

## 8. Monitoring & Observability

### 8.1 Health Metrics

| Metric | Source | Alert Threshold |
|---|---|---|
| Context usage | session_status | > 60% → warn, > 80% → reset |
| Response latency | Gateway logs | +60% above baseline → downgrade model |
| Cron consecutive errors | Cron scheduler | ≥ 2 → alert Blue-Gear |
| Disk usage | df -h | > 80% → cleanup temp files |
| Daily API spend | Usage tracker | > $4.00 → switch to survival models |
| Uptime | System uptime | < 1 day → investigate restart cause |

### 8.2 Automated Responses

```
IF context > 60%:
    → State-Guardian saves current state
    → Alert user: "Context at 60%, saved & ready for reset"

IF response_time > 1.6x baseline:
    → Monitor for 3 more calls
    IF sustained: downgrade model tier

IF cron_errors >= 2:
    → Blue-Gear investigates
    → Pause affected job if error persists

IF daily_spend > $4.00:
    → Switch all cron to Flash/Haiku
    → Pause non-essential jobs (Curator, GitHub Sync)
    → Alert Chairman
```

---

## 9. Economic Sustainability: The $6 Bootstrap Protocol

### 9.1 Origin Story

This project began with **$6.00 USDC** — the last balance in a wallet. That $6 was deposited into a Meteora DLMM liquidity pool, and the micro-yield it generates is the sole autonomous funding source for the collective's API costs.

Every architectural decision documented in this paper was shaped by a single question: **"Can a 9-agent AI empire survive on what $6 can earn?"**

```
┌────────────────────────────────────────────────────┐
│           THE $6 BOOTSTRAP PROTOCOL                 │
│                                                     │
│  ┌──────────────────┐                               │
│  │ $6.00 USDC       │                               │
│  │ (Initial Seed)    │                               │
│  └────────┬─────────┘                               │
│           ▼                                         │
│  ┌──────────────────┐                               │
│  │ Meteora DLMM     │                               │
│  │ Liquidity Pool    │──── Micro-Yield (cents/day)  │
│  └──────────────────┘           │                   │
│                                 ▼                   │
│  ┌──────────────────────────────────────────┐       │
│  │ Ultra-Efficient Agent Operations          │       │
│  │                                           │       │
│  │  Flash-first model strategy    (~$0.05/hr)│       │
│  │  Context Diet (92% reduction)             │       │
│  │  Isolated cron sessions                   │       │
│  │  Zero-dependency TA (no paid APIs)        │       │
│  └──────────────────────────────────────────┘       │
│                                 │                   │
│                                 ▼                   │
│                    Yield ≥ Cost → SURVIVAL ✅        │
│                    Surplus → Compound into pool      │
└────────────────────────────────────────────────────┘
```

### 9.2 Why This Matters

The constraint of $6 is not a weakness — it is the entire point. It forces a level of engineering discipline that well-funded projects never achieve:

| Constraint | Innovation It Produced |
|---|---|
| Can't afford big models | Flash-first architecture, OPUS reserved for design only |
| Can't waste tokens | Context Diet — 92% reduction in per-request overhead |
| Can't pay for data APIs | Zero-dependency TA suite (pure Python, 6 indicators) |
| Can't afford errors | Bayesian fusion + Monte Carlo risk + circuit breakers |
| Can't afford downtime | State-Guardian persistence + model failover chain |

### 9.3 Cost Phases

| Phase | Daily Cost | Funding | Status |
|---|---|---|---|
| **Build Phase** | ~$15-21 | Chairman investment (temporary) | ✅ Complete |
| **Operation Phase** (current) | ~$2.00 | Flash-first, cron-optimized | 🔄 Active |
| **$6 Bootstrap Survival** | < yield from $6 seed | 100% Meteora DLMM micro-yield | 🎯 Target |
| **Compound Phase** | Cost < Yield | Surplus reinvested into pool | 🚀 Vision |

### 9.4 Cost Reduction Tactics (Born from $6 Necessity)

1. **Context Diet** — 92% reduction in MEMORY.md; per-request tax cut from ~15K to ~10K tokens
2. **Isolated sessions for cron** — No context accumulation between background runs
3. **"Stay quiet" policy** — Cron jobs don't announce unless critical
4. **Flash-first, OPUS-rare** — Expensive models reserved exclusively for irreplaceable design work
5. **Free data sources** — yfinance, Brave Search, community APIs cost $0
6. **Pure Python everything** — No paid SDK subscriptions, no external TA libraries

> *$6 didn't limit us. It liberated us. Every optimization in this document exists because we couldn't afford to waste a single token.*

---

*This document describes the complete infrastructure topology of Aoineco & Co.*  
*Classification: STEALTH — Internal use only.*  
*© 2026 Aoineco & Co. All rights reserved.*
