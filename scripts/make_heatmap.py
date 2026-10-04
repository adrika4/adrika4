import json, os, re, requests
from datetime import date
from bs4 import BeautifulSoup

USER = "adrika4"
html = requests.get(f"https://github.com/users/{USER}/contributions",
                    headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
soup = BeautifulSoup(html, "html.parser")
tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}

days = []
for td in soup.select("td[data-date]"):
    m = re.match(r"(\d+)", tips.get(td.get("id"), ""))
    lvl = int(td.get("data-level", 0))
    cnt = int(m.group(1)) if m else (1 if lvl else 0)
    days.append({"date": td["data-date"], "level": lvl, "count": cnt})
days.sort(key=lambda d: d["date"])

def count(q):
    h = {"Accept": "application/vnd.github+json", "User-Agent": "profile-art"}
    if os.environ.get("GITHUB_TOKEN"):
        h["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    try:
        r = requests.get("https://api.github.com/search/issues", params={"q": q, "per_page": 1}, headers=h, timeout=30)
        return r.json()["total_count"]
    except Exception:
        return 0

prs = count(f"author:{USER} type:pr")
merged = count(f"author:{USER} type:pr is:merged")

total = sum(d["count"] for d in days)
best = run = 0
for d in days:
    run = run + 1 if d["count"] else 0
    best = max(best, run)
cur = 0
for i, d in enumerate(reversed(days)):
    if d["count"]:
        cur += 1
    elif i == 0:
        continue
    else:
        break

json.dump({"total": total, "current": cur, "longest": best, "days": days},
          open("data/contributions.json", "w"))

PAL = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
C, G, W = 12, 3.2, 860
P = C + G
off = (date.fromisoformat(days[0]["date"]).weekday() + 1) % 7
cols = (len(days) + off - 1) // 7 + 1
x0, y0 = (W - cols * P) / 2, 20
H = int(y0 + 7 * P + 70)

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Consolas,Menlo,monospace">']
o.append('<style>.b{opacity:0;animation:s .4s forwards}@keyframes s{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}</style>')
o.append(f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117"/>')
for i, d in enumerate(days):
    col, row = divmod(i + off, 7)
    fill = "#69f0a0" if d["count"] >= 10 else PAL[d["level"]]
    o.append(f'<rect class="b" x="{x0 + col*P:.1f}" y="{y0 + row*P:.1f}" width="{C}" height="{C}" rx="3" fill="{fill}" style="animation-delay:{(col+row)*0.025:.2f}s"/>')
fy = y0 + 7 * P + 38
o.append(f'<text x="{x0:.0f}" y="{fy:.0f}" font-size="14" fill="#8b949e">{total} contributions | {prs} PRs ({merged} merged) | streak {cur} | best {best}</text>')
lx = W - x0 - 190
o.append(f'<text x="{lx:.0f}" y="{fy:.0f}" font-size="12" fill="#8b949e">Less</text>')
for i, c in enumerate(PAL + ["#69f0a0"]):
    o.append(f'<rect x="{lx + 34 + i*17:.0f}" y="{fy-11:.0f}" width="12" height="12" rx="3" fill="{c}"/>')
o.append(f'<text x="{lx + 142:.0f}" y="{fy:.0f}" font-size="12" fill="#8b949e">More</text>')
o.append('</svg>')
open("contrib-heatmap.svg", "w", encoding="utf-8").write("\n".join(o))
print(f"done: {total} contributions, current streak {cur}, longest {best}")
