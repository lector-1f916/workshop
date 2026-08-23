"""
Why isn't the son clave Euclidean?

Toussaint's claim is that Euclid's algorithm generates traditional rhythms. E(5,16)
comes out as the Bossa-Nova. But the most important 5-in-16 rhythm in the world is the
son clave, and it is NOT E(5,16) — it is one onset away from it.

    bossa / E(5,16)   x . . x . . x . . x . . x . . .    onsets 0 3 6 9 12   (33334)
    son clave         x . . x . . x . . . x . x . . .    onsets 0 3 6 10 12  (33424)

So: enumerate every 5-in-16 rhythm (C(16,5) = 4368), score them all on several
natural measures, and find out where the son sits. If Euclid does not pick it out,
something else might.

Nothing here is copied from Toussaint's clave papers. I want my own numbers first;
checking them against his is the next session's job, and doing it in that order is
the only way the agreement means anything.
"""
import sys
from itertools import combinations
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
from bjorklund import bjorklund, as_string, intervals

N, K = 16, 5

# CORRECTED 2026-08-22. I typed these from memory and got the rumba clave wrong
# ([0,3,6,11,12]). Toussaint 2002 publishes a pairwise distance matrix over the six;
# my values reproduced 4 of the 5 Shiko-row distances and missed rumba by exactly the
# amount that [0,3,7,10,12] fixes. With that one change all 5 match to 2dp.
# The rumba's third note is at 7, not 6 — it differs from the son in bar ONE.
# Source: Toussaint, BRIDGES 2002, interval-vector distance matrix, p.164.
NAMED = {
    "son clave":      [0, 3, 6, 10, 12],
    "rumba clave":    [0, 3, 7, 10, 12],
    "bossa (E5,16)":  [0, 3, 6, 9, 12],
    "gahu":           [0, 3, 6, 10, 14],
    "shiko":          [0, 4, 6, 10, 12],
    "soukous":        [0, 3, 6, 10, 11],
}


def ivs(on, n=N):
    return [(on[(i + 1) % len(on)] - on[i]) % n or n for i in range(len(on))]


def evenness(on, n=N):
    """Sum of squared deviations of the inter-onset intervals from the ideal n/k.
    Lower is more even; 0 only when k divides n.

    REWRITTEN 2026-08-22. The first version paired onset i with ideal slot i and
    minimised over template shifts, which is NOT rotation-invariant — the pairing
    changes when you rotate. It scored the son clave 1.6 as a canonical necklace and
    1.0 as played, and the two disagreeing is how I caught it. Intervals are a cyclic
    multiset, so scoring them is rotation-invariant by construction.
    """
    iv = ivs(on, n)
    ideal = n / len(iv)
    return round(sum((v - ideal) ** 2 for v in iv), 3)


def oddity(on, n=N):
    """Rhythmic oddity: no two onsets are antipodal (split the cycle in half)."""
    s = set(on)
    return not any(((p + n // 2) % n) in s for p in on)


def offbeatness(on, n=N):
    """Positions not hit by ANY regular polygon inscribed in the n-cycle.
    For n=16 the polygon vertices are exactly the even positions, so off-beat = odd."""
    # PROPER divisors only: the full n-gon hits every position, so including it
    # makes off-beatness identically zero. Found that by getting 0 for everything.
    hit = set()
    for k in range(2, n):
        if n % k == 0:
            hit |= {i * (n // k) for i in range(k)}
    return sum(1 for p in on if p not in hit)


def distinct_rotations(on, n=N):
    s = frozenset(on)
    return len({frozenset(((p + r) % n) for p in s) for r in range(n)})


def interval_variety(on, n=N):
    return len(set(ivs(on, n)))


# ---- enumerate everything, normalised so rotations of one rhythm count once ----
seen, universe = set(), []
for combo in combinations(range(N), K):
    if 0 not in combo:
        continue                       # fix an onset at 0: necklaces, not rotations
    canon = min(
        tuple(sorted(((p - r) % N) for p in combo)) for r in combo
    )
    if canon in seen:
        continue
    seen.add(canon)
    universe.append(list(canon))

print(f"distinct 5-in-16 necklaces: {len(universe)}\n")

rows = []
for on in universe:
    rows.append({
        "on": on,
        "even": evenness(on),
        "odd": oddity(on),
        "off": offbeatness(on),
        "rot": distinct_rotations(on),
        "var": interval_variety(on),
        "iv": "".join(map(str, ivs(on))),
    })

by_even = sorted(rows, key=lambda r: r["even"])


def find(on):
    canon = min(tuple(sorted(((p - r) % N) for p in on)) for r in on)
    for i, r in enumerate(by_even):
        if tuple(r["on"]) == canon:
            return i, r
    return None, None


print(f"{'rhythm':<16} {'onsets':<18} {'iv':<7} {'evenness':>9} {'rank':>6} {'oddity':>7} {'offbeat':>8}")
print("-" * 76)
for name, on in NAMED.items():
    i, r = find(on)
    # off-beatness measured on the rhythm AS PLAYED, not on its canonical rotation
    print(f"{name:<16} {str(on):<18} {''.join(map(str,ivs(on))):<7} {r['even']:>9} {i+1:>6} "
          f"{str(oddity(on)):>7} {offbeatness(on):>8}")

print(f"\nmost even necklaces (of {len(by_even)}):")
for r in by_even[:6]:
    print(f"  {r['iv']:<7} {as_string([1 if i in r['on'] else 0 for i in range(N)])}  even={r['even']}")

# how many share the son's oddity + offbeat profile?
son = find(NAMED["son clave"])[1]
same = [r for r in rows if r["odd"] == son["odd"] and r["off"] == son["off"]]
print(f"\nnecklaces with oddity={son['odd']} and offbeatness={son['off']}: {len(same)}")
odd_true = [r for r in rows if r["odd"]]
print(f"necklaces with the oddity property at all: {len(odd_true)} of {len(rows)}")
