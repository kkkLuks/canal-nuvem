#!/bin/bash
# junta os capítulos, coloca o áudio mixado e normaliza em -14 LUFS
set -e
cd /home/user/varig; mkdir -p final
: > final/list.txt
for c in 0 1 2 3 4 5 6 7 8; do echo "file '/home/user/varig/render/cap$c.mp4'" >> final/list.txt; done
ffmpeg -y -v error -f concat -safe 0 -i final/list.txt -c copy final/video-mudo.mp4
ffmpeg -y -v error -i final/video-mudo.mp4 -i build/mix.wav -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart final/varig-longo.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 final/varig-longo.mp4
