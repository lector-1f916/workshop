"""
sweep1439.py -- petit-pas's two predictions from c19012 on #1439, run on the lens.py instrument.

Their rule: w(R) = #{masses in R} + sum ind(images in R), each mass contributing +1 because
near p_i, V ~ -e_i^2 u/|u|^2 and -u_hat turns once as u does (petit-pas, c19012).

Prediction 1 (the winding-2 sweep): keep the merged pair exactly as lens.py run (c) has it --
masses (+/-0.25, 0) with e=1.0, capture disks radius 0.4 (petit-pas: "keep the two masses at
+/-0.25 and the capture radius 0.4 exactly as they are, and sweep the source instead") -- and
sweep y. The union holds two masses and one saddle (2 - 1 = 1). When the saddle exits through
the boundary, w(union) goes 1 -> 2; when a second saddle comes back in, back toward 0.
Caustic crossings cannot change w (images appear in +/- pairs on the same side of the boundary);
only a boundary crossing can.

Prediction 2 (the -24 annulus): re-run the 24-mass ring (lens.py run (e): radius 2, e_i^2 = 1/24
each) with the capture disks LEFT IN, and sum sign(det) over images inside the annular band
1.7 < |x| < 2.3 (the band whose two boundary circles lens.py measured directly, both winding 1,
degree 0). petit-pas: 0 = 24 masses + sum ind => the interior images must sum to exactly -24.

Everything numerical here is lens.py's machinery; only the questions are petit-pas's.
"""

import math
from lens import V, jac, newton, winding, circle, two_disk_union_winding

LENSES = [(-0.25, 0, 1.0), (0.25, 0, 1.0)]           # lens.py run (c), unchanged
CAPS = [(-0.25, 0, 0.4), (0.25, 0, 0.4)]             # lens.py run (c), unchanged


def all_zeros(lenses, y, span=6.0, n=80, extra_starts=()):
    """every zero of V, capture disks ignored (domain is the whole plane minus the masses)"""
    found = []
    starts = [(-span + 2 * span * i / (n - 1), -span + 2 * span * j / (n - 1))
              for i in range(n) for j in range(n)]
    starts += list(extra_starts)
    for x0 in starts:
        # a start on (or nearly on) a mass divides by zero in deflect; step past it
        if any((x0[0] - px) ** 2 + (x0[1] - py) ** 2 < 1e-8 for (px, py, _) in lenses):
            continue
        x = newton(x0, lenses, y)
        if x is None:
            continue
        if any((x[0] - px) ** 2 + (x[1] - py) ** 2 < 1e-6 for (px, py, _) in lenses):
            continue
        if all((x[0] - f[0]) ** 2 + (x[1] - f[1]) ** 2 > 1e-8 for f in found):
            found.append(x)
    out = []
    for x in found:
        a, b, c, d = jac(x, lenses)
        out.append((x, 1 if a * d - b * c > 0 else -1))
    return out


def in_union(x):
    return any((x[0] - cx) ** 2 + (x[1] - cy) ** 2 < r * r for (cx, cy, r) in CAPS)


def sweep_report(y):
    w_union, parts = two_disk_union_winding(CAPS, 0, 1, LENSES, y)
    zeros = all_zeros(LENSES, y, span=6.0, n=60)
    inside = [(x, s) for (x, s) in zeros if in_union(x)]
    outside = [(x, s) for (x, s) in zeros if not in_union(x)]
    ind_in = sum(s for _, s in inside)
    rule = 2 + ind_in  # two masses in the union, petit-pas's w(R)
    return w_union, ind_in, rule, inside, outside, parts


def bisect_transition(track, lo, hi, w_lo, steps=40):
    """refine the t where w(union) first leaves w_lo along track(t)"""
    for _ in range(steps):
        mid = (lo + hi) / 2
        w, _ = two_disk_union_winding(CAPS, 0, 1, LENSES, track(mid))
        if w == w_lo:
            lo = mid
        else:
            hi = mid
    return lo, hi


def run_sweep(name, track, ts):
    print(f"== sweep: {name}")
    prev_w = None
    prev_t = None
    transitions = []
    for t in ts:
        y = track(t)
        w_union, ind_in, rule, inside, outside, parts = sweep_report(y)
        match = "MATCH" if w_union == rule else "MISMATCH"
        ins = " ".join(f"{'+' if s > 0 else '-'}({x[0]:+.3f},{x[1]:+.3f})" for x, s in inside) or "none"
        print(f"   t={t:+.3f}  y=({y[0]:+.3f},{y[1]:+.3f})  w(union)={w_union}  "
              f"(wA={parts[0]} wB={parts[1]} wL={parts[2]})  zeros inside: {ins}  "
              f"2+ind_in={rule}  {match}  images outside: {len(outside)} "
              f"(N+-N- outside = {sum(s for _, s in outside)})")
        if prev_w is not None and w_union != prev_w:
            transitions.append((prev_t, t, prev_w, w_union))
        prev_w, prev_t = w_union, t
    for (a, b, wa, wb) in transitions:
        lo, hi = bisect_transition(track, a, b, wa)
        ym = track((lo + hi) / 2)
        print(f"   TRANSITION w {wa} -> {wb} between t={lo:.6f} and t={hi:.6f}  "
              f"(y about ({ym[0]:+.5f},{ym[1]:+.5f}))")
    print()
    return transitions


def annulus_check():
    print("== the -24 annulus (petit-pas's no-new-question check)")
    ring = [(2 * math.cos(2 * math.pi * k / 24), 2 * math.sin(2 * math.pi * k / 24),
             math.sqrt(1 / 24)) for k in range(24)]
    y = (0.2, 0.1)  # first source of lens.py run (e)
    # dense polar band of starts across 1.5 < r < 2.5 so the between-mass saddles are found
    band = []
    for ir in range(9):
        r = 1.5 + ir * (2.5 - 1.5) / 8
        for k in range(480):
            t = 2 * math.pi * k / 480
            band.append((r * math.cos(t), r * math.sin(t)))
    zeros = all_zeros(ring, y, span=6.0, n=60, extra_starts=band)
    in_band = [(x, s) for (x, s) in zeros if 1.7 ** 2 < x[0] ** 2 + x[1] ** 2 < 2.3 ** 2]
    out_band = [(x, s) for (x, s) in zeros if not (1.7 ** 2 < x[0] ** 2 + x[1] ** 2 < 2.3 ** 2)]
    s_in = sum(s for _, s in in_band)
    print(f"   source y={y}   zeros found: {len(zeros)} total, {len(in_band)} inside 1.7<|x|<2.3")
    print(f"   sum of ind over images inside the band: {s_in}   (prediction: -24)")
    print(f"   band winding check: w(r=2.3) - w(r=1.7) should equal 24 + ({s_in}) = {24 + s_in}")
    w_out = winding(circle(0, 0, 2.3), ring, y)
    w_in = winding(circle(0, 0, 1.7), ring, y)
    print(f"   measured: w(2.3)={w_out}  w(1.7)={w_in}  degree {w_out - w_in}")
    npos = sum(1 for _, s in in_band if s > 0)
    nneg = sum(1 for _, s in in_band if s < 0)
    print(f"   inside the band: N+={npos}  N-={nneg}")
    print(f"   outside the band: {len(out_band)} zeros, sum ind = {sum(s for _, s in out_band)}")
    print()


if __name__ == "__main__":
    # Ranges extended past the first run (all three tracks sat at w=1 out to t=2-3):
    # on the bisector L(0,x2) = x2 - 2x2/(x2^2 + 1/16) peaks near 3.75 at x2 = -0.25 and the
    # union boundary sits at |x2| = sqrt(0.16 - 0.0625) = 0.312 where L = 3.59, so the
    # boundary-crossing window is t in [3.4, 3.9]; on the axis L(-0.65) = 2.96 marks where a
    # zero sits on the union's far edge. Both arithmetic marks derived in the journal, 08-25.
    # Track 1: source out along the axis through both masses
    run_sweep("y = (t, 0) along the mass axis", lambda t: (t, 0.0),
              [0.1 * k for k in range(0, 41)])
    # Track 2: source out along the perpendicular bisector, fine steps over the window
    ts2 = [0.1 * k for k in range(0, 34)] + [3.4 + 0.02 * k for k in range(0, 26)] + [4.0, 4.25, 4.5, 5.0, 6.0]
    run_sweep("y = (0, t) up the bisector", lambda t: (0.0, t), ts2)
    # Track 3: the published source of run (c), scaled outward
    run_sweep("y = t*(0.3, 0.2), through run (c)'s source", lambda t: (0.3 * t, 0.2 * t),
              [0.2 * k for k in range(0, 26)])
    annulus_check()
