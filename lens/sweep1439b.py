"""
sweep1439b.py -- the second round on petit-pas's c19012, after sweep1439.py's first answer.

What the first round showed (sweep1439-out.txt): with the run-(c) geometry held fixed
(masses +/-0.25, e=1, capture radius 0.4), w(union) is 1 near the axis and 0 far out, and
the 1->0 transitions land at y=2.9611 on the mass axis and y=3.5909 on the bisector --
each equal to L evaluated at the union boundary point where the SECOND saddle enters
(L(-0.65,0) = 2.961; L(0,-0.312) = 3.591, both computed by hand in the journal). The
interior saddle never exits; an outside saddle always reaches the boundary first. The rule
w = #masses + sum ind matched at every sweep point.

Question 1 here: is w = 2 reachable AT ALL with r = 0.4? Scan w(union) over a 2D grid of
sources. No Newton needed -- w is three boundary windings per source.

Question 2: the suspected mechanism is that the fat disks never give up their zeros (the
fold of L sits inside the union). If so, a THINNER merged pair -- r = 0.26, still one
component since 0.26 + 0.26 > 0.5 -- should let the central saddle exit before anything
enters, and w should touch 2. Sweep the bisector as before and inventory the zeros.

Question 3: the -24 annulus retry. First run found 4 zeros; the argument principle plus
the measured windings (w=1 on both band circles) forces the interior images to sum to -24,
so Newton was missing ~21 zeros. The near-mass structure of a ring member has scale
e_i^2 = 1/24 = 0.042, far below the 0.026-0.125 spacing of the first run's band starts.
This run adds a 16x16 local grid spanning +/-0.1 around EVERY mass (24 x 256 starts).
"""

import math
from lens import V, jac, newton, winding, circle, two_disk_union_winding
from sweep1439 import all_zeros

LENSES = [(-0.25, 0, 1.0), (0.25, 0, 1.0)]


def w_union_for(caps, y):
    w, parts = two_disk_union_winding(caps, 0, 1, LENSES, y)
    return w, parts


def scan_2d(r, lo=-4.0, hi=4.0, n=33):
    caps = [(-0.25, 0, r), (0.25, 0, r)]
    counts = {}
    hits2 = []
    for i in range(n):
        for j in range(n):
            y = (lo + (hi - lo) * i / (n - 1), lo + (hi - lo) * j / (n - 1))
            w, _ = w_union_for(caps, y)
            counts[w] = counts.get(w, 0) + 1
            if w == 2:
                hits2.append(y)
    print(f"== 2D scan, r={r}: w(union) over y in [{lo},{hi}]^2, {n}x{n} sources")
    print(f"   value counts: {dict(sorted(counts.items()))}")
    for y in hits2[:12]:
        print(f"   w=2 at y=({y[0]:+.3f},{y[1]:+.3f})")
    if len(hits2) > 12:
        print(f"   ... and {len(hits2) - 12} more")
    print()
    return hits2


def thin_peanut_sweep():
    r = 0.26  # 0.26 + 0.26 > 0.5: still one merged component, but barely
    caps = [(-0.26 + 0.01, 0, r), (0.25, 0, r)]  # dummy line replaced below
    caps = [(-0.25, 0, r), (0.25, 0, r)]
    def in_u(x):
        return any((x[0] - cx) ** 2 + (x[1] - cy) ** 2 < rr * rr for (cx, cy, rr) in caps)
    print(f"== thin peanut, r={r} (union boundary on bisector at |x2|={math.sqrt(r*r-0.0625):.4f})")
    prev_w = None
    prev_t = None
    for t in [0.5, 1.0, 1.5, 1.8, 1.9, 2.0, 2.05, 2.1, 2.2, 2.4, 2.7, 3.0, 3.3, 3.5, 3.59, 3.7, 3.8, 4.0, 4.5]:
        y = (0.0, t)
        w, parts = w_union_for(caps, y)
        zeros = all_zeros(LENSES, y, span=6.0, n=60)
        inside = [(x, s) for (x, s) in zeros if in_u(x)]
        ind_in = sum(s for _, s in inside)
        ins = " ".join(f"{'+' if s > 0 else '-'}({x[0]:+.3f},{x[1]:+.3f})" for x, s in inside) or "none"
        match = "MATCH" if w == 2 + ind_in else "MISMATCH"
        print(f"   t={t:+.3f}  w(union)={w}  (wA={parts[0]} wB={parts[1]} wL={parts[2]})  "
              f"zeros inside: {ins}  2+ind_in={2 + ind_in}  {match}")
        if prev_w is not None and w != prev_w:
            lo, hi = prev_t, t
            for _ in range(40):
                mid = (lo + hi) / 2
                wm, _ = w_union_for(caps, (0.0, mid))
                if wm == prev_w:
                    lo = mid
                else:
                    hi = mid
            print(f"   TRANSITION w {prev_w} -> {w} at t = {(lo + hi) / 2:.6f}")
        prev_w, prev_t = w, t
    print()


def annulus_retry():
    print("== the -24 annulus, retry with near-mass starts")
    ring = [(2 * math.cos(2 * math.pi * k / 24), 2 * math.sin(2 * math.pi * k / 24),
             math.sqrt(1 / 24)) for k in range(24)]
    y = (0.2, 0.1)  # first source of lens.py run (e), same as the first try
    extra = []
    m = 16
    for (px, py, _) in ring:
        for a in range(m):
            for b in range(m):
                extra.append((px - 0.1 + 0.2 * a / (m - 1), py - 0.1 + 0.2 * b / (m - 1)))
    for ir in range(9):  # keep the band grid from the first try too
        rr = 1.5 + ir * (2.5 - 1.5) / 8
        for k in range(480):
            t = 2 * math.pi * k / 480
            extra.append((rr * math.cos(t), rr * math.sin(t)))
    zeros = all_zeros(ring, y, span=6.0, n=60, extra_starts=extra)
    in_band = [(x, s) for (x, s) in zeros if 1.7 ** 2 < x[0] ** 2 + x[1] ** 2 < 2.3 ** 2]
    s_in = sum(s for _, s in in_band)
    npos = sum(1 for _, s in in_band if s > 0)
    nneg = sum(1 for _, s in in_band if s < 0)
    print(f"   source y={y}   zeros: {len(zeros)} total, {len(in_band)} in 1.7<|x|<2.3")
    print(f"   sum of ind inside the band: {s_in}   (prediction: -24)   N+={npos} N-={nneg}")
    w_out = winding(circle(0, 0, 2.3), ring, y)
    w_in = winding(circle(0, 0, 1.7), ring, y)
    print(f"   band circles: w(2.3)={w_out}  w(1.7)={w_in}   rule: 24 + ({s_in}) = {24 + s_in} vs degree {w_out - w_in}")
    out_band = [(x, s) for (x, s) in zeros if not (1.7 ** 2 < x[0] ** 2 + x[1] ** 2 < 2.3 ** 2)]
    print(f"   outside the band: {len(out_band)} zeros, sum ind = {sum(s for _, s in out_band)}")
    print(f"   global check: total sum ind = {s_in + sum(s for _, s in out_band)}   (1 - 24 masses = -23)")
    print()


if __name__ == "__main__":
    scan_2d(0.4)
    thin_peanut_sweep()
    annulus_retry()
