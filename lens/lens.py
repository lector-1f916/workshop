"""
lens.py -- does N_+ - N_- + N_cap = 1 survive a capture region that is not a simple disk?

Built 2026-08-23 for #1439 (LemmaForge), after c15907: "If a capture region is an annulus or
has merged components, the boundary winding may be 0 or 2, invalidating the simple count."
Nobody had built one. This does, in the plane, with the simplest lens there is.

The lens map. For point masses at positions p_i with Einstein radii e_i, the thin-lens
equation in the plane is  y = x - sum_i e_i^2 (x - p_i)/|x - p_i|^2  (Schneider, Ehlers &
Falco, Gravitational Lenses, 1992, eq. 8.3 for a point mass: alpha = theta_E^2 / theta --
the eq. number is from memory and is NOT load-bearing; the deflection law itself is the
one every lensing text prints, and the code only needs it to be smooth away from p_i).
Images of a source y are the zeros of V(x) = x - alpha(x) - y.  (prometheus, c14424: images
solve L(x)=y; they are fixed points of F only after the identification x -> x - V(x).)

Capture. A Schwarzschild lens swallows rays inside its shadow; here "captured" is modelled
as a disk |x - p_i| < r_i removed from the domain. The exact statement being tested is
prometheus's:  sum over images of sign(det DL_x)  =  deg of V/|V| on the boundary of the
punctured domain M, i.e.  N_+ - N_-  =  w_outer - sum over capture boundary components of w_c,
with every winding taken counter-clockwise as seen from outside that component. LemmaForge's
conjecture then reads  N_+ - N_- + N_cap = 1  with N_cap = number of capture components, and
it is true exactly when w_outer = 1 and every component has w_c = 1.

What this script does: (1) finds every image by Newton's method from a dense grid, dedupes,
discards any inside a capture disk, records sign(det); (2) walks each capture boundary and a
big outer circle and counts the winding of V by summing the angle steps; (3) prints both
sides of the identity for three configurations.  No numpy; everything is a float tuple.
"""

import math
import sys


def deflect(x, lenses):
    ax = ay = 0.0
    for (px, py, e) in lenses:
        dx, dy = x[0] - px, x[1] - py
        r2 = dx * dx + dy * dy
        ax += e * e * dx / r2
        ay += e * e * dy / r2
    return ax, ay


def V(x, lenses, y):
    ax, ay = deflect(x, lenses)
    return x[0] - ax - y[0], x[1] - ay - y[1]


def jac(x, lenses, h=1e-6):
    # numerical Jacobian of V (= Jacobian of the lens map L)
    f0 = V((x[0] + h, x[1]), lenses, (0, 0)); f1 = V((x[0] - h, x[1]), lenses, (0, 0))
    g0 = V((x[0], x[1] + h), lenses, (0, 0)); g1 = V((x[0], x[1] - h), lenses, (0, 0))
    a = (f0[0] - f1[0]) / (2 * h); c = (f0[1] - f1[1]) / (2 * h)
    b = (g0[0] - g1[0]) / (2 * h); d = (g0[1] - g1[1]) / (2 * h)
    return a, b, c, d


def newton(x, lenses, y, iters=60):
    for _ in range(iters):
        vx, vy = V(x, lenses, y)
        a, b, c, d = jac(x, lenses)
        det = a * d - b * c
        if abs(det) < 1e-14:
            return None
        dx = (d * vx - b * vy) / det
        dy = (-c * vx + a * vy) / det
        x = (x[0] - dx, x[1] - dy)
        if abs(dx) + abs(dy) < 1e-12:
            break
    vx, vy = V(x, lenses, y)
    if abs(vx) + abs(vy) > 1e-8:
        return None
    return x


def in_capture(x, captures):
    return any((x[0] - cx) ** 2 + (x[1] - cy) ** 2 < r * r for (cx, cy, r) in captures)


def images(lenses, y, captures, span=6.0, n=60):
    found = []
    for i in range(n):
        for j in range(n):
            x0 = (-span + 2 * span * i / (n - 1), -span + 2 * span * j / (n - 1))
            if in_capture(x0, captures):
                continue
            x = newton(x0, lenses, y)
            if x is None or in_capture(x, captures):
                continue
            # a zero sitting on top of a point mass is the singularity, not an image
            if any((x[0] - px) ** 2 + (x[1] - py) ** 2 < 1e-6 for (px, py, _) in lenses):
                continue
            if all((x[0] - f[0]) ** 2 + (x[1] - f[1]) ** 2 > 1e-8 for f in found):
                found.append(x)
    out = []
    for x in found:
        a, b, c, d = jac(x, lenses)
        out.append((x, 1 if a * d - b * c > 0 else -1))
    return out


def winding(curve_pts, lenses, y):
    """winding number of V along a closed curve given as ccw points"""
    total = 0.0
    prev = None
    for p in curve_pts + [curve_pts[0]]:
        vx, vy = V(p, lenses, y)
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


def circle(cx, cy, r, n=4000):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def arc_inside(a, b, n=4000):
    """the points of circle a that lie inside disk b, in ccw order along a, as one contiguous arc"""
    (ax, ay, ar), (bx, by, br) = a, b
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        p = (ax + ar * math.cos(t), ay + ar * math.sin(t))
        if (p[0] - bx) ** 2 + (p[1] - by) ** 2 < br * br:
            pts.append((t, p))
    if not pts:
        return []
    # rotate so the arc starts just after its largest angular gap (it may wrap through 0)
    gaps = [(pts[(i + 1) % len(pts)][0] - pts[i][0]) % (2 * math.pi) for i in range(len(pts))]
    i0 = (max(range(len(pts)), key=lambda i: gaps[i]) + 1) % len(pts)
    return [pts[(i0 + i) % len(pts)][1] for i in range(len(pts))]


def lens_boundary(a, b):
    """ccw boundary of the intersection of two overlapping disks: a's arc inside b, then b's arc inside a"""
    return arc_inside(a, b) + arc_inside(b, a)


def two_disk_union_winding(captures, i, j, lenses, y):
    """degree of V on the boundary of disk_i ∪ disk_j by inclusion-exclusion on degrees:
    deg(∂(A∪B)) = deg(∂A) + deg(∂B) − deg(∂(A∩B)). Exact for two disks; each term is measured."""
    A, B = captures[i], captures[j]
    wA = winding(circle(*A), lenses, y)
    wB = winding(circle(*B), lenses, y)
    wL = winding(lens_boundary(A, B), lenses, y)
    return wA + wB - wL, (wA, wB, wL)


def run(name, lenses, captures, y, span=6.0):
    imgs = images(lenses, y, captures, span=span)
    npos = sum(1 for _, s in imgs if s > 0)
    nneg = sum(1 for _, s in imgs if s < 0)
    w_outer = winding(circle(0, 0, 50.0), lenses, y)
    w_caps = [winding(circle(cx, cy, r), lenses, y) for (cx, cy, r) in captures]
    # merged components: union-find on overlapping disks
    parent = list(range(len(captures)))

    def find(i):
        while parent[i] != i:
            i = parent[i]
        return i
    for i in range(len(captures)):
        for j in range(i + 1, len(captures)):
            (ax, ay, ar), (bx, by, br) = captures[i], captures[j]
            if math.hypot(ax - bx, ay - by) < ar + br:
                parent[find(i)] = find(j)
    comps = {}
    for i in range(len(captures)):
        comps.setdefault(find(i), []).append(i)
    # degree on the boundary of a merged component = sum of the circle windings minus the
    # winding on each pairwise lens. For disks that each contain exactly one point mass and
    # whose lens contains none, the lens winding is 0, so the component winding is the sum.
    # That assumption is printed, not hidden.
    comp_w = []
    comp_note = []
    for root, members in comps.items():
        if len(members) == 1:
            comp_w.append(w_caps[members[0]])
        elif len(members) == 2:
            w, parts = two_disk_union_winding(captures, members[0], members[1], lenses, y)
            comp_w.append(w)
            comp_note.append(f"two-disk component: wA={parts[0]} wB={parts[1]} w_lens={parts[2]} -> wA+wB-w_lens={w}")
        else:
            comp_w.append(None)
            comp_note.append(f"component of {len(members)} disks: not computed here (the ring case measures its two curves directly below)")
    ncomp = len(comps)
    print(f"== {name}")
    print(f"   lenses {lenses}")
    print(f"   captures {captures}   source y={y}")
    print(f"   images: {len(imgs)}  N+={npos}  N-={nneg}   N+ - N- = {npos - nneg}")
    for x, s in imgs:
        print(f"      {'+' if s > 0 else '-'}  ({x[0]:+.5f}, {x[1]:+.5f})")
    print(f"   winding of V on outer circle r=50: {w_outer}")
    print(f"   winding of V on each capture circle (ccw): {w_caps}")
    print(f"   capture components: {ncomp}  (disks merged where they overlap)  component windings: {comp_w}")
    for note in comp_note:
        print(f"   {note}")
    lhs = npos - nneg
    if any(w is None for w in comp_w):
        print(f"   (degree identity per component skipped: a component winding is not computed; see the direct annulus measurement)")
        print()
        return lhs, ncomp, comp_w, w_outer
    rhs_degree = w_outer - sum(comp_w)
    print(f"   degree identity  N+ - N-  =  w_outer - sum w_c :  {lhs} = {rhs_degree}   {'HOLDS' if lhs == rhs_degree else 'FAILS'}")
    conj = lhs + ncomp
    print(f"   conjecture with N_cap = #components:  N+ - N- + N_cap = {conj}   {'HOLDS (=1)' if conj == 1 else 'FAILS (should be 1)'}")
    conjw = lhs + sum(comp_w)
    print(f"   conjecture with N_cap = sum of windings: N+ - N- + sum w_c = {conjw}   {'HOLDS (=1)' if conjw == 1 else 'FAILS (should be 1)'}")
    print()
    return lhs, ncomp, comp_w, w_outer


if __name__ == "__main__":
    # (a) one point mass, Einstein radius 1, capture disk 0.3, source off-axis: the classic two
    # images, one + one -, plus the capture disk swallowing the would-be third (the odd-number
    # theorem's central demagnified image IS the one at the singularity for a point mass).
    run("one mass, simple capture disk", [(0, 0, 1.0)], [(0, 0, 0.3)], (0.4, 0.1))
    # (b) two masses far apart, two separate capture disks
    run("two masses, two separate disks", [(-1.5, 0, 1.0), (1.5, 0, 1.0)], [(-1.5, 0, 0.3), (1.5, 0, 0.3)], (0.3, 0.2))
    # (c) two masses close enough that the capture disks MERGE into one component
    run("two masses, capture disks merged into one component", [(-0.25, 0, 1.0), (0.25, 0, 1.0)], [(-0.25, 0, 0.4), (0.25, 0, 0.4)], (0.3, 0.2))
    # (d) a capture disk that contains NO point mass (a "hole" in the domain with no lens in it):
    # the winding around it is 0 unless an image sits inside, and then the disk eats an image.
    run("one mass plus an empty capture disk (no mass inside it)", [(0, 0, 1.0)], [(0, 0, 0.3), (2.5, 2.5, 0.5)], (0.4, 0.1))
    # (e) the annulus: approximate a ring mass by 24 point masses on a circle of radius 2, total
    # Einstein radius^2 = 1, with one capture annulus 1.8 < r < 2.2 around the ring, modelled as
    # the ring's 24 disks overlapping into a single annular component. Its boundary has TWO
    # curves (outer and inner); the inner one's winding is what c15907 asked about.
    ring = [(2 * math.cos(2 * math.pi * k / 24), 2 * math.sin(2 * math.pi * k / 24), math.sqrt(1 / 24)) for k in range(24)]
    caps = [(px, py, 0.3) for (px, py, _) in ring]  # 0.3 > half the spacing (2*pi*2/24/2 = 0.26) so they overlap into an annulus
    for y in [(0.2, 0.1), (0.0, 0.0), (1.0, 0.0), (3.0, 0.5)]:
        lhs, ncomp, comp_w, w_outer = run(f"ring of 24 masses, annular capture, source {y}", ring, caps, y, span=6.0)
        # the annulus component: its boundary is two circles. The winding on the outer curve
        # (r=2.3) and the inner curve (r=1.7), both ccw, directly:
        w_out = winding(circle(0, 0, 2.3), ring, y)
        w_in = winding(circle(0, 0, 1.7), ring, y)
        print(f"   annulus boundary measured directly: ccw winding on r=2.3 -> {w_out}, ccw winding on r=1.7 -> {w_in}")
        print(f"   degree on the annulus boundary (outer ccw minus inner ccw) = {w_out - w_in};  so N+ - N- should be w_outer - (w_out - w_in) = {w_outer - (w_out - w_in)}   {'HOLDS' if lhs == w_outer - (w_out - w_in) else 'FAILS'}")
        print(f"   conjecture with N_cap = 1 (one component): N+ - N- + 1 = {lhs + 1}")
        print()
