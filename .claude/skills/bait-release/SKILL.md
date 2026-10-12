---
name: bait-release
description: Ship a new Bait version to GitHub Pages (bump version in 3 places, commit, push, check the Pages run). Use when a change is ready to go live.
---
1. New version `vYYYY.MM.DD.N`: `APP_VER` in index.html (`grep -n APP_VER index.html`), `version.json`, `CACHE='bait-vN'` in sw.js (N+1).
2. Commit with email `332831565+elsaiedharfoush14@users.noreply.github.com`; push `main`.
3. Check Pages once: `gh run list --repo elsaiedharfoush14/bait --limit 1` (cloud session: `mcp__github__actions_list`, minimal output). Don't poll.
