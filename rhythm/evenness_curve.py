"""
evenness_curve.py — the whole curve, so there is no threshold to tune.

FINDING-002 claimed the Son clave was "the unique non-maximally-even survivor" of a
filter. PREREG-005 showed the filter was chosen because the Son satisfies it, i.e. the
constraint-selection form of Gelman & Loken's forking paths (2013): "the researcher
degrees of freedom do not feel like degrees of freedom because, conditional on the data,
each choice appears to be deterministic."

The fix is not a better threshold. It is no threshold. Enumerate every 5-onset pattern in
a timespan of 16, score all of them, and publish where the six named rhythms land in the
full distribution. A percentile needs no cut-off, so there is no fork to walk down.

EVENNESS MEASURE, sourced on the line it is used:
  [DG] Demaine, Gomez-Martin, Meijer, Rappaport, Taslakian, Toussaint, Winograd, Wood,
       "The Distance Geometry of Music", arXiv:0705.4085:
       "The measure of evenness we consider here is the sum of all pairwise Euclidean
        distances between points on the circle, as described by Block and Douthett
        [BD94]. This measure is more discriminating than the others, and is therefore
        the preferred measure of evenness."
  Same paper, the validation target this file checks itself against:
       "this measure distinguishes all of the six rhythms in Figure 1, ranking the
        Bossa-Nova rhythm as the most even, followed by the Son, Rumba, Shiko, Gahu,
        and Soukous."
  And the claim the curve is testing:
       "Euclidean rhythms are the unique rhythms that maximize this notion of evenness."
"""
import math
from itertools import combinations
from rhythms_sourced import RHYTHMS, TIMESPAN
from bjorklund import bjorklund

N = TIMESPAN          # 16
K = 5                 # onsets in all six named 4/4 clave/bell timelines

def evenness(onsets, n=N):
    """Sum of all pairwise Euclidean (chordal) distances, unit circle. [DG], above."""
    pts = [(math.cos(2*math.pi*o/n), math.sin(2*math.pi*o/n)) for o in onsets]
    return sum(math.dist(pts[i], pts[j])
               for i in range(len(pts)) for j in range(i+1, len(pts)))

def canonical(onsets, n=N):
    """Rotation class representative, so a necklace is counted once."""
    best = None
    for r in range(n):
        rot = tuple(sorted(((o + r) % n) for o in onsets))
        if best is None or rot < best:
            best = rot
    return best

def euclidean_onsets(k, n):
    """E(k,n) as an onset list, from the local Bjorklund implementation."""
    pat = bjorklund(k, n)
    return [i for i, b in enumerate(pat) if b]

# ---- the full enumeration, no filter of any kind -------------------------------------
all_subsets = [tuple(c) for c in combinations(range(N), K)]
necklaces = sorted({canonical(s) for s in all_subsets})
scored_neck = sorted(((evenness(s), s) for s in necklaces), reverse=True)
scored_subs = sorted((evenness(s) for s in all_subsets), reverse=True)

print(f"5-onset patterns in timespan 16: {len(all_subsets)} subsets, "
      f"{len(necklaces)} rotation classes")
print()

# ---- self-check against the paper's own printed ranking -------------------------------
named = {name: (onsets, note) for name, (onsets, note) in RHYTHMS.items()}
order = sorted(named, key=lambda nm: evenness(named[nm][0]), reverse=True)
expected = ["bossa-nova", "son", "rumba", "shiko", "gahu", "soukous"]
print("VALIDATION — [DG]'s printed ranking of the six, recomputed here:")
print("  computed:", " > ".join(order))
print("  printed :", " > ".join(expected))
print("  MATCH" if order == expected else "  *** MISMATCH — stop and fix before reading on")
print()

# ---- where E(5,16) sits ---------------------------------------------------------------
e516 = euclidean_onsets(K, N)
e516_score = evenness(e516)
top = scored_neck[0]
print(f"E(5,16) from bjorklund.py = {e516}  evenness {e516_score:.6f}")
print(f"most even rotation class  = {list(top[1])}  evenness {top[0]:.6f}")
print("  E(5,16) IS the maximum" if abs(e516_score - top[0]) < 1e-9
      else "  E(5,16) is NOT the maximum -- that would refute [DG]")
ties_at_max = [s for v, s in scored_neck if abs(v - top[0]) < 1e-9]
print(f"  rotation classes tied at the maximum: {len(ties_at_max)}")
print()

# ---- THE CURVE: every named rhythm's position, no cut-off ------------------------------
print("THE WHOLE CURVE — each named rhythm's place among all 5-in-16 patterns.")
print("No threshold is applied anywhere in this file.")
print()
print(f"{'rhythm':11s} {'evenness':>10s} {'rank/necklace':>14s} {'pctile':>7s} "
      f"{'rank/subset':>12s} {'pctile':>7s}  box")
for nm in order:
    onsets = named[nm][0]
    v = evenness(onsets)
    rn = sum(1 for x, _ in scored_neck if x > v + 1e-9) + 1
    rs = sum(1 for x in scored_subs if x > v + 1e-9) + 1
    pn = 100.0 * (len(scored_neck) - rn + 1) / len(scored_neck)
    ps = 100.0 * (len(scored_subs) - rs + 1) / len(scored_subs)
    box = "".join("x" if i in onsets else "." for i in range(N))
    print(f"{nm:11s} {v:10.6f} {rn:8d}/{len(scored_neck):<5d} {pn:6.2f}% "
          f"{rs:6d}/{len(scored_subs):<5d} {ps:6.2f}%  {box}")
print()

# ---- the distribution itself, so a reader can see the shape ---------------------------
vals = [v for v, _ in scored_neck]
lo, hi = min(vals), max(vals)
BINS = 20
counts = [0]*BINS
for v in vals:
    b = min(BINS-1, int(BINS * (v - lo) / (hi - lo)))
    counts[b] += 1
print(f"distribution over {len(vals)} rotation classes, evenness {lo:.4f}..{hi:.4f}")
for b in range(BINS-1, -1, -1):
    edge = lo + (hi - lo) * b / BINS
    print(f"  {edge:7.4f} {'#' * counts[b]:<40s} {counts[b]}")

# ---- the top of the curve, named where a name exists ----------------------------------
print()
print("TOP 20 ROTATION CLASSES of the 273, with the traditional names attached.")
print("The unnamed ones are the interesting part: patterns more even than a named")
print("rhythm that no tradition in Toussaint's set appears to have selected.")
by_canon = {canonical(named[nm][0]): nm for nm in named}
for i, (v, s) in enumerate(scored_neck[:20], 1):
    nm = by_canon.get(s, "")
    box = "".join("x" if j in s else "." for j in range(N))
    print(f"  {i:3d}  {v:10.6f}  {box}  {nm}")

# ---- chirality: the measure cannot see mirror images -----------------------------------
print()
print("CHIRALITY. Sum-of-pairwise-Euclidean-distance is invariant under reflection, so a")
print("pattern and its mirror image always score identically. Which of the six are")
print("palindromic (their own mirror, as necklaces) and which have an unnamed twin?")
print()
def mirror(onsets, n=N):
    return canonical(tuple(sorted((-o) % n for o in onsets)), n)
for nm in order:
    c = canonical(named[nm][0])
    m = mirror(named[nm][0])
    v = evenness(named[nm][0])
    rn = sum(1 for x, _ in scored_neck if x > v + 1e-9) + 1
    tied = [s for x, s in scored_neck if abs(x - v) < 1e-9]
    twin = "self (palindrome)" if m == c else \
        "twin " + "".join("x" if j in m else "." for j in range(N)) + \
        (" [named: " + by_canon[m] + "]" if m in by_canon else " [UNNAMED]")
    print(f"  {nm:11s} rank {rn:3d}  tied_classes {len(tied)}  {twin}")

vals_all = [v for v, _ in scored_neck]
lo, hi = min(vals_all), max(vals_all)
son_v = evenness(named['son'][0])
print()
print(f"Range of the whole space: {lo:.6f} .. {hi:.6f}  (spread {hi-lo:.6f})")
print(f"Son sits {(hi-son_v):.6f} below the maximum, i.e. "
      f"{100*(son_v-lo)/(hi-lo):.3f}% of the way from floor to ceiling.")

# ---- the three unnamed twins, written out for anyone with a bigger corpus --------------
print()
print("THE THREE UNNAMED TWINS, in the forms a reader can look up. If any of these is a")
print("named timeline somewhere, the chirality observation below is dead and I want to")
print("know. Neither paper on disk (Toussaint 2002, Demaine et al. 2007) names them.")
for nm in ["rumba", "gahu", "soukous"]:
    m = mirror(named[nm][0])
    on = list(m)
    iv = tuple((on[(i+1) % K] - on[i]) % N for i in range(K))
    box = "".join("x" if j in m else "." for j in range(N))
    print(f"  mirror of {nm:8s}  {box}  onsets {on}  intervals {iv}  "
          f"reduced {tuple(x-1 for x in iv)}")
