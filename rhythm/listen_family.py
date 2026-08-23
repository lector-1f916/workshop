"""
listen_family.py — FINDING-007 Addendum 3 for the ear.

Son, rumba and gahu are the same five intervals {2,3,3,4,4} in three orders, and that
multiset is one of only two (of 32) where the Longuet-Higgins & Lee syncopation index
cannot tell any arrangement from its mirror at any starting point. This plays the three
in a row, four cycles each, with a low thud on the one of every cycle so the downbeat —
the thing the syncopation measure is about — is audible. Then the three mirrors.

Patterns come from rhythms_sourced.py (each line cites its paper). Nothing typed here.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from rhythms_sourced import RHYTHMS, TIMESPAN
from listen import render, write, boxes, SR
from syncopation import mirror, lhl

def thud(freq=70.0, dur=0.12, amp=0.8):
    n = int(SR * dur)
    return [amp * math.sin(2 * math.pi * freq * i / SR) * (1 - i / n) ** 2 for i in range(n)]

def with_downbeat(samples, timespan, bpm=96, reps=4):
    pulse = 60.0 / bpm / 4
    out = list(samples)
    th = thud()
    for r in range(reps):
        start = int(SR * pulse * r * timespan)
        for i, v in enumerate(th):
            if start + i < len(out):
                out[start + i] += v
    peak = max(1e-9, max(abs(v) for v in out))
    return [v / peak * 0.95 for v in out]

if __name__ == "__main__":
    outdir = os.path.join(os.path.dirname(__file__), "out")
    gap = [0.0] * (SR // 2)
    named, mirrored = [], []
    for name in ("son", "rumba", "gahu"):
        on, _ = RHYTHMS[name]
        m = mirror(on)
        named += with_downbeat(render(on, TIMESPAN), TIMESPAN) + gap
        mirrored += with_downbeat(render(m, TIMESPAN), TIMESPAN) + gap
        print(f"{name:6s} {boxes(on, TIMESPAN)} LHL {lhl(on)}   mirror {boxes(m, TIMESPAN)} LHL {lhl(m)}")
    write(os.path.join(outdir, "family-son-rumba-gahu.wav"), named)
    write(os.path.join(outdir, "family-mirrors.wav"), mirrored)
    print("out/family-son-rumba-gahu.wav, out/family-mirrors.wav — thud = the one.")
