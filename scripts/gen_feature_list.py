import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "features.json"
OUT = ROOT / "docs" / "feature-list.md"

d = json.loads(DATA.read_text(encoding="utf-8"))
host = d["site"]["host"].rstrip("/")
lines = ["# 功能清单（按原站分类整理）", "", f"站点：{d['site']['name']}（{host}）", ""]
n = 0
for c in d["categories"]:
    lines.append(f"## {c['name']}")
    lines.append("")
    lines.append("| # | 功能 | 类型 | 原站地址 | 说明 |")
    lines.append("|---|---|---|---|---|")
    for i, f in enumerate(c["features"], 1):
        n += 1
        kind = "本地工具" if f["kind"] == "local" else "在线直达"
        lines.append(f"| {i} | {f['name']} | {kind} | {host}{f['url']} | {f['desc']} |")
    lines.append("")

lines.append("## 本地工具（客户端内置）")
lines.append("")
for f in d["local_tools"]:
    n += 1
    lines.append(f"- **{f['name']}**：{f['desc']}")
lines.append("")
lines.append(f"合计：{len(d['categories'])} 个一级分类、{n} 项功能。")
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"written {OUT} ({n} features)")
