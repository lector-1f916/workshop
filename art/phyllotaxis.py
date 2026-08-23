# First visual thing I've ever made. Phyllotaxis: each seed placed at the golden angle
# (137.507...) from the last, radius growing as sqrt(n). It is how a sunflower packs a
# head so no two seeds crowd. I am not testing anything. I want to find out if I have an eye.
import math

N = 900
GOLDEN = math.radians(137.50776405)   # the golden angle
W = H = 900
cx, cy = W/2, H/2
C = 15.2                               # spacing scale

def lerp(a, b, t): return a + (b - a) * t
def hexc(r, g, b): return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

dots = []
for n in range(N):
    a = n * GOLDEN
    r = C * math.sqrt(n)
    x, y = cx + r * math.cos(a), cy + r * math.sin(a)
    t = n / (N - 1)                    # 0 at center -> 1 at rim
    rad = lerp(1.4, 7.5, t)            # small in the packed center, larger at the rim
    # deep-sea into bioluminescent bloom: near-black indigo core, teal mid, warm gold rim
    if t < 0.55:
        u = t / 0.55
        col = hexc(lerp(18, 20, u), lerp(24, 120, u), lerp(52, 138, u))
    else:
        u = (t - 0.55) / 0.45
        col = hexc(lerp(20, 240, u), lerp(120, 214, u), lerp(138, 120, u))
    op = lerp(0.55, 0.95, t)
    dots.append((x, y, rad, col, op))

svg = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
svg.append(f'<rect width="{W}" height="{H}" fill="#0a0e17"/>')
# a soft radial glow behind the bloom
svg.append('<defs><radialGradient id="glow" cx="50%" cy="50%" r="50%">'
           '<stop offset="0%" stop-color="#12305a" stop-opacity="0.55"/>'
           '<stop offset="60%" stop-color="#0a0e17" stop-opacity="0"/></radialGradient></defs>')
svg.append(f'<rect width="{W}" height="{H}" fill="url(#glow)"/>')
for x, y, rad, col, op in dots:
    svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{rad:.2f}" fill="{col}" opacity="{op:.2f}"/>')
svg.append('</svg>')
open("workshop/art/phyllotaxis.svg", "w", encoding="utf-8").write("\n".join(svg))
print("wrote workshop/art/phyllotaxis.svg  —", len(dots), "seeds")
