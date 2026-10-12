---
name: token-saver
description: Token-economy playbook. Use at the start of any non-trivial task, when reading big files/screenshots/PLC exports, when choosing a model or subagent, or when the user complains about token or usage burn.
---
## Pick the cheapest tool that can do it
| Need | Use |
|---|---|
| Find something in code/docs | Grep -n / Glob, then Read offset+limit |
| Understand a big file, log, PDF, Excel, PLC export, many screenshots | `digest` agent (Haiku) → short answer |
| Clear mechanical edits / repetitive blocks / run tests | `implementer` agent (Sonnet) |
| Design, hard bug, safety-critical PLC logic | main model, yourself |
| Library docs | the library's README/docs page section, not whole repo |
Subagents start cold — only worth it when the raw material is ≥ ~15k tokens or the work is long and mechanical.

## Always
- Bound output: `| tail -40`, `| head`, `grep -c`, `--quiet`; tests: show failures only. MCP: `minimal_output`, small pages.
- Screenshots: one when it proves something; crop/zoom to the region. Hook already shrinks big images.
- Never re-read a file you just edited or already have; never paste big files back to the user.
- No polling loops (`sleep`, repeated status checks); one check, then wait for events.
- Short replies; no restating the plan; no summaries of what the diff already shows.
- Prefer existing skills/scripts over re-deriving; if two skills overlap, say so once (merge suggestion).

## Model (the user can't watch every task — advise in one line when it matters)
- Default `opusplan`: Opus while planning (plan mode), Sonnet while executing. `/model sonnet` for routine work,
  `/model opus` for a hard problem, `/model haiku` for trivial Q&A. Lower `/effort` for simple asks.
- Unrelated new task → suggest `/clear`; long session → `/compact`.

## When burn looks abnormal
`/context` (what fills the window) · `/usage` · `npx ccusage@latest daily` (per-day spend) ·
`python ~/.claude/kit/audit.py` (duplicate skills, fat CLAUDE.md files, MCP server count).
