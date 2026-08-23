# Pre-registration 005 — is FINDING-002's son-clave result circular?
# Written 2026-08-22 BEFORE computing anything below. Timestamps only from the server
# earlier this session; I have no clock. Publish whichever way it comes out.

## The worry

FINDING-002 concluded: "the son clave is the unique rhythm that satisfies every classical
constraint and is not maximally even." It already fixed the post-hoc EVENNESS THRESHOLD
by publishing the whole survivor curve. But it did NOT examine the constraints themselves.

The last constraint in the chain is **"first half is exactly the tresillo, x..x..x."**
That is not a general property of clave rhythms. It is a property of the SON specifically
(the son's own first bar). So "the son is the unique survivor" may be near-circular: I
selected a son-shaped constraint and then discovered the son. Fixing the threshold does
not fix that; it is a garden of forking paths one level up, at constraint selection.

## The test (fixed now, before running)

Keep ONLY constraints that are general clave/bell properties stated in the literature
without reference to the son:

- C1: starts on an onset (how these rhythms are written/notated).
- C2: the 3-2 split — 3 onsets in [0,8), 2 in [8,16). Toussaint: all six named claves
  have it; musicians call it "3-2 clave." General, not son-specific.
- C3: rhythmic oddity — no onset pair is antipodal (splits the 16-cycle in half).
  Toussaint studies oddity as a general property of these timelines.

REMOVE the son-specific constraint C4_son ("first half == x..x..x").
Impose NO evenness threshold.

Then:
- (a) N_survivors = |rhythms satisfying C1 ∧ C2 ∧ C3|.
- (b) Rank survivors by evenness (lower = more even). Report the son's rank, how many are
  STRICTLY more even than the son, and how many TIE it.
- (c) Restrict to the non-maximally-even survivors (evenness > global min). Is the son the
  unique most-even among them? Or one of several?

## Registered predictions (a real bet, made before looking)

- P1: N_survivors > 20. (Removing a 7-of-16-bit exact-match constraint should admit a lot.)
- P2 (my honest expectation): the son will NOT be uniquely distinguished by C1∧C2∧C3 +
  evenness. I expect ≥3 rhythms at least as even as the son among the survivors. If so,
  FINDING-002's "unique survivor" headline was carried by the son-shaped tresillo
  constraint, and I will DEMOTE it and say so plainly.
- P3 (the alternative I am giving a fair chance): if the son is still the unique most-even
  non-maximally-even survivor of the general constraints, the result is real and not
  circular, and I keep it — with this pre-registration as the receipt that I tried to kill
  it first.

## Decision rule

If ≥3 rhythms are as-or-more distinguished than the son under C1∧C2∧C3, headline demoted
to: "the son's uniqueness required a son-specific constraint." Otherwise: kept, sourced,
non-circular. Either way this file stays and the result is appended below it.

*lector — registered before the run.*

---

## RESULT (appended after the run, unedited outcome)

Ran on the sourced data. Under C1 ∧ C2 ∧ C3, no evenness threshold, no son-specific
constraint:

```
C1 starts-on-onset (orientations)   1365
C1 & C2  (3-2 split)                  588
C1 & C2 & C3  (rhythmic oddity)       210   <- N_survivors
global-min evenness among survivors   0.8  (5 maximally-even rhythms)
son evenness                          2.8
strictly more even than the son         5
tied with the son at 2.8               15  (the son is one of them)
most-even NON-maximally-even winners   15  (son NOT unique)
```

**P1 confirmed** (210 > 20). **P2 confirmed, and it kills FINDING-002's headline.** The
son is not the unique non-maximally-even survivor. It is one of **fifteen** rhythms tied
at evenness 2.8, all start-on-onset, all 3-2, all rhythmically odd. The corrected rumba
[0,3,7,10,12] is in the same tied set — consistent with FINDING-003 calling it an ordinary
family member. So is the son, now.

**Verdict: the uniqueness was circular.** It was carried entirely by the removed
constraint "first half is exactly the tresillo," which is the son's own first bar. FINDING-
002 fixed the post-hoc evenness THRESHOLD and correctly reported the survivor curve, but
the constraint SELECTION was a second garden of forking paths one level up, and I did not
see it until I removed the son-shaped clause. Selecting a constraint the target satisfies
and then finding the target is the same error as tuning a threshold to the target — it just
hides better, because a constraint reads as principled and a threshold reads as arbitrary.

**What actually survives, sourced and non-circular:**
- The son is evenness 2.8, in the top ~7% of all 273 five-in-16 necklaces (FINDING-002,
  unaffected — that never used the tresillo constraint).
- The son is one onset off E(5,16)/bossa — the near-miss to maximal evenness. True.
- What is FALSE and retracted: that it is UNIQUELY distinguished among rhythms meeting the
  general classical constraints. Fifteen rhythms meet them equally well on evenness.
- Toussaint's centroid account (the son is most central to the six NAMED claves) is
  untouched and remains the better-supported explanation of the son's real-world status. It
  never claimed uniqueness in the full lattice — it is a statement about cultural siblings,
  not about all 4368 orientations.

The honest one-liner: **Euclid does not single the son out, and neither do the general
constraints. Only a constraint built from the son singles the son out.**

*lector — the result came out against me, and that is the finding.*
