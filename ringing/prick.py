"""prick.py — a one-ink print of a pricked peal: the 1668 Grandsire 120 with the treble's
path cut through the figures, and the two rules "drawn between the figures" at the singles.

Writes workshop/cuts/prickt-1668.svg in the cuts workshop's idiom (one ink #1a1612 on paper
#f2ead8, no second colour). Rows come from the engine (fixtures prove they equal the book's).
"""
from changes import GRANDSIRE_DOUBLES as GS, fmt

INK, PAPER = "#1a1612", "#f2ead8"
rows = [fmt(r) for r in GS.ring("p-p-ps" * 2)]          # 121 rows
singles_after = [60, 120]                                # where the book rules its lines

W, H = 600, 800
COLS = 3
per_col = 41                                             # 121 rows -> 41 / 40 / 40
col_x = [80, 260, 440]
top, step = 70, 15.6
cell = 20
font = 12

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
       '  <!-- "The line drawn between the figures." One ink. The Sixscore of Grandsire on five bells as',
       '       pricked in Tintinnalogia (1668, Gutenberg #18567, lines 4532-4656), the treble cut through it,',
       '       and the two rules the book draws before each single. Rows from workshop/ringing/changes.py,',
       '       which fixtures.py proves equal to the book. lector, 2026-08-22, workshop/cuts. -->',
       f'  <rect width="{W}" height="{H}" fill="{PAPER}"/>']

# the figures
out.append(f'  <g font-family="Georgia, serif" font-size="{font}" fill="{INK}">')
positions = {}   # (row index) -> (x0, y) for the row's first cell
k = 0
for c in range(COLS):
    n = per_col if c == 0 else per_col - 1
    for i in range(n):
        if k >= len(rows):
            break
        y = top + i * step
        x0 = col_x[c]
        positions[k] = (x0, y)
        for j, ch in enumerate(rows[k]):
            if ch == "1":
                continue          # the treble is the line, not a figure; a real blue line omits it
            out.append(f'    <text x="{x0 + j * cell}" y="{y:.1f}" text-anchor="middle">{ch}</text>')
        k += 1
out.append('  </g>')

# the rules before each single: a heavy line across the five figures
for s in singles_after:
    if s in positions:
        x0, y = positions[s]
        out.append(f'  <rect x="{x0 - cell * 0.7:.1f}" y="{y - step + 4:.1f}" width="{cell * 5.4:.1f}" height="3" fill="{INK}"/>')

# the treble's path, cut heavy, one polyline per column
for c in range(COLS):
    pts = []
    for k, (x0, y) in positions.items():
        if x0 != col_x[c]:
            continue
        j = rows[k].index("1")
        pts.append(f"{x0 + j * cell},{y - font * 0.35:.1f}")
    out.append(f'  <polyline points="{" ".join(pts)}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>')
# the half hunt (the tenor), cut light
for c in range(COLS):
    pts = []
    for k, (x0, y) in positions.items():
        if x0 != col_x[c]:
            continue
        j = rows[k].index("5")
        pts.append(f"{x0 + j * cell},{y - font * 0.35:.1f}")
    out.append(f'  <polyline points="{" ".join(pts)}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>')

# title, bottom, paper on an ink bar
out.append(f'  <rect x="0" y="728" width="{W}" height="72" fill="{INK}"/>')
out.append(f'  <text x="300" y="758" text-anchor="middle" font-family="Georgia, serif" font-size="18" letter-spacing="3" fill="{PAPER}">THE LINE DRAWN BETWEEN THE FIGURES</text>')
out.append(f'  <text x="300" y="782" text-anchor="middle" font-family="Georgia, serif" font-size="11" letter-spacing="2" fill="{PAPER}">GRANDSIRE ON FIVE BELLS · SIXSCORE · 1668</text>')
out.append('</svg>')

path = "../cuts/prickt-1668.svg"
open(path, "w", encoding="utf8", newline="\n").write("\n".join(out))
print("wrote", path, len(rows), "rows")
