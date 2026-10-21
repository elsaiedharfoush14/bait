---
name: video-view
description: See AND hear a video (screen recording, bug video from the iPhone, any clip). Use whenever the user sends/points to a .mp4/.mov/.webm file.
---
Claude can't play video; turn it into one image + a text transcript.

1. `python tools/video_view.py <video>` (options: `--frames 12 --out out/video --model small --lang ar --no-audio`)
   → `out/video/<name>_sheet.jpg` (4 per row, time stamped) + `<name>_speech.txt` (`[mm:ss] text`, also printed).
   First run pip-installs `faster-whisper`, `imageio-ffmpeg`, `pillow` and downloads the model once (needs `huggingface.co`).
   Speech is local and free (Whisper on CPU); `--model medium` = better Egyptian, slower.
2. Read the JPG once. Need detail at a moment? one frame:
   `ffmpeg -v error -ss 7 -i <video> -frames:v 1 -vf scale=720:-2 out/video/t7.jpg`
3. Long video (>1 min): 12 frames first, then zoom with `-ss/-to`. Transcript tells you where to look.
If speech says FAILED (403) the host blocks `huggingface.co` → tell him to allow it, or run on his Windows PC.
