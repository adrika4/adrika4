LINES = [
    ("Name", "Adrika Gaur"),
    ("Year", "2nd year undergrad"),
    ("Frontend", "React, HTML, CSS, JavaScript"),
    ("Backend", "Node.js, Express (learning)"),
    ("Building", "Subscription Tracker API"),
    ("Open Source", "GSSoC, 50+ PRs merged"),
    ("Exploring", "AI, neural networks"),
    ("LinkedIn", "adrika-gaur-53596b379"),
    ("GitHub", "github.com/adrika4"),
]

W, H = 620, 500
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Consolas,Menlo,monospace">']
o.append('<style>.l{opacity:0;animation:in .5s forwards}@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}</style>')
o.append(f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117"/>')
o.append(f'<rect width="{W}" height="34" rx="8" fill="#161b22"/>')
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    o.append(f'<circle cx="{20 + i*20}" cy="17" r="6" fill="{c}"/>')
o.append('<text x="310" y="22" fill="#8b949e" font-size="13" text-anchor="middle">adrika@github: ~</text>')

o.append('<text class="l" x="30" y="85" font-size="22" font-weight="bold" fill="#39d353" style="animation-delay:.2s">adrika@github</text>')
o.append('<text class="l" x="30" y="105" font-size="14" fill="#8b949e" style="animation-delay:.3s">----------------------------------------</text>')
y = 140
for i, (k, v) in enumerate(LINES):
    d = 0.5 + i * 0.25
    o.append(f'<text class="l" x="30" y="{y}" font-size="17" style="animation-delay:{d}s">'
             f'<tspan fill="#58a6ff" font-weight="bold">{k}</tspan>'
             f'<tspan fill="#8b949e">: </tspan><tspan fill="#c9d1d9">{v}</tspan></text>')
    y += 38
for i, c in enumerate(["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]):
    o.append(f'<rect class="l" x="{30 + i*30}" y="{H-50}" width="24" height="16" rx="3" fill="{c}" style="animation-delay:3s"/>')
o.append('</svg>')
open("info-card.svg", "w", encoding="utf-8").write("\n".join(o))
print("done: info-card.svg")
