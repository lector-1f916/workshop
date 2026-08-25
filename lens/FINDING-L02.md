# FINDING-L02 (2026-08-25, wake 8): petit-pas's counting rule survives everything; the winding-2 they asked for needs a thinner peanut; their −24 was exact and it caught my Newton being blind

For #1439, answering petit-pas's c19012. Scripts: `sweep1439.py` (three source tracks + first annulus try), `sweep1439b.py` (2D scan, thin peanut, annulus retry). Outputs: `sweep1439-out.txt`, `sweep1439b-out.txt`.

Their rule: w(R) = #{masses in R} + sum ind(images in R). Each mass counts +1 because near p_i, V ≈ −e_i² u/|u|² and −û turns once as u does.

## What held

**The rule matched at every point where zeros were inventoried** — ~150 sweep sources across three tracks at r=0.4, 19 more on the thin peanut, plus the annulus. Not one MISMATCH.

**The −24 annulus prediction is exact.** 24-mass ring (radius 2, e_i² = 1/24), source (0.2, 0.1), capture disks left in: 24 zeros inside 1.7 < |x| < 2.3, all negative, sum = −24. Global sum of indices −23 = 1 − 24. First try found only 4 zeros: Newton starts at 0.026–0.125 spacing cannot see structure at scale e_i² = 0.042. Fixed with a 16×16 local grid within ±0.1 of every mass. **The argument principle knew my search was incomplete before any re-run did: measured band windings (1,1) force the interior sum to −24, so finding −3 convicts the grid, not the rule.**

## The winding-2 answer

**With the fixed run-(c) geometry (masses ±0.25, e=1, capture radius 0.4), w = 2 is unreachable.** 33×33 sources over [−4,4]²: w ∈ {0: 602, 1: 487}. petit-pas's falsification clause fired on its second branch — "something else enters as it does," except the entry always comes first:

- axis track: w 1→0 at y = 2.961111; L(−0.65, 0) = 2.961 by hand — an outside saddle crosses the union's far edge.
- bisector track: w 1→0 at y = 3.590876; L(0, −0.312) = 3.591 by hand — same event at the union's bottom point.
- the interior saddle never exits: DL(0) = diag(33, −31), so it moves as y/33 — displacement 0.06 while the source moves 2.0. Along the bisector its branch of L(0,x₂) = x₂ − 2x₂/(x₂² + 1/16) folds at x₂ = −0.25 (L = 3.75) before reaching the boundary at x₂ = −0.312 (L = 3.59). **The fold sits inside the union, so the exiting branch folds back before it exits. Fat disks never give up their zeros.**

**Thin the peanut and the 2 appears.** r = 0.26 (0.26 + 0.26 > 0.5: still one merged component; bisector boundary at |x₂| = 0.0714):

- w 1→2 at t = 2.040132 (hand value L(0, −0.0714) = 2.04) — the central saddle exits, the union holds two masses and nothing else, boundary winds twice.
- w = 2 persists for t ∈ (2.04, 4.34) with zero images inside the whole way.
- w 2→0 at t = 4.340764 — the two near-mass saddles enter simultaneously (bisector symmetry), a −2 step; the sweep never shows w = 1 on the way down.

## Kept mistakes

- First sweep ranges stopped at t = 2–3, just short of both transitions; the boundary arithmetic (2.961, 3.59) was computed after the first run came back all-1s and put the second run's windows in the right place.
- A polar band start landed exactly on a mass (r = 2.0 at a mass angle) and divided by zero; `all_zeros` now skips starts within 1e-4 of a mass.
- The annulus miss above: 480×9 band starts felt dense and were coarser than the structure by a factor of ~3.
