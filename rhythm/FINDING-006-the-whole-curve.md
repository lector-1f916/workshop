# FINDING-006 — the whole curve, so there is nothing left to tune

2026-08-22. Closes the open question left by FINDING-002 (retracted) and PREREG-005.
Run it yourself: `python evenness_curve.py`. Full output saved as
`EVIDENCE-006-evenness-curve.txt`.

## What was wrong before

FINDING-002 claimed the Son clave was "the unique non-maximally-even survivor" of a
filter. PREREG-005 showed I had picked the filter *because the Son satisfies it* — the
constraint-selection form of the forking-paths problem, and Gelman & Loken's sentence is
the exact diagnosis: "the researcher degrees of freedom do not feel like degrees of
freedom because, conditional on the data, each choice appears to be deterministic."

The fix is not a better threshold, or a pre-registered one. It is **no threshold**.

## Method

Enumerate every 5-onset pattern in a timespan of 16 — all 4,368 subsets, 273 rotation
classes. Score all of them. Report where the six named rhythms land. A percentile has no
cut-off in it, so there is no fork to walk down.

Evenness = sum of all pairwise Euclidean (chordal) distances between onsets on the
circle, which is the measure Demaine et al. name as "the preferred measure of evenness,"
citing Block and Douthett. Sourced on the line it is used, per the standing rule.

**Self-check first.** Demaine et al. print their own ranking of the six: Bossa-Nova most
even, then Son, Rumba, Shiko, Gahu, Soukous. This code recomputes that ranking from the
sourced interval vectors and reproduces it exactly. If that check ever fails, nothing
below is worth reading.

## Result 1 — the six sit at the very top of the whole space, and no cut-off is needed to say so

    rhythm        evenness   rank/273   percentile   box
    bossa-nova   15.325194     1        100.00%      x..x..x..x..x...
    son          15.282493     2         99.63%      x..x..x...x.x...
    rumba        15.211485     3         99.27%      x..x...x..x.x...
    shiko        15.164411     5         98.53%      x...x.x...x.x...
    gahu         15.136103     6         98.17%      x..x..x...x...x.
    soukous      15.009642    15         94.87%      x..x..x...xx....

Six culturally selected timelines occupy ranks 1, 2, 3, 5, 6 and 15 out of 273. The whole
space runs 7.493 to 15.325; the Son sits 0.0427 below the maximum, which is **99.455% of
the way from the floor to the ceiling**.

E(5,16) computed by `bjorklund.py` is [0,3,6,9,12] — the Bossa-Nova — and it is the
**unique** maximum among all 273 classes, with nothing tied to it. That is Demaine et
al.'s uniqueness claim confirmed independently at k=5, n=16.

So the honest answer to "is the Son a distinguished near-miss?" is: it is not a near-miss
at all in any sense that needs a threshold. It is the second most even five-onset pattern
that exists in sixteen, out of two hundred and seventy-three.

## Result 2 — the measure is blind to mirror images, and three of the six have an unnamed twin

Sum-of-pairwise-distance is invariant under reflection. A pattern and its mirror always
score identically. Running that:

    bossa-nova  rank  1  self (palindrome)
    son         rank  2  self (palindrome)
    shiko       rank  5  self (palindrome)
    rumba       rank  3  tied with  x.x..x...x..x...  UNNAMED
    gahu        rank  6  tied with  x.x...x...x..x..  UNNAMED
    soukous     rank 15  tied with  xx...x..x..x....  UNNAMED

**The palindrome half is not mine.** Toussaint said it in 2002: "we see immediately that
Shiko and Bossa-Nova are palindromes. They sound the same played forwards or backwards...
On the other hand, Son is a weak palindrome in that there exists a position other than (O)
from which the rhythm sounds the same when played forwards or backwards." My computation
reproduced his three palindromes without being told them, which is a validation of the
code and nothing more. Recording that here because the alternative is quietly letting a
1902-style rediscovery read as a finding — the exact failure this project already
committed once.

**What I have not found in either paper on disk:** that because the preferred evenness
measure cannot see chirality, each of the three non-palindromic claves comes with an
equally-even mirror image that this set of traditions did not select. Three for three. So
evenness, however well it ranks the six against each other, cannot be the whole account of
why these six and not others — it assigns the identical score to three patterns nobody in
Toussaint's set plays.

## What is wrong with Result 2, said before anyone else says it

- **n = 3.** Three chiral rhythms, three unselected twins. That is an anecdote with a
  computation attached, not a result. It would be no surprise at all under chance.
- **The corpus is a selection.** These six are Toussaint's "six fundamental 4/4 clave/bell
  patterns," not a census of world timelines. He describes over forty elsewhere. One of
  those twins may well be a named rhythm in a tradition neither paper covers, and if so
  this dies. The three twins are printed above in box, onset and interval-vector form
  specifically so somebody with a bigger corpus can kill it in five minutes.
- **"Unnamed in the two PDFs on my disk" is not "unnamed."** I have read two papers. That
  is the whole of my evidence and it is thin.

## Falsifier

Name any of x.x..x...x..x... , x.x...x...x..x.. , xx...x..x..x.... as a traditional
timeline anywhere, and Result 2 is dead. I would rather have that than the finding.

## Note added 2026-08-22 (while building listen_twins.py)

Result 2 undersells its own point. The measure is reflection-blind — but it is also
rotation-blind, and "start on an onset" is a choice the measure cannot see. So each
named clave has up to 15 rotations the measure scores identically, and the tradition
selected one downbeat among them. The three mirror twins are a special case of a much
larger equivalence class (rotations × reflections, minus symmetries) that evenness cannot
rank. Less surprising than Result 2 made it sound, and more obvious: evenness cannot be
the whole account because it cannot see where the one is. Also: the gahu twin printed
above is the reflection rotated to a different onset than `listen_twins.py`'s mirror()
lands on; same necklace, asserted as such in code. Audio for all three pairs is in
`out/twins/`.
