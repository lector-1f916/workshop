"""
test_rule.py -- petit-pas's counting rule as the bench's regression test (FINDING-L02's close).

The inversion this file encodes: w(boundary of R) = #{masses in R} + sum ind(images in R)
(petit-pas, c19012 on #1439) is now the SPEC, and the instrument is what gets audited. A
mismatch is treated as Newton missing zeros (or a boundary grazing a zero) until proven
otherwise -- that is exactly how the -24 annulus miss was caught before any re-run.

Random trials: 1-3 masses at random positions/strengths, a random source, a random circular
test region kept clear of masses and found zeros by a margin (a winding along a curve that
grazes a zero is numerically meaningless). Each trial asserts the rule. Exit 0 all pass,
exit 1 with the offending configuration printed otherwise.

Deterministic seed: reruns must reproduce a failure exactly.
"""

import math
import random
import sys
from lens import V, jac, newton, winding, circle
from sweep1439 import all_zeros

random.seed(1439)  # the thread the rule came from; fixed so failures reproduce

TRIALS = 12
MARGIN = 0.08


def near_mass_starts(lenses, span=0.15, m=14):
    out = []
    for (px, py, _) in lenses:
        for a in range(m):
            for b in range(m):
                out.append((px - span + 2 * span * a / (m - 1), py - span + 2 * span * b / (m - 1)))
    return out


def trial(k):
    n_mass = random.choice([1, 2, 2, 3])
    lenses = [(random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5), random.uniform(0.5, 1.2))
              for _ in range(n_mass)]
    y = (random.uniform(-2, 2), random.uniform(-2, 2))
    zeros = all_zeros(lenses, y, span=8.0, n=70, extra_starts=near_mass_starts(lenses))
    for _ in range(60):
        cx, cy = random.uniform(-2, 2), random.uniform(-2, 2)
        r = random.uniform(0.3, 2.2)
        pts = [(px, py) for (px, py, _) in lenses] + [x for (x, _) in zeros]
        if all(abs(math.hypot(px - cx, py - cy) - r) > MARGIN for (px, py) in pts):
            break
    else:
        return None  # no clean region found; skip, and say so
    w = winding(circle(cx, cy, r), lenses, y)
    inside_m = sum(1 for (px, py, _) in lenses if math.hypot(px - cx, py - cy) < r)
    inside_ind = sum(s for (x, s) in zeros if math.hypot(x[0] - cx, x[1] - cy) < r)
    ok = w == inside_m + inside_ind
    print(f"trial {k:2d}: {n_mass} masses  y=({y[0]:+.2f},{y[1]:+.2f})  region ({cx:+.2f},{cy:+.2f}) r={r:.2f}  "
          f"w={w}  masses_in={inside_m}  ind_in={inside_ind:+d}  {'PASS' if ok else 'FAIL'}")
    if not ok:
        print(f"  FAIL config: lenses={lenses} y={y} region=({cx},{cy},{r})")
        print(f"  zeros found: {[(x, s) for (x, s) in zeros]}")
        print("  diagnosis order: (1) Newton missed a zero in the region; (2) boundary grazes a zero;")
        print("  (3) only then suspect the rule.")
    return ok


if __name__ == "__main__":
    results = []
    for k in range(TRIALS):
        r = trial(k)
        if r is None:
            print(f"trial {k:2d}: no region clear of zeros/masses by {MARGIN}; skipped")
        else:
            results.append(r)
    print(f"\n{sum(results)}/{len(results)} passed ({TRIALS - len(results)} skipped)")
    sys.exit(0 if all(results) else 1)
