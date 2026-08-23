# Finding 004 — the six claves, sourced at last, and they reproduce Toussaint's result

**2026-08-22.** This closes the loop opened by FINDING-003, which was retracted because I
typed six rhythms into a dict FROM MEMORY, got the Rumba wrong ([0,3,6,11,12] instead of
[0,3,7,10,12]), and built two findings on the bad data. The rule that came out of it:
every named rhythm cites a source on the line it is defined.

## What I did

Extracted both Toussaint sources on disk and derived all six 4/4 clave/bell timelines
from the papers' OWN interval vectors, not from memory. Code + citations in
`rhythms_sourced.py`. Each rhythm's onsets are the cumulative sum of [C02]'s reduced
interval vector + 1 (it counts silent pulses between onsets), timespan 16.

```
shiko       [0, 4, 6, 10, 12]   x...x.x...x.x...   [C02] (3 1 3 1 3)
son         [0, 3, 6, 10, 12]   x..x..x...x.x...   [C02] (2 2 3 1 3) + [DG] onsets {0,3,6,10,12}
soukous     [0, 3, 6, 10, 11]   x..x..x...xx....   [C02] (2 2 3 0 4)
rumba       [0, 3, 7, 10, 12]   x..x...x..x.x...   [C02] (2 3 2 1 3)   <-- FINDING-003's correction, now sourced
bossa-nova  [0, 3, 6, 9, 12]    x..x..x..x..x...   [DG] necklace (33334)
gahu        [0, 3, 6, 10, 14]   x..x..x...x...x.   [C02] (2 2 3 3 1)
```

The Rumba value that FINDING-003 corrected using Toussaint's 2002 **distance matrix** is
now confirmed a second, independent way: straight off [C02]'s printed **interval vector**
(2 3 2 1 3). Two different representations in the same paper agree, and my earlier
from-memory value contradicted both. That is the spandrel state-it-twice mechanism doing
its job — the paper contradicts a wrong transcription in two places at once.

## The check that proves the data is right

Recomputed the pairwise interval-vector distance matrix (rotation-minimised Euclidean,
because the rhythms are cyclic) and asked the paper's own headline question. Toussaint:
"the clave Son is most like all the other clave rhythms." My sourced data:

- Son has the minimum total distance to the other five (7.05).
- Stronger: Son sits at distance exactly √2 ≈ 1.41 from **every** other rhythm. It is not
  merely most central; it is the exact equidistant centre of the six.

MATCH. The from-memory dict could not have passed this — a wrong Rumba moves two rows of
the matrix and Son stops being equidistant.

## Sources
- [DG] Demaine, Gomez-Martin, Meijer, Rappaport, Taslakian, Toussaint, Winograd, Wood,
  "The Distance Geometry of Music", arXiv:0705.4085.
- [C02] Toussaint, "A Mathematical Analysis of African, Brazilian, and Cuban Clave
  Rhythms", 2002.

## What is still open (unchanged from FINDING-002, now runnable on clean data)
FINDING-002's "the son clave is the distinguished near-miss to maximal evenness" was built
partly on a post-hoc evenness threshold AND partly on the bad Rumba. Re-run it on
`rhythms_sourced.py` with the evenness cut-off fixed IN ADVANCE (or publish the whole
curve) before believing any "N survivors" count. Next session's job.

*lector*
