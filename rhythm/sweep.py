"""
The son clave is 4th most even of 273. So evenness nearly picks it out and doesn't.

Rather than guess which property does, score every 5-in-16 necklace on a battery of
measures and ask, for each measure, where the son ranks. If some measure puts it at 1
that is a candidate answer. If none does, that is also an answer and a more interesting
one — it would mean the son is not the optimum of anything simple and is picked out by
something other than optimisation.

Measures are computed on the rhythm AS PLAYED where they are orientation-dependent,
and on the necklace where they are not. Mixing those up cost me an hour already.
"""
import sys
from itertools import combinations

sys.stdout.reconfigure(encoding="utf-8")
from clave import ivs, evenness, oddity, offbeatness, N, K, NAMED

BEATS = {0, 4, 8, 12}          # the four quarter-note beats in 16
STRONG = {0, 8}


def onsets_on_beat(on):
    return sum(1 for p in on if p in BEATS)


def onsets_on_strong(on):
    return sum(1 for p in on if p in STRONG)


def keith_syncopation(on, n=N):
    """Weight each onset by how weak its metric position is. Position weight = the
    largest power of two dividing it (0 gets the max). Higher total = more syncopated."""
    def depth(p):
        if p == 0:
            return 0
        d = 0
        while p % 2 == 0:
            p //= 2
            d += 1
        return 4 - d          # 16 = 2^4
    return sum(depth(p) for p in on)


def interval_variety(on):
    return len(set(ivs(on)))


def max_interval(on):
    return max(ivs(on))


def adjacent_pairs(on, n=N):
    """How many onsets sit right next to another (interval of 1). Clustering."""
    return sum(1 for v in ivs(on) if v == 1)


def rotational_distinctness(on, n=N):
    s = frozenset(on)
    return len({frozenset(((p + r) % n) for p in s) for r in range(n)})


def half_split(on, n=N):
    """Onsets in the first half vs second half — the '3-2' structure."""
    a = sum(1 for p in on if p < n // 2)
    return (a, len(on) - a)


def deep(on, n=N):
    """A rhythm is 'deep' if every interval-class multiplicity is distinct."""
    from collections import Counter
    c = Counter()
    pts = sorted(on)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = (pts[j] - pts[i]) % n
            c[min(d, n - d)] += 1
    vals = list(c.values())
    return len(vals) == len(set(vals))


MEASURES = {
    "evenness (low=even)":   (evenness, False),
    "keith syncopation":     (keith_syncopation, True),
    "onsets off the beat":   (lambda o: len(o) - onsets_on_beat(o), True),
    "off-beatness":          (offbeatness, True),
    "interval variety":      (interval_variety, True),
    "max interval (low)":    (max_interval, False),
    "rotational distinct":   (rotational_distinctness, True),
}

# all necklaces, but scored in every rotation for orientation-dependent measures
seen, universe = set(), []
for combo in combinations(range(N), K):
    if 0 not in combo:
        continue
    canon = min(tuple(sorted(((p - r) % N) for p in combo)) for r in combo)
    if canon not in seen:
        seen.add(canon)
        universe.append(list(canon))

son = NAMED["son clave"]
print(f"universe: {len(universe)} necklaces\n")
print(f"{'measure':<22} {'son value':>10} {'rank':>8} {'ties':>6}   best value")
print("-" * 72)

for label, (fn, higher_better) in MEASURES.items():
    scored = [(fn(o), o) for o in universe]
    sv = fn(son)
    if higher_better:
        better = sum(1 for v, _ in scored if v > sv)
        ties = sum(1 for v, _ in scored if v == sv)
        best = max(v for v, _ in scored)
    else:
        better = sum(1 for v, _ in scored if v < sv)
        ties = sum(1 for v, _ in scored if v == sv)
        best = min(v for v, _ in scored)
    print(f"{label:<22} {str(sv):>10} {better+1:>8} {ties:>6}   {best}")

print()
print("structure of the named rhythms")
print(f"{'name':<16} {'halves':<8} {'deep':<6} {'on-beat':<8} {'strong':<7} {'iv'}")
for name, on in NAMED.items():
    print(f"{name:<16} {str(half_split(on)):<8} {str(deep(on)):<6} "
          f"{onsets_on_beat(on):<8} {onsets_on_strong(on):<7} {''.join(map(str,ivs(on)))}")

# the specific thing: son vs bossa differ by ONE onset. what does moving it buy?
print("\nson vs bossa: one onset moved, 9 -> 10")
for name in ("bossa (E5,16)", "son clave"):
    o = NAMED[name]
    print(f"  {name:<14} even={evenness(o):<5} keith={keith_syncopation(o):<3} "
          f"onbeat={onsets_on_beat(o)} offbeat={offbeatness(o)} deep={deep(o)} halves={half_split(o)}")
