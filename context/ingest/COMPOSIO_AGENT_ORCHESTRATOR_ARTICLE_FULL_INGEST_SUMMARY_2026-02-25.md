# Full Ingest Summary — “The Self-Improving AI System That Built Itself” (Prateek @agent_wrapper)

Source file:
- `/Users/silkroadcat/.openclaw/media/inbound/file_568---0f683f1a-7bac-4797-bb60-6ca9ea38e0ee.docx`
- Extracted text: `context/ingest/inbound_doc_568_2026-02-25.txt`

Primary external references mentioned:
- Repo: https://github.com/ComposioHQ/agent-orchestrator
- Metrics release: https://github.com/ComposioHQ/agent-orchestrator/releases/tag/metrics-v1
- Visualizations: https://pkarnal.com/ao-labs/

---

## 0) Executive summary
This article describes an **agent-orchestrator that is itself an AI agent** (not just scripts), managing many parallel coding agents through a plugin system and a reactions pipeline. The key claim: the real bottleneck is not code generation, but **human attention** (CI babysitting, review routing, conflict resolution). The system closes the loop by routing CI failures and review comments back into the correct agent sessions automatically, and then logging session outcomes to continuously improve orchestration policies.

---

## 1) Key points (condensed)
- Starts from “parallel agents” but hits the scaling limit: **human babysitting**.
- Evolves from bash scripts (~2,500 LOC managing tmux + worktrees) into a full orchestrator.
- “Inception” dynamic: agents help build the orchestrator that manages them.
- System scale claims: ~40K TypeScript LOC, 17 plugins, 3,288 tests built in ~8 days; 27 PRs merged in a single day.
- Orchestrator differentiator: intelligent routing of events (CI fails, review comments) back into sessions; minimal human plumbing.

---

## 2) Architecture (what matters)
### 2.1 Plugin system (8 swappable slots)
- Replaceable runtime (tmux/process/docker), tracker (GitHub/Linear), notifier (Slack/Telegram), SCM integration, etc.
- Why it matters to AOI: AOI Core should treat integrations as swappable modules behind stable receipts/proofs.

### 2.2 Session lifecycle
Issue → workspace/worktree → runtime session → agent works → PR created → CI/review events → reactions → merge.

### 2.3 Reactions pipeline (self-healing CI)
Events trigger actions:
- `ci_failed` → spawn/fix agent with failure logs
- `changes_requested` → agent addresses comments
- `approved` → notify human

Why it matters: AOI already has “circuit breaker + queue + proof bundle”; this is the “PR/CI analog” of the same concept.

---

## 3) Activity detection (important implementation detail)
Instead of asking the agent what it’s doing, it reads structured session artifacts:
- Claude Code writes JSONL event files per session
- orchestrator parses them to detect: active/idle/waiting/tooling/finished

AOI take-away: **don’t trust self-report; trust receipts/log files**.

---

## 4) Web dashboard (ops UX)
- Next.js 15
- SSE for real-time updates (no polling)
- “attention zones” grouping sessions by what needs human attention
- live terminal (xterm.js)

AOI take-away: if we build a Bazaar ops console, the “attention zone” framing is a strong pattern.

---

## 5) Self-improvement loop
- logs performance and outcomes
- runs retrospectives
- updates orchestration policies (prompt shapes, guardrails)

This is essentially: Agents build → orchestrator observes → orchestrator adjusts → agents build better.

---

## 6) Clear separation of human vs agent work
- claims to use git trailers to label which model wrote commits
- human focuses on architecture decisions + conflict resolution + judgment calls

AOI take-away: for Code Necromancy and Bazaar governance, provenance tagging is a core trust primitive.

---

## 7) Risks / cautions for AOI adoption
- Some ecosystems demonstrate dangerous flags/bypass permissions; AOI must remain fail-closed.
- RAM/disk amplification from worktrees + node_modules is real; needs caps and scheduling.

---

## 8) Actionable AOI next steps (recommended)
1) Add “Reactions” concept to AOI Council / Bazaar ops:
   - failure → route back to worker/agent session
   - approval → notify only
2) Define “receipt artifacts” for agent sessions (JSONL) and stop relying on self-report.
3) For Code Necromancy: implement a strict DoD gate template (tests + review + provenance + proof).
