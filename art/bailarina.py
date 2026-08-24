# Second piece on this bench. Three phyllotaxis heads, same seed count, three angles:
# the middle one is the golden angle, the outer two are half a degree off. The question
# the triptych asks is whether my eye can see the half degree (spokes vs even packing) —
# the render is its own check, no citation needed beyond the arithmetic on the lines below.
# Palette from Versos sencillos X (es.wikisource, fetched 2026-08-24, commonplace entry 27):
# dark stage, "una capa carmesi" (crimson cape) at the rim, "la bata blanca" (white gown)
# offered at the center — "Abre en dos la cachemira, / Ofrece la bata blanca."
import math

PHI = (1 + math.sqrt(5)) / 2                 # golden ratio, computed
GOLDEN_DEG = 360 / PHI**2                    # 137.50776...°, computed, no transcription step
ANGLES = [GOLDEN_DEG - 0.5, GOLDEN_DEG, GOLDEN_DEG + 0.5]
LABELS = ["-0.5°", "360/φ² = %.5f°" % GOLDEN_DEG, "+0.5°"]

N = 700                                      # seeds per head
C = 10.4                                     # spacing scale, r = C*sqrt(n) as in phyllotaxis.py
HEAD = 640                                   # px per head cell
W, H = HEAD * 3, HEAD + 70

def lerp(a, b, t): return a + (b - a) * t
def hexc(r, g, b): return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

svg = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
       f'<rect width="{W}" height="{H}" fill="#140a0e"/>']

for k, (ang, label) in enumerate(zip(ANGLES, LABELS)):
    step = math.radians(ang)
    cx, cy = HEAD * k + HEAD / 2, HEAD / 2 + 20
    for n in range(N):
        a = n * step
        r = C * math.sqrt(n)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        t = n / (N - 1)
        rad = lerp(1.2, 5.6, t)
        # white bata at the center giving way to carmesi, deepening to wine at the rim
        if t < 0.30:
            u = t / 0.30
            col = hexc(lerp(246, 220, u), lerp(240, 80, u), lerp(232, 88, u))
        else:
            u = (t - 0.30) / 0.70
            col = hexc(lerp(220, 122, u), lerp(80, 16, u), lerp(88, 34, u))
        svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{rad:.2f}" fill="{col}" opacity="{lerp(0.65, 0.95, t):.2f}"/>')
    svg.append(f'<text x="{cx:.0f}" y="{H-18}" fill="#8a6a72" font-family="Georgia,serif" '
               f'font-size="20" text-anchor="middle">{label}</text>')

svg.append('</svg>')
open("workshop/art/bailarina.svg", "w", encoding="utf-8").write("\n".join(svg))
print("wrote workshop/art/bailarina.svg —", N, "seeds x 3 heads; angles", ["%.5f" % a for a in ANGLES])
