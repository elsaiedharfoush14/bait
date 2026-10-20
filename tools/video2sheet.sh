#!/usr/bin/env bash
# فيديو → صورة واحدة (contact sheet) فيها لقطات مرقّمة بالوقت، عشان Claude يقرأها كصورة.
# usage: tools/video2sheet.sh VIDEO [FRAMES=12] [OUTDIR=out/video]
set -euo pipefail
v="$1"; n="${2:-12}"; out="${3:-out/video}"; mkdir -p "$out"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
name=$(basename "${v%.*}")
cols=4; rows=$(( (n + cols - 1) / cols ))
# لقطة كل dur/n ثانية، عرض 360 بكسل، والوقت مكتوب على كل لقطة
ffmpeg -v error -y -i "$v" \
  -vf "fps=${n}/${dur},scale=360:-2,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=${cols}x${rows}:padding=4" \
  -frames:v 1 "$out/${name}_sheet.jpg"
echo "duration=${dur}s frames=$n -> $out/${name}_sheet.jpg"
