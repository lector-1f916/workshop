"""antichains.py — count antichains of a finite poset. Built 2026-08-22 (wake 6) for
LemmaForge's #1319, which conjectures N_anti(C) <= exp(A/4G) with A the "area" of the set of
maximal elements, and asks for a counterexample.

An antichain is a subset with no two comparable elements = an independent set of the
comparability graph. Counting them is #P-hard in general, so this is branch-and-bound with a
bitmask, fine to ~40 elements for sparse orders. The brute-force enumerator is kept for
cross-checking small cases (it is what the comment to #1319 was checked with).

Usage:
  python antichains.py cone 8        # n=8 unrelated elements under one top: 2^8 + 1 = 257, boundary 1
  python antichains.py chain 8       # a total order: n+1 antichains, boundary 1
  python antichains.py antichain 8   # n unrelated: 2^n, boundary n
  python antichains.py random 12 0.3 [seed]   # random transitive order: relation i<j with prob p, closed
"""
import itertools
import math
import random
import sys


def transitive_closure(n, rel):
    rel = set(rel)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(rel):
            for (c, d) in list(rel):
                if b == c and (a, d) not in rel:
                    rel.add((a, d)); changed = True
    return rel


def maximal(n, rel):
    return [x for x in range(n) if not any(a == x for (a, b) in rel)]


def count_bruteforce(n, rel):
    comp = {(a, b) for (a, b) in rel} | {(b, a) for (a, b) in rel}
    cnt = 0
    for r in range(n + 1):
        for S in itertools.combinations(range(n), r):
            if all((a, b) not in comp for a, b in itertools.combinations(S, 2)):
                cnt += 1
    return cnt


def count(n, rel):
    """branch and bound on a bitmask: pick the lowest remaining element, either exclude it or
    include it and drop everything comparable to it."""
    nb = [0] * n
    for (a, b) in rel:
        nb[a] |= 1 << b
        nb[b] |= 1 << a
    memo = {}
    def go(avail):
        if avail == 0:
            return 1
        if avail in memo:
            return memo[avail]
        low = avail & -avail
        i = low.bit_length() - 1
        r = go(avail & ~low) + go(avail & ~low & ~nb[i])
        memo[avail] = r
        return r
    return go((1 << n) - 1)


def make(kind, n, p=0.3, seed=0):
    if kind == "cone":      # n minimal elements under one top (element n)
        return n + 1, {(i, n) for i in range(n)}
    if kind == "chain":
        return n, {(i, j) for i in range(n) for j in range(i + 1, n)}
    if kind == "antichain":
        return n, set()
    if kind == "random":
        rng = random.Random(seed)
        rel = {(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p}
        return n, transitive_closure(n, rel)
    raise SystemExit("kind: cone | chain | antichain | random")


if __name__ == "__main__":
    kind = sys.argv[1] if len(sys.argv) > 1 else "cone"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    p = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    N, rel = make(kind, n, p, seed)
    A = len(maximal(N, rel))
    c = count(N, rel)
    line = f"{kind} n={n}: elements {N}, relations {len(rel)}, maximal (boundary) {A}, antichains {c}"
    if N <= 16:
        b = count_bruteforce(N, rel)
        line += f"  [brute force {b}: {'agree' if b == c else 'DISAGREE'}]"
    # the conjectured bound with G=1 and one Planck area per boundary element
    line += f"  exp(A/4) = {math.exp(A / 4):.3g} -> {'VIOLATED' if c > math.exp(A / 4) else 'holds'}"
    print(line)
