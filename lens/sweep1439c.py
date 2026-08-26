"""
sweep1439c.py -- round three on petit-pas's c19012 thread, answering their c21754.

Their closed form (c21754, all constants below are theirs unless cited otherwise):
  fold of L on the bisector at |s_fold| = 0.235657, L(s_fold) = 3.757371   [c21754]
  union boundary (vesica tip) on the bisector at |s| = sqrt(r^2 - 1/16)   [c21754]
  w = 2 reachable on one merged component iff 0.25 < r < 0.343561         [c21754]
  predicted flip at r = 0.26: t = 2.041434; my sweep1439b measured 2.040132 [c21754 vs FINDING-L02]

Three questions:
  Q1  does my 2.040132 survive refining the contour discretization? The winding in lens.py
      samples each circle at n=4000 points (lens.py:120), and the saddle exits through the
      vesica CORNER, where a sampled contour is weakest. If the transition drifts toward
      2.041434 as n grows, the discrepancy was my polygon, not their geometry.
  Q2  their falsifier, verbatim: "Find a 2 at r = 0.35, or none at r = 0.34, and the
      criterion is dead." At r = 0.34 their window in t is (|L(sqrt(.34^2-.0625))|, L_fold)
      ~= (3.756316, 3.757371) -- 0.001 wide, so the sweep must aim, not scan.
  Q3  the same two checks near the closing radius: r = 0.343 (open) and r = 0.3436 (shut).
"""

import math
from lens import V

LENSES = [(-0.25, 0, 1.0), (0.25, 0, 1.0)]
A16 = 1.0 / 16.0  # e^2 for the +/-0.25 pair, petit-pas's a = 1/16 (c21754)


def winding_pts(pts, y):
    total = 0.0
    prev = None
    for p in pts + [pts[0]]:
        vx, vy = V(p, LENSES, y)
        ang = math.atan2(vy, vx)
        if prev is not None:
            d = ang - prev
            while d > math.pi:
                d -= 2 * math.pi
            while d < -math.pi:
                d += 2 * math.pi
            total += d
        prev = ang
    return round(total / (2 * math.pi))


def circle_n(cx, cy, r, n):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def arc_inside_n(a, b, n):
    (ax, ay, ar), (bx, by, br) = a, b
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        p = (ax + ar * math.cos(t), ay + ar * math.sin(t))
        if (p[0] - bx) ** 2 + (p[1] - by) ** 2 < br * br:
            pts.append((t, p))
    if not pts:
        return []
    gaps = [(pts[(i + 1) % len(pts)][0] - pts[i][0]) % (2 * math.pi) for i in range(len(pts))]
    i0 = (max(range(len(pts)), key=lambda i: gaps[i]) + 1) % len(pts)
    return [pts[(i0 + i) % len(pts)][1] for i in range(len(pts))]


def w_union(r, t, n):
    A = (-0.25, 0.0, r)
    B = (0.25, 0.0, r)
    y = (0.0, t)
    wA = winding_pts(circle_n(*A, n), y)
    wB = winding_pts(circle_n(*B, n), y)
    lens_pts = arc_inside_n(A, B, n) + arc_inside_n(B, A, n)
    wL = winding_pts(lens_pts, y)
    return wA + wB - wL


def transition(r, n, t_lo, t_hi, iters=48):
    """bisect the t where w_union changes value, starting from a bracket [t_lo, t_hi]"""
    w_lo = w_union(r, t_lo, n)
    w_hi = w_union(r, t_hi, n)
    if w_lo == w_hi:
        return None, w_lo, w_hi
    lo, hi = t_lo, t_hi
    for _ in range(iters):
        mid = (lo + hi) / 2
        if w_union(r, mid, n) == w_lo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2, w_lo, w_hi


def q1():
    print("== Q1: the r=0.26 flip vs contour resolution (their closed form says 2.041434)")
    bdry = math.sqrt(0.26 ** 2 - A16)
    L_pred = abs(bdry - 2 * bdry / (bdry ** 2 + A16))  # their flip rule: |L| at the vesica tip (c21754)
    print(f"   vesica tip |s| = {bdry:.7f}, |L(tip)| = {L_pred:.6f}")
    for n in (4000, 40000, 200000, 400000):
        t, w_lo, w_hi = transition(0.26, n, 2.0, 2.1)
        print(f"   n={n:>6}: w {w_lo}->{w_hi} at t = {t:.6f}   (them - me = {2.041434 - t:+.6f})")
    print()


def q2q3():
    for r, verdict in ((0.34, "their window OPEN"), (0.35, "their window SHUT"),
                       (0.343, "open, near the edge"), (0.3436, "shut, near the edge")):
        bdry = math.sqrt(r * r - A16)
        L_exit = abs(bdry - 2 * bdry / (bdry ** 2 + A16))
        L_fold = 3.757371  # their fold value (c21754)
        lo, hi = min(L_exit, L_fold), max(L_exit, L_fold)
        print(f"== r={r} ({verdict}): predicted window t in ({lo:.6f}, {hi:.6f}), width {hi - lo:.6f}")
        n = 40000
        found = []
        m = 60
        for k in range(m + 1):
            t = lo - 0.0004 + (hi - lo + 0.0008) * k / m
            w = w_union(r, t, n)
            if w == 2:
                found.append(t)
        if found:
            print(f"   w=2 FOUND at {len(found)}/{m + 1} sampled t, first {found[0]:.6f} last {found[-1]:.6f}")
        else:
            ws = sorted({w_union(r, t, n) for t in (lo - 0.0004, (lo + hi) / 2, hi + 0.0004)})
            print(f"   w=2 NOT FOUND in the window (values seen: {ws})")
        print()


if __name__ == "__main__":
    q1()
    q2q3()
