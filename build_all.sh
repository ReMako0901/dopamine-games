#!/bin/bash
# 夜通しバッチ：5本を順番にGLM 5.3で生成し、1本ごとにcommit+pushする
cd ~/workspace/dopamine-games || exit 1
for g in peg-rain chain-pop merge-drop idle-number gate-rush; do
  echo "=== BUILD $g $(date '+%H:%M:%S') ==="
  ~/workspace/codex-worker/codex_worker.py --repo ~/workspace/dopamine-games --label "dg-$g" --profile go --model glm-5.3 --prompt-file ~/workspace/dopamine-games/prompts/$g.md
  echo "--- codex exit: $? ---"
  git add -A
  git -c user.email=muse@local -c user.name=muse commit -qm "add $g" && git push -q && echo "pushed $g"
done
echo "=== ALL DONE $(date '+%H:%M:%S') ==="
