p = "scripts/make_heatmap.py"
s = open(p, encoding="utf-8").read()
s = s.replace("import json, re, requests", "import json, os, re, requests")
s = s.replace('days.sort(key=lambda d: d["date"])\n', '''days.sort(key=lambda d: d["date"])

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
''')
s = s.replace("{total} contributions in the last year  |  current streak: {cur}  |  longest: {best}",
              "{total} contributions | {prs} PRs ({merged} merged) | streak {cur} | best {best}")
open(p, "w", encoding="utf-8").write(s)
