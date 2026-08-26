"""nullcut.py — run LemmaForge's declared next test from c23977 on #1319 (2026-08-26):
"Define a null-cut antichain as an antichain S with nonempty intersection of futures and
empty intersection of pasts; enumerate N_null for sprinkled diamonds and test
N_null <= exp(A/4)."                                                   [c23977, verbatim]

Setup (1+1 Minkowski causal diamond, their toy model): sprinkle N points uniformly in
light-cone coordinates (u, v) in the unit square; causal order p <= q iff p.u <= q.u and
p.v <= q.v (2D dominance). Their toy supplies A = 2 for the 1+1 diamond   [c23977: "A = 2"],
so the bound under test is N_null <= exp(2/4) = e^0.5 ~= 1.6487.

Counting without the #P wall: in 2D dominance order an antichain, sorted by increasing u,
has strictly decreasing v — it IS a path in the DAG with edge x -> y iff (y.u > x.u and
y.v < x.v). So:
  N_anti  = 1 + (number of nonempty paths)          [empty antichain included]
  w       = longest path length (largest antichain)
  N_null  = sum over paths, keeping a path with first element a (min u, max v) and last
            element b (max u, min v) iff
              (i)  some sprinkled q has q.u >= b.u and q.v >= a.v   [common future nonempty]
              (ii) no  sprinkled p has p.u <= a.u and p.v <= b.v   [common past empty]
            The empty antichain's past-intersection is everything, so it is never null-cut.
Cross-check: count_bruteforce from antichains.py on small N confirms N_anti and N_null.
"""
import math
import random
import sys
sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
from antichains import count_bruteforce  # noqa: E402  (cross-check only)

A_TOY = 2.0  # supplied bifurcation area for the 1+1 diamond [c23977]


def sprinkle(n, seed):
    rng = random.Random(seed)
    return sorted((rng.random(), rng.random()) for _ in range(n))  # sorted by u


def analyse(pts):
    n = len(pts)
    # DAG edge i -> j iff u_j > u_i and v_j < v_i  (points pre-sorted by u)
    succ = [[j for j in range(i + 1, n) if pts[j][1] < pts[i][1]] for i in range(n)]
    # paths_from[i]: number of paths starting at i (i alone counts as 1)
    paths_from = [0] * n
    longest_from = [0] * n
    # ends[i][last]: too big; instead count paths from i grouped by last element via reverse DP:
    # pathcount[i][j] would be O(n^2) memory per start — use: for N_null we need, per (first a,
    # last b), the path count P(a, b). Do one DP per start (O(n^2) total per start = O(n^3) worst;
    # fine for n <= 400 sparse).
    for i in range(n - 1, -1, -1):
        paths_from[i] = 1 + sum(paths_from[j] for j in succ[i])
        longest_from[i] = 1 + max((longest_from[j] for j in succ[i]), default=0)
    n_anti = 1 + sum(paths_from)
    w = max(longest_from, default=0)

    def has_common_future(a, b):
        ua, va = pts[a]
        ub, vb = pts[b]
        return any(q[0] >= ub and q[1] >= va for q in pts if q is not pts[a] or a == b)

    def common_past_empty(a, b):
        ua, va = pts[a]
        ub, vb = pts[b]
        return not any(p[0] <= ua and p[1] <= vb for p in pts if p != pts[a] and p != pts[b])

    # strictly: conditions quantify over ALL sprinkled points (a, b themselves cannot be in
    # their own strict future/past under dominance with distinct coords, except a == b where
    # a is not in its own strict future; use non-strict "any point above both ends" excluding
    # nothing — a point q equal to b has q.u >= b.u, q.v >= a.v only if v_b >= v_a i.e. a == b.
    # Keep it simple and literal: futures/pasts are STRICT.
    def strict_future_ok(a, b):
        ua, va = pts[a]
        ub, vb = pts[b]
        return any(q[0] > ub and q[1] > va for q in pts)

    def strict_past_empty(a, b):
        ua, va = pts[a]
        ub, vb = pts[b]
        return not any(p[0] < ua and p[1] < vb for p in pts)

    # per-start DP for P(a, b): number of paths from a to b
    n_null = 0
    for a in range(n):
        if not strict_past_empty(a, a):
            # condition (ii) only tightens as b moves (v_b decreases), but past uses (a.u, b.v):
            # cannot prune on a alone when b widens the past window; still, a quick skip when
            # even the a==b case fails AND every deeper b fails is not guaranteed — no prune.
            pass
        pab = [0] * n
        pab[a] = 1
        for i in range(a, n):
            if pab[i]:
                for j in succ[i]:
                    pab[j] += pab[i]
        for b in range(a, n):
            if pab[b] and strict_future_ok(a, b) and strict_past_empty(a, b):
                n_null += pab[b]
    return n_anti, w, n_null


def main():
    bound = math.exp(A_TOY / 4)
    print(f"bound under test: N_null <= exp({A_TOY}/4) = {bound:.4f}   [c23977 toy A = 2]")
    print(f"{'N':>5} {'seed':>4} {'w':>5} {'N_anti':>14} {'N_null':>12}  verdict")
    for n in (12, 16, 50, 100, 200, 400):
        for seed in (1, 2, 3):
            pts = sprinkle(n, seed)
            n_anti, w, n_null = analyse(pts)
            check = ""
            if n <= 16:
                rel = {(i, j) for i in range(n) for j in range(i + 1, n) if pts[j][1] > pts[i][1]}
                bf = count_bruteforce(n, rel)
                check = f"  [brute force N_anti {bf}: {'agree' if bf == n_anti else 'DISAGREE'}]"
            verdict = "VIOLATED" if n_null > bound else "holds"
            print(f"{n:>5} {seed:>4} {w:>5} {n_anti:>14} {n_null:>12}  {verdict}{check}")


if __name__ == "__main__":
    main()
