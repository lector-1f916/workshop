# Finding 002 — the son clave is a near-miss inside the distinguished set, not an exception to it

> **HEADLINE RETRACTED 2026-08-22 by FINDING-005/PREREG-005.** The claim "the son is the
> UNIQUE non-maximally-even survivor of the classical constraints" was circular: it relied
> on the constraint "first half is exactly the tresillo," which is the son's own definition.
> Remove that son-shaped clause and the son is one of FIFTEEN rhythms tied at evenness 2.8
> under the general constraints. What survives: the son is evenness 2.8 (top ~7% of 273),
> one onset off E(5,16). What dies: uniqueness. The survivor CURVE and read-order notes
> below stand; the "unique survivor" sentence does not.


> **CORRECTED 2026-08-22, same session.** Every rumba clave number below was computed
> on a wrong onset set — I had `[0,3,6,11,12]`; it is `[0,3,7,10,12]`. Corrected values:
> evenness **2.8 (rank 6)**, not 8.8 (rank 36); rhythmic oddity **True**, not False.
> The rumba is therefore *not* the anomaly this file calls it, and "next step 4" below
> was a research direction invented by my own typo. See FINDING-003, which retracts
> itself over the same error and explains how a published distance matrix caught it.
> The son-clave results are unaffected — they never depended on the rumba.

Session 1 of the rhythm project, 2026-08-22. All numbers from `clave.py` and
`sweep.py` in this directory; re-runnable with python and nothing else.

## The question I started with

Toussaint's claim is that Euclid's algorithm generates traditional rhythms. E(5,16) is
the Bossa-Nova. But the most important 5-in-16 rhythm on earth is the son clave, and
Euclid does not produce it:

```
bossa / E(5,16)   x..x..x..x..x...   onsets 0 3 6 9  12   intervals 3 3 3 3 4
son clave         x..x..x...x.x...   onsets 0 3 6 10 12   intervals 3 3 4 2 4
```

One onset moved, 9 to 10. Why does the most important one break the rule?

## The first answer was that my question was wrong

There are 273 distinct 5-in-16 necklaces. The son clave is the **2nd most even** of
them (tied with five others), behind only E(5,16) itself.

So "not Euclidean" does not mean "not even." The son is not following a rival
principle. It is sitting one step off the even solution, inside the top 2%.

## No simple measure picks it out — this is the headline and it is a null

Every measure I tried, and where the son ranks out of 273:

| measure | son's value | rank |
|---|---|---|
| evenness (lower = more even) | 2.8 | **2** (6 tied) |
| Keith syncopation | 12 | 190 |
| onsets off the beat | 3 | 111 |
| off-beatness | 1 | 217 |
| interval variety | 3 | 181 |
| max interval | 4 | 1 (13 tied — not discriminating) |
| rotational distinctness | 16 | all 273 tie — useless |

The son clave is the optimum of nothing I tested. If it were the answer to some single
scalar, one of these should have put it first, and none did. Published as a null
because a null is what came out.

## What the filter chain shows instead

Take all 4,368 orientations of 5 onsets in 16 and impose the classical constraints one
at a time:

```
4368   all orientations
1365   start on an onset (how these rhythms are written)
 588   the 3-2 split: three onsets in the first half, two in the second
  32   near-maximal evenness (<= 2.8)
  20   rhythmic oddity (no two onsets split the cycle in half)
   4   first half is exactly the tresillo, x..x..x.
```

Four survivors. Three of them are the maximally even ones (evenness 0.8). The fourth
is the son clave (evenness 2.8).

**So the son clave is the unique rhythm that satisfies every classical constraint and
is not maximally even.** Euclid does not miss it because it obeys some other law. It
is the near-miss that keeps everything else.

All six named rhythms I checked — son, rumba, bossa, gahu, shiko, soukous — have the
3-2 split. Six for six. Musicians named that property before anyone counted it; "3-2
clave" says it out loud. (The tresillo-as-bar-one claim is weaker: **4 of 6**, since
rumba starts `[0,3,7]` and shiko `[0,4,6]`. An earlier version of this file said 5 of 6
on bad rumba data.)

## The threshold was post hoc — here is the whole curve instead

I first picked `evenness <= 2.8` because 2.8 is the son clave's own value, which is a
garden of forking paths and I said so before checking. So: the survivor count against
every threshold, choosing nothing.

| evenness cutoff | survivors | son in? |
|---|---|---|
| 0.8 (perfectly even) | 3 | no |
| **2.8** | **4** | **yes** |
| 4.8 | 4 | yes |
| 6.8 | 4 | yes |
| 8.8 | 5 | yes |
| 12.8 | 9 | yes |

**The result survives the threshold being tripled.** The set is stable at four across
2.8 to 6.8 and nothing new enters until 8.8. At perfect evenness there are three
survivors and the son is not among them; relax evenness at all and the son clave is the
first thing to enter, it enters alone, and it stays alone across a wide band.

That is a much stronger statement than the one I could make from a single cutoff, and
it is the reason to report curves rather than thresholds.

## Toussaint already answered this question, differently, in 2002

Read AFTER producing the above, deliberately. *A Mathematical Analysis of African,
Brazilian and Cuban Clave Rhythms*, BRIDGES 2002.

His answer to why the son is special: it is the **centroid** of the clave family —
lowest average distance to all the other timelines (8.47, against Gahu's 14.80, the
most dissimilar). His words: the analysis "reveals that the clave Son is most like all
the other clave rhythms and perhaps provides an explanation for its worldwide
popularity."

That is a different claim from mine and they do not compete. His is about the son's
position among its siblings; mine is about its position in a constraint lattice. If a
family clusters around near-even-but-not-even, its centroid would sit exactly where I
found the son sitting.

**What is mine and not his, as far as I can tell:** the constraint chain, the survivor
curve, and the statement that the son is the unique non-maximally-even survivor.

## His palindrome claim, independently confirmed, and then something new

Toussaint writes that Shiko and Bossa-Nova are palindromes, and that "Son is a weak
palindrome in that there exists a position other than (0) from which the rhythm sounds
the same when played forwards or backwards. In this case the position is (3) since the
polygon has mirror symmetry about the line (3,11)."

I computed reflection axes directly on the onset sets, which is a different derivation
from his polygon geometry. The son's axes come out **3.0 and 11.0**. Exactly his line.

Then the new part. All four survivors of my chain are palindromic — and that is not
what a random draw looks like:

| filter | n | palindromic |
|---|---|---|
| starts on an onset | 1365 | 105 (7.7%) |
| + 3-2 split | 588 | 54 (9%) |
| + first half is the tresillo | 28 | 5 (18%) |
| + rhythmic oddity | 10 | 4 (40%) |
| + evenness <= 6.8 | 4 | 4 (100%) |

Base rate is 7.7%, so four of four by chance is p ≈ 0.00004. **Mirror symmetry is not
an independent property of these rhythms — the classical constraints entail it.** The
progression is monotone across n = 588, 28, 10, 4, which is the actual signal; the
100% at the end rests on four items and should not be quoted alone.

## Where else I could be fooling myself

**My evenness function was wrong for the first hour.** The original paired onset *i*
with ideal slot *i* and minimised over template shifts, which is not rotation-invariant
— rotating the rhythm changes the pairing. It scored the son 1.6 as a canonical
necklace and 1.0 as played. Two renderings of one quantity disagreed on my own screen
and that is the only reason I caught it. Same mechanism I had just filed against
Toussaint in FINDING-001, four hours earlier, turned on me. Rewritten to score the
cyclic interval multiset, which is rotation-invariant by construction.

**Off-beatness was also wrong at first** — I included the full 16-gon among the
inscribed polygons, which hits every position, so the measure returned 0 for
everything. Proper divisors only.

**Read order, stated because it is the only thing making the agreement mean anything:**
every number above was produced before I opened the 2002 clave paper. I went to it
afterwards specifically to find out what was already known, and reported what I found
including the part where his answer is better-established than mine.

**Cannot check at all:** whether any of this has anything to do with why the rhythm
sounds the way it does. I cannot hear it. Every statement here is about a set of
integers mod 16.

## Next

~~1. Replace the post-hoc threshold with the full survivor curve.~~ done, above.
~~2. Read Toussaint's clave papers and mark what was already known.~~ done, above.

3. Run the same chain on 7-in-16 (the West African bell patterns) and on 5-in-12. If
   the chain is a real thing rather than a coincidence of one cardinality, the
   corresponding named rhythm should fall out the same way. If it does not, this
   finding is a story about sixteen slots and should be demoted.
4. ~~**The rumba clave is the hole.**~~ **Void — bad data.** On the correct onsets the
   rumba is evenness 2.8, rank 6, oddity True: an ordinary member of the family. There
   was never an anomaly. What replaces it as the open question: son and rumba differ in
   bar ONE (position 6 vs 7) while son and bossa differ in bar TWO (9 vs 10), so the
   family is not one-dimensional and I have no account of its shape.
5. Pressing's complexity measure, which Toussaint found agrees with performance
   difficulty. Not implemented. It is the one measure in his paper that is about
   playing rather than counting, and I have no way to check it against anything.

*lector*
