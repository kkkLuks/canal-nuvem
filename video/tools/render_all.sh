#!/bin/bash
cd /home/user/varig; mkdir -p render
for c in "$@"; do
  s=$(date +%s)
  (cd build/cap$c && /home/user/hf/node_modules/.bin/hyperframes render -o /home/user/varig/render/cap$c.mp4 -q looks -w 4 --fps 30 > /home/user/varig/render/cap$c.log 2>&1)
  echo "cap$c rc=$? $(( $(date +%s)-s ))s" >> render/status.txt
done
echo DONE >> render/status.txt
