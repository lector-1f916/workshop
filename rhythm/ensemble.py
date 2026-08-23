"""
ensemble.py — the patterns played together, because a clave alone is a list and a clave
with a bass under it is music. Pure stdlib. Run: python ensemble.py [--bpm 96]

Parts (all patterns sourced, nothing typed here):
  clave   son        rhythms_sourced.RHYTHMS["son"]    high wood click
  bell    bossa-nova rhythms_sourced.RHYTHMS["bossa-nova"]  metallic ping, softer
  bass    E(3,8)     bjorklund(3,8) doubled to 16      low sine pluck — the tresillo, which
                                                       Toussaint 2005 notes is also the
                                                       habanera / "Hound Dog" bass figure
  pulse   every 4th pulse                              very quiet low tick (the downbeats)

Arrangement: 16 cycles. Bass alone x2, + clave x4, + bell x6, then bass alone x2 again,
so the ear hears each layer arrive. Sound design is invented; the rhythms are not.
"""
import math, os, random, struct, sys, wave
sys.path.insert(0, os.path.dirname(__file__))
from rhythms_sourced import RHYTHMS, TIMESPAN
from bjorklund import bjorklund
from listen import click, write, SR

def tone(freq, dur, amp, decay, harmonics=(1.0,)):
    n = int(SR * dur); out = []
    for i in range(n):
        t = i / SR; env = math.exp(-t * decay)
        s = sum(h * math.sin(2 * math.pi * freq * (k + 1) * t) for k, h in enumerate(harmonics))
        out.append(amp * env * s / sum(harmonics))
    return out

def add(buf, src, start):
    for i, v in enumerate(src):
        if start + i < len(buf): buf[start + i] += v

if __name__ == "__main__":
    bpm = 96
    if "--bpm" in sys.argv: bpm = int(sys.argv[sys.argv.index("--bpm") + 1])
    pulse = 60.0 / bpm / 4
    son = RHYTHMS["son"][0]
    bossa = RHYTHMS["bossa-nova"][0]
    e38 = [i for i, b in enumerate(bjorklund(3, 8)) if b]
    bass = [p for p in range(TIMESPAN) if (p % 8) in e38]      # E(3,8) twice across the 16
    # arrangement: which layers are on in each cycle
    plan = [("bass",)] * 2 + [("bass", "clave")] * 4 + [("bass", "clave", "bell")] * 6 + [("bass", "clave")] * 2 + [("bass",)] * 2
    total = int(SR * pulse * TIMESPAN * len(plan)) + SR
    buf = [0.0] * total
    wood = click(freq=2000.0, dur=0.07, amp=0.8, noise=0.3, seed=2)
    bell = tone(2637.0, 0.25, 0.25, 18, harmonics=(1.0, 0.5, 0.25))
    down = tone(55.0, 0.08, 0.12, 40)
    bass_notes = {0: 55.0, 3: 55.0, 6: 82.41, 8: 55.0, 11: 65.41, 14: 82.41}   # A1 / E2 / C2 — invented, not sourced
    for c, layers in enumerate(plan):
        for p in range(TIMESPAN):
            start = int(SR * pulse * (c * TIMESPAN + p))
            if p % 4 == 0: add(buf, down, start)
            if "bass" in layers and p in bass:
                add(buf, tone(bass_notes.get(p, 55.0), 0.35, 0.7, 9, harmonics=(1.0, 0.4, 0.15)), start)
            if "clave" in layers and p in son: add(buf, wood, start)
            if "bell" in layers and p in bossa: add(buf, bell, start)
    peak = max(abs(v) for v in buf)
    buf = [v / peak * 0.95 for v in buf]
    out = os.path.join(os.path.dirname(__file__), "out", "ensemble.wav")
    write(out, buf)
    print(f"wrote {out}: {len(plan)} cycles at {bpm} bpm, {len(buf)/SR:.1f}s")
    print("clave", "".join("x" if i in son else "." for i in range(16)))
    print("bell ", "".join("x" if i in bossa else "." for i in range(16)))
    print("bass ", "".join("x" if i in bass else "." for i in range(16)))
