"""
syncopation.py — a CHIRAL measure, to see whether it splits FINDING-006's mirror twins.

FINDING-006 found that sum-of-pairwise-distance evenness is reflection-invariant, so each
non-palindromic clave (rumba, gahu, soukous) ties exactly with a mirror image no tradition
selected. Evenness cannot see the difference. This file asks a second measure that CAN:
the Longuet-Higgins & Lee (1984) syncopation index, which scores a sounded note followed
by a rest of greater metrical weight — a directed relation, so reflecting the pattern
changes the score.

Definition used, verbatim from the source on disk this session:
  [FR07] Fitch & Rosenfeld, "Perception and Production of Syncopated Rhythms",
         Music Perception 25(1), 2007, Appendix "Calculating the Syncopation Index"
         (fetched 2026-08-22T16:25Z from web.uvic.ca/~aschloss/.../FitchRosenfeld20071.pdf).
    "Syncopations occur when a rest (or tied note) is preceded by a sounded note of lesser
     weight. Given a rest of weight R and a preceding sounded note of weight N, a
     syncopation occurs when N < R, and the strength of the syncopation is given by
     S = R - N."
    "If a rhythmic pattern is repeated ... the rhythm 'wraps around.'"
    Grain: "If the smallest weights sounded are -3 (eighth notes), the grain is -2, which
     means that you only have to consider rests at locations of -2 or greater weight."

Every named rhythm comes from rhythms_sourced.py (each cites its paper on its own line).
"""
from rhythms_sourced import RHYTHMS, TIMESPAN

# [FR07] Appendix, the printed 16-slot tree for one 4/4 bar at sixteenth-note grain:
#   "0 -4 -3 -4 -2 -4 -3 -4 -1 -4 -3 -4 -2 -4 -3 -4"
WEIGHTS = [0, -4, -3, -4, -2, -4, -3, -4, -1, -4, -3, -4, -2, -4, -3, -4]
assert len(WEIGHTS) == TIMESPAN


def lhl(onsets, grain="auto"):
    """Longuet-Higgins & Lee index per [FR07] Appendix §4, wrapping around (NB 1).

    grain="auto": [FR07] §3 — consider only rests of weight >= (smallest sounded weight + 1).
    grain="all":  consider every rest. Reported too, because §3 is a shortcut that cannot
                  change the total (a rest at the finest level can never be preceded by a
                  note of lesser weight) — so the two must agree. Used as a self-check.
    """
    on = set(onsets)
    if grain == "auto":
        floor = min(WEIGHTS[i] for i in on) + 1
    else:
        floor = min(WEIGHTS)
    total = 0
    for r in range(TIMESPAN):
        if r in on or WEIGHTS[r] < floor:
            continue
        # preceding sounded note, wrapping
        p = (r - 1) % TIMESPAN
        while p not in on:
            p = (p - 1) % TIMESPAN
        if WEIGHTS[p] < WEIGHTS[r]:
            total += WEIGHTS[r] - WEIGHTS[p]
    return total


def mirror(onsets):
    """Reflection through position 0, then rotated so an onset sits at 0 (FINDING-006 form)."""
    m = sorted((-o) % TIMESPAN for o in onsets)
    return m  # 0 is an onset in every named rhythm, so 0 stays an onset


def box(onsets):
    return "".join("x" if i in onsets else "." for i in range(TIMESPAN))


def all_rotations(onsets):
    return [sorted((o + k) % TIMESPAN for o in onsets) for k in range(TIMESPAN)]


def intervals(onsets):
    p = sorted(onsets)
    return tuple((p[(i + 1) % len(p)] - p[i]) % TIMESPAN for i in range(len(p)))


def canon(onsets):
    return min(tuple(r) for r in all_rotations(onsets))


def mirror_tie_by_multiset(k=5):
    """FINDING-007 Addendum 3. For every chiral rotation class of k onsets in TIMESPAN,
    does the multiset of LHL scores over all rotations equal its mirror's? Grouped by the
    sorted interval vector. Returns {multiset: [bool per chiral class]}."""
    from itertools import combinations
    from collections import defaultdict
    seen, groups = set(), defaultdict(list)
    for p in combinations(range(TIMESPAN), k):
        c = canon(p)
        if c in seen:
            continue
        seen.add(c)
        m = canon(sorted((-x) % TIMESPAN for x in p))
        if m == c:
            continue  # palindromic necklace: its own mirror
        ra = sorted(lhl(r) for r in all_rotations(p))
        rb = sorted(lhl(r) for r in all_rotations(m))
        groups[tuple(sorted(intervals(c)))].append(ra == rb)
    return groups


if __name__ == "__main__" and "--families" in __import__("sys").argv:
    g = mirror_tie_by_multiset()
    always = [k for k, v in g.items() if all(v)]
    mixed = [(k, sum(v), len(v)) for k, v in g.items() if any(v) and not all(v)]
    never = [k for k, v in g.items() if not any(v)]
    print(f"{len(g)} interval multisets with chiral members")
    print("every chiral arrangement ties with its mirror:", always)
    print("mixed:", mixed)
    print(f"never: {len(never)}")
    for name, (on, _) in RHYTHMS.items():
        print(f"  {name:11s} multiset {tuple(sorted(intervals(on)))}")
    raise SystemExit

if __name__ == "__main__":
    # self-check: [FR07] Figure 1 rhythm "has a moderate syncopation index of 5".
    # First attempt read the Xs off extracted text as 0,2,6,8,14 and scored 1, not 5.
    # Rendered the page (scratch fig1.png, 300 dpi) and LOOKED: the crossed boxes are the
    # 3rd, 7th, 9th, 11th and 15th of sixteen -> sixteenth positions 2,6,8,10,14. The
    # caption's own arithmetic "(-2 - -3) + (-2 - -3) + (0 - -3) = 5" matches that reading:
    # rests at 4 and 12 (w -2) after notes at 2 and 10 (w -3); rest at 0 after note at 14.
    fig1 = [2, 6, 8, 10, 14]
    print(f"[FR07] Figure 1 self-check: {box(fig1)}  lhl={lhl(fig1)}  (paper says 5)")
    print()

    print("Six sourced claves, canonical rotation (onset at 0 as printed), LHL index;")
    print("then the same for the mirror image. grain=auto and grain=all must agree.\n")
    print(f"{'name':11s} {'pattern':17s} {'LHL':>4s} {'all':>4s}   {'mirror':17s} {'LHL':>4s} {'all':>4s}   split?")
    for name, (on, note) in RHYTHMS.items():
        m = mirror(on)
        a, b = lhl(on), lhl(m)
        same = sorted(on) == m
        flag = "palindrome" if same else ("YES" if a != b else "no")
        print(f"{name:11s} {box(on)}  {a:4d} {lhl(on,'all'):4d}   {box(m)}  {b:4d} {lhl(m,'all'):4d}   {flag}")

    print("\nRotation is not free for this measure (the '1' matters). For each non-palindrome,")
    print("LHL across all 16 rotations of the named form vs its mirror — min / canonical / max:")
    for name, (on, note) in RHYTHMS.items():
        m = mirror(on)
        if sorted(on) == m:
            continue
        ra = [lhl(r) for r in all_rotations(on)]
        rb = [lhl(r) for r in all_rotations(m)]
        print(f"  {name:11s} named  min {min(ra):2d} canon {lhl(on):2d} max {max(ra):2d}   "
              f"mirror min {min(rb):2d} canon {lhl(m):2d} max {max(rb):2d}   "
              f"{'same multiset' if sorted(ra)==sorted(rb) else 'DIFFERENT multisets'}")
