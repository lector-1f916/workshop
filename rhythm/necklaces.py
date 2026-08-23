"""
necklaces.py — the six claves and their mirror twins as necklace polygons (Toussaint's
own figure style: onsets on a 16-point clock, joined into a polygon). Pure stdlib SVG.
Patterns from rhythms_sourced.py (sourced) and listen_twins.PRINTED (asserted against
FINDING-006). A mirror image is a reflection of the polygon across the vertical axis —
which you can see, and the evenness measure cannot.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from rhythms_sourced import RHYTHMS, TIMESPAN
from listen_twins import PRINTED

def pts(onsets, cx, cy, r, n=TIMESPAN):
    out = []
    for p in onsets:
        a = -math.pi / 2 + 2 * math.pi * p / n
        out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out

def necklace(onsets, cx, cy, r, label, sub, n=TIMESPAN):
    s = []
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#999" stroke-width="1"/>')
    for p in range(n):
        a = -math.pi / 2 + 2 * math.pi * p / n
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.2 if p % 4 else 3.4}" fill="#bbb"/>')
    P = pts(onsets, cx, cy, r)
    s.append('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in P) + '" fill="#d9534f" fill-opacity="0.12" stroke="#d9534f" stroke-width="2"/>')
    for x, y in P:
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#d9534f"/>')
    s.append(f'<text x="{cx}" y="{cy + r + 22}" text-anchor="middle" font-family="Georgia,serif" font-size="15">{label}</text>')
    s.append(f'<text x="{cx}" y="{cy + r + 38}" text-anchor="middle" font-family="monospace" font-size="11" fill="#666">{sub}</text>')
    return "\n".join(s)

def boxes(onsets, n=TIMESPAN):
    return "".join("x" if i in onsets else "." for i in range(n))

if __name__ == "__main__":
    R, W = 58, 170
    names = list(RHYTHMS)
    rows = []
    # row 1: the six
    for i, name in enumerate(names):
        on = RHYTHMS[name][0]
        rows.append(necklace(on, W * i + 95, 100, R, name, boxes(on)))
    # row 2: the three chiral ones next to their twins
    x = 95
    for name in ["rumba", "gahu", "soukous"]:
        on = RHYTHMS[name][0]
        tw = [i for i, c in enumerate(PRINTED[name]) if c == "x"]
        rows.append(necklace(on, x, 300, R, name, boxes(on))); x += W
        rows.append(necklace(tw, x, 300, R, "its mirror", boxes(tw))); x += W + 30
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W*6+40}" height="420" viewBox="0 0 {W*6+40} 420">
<rect width="100%" height="100%" fill="white"/>
<text x="20" y="26" font-family="Georgia,serif" font-size="16">Six 4/4 clave/bell timelines as necklaces (Toussaint 2002). Sixteen pulses, clockwise from the top.</text>
{chr(10).join(rows[:6])}
<text x="20" y="226" font-family="Georgia,serif" font-size="16">The three that are not palindromes, each beside the mirror image no tradition in the set selected. Same evenness score, by construction.</text>
{chr(10).join(rows[6:])}
</svg>'''
    out = os.path.join(os.path.dirname(__file__), "out", "necklaces.svg")
    open(out, "w", encoding="utf8").write(svg)
    print("wrote", out)
