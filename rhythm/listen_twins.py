"""
listen_twins.py — A/B pairs for FINDING-006 Result 2. Each chiral clave next to the
equally-even mirror image no tradition in Toussaint's six selected. Evenness cannot tell
them apart. Can an ear? I cannot run this test; whoever can, the files are in out/twins/.

Each file: 4 cycles of the named rhythm, half a second of silence, 4 cycles of its twin.
The twin is COMPUTED here as the reflection of the sourced pattern (reverse the boxes,
rotate so an onset sits at 0) and then asserted against the box strings printed in
FINDING-006-the-whole-curve.md, so the finding and the audio cannot drift apart.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from rhythms_sourced import RHYTHMS, TIMESPAN
from listen import render, write, boxes, SR

PRINTED = {  # FINDING-006-the-whole-curve.md, Result 2 table
    "rumba":   "x.x..x...x..x...",
    "gahu":    "x.x...x...x..x..",
    "soukous": "xx...x..x..x....",
}

def mirror(onsets, n):
    bits = [1 if i in onsets else 0 for i in range(n)][::-1]
    k = bits.index(1)
    bits = bits[k:] + bits[:k]
    return [i for i, b in enumerate(bits) if b]

if __name__ == "__main__":
    outdir = os.path.join(os.path.dirname(__file__), "out", "twins")
    os.makedirs(outdir, exist_ok=True)
    for name, printed in PRINTED.items():
        onsets, note = RHYTHMS[name]
        tw = mirror(onsets, TIMESPAN)
        # same necklace? (FINDING-006 printed gahu's twin from a different onset; both are right)
        rots = {boxes(tw, TIMESPAN)[k:] + boxes(tw, TIMESPAN)[:k] for k in range(TIMESPAN)}
        assert printed in rots, (name, boxes(tw, TIMESPAN), printed)
        tw = [i for i, ch in enumerate(printed) if ch == "x"]   # render the rotation the finding printed
        a = render(onsets, TIMESPAN); b = render(tw, TIMESPAN)
        write(os.path.join(outdir, f"{name}-then-twin.wav"), a + [0.0] * (SR // 2) + b)
        write(os.path.join(outdir, f"twin-then-{name}.wav"), b + [0.0] * (SR // 2) + a)
        print(f"{name:8s} {boxes(onsets, TIMESPAN)}  |  twin {printed}   (asserted against FINDING-006)")
    print(f"\n6 files in {outdir}. Listening test: can you tell which half is the named one?")
