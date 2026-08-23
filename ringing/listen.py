"""listen.py — render a touch as a WAV so a person can hear whether a 120 sounds like one.

Usage:  python listen.py "Plain Bob Doubles" "ppp-ppp-ppp-" out/pb-120.wav
        python listen.py "Grandsire Doubles" "p-p-psp-p-ps" out/gs-120.wav

Timing rule, sourced: en.wikipedia.org/wiki/Change_ringing (raw wikitext, fetched 2026-08-22):
  "It is the custom to leave a pause of one beat after every alternate row, i.e., after the
   ringing of each 'backstroke' row. This is called 'open handstroke' ringing"
So: rows alternate handstroke/backstroke; after each backstroke row, one empty beat.

Pitches, SOURCED (2026-08-22T21:0xZ, after the first renders went out with a from-memory
tuning): Tintinnalogia (1668), "Of the Beginning of Changes", sources/tintinnalogia-pg18567.txt
lines 233-248: "begin at the Tenor, or biggest Bell, and count 3 whole Notes, then a half Note,
or Sharp, 3 whole Notes, then a half Note ... On Six, 123:456 the half Note or Sharp is between
3 and 4." Counting up from the tenor: whole, whole, half, whole, whole — the first six notes of
a major scale with the TENOR as the keynote, treble on the sixth. In C: tenor C4, then D E F G,
treble A4. My first version had the treble on the eighth (C B A G F E), from memory, and was
wrong by the book's rule. The cover bell is the tenor (Wikipedia's Grandsire article: "normally
a cover bell ringing in last place at each row"); the five working bells are A G F E D.
Bell tone: a decaying sum of partials with a flat-ish minor-third "tierce" (from memory, the
tierce is the famous minor third in a bell's spectrum; unsourced here, purely for the ear).
"""
import math
import os
import struct
import sys
import wave

from changes import METHODS, prove, fmt

RATE = 44100
BEAT = 0.21          # seconds between strikes; ~peal speed for a light six is a guess, not sourced
NOTES = {"A4": 440.0, "G4": 392.0, "F4": 349.23, "E4": 329.63, "D4": 293.66, "C4": 261.63}   # equal temperament, A4=440
RING = ["A4", "G4", "F4", "E4", "D4", "C4"]   # bells 1..5 + tenor cover (6); Tintinnalogia 1668 rule, see docstring


def bell(freq, seconds=1.6):
    n = int(RATE * seconds)
    out = [0.0] * n
    # partials: hum (0.5), prime (1), tierce (1.2 = minor third), quint (1.5), nominal (2)
    for mult, amp, decay in ((0.5, 0.35, 0.9), (1.0, 0.5, 1.4), (1.2, 0.3, 1.8), (1.5, 0.15, 2.5), (2.0, 0.25, 3.5)):
        w = 2 * math.pi * freq * mult / RATE
        for i in range(n):
            t = i / RATE
            out[i] += amp * math.sin(w * i) * math.exp(-decay * t * 1.6)
    return out


def render(rows, with_cover=True):
    stage = len(rows[0])
    bells = {b: bell(NOTES[RING[b - 1]]) for b in range(1, stage + 1)}
    cover = bell(NOTES[RING[stage]]) if with_cover else None
    per_row = stage + (1 if with_cover else 0)
    t = 0.0
    events = []
    for k, row in enumerate(rows):
        for pos, b in enumerate(row):
            events.append((t + pos * BEAT, bells[b]))
        if with_cover:
            events.append((t + stage * BEAT, cover))
        t += per_row * BEAT
        if k % 2 == 1:           # after each backstroke row, one open beat
            t += BEAT
    total = int(RATE * (t + 2.0))
    buf = [0.0] * total
    for start, smp in events:
        s0 = int(start * RATE)
        for i, v in enumerate(smp):
            if s0 + i < total:
                buf[s0 + i] += v
    peak = max(1e-9, max(abs(v) for v in buf))
    return [v / peak * 0.9 for v in buf]


def write_wav(path, samples):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(v * 32767)) for v in samples))


if __name__ == "__main__":
    name, calling, out = sys.argv[1], sys.argv[2], sys.argv[3]
    m = METHODS[name]
    rows = m.ring(calling)
    p = prove(rows)
    print(f"{m.name} {calling!r}: {p.length} rows, true={p.true}, round={p.comes_round}")
    if not (p.true and p.comes_round):
        print("refusing to render a false touch; fix the calling first")
        sys.exit(1)
    # ring rounds twice first, as a band would, then the touch, then rounds once
    seq = [rows[0], rows[0]] + rows[1:] + [rows[-1]]
    write_wav(out, render(seq))
    print("wrote", out, f"{len(seq)} rows")
