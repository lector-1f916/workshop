"""
rhythms_sourced.py — the six 4/4 clave/bell timelines, each SOURCED on its defining line.

Written 2026-08-22 to pay down FINDING-003, which was RETRACTED because I typed six
rhythms into a dict FROM MEMORY, got the Rumba wrong, and built two findings on it.
Rule now: every named rhythm cites a source on the line it is defined. No magic numbers.

Two papers, both on disk in this folder and re-extracted this session:
  [DG]  Demaine, Gomez-Martin, Meijer, Rappaport, Taslakian, Toussaint, Winograd, Wood,
        "The Distance Geometry of Music", arXiv:0705.4085. (state/tmp/distgeo.txt)
  [C02] Toussaint, "A Mathematical Analysis of African, Brazilian, and Cuban Clave
        Rhythms", 2002. (workshop/rhythm/clave2002.txt)

[C02] represents each rhythm by a reduced interval vector = (played inter-onset
intervals) minus 1 each (it counts SILENT pulses between onsets). So onsets are the
cumulative sum of (reduced_vector + 1), starting at 0, in a timespan of 16.
Cross-check: [DG] prints the Son explicitly as onsets {0,3,6,10,12}, distance sequence
(3,3,4,2,4) — and (3,3,4,2,4)-1 = (2,2,3,1,3) = [C02]'s Son. The two papers agree.
"""

TIMESPAN = 16

# name: (reduced_interval_vector_from_C02, source_note)
_REDUCED = {
    # [C02] line ~638: "Shiko (3 1 3 1 3)"
    "shiko":      ((3, 1, 3, 1, 3), "[C02] interval-vector (3 1 3 1 3)"),
    # [C02] line ~637: "Son (2 2 3 1 3)"; [DG] prints onsets {0,3,6,10,12} explicitly.
    "son":        ((2, 2, 3, 1, 3), "[C02] (2 2 3 1 3) + [DG] onsets {0,3,6,10,12}"),
    # [C02] line ~638: "Soukous (2 2 3 0 4)"
    "soukous":    ((2, 2, 3, 0, 4), "[C02] interval-vector (2 2 3 0 4)"),
    # [C02] line ~637: "Rumba (2 3 2 1 3)"  <-- the value FINDING-003 corrected to, now
    # sourced independently of the distance matrix that first caught the error.
    "rumba":      ((2, 3, 2, 1, 3), "[C02] interval-vector (2 3 2 1 3)"),
    # [DG] line ~1350: Bossa-Nova necklace (33334); reduced = (2 2 2 2 3).
    "bossa-nova": ((2, 2, 2, 2, 3), "[DG] necklace (33334), the maximally-even one"),
    # [C02] line ~637: "Gahu (2 2 3 3 1)"
    "gahu":       ((2, 2, 3, 3, 1), "[C02] interval-vector (2 2 3 3 1)"),
}

def _onsets(reduced):
    played = [x + 1 for x in reduced]
    assert sum(played) == TIMESPAN, (reduced, sum(played))
    out, t = [], 0
    for iv in played:
        out.append(t); t += iv
    return out

RHYTHMS = {name: (_onsets(rv), note) for name, (rv, note) in _REDUCED.items()}

if __name__ == "__main__":
    for name, (onsets, note) in RHYTHMS.items():
        played = [(onsets[(i+1) % 5] - onsets[i]) % TIMESPAN for i in range(5)]
        box = "".join("x" if i in onsets else "." for i in range(TIMESPAN))
        print(f"{name:11s} {onsets}  intervals {tuple(played)}  {box}   {note}")
