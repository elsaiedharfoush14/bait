"""Install the token kit into ~/.claude (Windows / macOS / Linux). Safe to re-run (updates in place).
   python install.py            -> install / update
   python install.py --no-model -> don't set the default model to opusplan
"""
import json, os, re, shutil, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.join(os.path.expanduser("~"), ".claude")
KIT = os.path.join(HOME, "kit")


def copy(src, dst):
    if os.path.isdir(src): shutil.copytree(src, dst, dirs_exist_ok=True)
    else: os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)


def main():
    os.makedirs(HOME, exist_ok=True)
    copy(os.path.join(HERE, "hooks"), os.path.join(KIT, "hooks"))
    copy(os.path.join(HERE, "audit.py"), os.path.join(KIT, "audit.py"))
    copy(os.path.join(HERE, "agents"), os.path.join(HOME, "agents"))
    copy(os.path.join(HERE, "skills"), os.path.join(HOME, "skills"))

    sp = os.path.join(HOME, "settings.json")
    s = {}
    if os.path.exists(sp):
        shutil.copy2(sp, sp + time.strftime(".bak-%Y%m%d%H%M%S"))
        with open(sp, encoding="utf-8") as f: s = json.load(f)
    py = sys.executable.replace("\\", "/")
    guard = os.path.join(KIT, "hooks", "read_guard.py").replace("\\", "/")
    cmd = f'"{py}" "{guard}"'
    pre = s.setdefault("hooks", {}).setdefault("PreToolUse", [])
    pre[:] = [h for h in pre if "read_guard.py" not in json.dumps(h)]
    pre.append({"matcher": "Read", "hooks": [{"type": "command", "command": cmd, "timeout": 15}]})
    env = s.setdefault("env", {})
    env.setdefault("MAX_MCP_OUTPUT_TOKENS", "10000")
    env.setdefault("BASH_MAX_OUTPUT_LENGTH", "20000")
    if "--no-model" not in sys.argv: s.setdefault("model", "opusplan")
    with open(sp, "w", encoding="utf-8") as f: json.dump(s, f, indent=2, ensure_ascii=False)

    cp = os.path.join(HOME, "CLAUDE.md")
    old = open(cp, encoding="utf-8").read() if os.path.exists(cp) else ""
    block = open(os.path.join(HERE, "CLAUDE.user.md"), encoding="utf-8").read().strip()
    old = re.sub(r"<!-- token-kit:start -->.*?<!-- token-kit:end -->\n?", "", old, flags=re.S).rstrip()
    with open(cp, "w", encoding="utf-8") as f: f.write((old + "\n\n" if old else "") + block + "\n")

    try:
        import PIL  # noqa: F401
    except ImportError:
        print("  (optional) pip install pillow  -> lets the hook shrink big screenshots")
    print("Token kit installed in", HOME)
    print("  hook  :", cmd)
    print("  model :", s.get("model"), "| agents: digest (haiku), implementer (sonnet) | skill: token-saver")
    print("Restart Claude Code, then check /hooks and /agents.")


if __name__ == "__main__":
    main()
