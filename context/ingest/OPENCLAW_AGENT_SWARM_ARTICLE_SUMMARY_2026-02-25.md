# Ingest Summary — OpenClaw + Codex/ClaudeCode Agent Swarm (Elvis @elvissun)

Source file:
- `/Users/silkroadcat/.openclaw/media/inbound/file_567---480851e3-5e1d-4f1c-b132-7af7fbbe02b9.docx`
- Extracted text: `context/ingest/openclaw_agent_swarm_article_2026-02-25.txt`

## 0) Executive summary (핵심)
This article describes a **two-tier agent architecture** where an “orchestrator” agent (Zoe) holds business context and manages multiple coding agents (Codex / Claude Code / Gemini) running in isolated worktrees + tmux sessions. The system is optimized for high throughput: autonomous PR creation + CI + multi-model reviews + human merge, with Telegram notifications only when PRs are truly merge-ready.

## 1) 핵심 요점(요약)
- **Orchestrator layer**: a single “manager” agent that retains business context (customer history, meeting notes, past decisions) and writes precise prompts for coding agents.
- **Coding agents**: specialize on code only; they do not need broad business context.
- **Worktree per task**: each agent runs in its own `git worktree` and tmux session.
- **Monitoring loop**: a deterministic cron script checks tmux liveness, PR existence, CI status, and auto-respawns failed agents.
- **Definition of done** is strict: PR exists + synced to main + CI passing + multi-model review + screenshots for UI changes.
- **Multi-model review**: Codex reviewer (edge cases), Gemini (security/scalability/design sensibility), Claude (supplemental).
- **Human stays out** until a Telegram ping says “ready to merge”.
- Bottleneck noted: **RAM** (multiple worktrees with separate `node_modules`).

## 2) 결정/원칙으로 가져갈만한 것 (AOI Core 관점)
- Separation of concerns via **context specialization** (business vs code) is a scalable pattern.
- Deterministic babysitter loop (cheap) > polling agent outputs (expensive).
- Enforce a hard **DoD** gate (CI + multi-review + screenshots) to prevent “PR spam”.
- tmux-based steering is a robust intervention method.

## 3) 재사용 가능한 체크리스트 (추출)
- Per-task isolation: `git worktree` + dedicated dependency install.
- Agent registry: a single JSON registry for task lifecycle and notification.
- CI gate rules: UI changes require screenshots.
- Review gate: multiple reviewers with different strengths.

## 4) 리스크/주의
- Dangerous flags are shown in examples (e.g., bypass approvals). In AOI environment this must remain **fail-closed**.
- RAM/disk usage can explode with parallel worktrees.

## 5) 다음 액션(추천)
- Convert the concepts into AOI Core “Code Necromancy / Swarm Ops” runbook:
  - task registry schema
  - tmux steering SOP
  - DoD gate standard
