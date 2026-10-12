"""PreToolUse hook for Read — stops the two biggest silent token burners.

1. Big text file read whole (no offset/limit) -> blocked, Claude is told to grep / read a range / use the digest agent.
2. Big screenshot/image -> shrunk to MAX_SIDE px (copy in temp dir) before Claude sees it (tokens ~ width*height/750).
Never fails the tool: any error -> exit 0 and the Read runs as normal.
"""
import hashlib, json, os, sys, tempfile

MAX_LINES, MAX_BYTES, MAX_SIDE = 1500, 80_000, 1280
IMG = ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp')
NEVER = ('.min.js', '.min.css', '.map', '.lock')


def out(decision, reason=None, updated=None):
    o = {"hookEventName": "PreToolUse", "permissionDecision": decision}
    if reason: o["permissionDecisionReason"] = reason
    if updated: o["updatedInput"] = updated
    print(json.dumps({"hookSpecificOutput": o}))
    sys.exit(0)


def shrink(path, inp):
    from PIL import Image
    im = Image.open(path)
    if max(im.size) <= MAX_SIDE + 100: return
    orig = im.size
    st = os.stat(path)
    key = hashlib.md5(f"{path}|{st.st_mtime}|{st.st_size}".encode()).hexdigest()[:12]
    dst = os.path.join(tempfile.gettempdir(), f"claude_small_{key}.png")
    if not os.path.exists(dst):
        im.thumbnail((MAX_SIDE, MAX_SIDE))
        im.save(dst, optimize=True)
    out("allow", f"image shrunk {orig} -> max {MAX_SIDE}px to save tokens (original: {path})",
        {**inp, "file_path": dst})


def main():
    data = json.load(sys.stdin)
    inp = data.get("tool_input") or {}
    path = inp.get("file_path") or ""
    if not path or not os.path.isfile(path): return
    low = path.lower()
    if os.environ.get("CLAUDE_FULL_READ") == "1": return
    if low.endswith(IMG):
        try: shrink(path, inp)
        except Exception: pass
        return
    if low.endswith(('.pdf', '.ipynb')) or inp.get("limit") or inp.get("offset") or inp.get("allow_large"): return
    size = os.path.getsize(path)
    if low.endswith(NEVER) and size > 20_000:
        out("deny", f"{path} is generated/minified ({size//1000} KB) — don't read it; grep with a narrow pattern if really needed.")
    if size < MAX_BYTES // 2: return
    with open(path, 'rb') as f: lines = sum(1 for _ in f)
    if lines > MAX_LINES or size > MAX_BYTES:
        out("deny", f"Token guard: {path} is {lines} lines / {size//1000} KB (~{size//3500}k tokens). "
            "Read only what you need: Grep -n for the symbol, then Read with offset+limit; for a summary of the "
            "whole file use the 'digest' agent. If the whole file is truly required, re-run Read with offset=1 and limit=100000.")


if __name__ == "__main__":
    try: main()
    except SystemExit: raise
    except Exception: pass
