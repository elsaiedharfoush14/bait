---
name: token-saver
description: Rules to keep Claude Code token use low in this repo (and the sister repo uues-petty-cash). Use at the start of any session, or when he complains about token/usage burn.
---
**Session habits (tell him in Egyptian Arabic when relevant)**
- One task per session; `/clear` between unrelated tasks; `/compact` when a session gets long. Long chats re-send all history every turn.
- `/context` shows what fills the window; `/usage` (or `/cost`) shows spend. Check these first when burn looks abnormal.
- Default model Sonnet for routine edits; Opus only for hard bugs/design. `/model` to switch. Lower effort for simple asks.
- Disable MCP servers/connectors not needed for the task (`/mcp`). Tool Search defers schemas, but each server still costs.
- Subagents / "deep research" multiply cost (each starts cold) — only when he asks.

**Working rules for Claude**
- Code: `bait-map` skill first; read line ranges, never whole index.html; never touch exceljs.min.js.
- Bound every output: `| head`, `| tail`, `grep -c`, GitHub MCP `minimal_output`/small pages. No polling loops, no repeated `gh run` checks.
- Screenshots/browser previews are expensive (images); take one when it proves something, not per step.
- Don't re-read a file just edited; don't re-derive what CLAUDE.md already says.
- Reply short.
