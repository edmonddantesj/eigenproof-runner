# Ingest Policy — Triage Default v0.1

Decision date: 2026-02-25

## Default mode
- **Triage ingest is the default** for long documents/links.
- Goal: minimize token/context cost while still capturing actionable signal.

## Triage procedure (60s rule)
1) Extract structure-first: title, headings, table of contents, summary, conclusion, code blocks.
2) Assign a value score (0–3):
   - 0: not relevant
   - 1: mildly relevant
   - 2: useful
   - 3: critical / high leverage
3) Output:
   - If score < 2: produce a 10-line summary + file path, then stop.
   - If score >= 2: escalate to Full ingest.

## Exception (mandatory full ingest)
- **Conversation history provided by the user must always be Full ingest.**
  - Read end-to-end before summarizing.
  - Then: summary first → analysis → SSOT save.

## Notes
- Even in Full ingest, avoid re-printing original long text in chat. Store SSOT locally and reference paths.
