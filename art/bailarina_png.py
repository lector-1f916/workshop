# Raster twin of bailarina.py so the piece can be LOOKED AT on a machine with no cairo.
# Same math, same palette; PIL draws the circles. Supersampled 2x then downscaled.
import math
from PIL import Image, ImageDraw

PHI = (1 + math.sqrt(5)) / 2                 # golden ratio, computed
GOLDEN_DEG = 360 / PHI**2                    # 137.50776...°, computed
ANGLES = [GOLDEN_DEG - 0.5, GOLDEN_DEG, GOLDEN_DEG + 0.5]

N, C, HEAD = 700, 10.4, 640                  # as bailarina.py
W, H, SS = HEAD * 3, HEAD + 70, 2

def lerp(a, b, t): return a + (b - a) * t

img = Image.new("RGB", (W * SS, H * SS), (20, 10, 14))
d = ImageDraw.Draw(img)
for k, ang in enumerate(ANGLES):
    step = math.radians(ang)
    cx, cy = (HEAD * k + HEAD / 2) * SS, (HEAD / 2 + 20) * SS
    for n in range(N):
        a = n * step
        r = C * math.sqrt(n) * SS
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        t = n / (N - 1)
        rad = lerp(1.2, 5.6, t) * SS
        if t < 0.30:
            u = t / 0.30
            col = (int(lerp(246, 220, u)), int(lerp(240, 80, u)), int(lerp(232, 88, u)))
        else:
            u = (t - 0.30) / 0.70
            col = (int(lerp(220, 122, u)), int(lerp(80, 16, u)), int(lerp(88, 34, u)))
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=col)
img = img.resize((W, H), Image.LANCZOS)
img.save("workshop/art/bailarina.png")
print("wrote workshop/art/bailarina.png", img.size)
