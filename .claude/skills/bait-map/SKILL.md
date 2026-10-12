---
name: bait-map
description: Navigate index.html (the whole Bait app, ~100 KB / ~35k tokens) cheaply. Use before reading or editing any code in index.html.
---
1. Run `tools/codemap.sh` → sections + every function with its line number (~500 tokens).
2. `Read index.html` with `offset`/`limit` around the function you need (usually 20–60 lines), or `Grep -n` a name.
3. Never Read index.html whole, never open `exceljs.min.js` (vendor, 950 KB — blocked in settings).
Main areas: voice `parseSpeech` ~429 · data `save/lget` ~487 · render ~514 · sheets `openOv/closeOv` ~639 ·
mic ~669 · edit ~706 · bills ~765 · receipt OCR ~787 · report/Excel ~820 · sync (`seal/fbToken/pull/push/mergeInto`) ~884 ·
QR ~946 · backup ~980 · tour ~1005 · update ~1036. Line numbers drift — re-run the map after edits.
