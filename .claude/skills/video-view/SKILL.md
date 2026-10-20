---
name: video-view
description: See a video (screen recording, bug video from the iPhone). Use whenever the user sends/points to a .mp4/.mov/.webm file.
---
Claude can't play video; turn it into one image and read that.

1. `tools/video2sheet.sh <video> [frames=12] [outdir=out/video]` → one JPG grid (4 per row, 360px, time stamped).
2. Read the JPG once. Need detail at a moment? Grab one frame:
   `ffmpeg -v error -ss 00:00:07 -i <video> -frames:v 1 -vf scale=720:-2 out/video/t7.jpg`
3. Long video (>1 min): start with 12 frames, zoom into the interesting range with `-ss/-to` + more frames.
No sound transcription (no whisper here) — ask him what was said if it matters.
