#!/bin/bash
# 100本量産バッチ：5本ずつGLMで生成→メニュー更新→commit+push。週次クォータが尽きたら止まる。
cd ~/workspace/dopamine-games || exit 1
for b in $(seq -w 1 20); do
  # 週次使用率チェック（95%以上なら停止）
  week=$(~/workspace/custom-connectors/custom.opencode-go/bin/go_usage.py 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['usage']['weekly']['percent'])" 2>/dev/null)
  echo "batch $b weekly usage: ${week:-unknown}%"
  if [ -n "$week" ] && python3 -c "exit(0 if float('$week') >= 95 else 1)"; then
    echo "QUOTA STOP at batch $b"
    break
  fi
  echo "=== BATCH $b $(date '+%H:%M:%S') ==="
  ~/workspace/codex-worker/codex_worker.py --repo ~/workspace/dopamine-games --label "dg100-b$b" --profile go --model glm-5.3 --prompt-file ~/workspace/dopamine-games/prompts100/batch-$b.md
  echo "--- codex exit: $? ---"
  python3 gen_menu.py
  git add -A
  git -c user.email=muse@local -c user.name=muse commit -qm "batch $b" && git push -q && echo "pushed batch $b"
done
echo "=== FACTORY DONE $(date '+%H:%M:%S') ==="
ls g*.html 2>/dev/null | wc -l
