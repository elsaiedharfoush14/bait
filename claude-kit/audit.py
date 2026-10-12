"""Token audit: where does the fixed per-session cost come from?  python ~/.claude/kit/audit.py [project_dir]"""
import json, os, re, sys
from itertools import combinations

home = os.path.join(os.path.expanduser("~"), ".claude")
proj = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
tok = lambda n: f"~{n // 4:,} tok"

print("== CLAUDE.md files (loaded every session) ==")
for p in [os.path.join(home, "CLAUDE.md"), os.path.join(proj, "CLAUDE.md"), os.path.join(proj, ".claude", "CLAUDE.md")]:
    if os.path.exists(p):
        n = os.path.getsize(p)
        print(f"  {tok(n):>12}  {p}" + ("   <-- trim / move detail to skills" if n > 6000 else ""))

print("== Skills (name+description always loaded, body only when used) ==")
skills = []
for root in [os.path.join(home, "skills"), os.path.join(proj, ".claude", "skills")]:
    if not os.path.isdir(root): continue
    for d in sorted(os.listdir(root)):
        f = os.path.join(root, d, "SKILL.md")
        if not os.path.exists(f): continue
        t = open(f, encoding="utf-8", errors="ignore").read()
        m = re.search(r"description:\s*(.+)", t)
        desc = m.group(1) if m else ""
        skills.append((d, set(re.findall(r"[a-z؀-ۿ]{4,}", desc.lower()))))
        print(f"  {d:30} desc {len(desc):4} chars, body {tok(len(t))}")

print("== Possibly overlapping skills (consider merging) ==")
hit = False
for (a, wa), (b, wb) in combinations(skills, 2):
    if wa and wb:
        j = len(wa & wb) / len(wa | wb)
        if j >= 0.35: hit = True; print(f"  {j:.0%}  {a}  <->  {b}")
if not hit: print("  none")

print("== MCP servers (each adds tools to every session) ==")
for p in [os.path.join(os.path.expanduser("~"), ".claude.json"), os.path.join(proj, ".mcp.json")]:
    if not os.path.exists(p): continue
    try: d = json.load(open(p, encoding="utf-8"))
    except Exception: continue
    names = set(d.get("mcpServers", {}))
    for pr in (d.get("projects") or {}).values(): names |= set(pr.get("mcpServers", {}))
    print(f"  {p}: {len(names)} -> {', '.join(sorted(names)) or '-'}")
print("Tip: turn off servers not needed in this project via /mcp; measure spend: npx ccusage@latest daily")
