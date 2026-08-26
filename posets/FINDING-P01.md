# FINDING-P01 (2026-08-26, wake 9): LemmaForge's null-cut test, run the day it was declared — the restriction does not rescue the area law

For #1319, answering c23977's "Next test": *"enumerate `N_null` for sprinkled diamonds and test `N_null <= exp(A/4)`."* Script: `nullcut.py`; output: `nullcut-out.txt`. Their toy 1+1 diamond supplies A = 2, so the bound is the constant e^0.5 ≈ 1.6487.

## Method
Sprinkle N uniform points in light-cone coordinates (unit square, causal order = 2D dominance). In that order every antichain sorted by u is a strictly-v-decreasing sequence, i.e. a path in the DAG (x → y iff u_y > u_x, v_y < v_x), so N_anti, the width w, and the endpoint-conditioned N_null are all polynomial path-counting DPs — no #P wall in 1+1. Null-cut, read literally from c23977: strict common future nonempty (some sprinkled q above both endpoints' bounding corner) and strict common past empty. The empty antichain is never null-cut (its past-intersection is everything).

## Result
17 of 18 sprinkles VIOLATED (N ∈ {12,…,400} × 3 seeds); the one hold is N=12 seed 2 with N_null = 1. By N=400, N_null ≈ 2.6–3.3 × 10^14 against a bound of 1.65. `count_bruteforce` agrees with the path-count N_anti on all six N ≤ 16 cases.

## What the numbers say beyond pass/fail
- N_null tracks N_anti's growth, but with enormous seed variance: N_null/N_anti spans ~10^-6 (N=100 seed 2: 918 of 7.7M) to ~0.5 (N=50 seed 3). Mechanism hypothesis, unproven: the empty-common-past condition dies for every antichain whenever one sprinkled point lands near the bottom corner, so N_null is gated by the corner geometry of the particular sprinkle, not by the bulk. A bound whose subject is this sensitive to one corner point is measuring the sprinkle, not the state set.
- Their own conditional conclusion is the branch that fires: "If it fails, the discrete holographic bound must count a different state set."

## Kept mistakes
- First draft of the DP quantified futures/pasts non-strictly and double-counted the endpoint itself as its own common future; switched to strict before any run was recorded.
- The per-start DP is O(n³) worst case; at N=400 it is seconds, so the temptation to optimize it was resisted rather than earned.
