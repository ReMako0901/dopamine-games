# index.html を再生成する：定番6本＋存在する gNNN.html を manifest の名前で並べる
import os

ORIGINALS = [
 ("https://remako0901.github.io/number-burst/", "NUMBER BURST", "玉が壁に当たるたび増殖する。無限。"),
 ("peg-rain.html", "PEG RAIN", "落ちる玉がペグで増えて、皿の倍率でスコア爆発。"),
 ("chain-pop.html", "CHAIN POP", "1個タップで連鎖爆発。深い連鎖ほど跳ねる。"),
 ("merge-drop.html", "MERGE DROP", "同じ数字が合体して2倍に育つ。桁が増える。"),
 ("idle-number.html", "IDLE NUMBER", "放置で数字が加速しながら増え続ける。"),
 ("gate-rush.html", "GATE RUSH", "×2ゲートをくぐるたび玉が倍になる流れ。"),
]

titles = {}
if os.path.exists("manifest.tsv"):
    for line in open("manifest.tsv", encoding="utf-8"):
        parts = line.rstrip("\n").split("\t")
        if len(parts) == 2:
            titles[parts[0]] = parts[1]

items = []
for href, name, desc in ORIGINALS:
    items.append(f'<a href="{href}"><b>{name}</b><span>{desc}</span></a>')
count = 0
for i in range(1, 101):
    fname = f"g{i:03d}.html"
    if os.path.exists(fname):
        count += 1
        items.append(f'<a href="{fname}"><b>{titles.get(fname, fname)}</b><span>{fname}</span></a>')

html = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>DOPAMINE GAMES</title>
<style>
  :root {{ color-scheme: dark; }}
  * {{ margin: 0; box-sizing: border-box; }}
  body {{ background: #0a0a0f; color: #f2f2f2; font-family: system-ui, sans-serif; padding: 32px 20px; }}
  h1 {{ font-size: 28px; font-weight: 900; letter-spacing: .08em; margin-bottom: 8px; }}
  p {{ color: #9a9aad; font-size: 13px; margin-bottom: 24px; }}
  a {{ display: block; padding: 16px; margin-bottom: 10px; background: #16161f; border: 1px solid #2a2a38; border-radius: 12px; color: #f2f2f2; text-decoration: none; }}
  a b {{ font-size: 18px; display: block; margin-bottom: 2px; }}
  a span {{ font-size: 12px; color: #9a9aad; }}
</style>
</head>
<body>
<h1>DOPAMINE GAMES</h1>
<p>量産分 {count} / 100 本</p>
{chr(10).join(items)}
</body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(html)
print(f"menu updated: {count} mass-produced games listed")
