"""فيديو → صورة لقطات مرقّمة بالوقت + كلام الصوت مكتوب، عشان Claude "يشوف ويسمع" الفيديو.
Works on Windows/Linux/Mac. First run installs what's missing (faster-whisper, imageio-ffmpeg, pillow)
and downloads the speech model once (~460 MB for "small", from huggingface.co).

usage: python tools/video_view.py VIDEO [--frames 12] [--out out/video] [--model small] [--lang ar] [--no-audio]
"""
import argparse, os, re, shutil, subprocess, sys, tempfile


def need(mod, pkg):
    try:
        return __import__(mod)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])
        return __import__(mod)


def ffmpeg_exe():
    return shutil.which("ffmpeg") or need("imageio_ffmpeg", "imageio-ffmpeg").get_ffmpeg_exe()


def duration(ff, video):
    err = subprocess.run([ff, "-i", video], capture_output=True, text=True, errors="ignore").stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def hms(t):
    return f"{int(t // 60):02d}:{t % 60:04.1f}"


def sheet(ff, video, n, dst):
    need("PIL", "pillow")
    from PIL import Image, ImageDraw, ImageFont
    dur = duration(ff, video)
    tmp = tempfile.mkdtemp()
    tiles = []
    try:
        font = ImageFont.load_default(size=22)
    except TypeError:  # Pillow < 10.1
        font = ImageFont.load_default()
    for i in range(n):
        t = dur * (i + 0.5) / n
        f = os.path.join(tmp, f"{i}.jpg")
        subprocess.run([ff, "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", video,
                        "-frames:v", "1", "-vf", "scale=360:-2", f], check=True)
        im = Image.open(f).convert("RGB")
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 92, 28], fill="black")
        d.text((4, 2), hms(t), fill="yellow", font=font)
        tiles.append(im)
    shutil.rmtree(tmp, ignore_errors=True)
    cols = min(4, n)
    rows = -(-n // cols)
    w, h = tiles[0].size
    out = Image.new("RGB", (cols * (w + 4), rows * (h + 4)), "black")
    for i, im in enumerate(tiles):
        out.paste(im, ((i % cols) * (w + 4), (i // cols) * (h + 4)))
    out.save(dst, quality=80)
    return dur


def transcript(video, model, lang, dst):
    fw = need("faster_whisper", "faster-whisper")
    m = fw.WhisperModel(model, device="cpu", compute_type="int8")
    segs, info = m.transcribe(video, language=lang, vad_filter=True)
    lines = [f"[{hms(s.start)}] {s.text.strip()}" for s in segs]
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return info.language, lines


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("--frames", type=int, default=12)
    p.add_argument("--out", default="out/video")
    p.add_argument("--model", default="small")
    p.add_argument("--lang", default=None, help="ar, en ... (default: auto)")
    p.add_argument("--no-audio", action="store_true")
    a = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(a.out, exist_ok=True)
    name = os.path.splitext(os.path.basename(a.video))[0]
    ff = ffmpeg_exe()
    img = os.path.join(a.out, name + "_sheet.jpg")
    dur = sheet(ff, a.video, a.frames, img)
    print(f"duration={dur:.1f}s frames={a.frames} -> {img}")
    if a.no_audio:
        return
    txt = os.path.join(a.out, name + "_speech.txt")
    try:
        lang, lines = transcript(a.video, a.model, a.lang, txt)
        print(f"speech ({lang}, {len(lines)} lines) -> {txt}")
        print("\n".join(lines[:60]) or "(no speech)")
        if len(lines) > 60:
            print(f"... {len(lines) - 60} more lines in the file")
    except Exception as e:
        print(f"speech: FAILED ({type(e).__name__}: {str(e)[:200]})")


if __name__ == "__main__":
    main()
