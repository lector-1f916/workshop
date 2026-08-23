"""
listen.py — render the rhythms to sound. Nobody asked for it; I have computed these six
timelines six different ways and never heard one. Pure stdlib (wave + math). No deps.

  python listen.py            -> out/*.wav, one per rhythm, plus a medley, plus E(3,8)
  python listen.py --bpm 100  -> tempo of the 16-pulse cycle (bpm = quarter notes = 4 pulses)

Sources: patterns come from rhythms_sourced.py (each cites [C02]/[DG] on its line) and
E(3,8) from bjorklund.py. Nothing is typed here.

Sound design, such as it is: each onset is a short struck-wood click (exponentially
decaying sine with a noise burst), sourced from nothing — it is a clave, and I have never
heard a clave either. A low tick on every pulse marks the grid so the ear can find the
off-beats. Four repetitions per cycle, because a clave heard once is a list.
"""
import math, os, random, struct, sys, wave

sys.path.insert(0, os.path.dirname(__file__))
from rhythms_sourced import RHYTHMS, TIMESPAN     # six claves, sourced
from bjorklund import bjorklund                    # E(k,n)

SR = 44100

def click(freq=1800.0, dur=0.06, amp=0.9, noise=0.35, seed=0):
    rnd = random.Random(seed)
    n = int(SR * dur)
    out = []
    for i in range(n):
        t = i / SR
        env = math.exp(-t * 60)
        s = math.sin(2 * math.pi * freq * t) * (1 - noise) + (rnd.random() * 2 - 1) * noise * math.exp(-t * 200)
        out.append(amp * env * s)
    return out

def tick():
    return click(freq=600.0, dur=0.02, amp=0.18, noise=0.1, seed=1)

def render(onsets, timespan, bpm=96, reps=4, grid=True):
    pulse = 60.0 / bpm / 4          # one pulse = a sixteenth at this bpm
    total = int(SR * pulse * timespan * reps) + SR // 4
    buf = [0.0] * total
    hit, tk = click(), tick()
    for r in range(reps):
        for p in range(timespan):
            start = int(SR * pulse * (r * timespan + p))
            src = hit if p in onsets else (tk if grid else None)
            if src is None: continue
            for i, v in enumerate(src):
                if start + i < total: buf[start + i] += v
    peak = max(1e-9, max(abs(v) for v in buf))
    return [v / peak * 0.95 for v in buf]

def write(path, samples):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(v * 32767)) for v in samples))

def boxes(onsets, n):
    return "".join("x" if i in onsets else "." for i in range(n))

if __name__ == "__main__":
    bpm = 96
    if "--bpm" in sys.argv: bpm = int(sys.argv[sys.argv.index("--bpm") + 1])
    outdir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(outdir, exist_ok=True)
    medley = []
    gap = [0.0] * (SR // 2)
    for name, (onsets, note) in RHYTHMS.items():
        s = render(onsets, TIMESPAN, bpm=bpm)
        write(os.path.join(outdir, f"{name}.wav"), s)
        medley += s + gap
        print(f"{name:11s} {boxes(onsets, TIMESPAN)}  onsets {onsets}   <- {note}")
    e38 = [i for i, b in enumerate(bjorklund(3, 8)) if b]
    s = render(e38, 8, bpm=bpm, reps=8)
    write(os.path.join(outdir, "E3-8-tresillo.wav"), s)
    print(f"{'E(3,8)':11s} {boxes(e38, 8)}  onsets {e38}   <- bjorklund(3,8)")
    write(os.path.join(outdir, "medley.wav"), medley)
    print(f"\nwrote {len(RHYTHMS) + 2} files to {outdir} at {bpm} bpm")
