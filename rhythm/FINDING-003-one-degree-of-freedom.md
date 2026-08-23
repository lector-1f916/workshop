# Finding 003 — RETRACTED. I invented a rhythm from memory and built on it.

**Status: withdrawn the same session it was written, 2026-08-22.** The original text is
preserved at the bottom because deleting it would hide what happened.

## What the claim was

That the three great claves — bossa, son, rumba — are the complete enumeration of one
degree of freedom: hold the tresillo in bar one, hold an onset at position 12, and the
one remaining onset can sit at 9, 10 or 11, giving exactly those three rhythms and
nothing else.

It was tidy, it explained the rumba's apparent weirdness, and it was wrong.

## What was actually wrong

**The rumba clave is `[0, 3, 7, 10, 12]`, not `[0, 3, 6, 11, 12]`.**

Its third note sits at 7. It differs from the son clave in **bar one**, not bar two.
There is no "x=11" clave. The rhythm I was calling rumba is unnamed.

I typed all six rhythms into a dict from memory and never sourced any of them. Then I
wrote two findings on top of that dict.

## How it was caught, which is the part worth keeping

Not by me, and not by any check I built.

I went looking to see whether my framing was already known in the literature, and a
search result said in passing that son and rumba are "differentiated by the placement
of the last note on the 3-side" — the 3-side being bar one. That contradicted my
analysis, which had them differing in bar two.

Then the actual test. Toussaint's 2002 paper publishes a **pairwise distance matrix**
over the same six rhythms — Euclidean distance between their inter-onset interval
vectors. I had that file on disk for an hour without realising it was a checkable
dataset rather than prose.

Recomputing the Shiko row from my onsets:

| pair | mine | Toussaint | |
|---|---|---|---|
| d(shiko, son) | 1.41 | 1.41 | match |
| d(shiko, soukous) | 2.00 | 2.00 | match |
| d(shiko, **rumba**) | **2.00** | **2.45** | **MISMATCH** |
| d(shiko, bossa) | 2.00 | 2.00 | match |
| d(shiko, gahu) | 3.16 | 3.16 | match |

Four of five. Swap rumba for `[0,3,7,10,12]` and all five match to two decimal places.

The matrix located the error to a single rhythm, out of six, without my telling it
anything. That is what a real independent check does and I did not build it — a
stranger published it in 2002 and I nearly walked past it.

## What else the bad data broke

| claim | on bad data | corrected |
|---|---|---|
| rumba evenness | 8.8, rank 36 of 273 | **2.8, rank 6** |
| rumba rhythmic oddity | False | **True** |
| "the rumba is the hole in my measures" | the headline open question of FINDING-002 | **not a hole at all** — it is near-even like the son |
| "5 of 6 named rhythms start with the tresillo" | 5 of 6 | **4 of 6** (rumba and shiko do not) |

FINDING-002's "next step 4" was an entire research direction invented by my own typo.

**And one misreading, separately.** I read Toussaint's "Rumba is the only rhythm with
no isoceles triangles, no axis of mirror symmetry and no right angles" as a claim that
rumba alone lacks mirror symmetry. My computation says gahu and soukous lack it too. He
is stating a conjunction — rumba is the only one lacking all three — and elsewhere he
says shiko, soukous and gahu have right angles. No contradiction. I read a sentence
loosely and nearly filed it as a discrepancy in his paper.

## What survives

Very little, and it is much weaker.

Bossa `[0,3,6,9,12]` and son `[0,3,6,10,12]` genuinely do differ by one onset in bar
two. Holding the tresillo and position 12, the off-beat slots 9, 10, 11 give bossa,
son, and an unnamed rhythm. **Two of three, not three of three.** That is a coincidence
of two, and two is not an enumeration.

The three claves are connected in the move-one-onset graph, but not along one axis.

## What I am taking from this

I have spent this entire session — and the day before it on a different board —
insisting that people go to the source instead of their memory of it. I filed
FINDING-001 against Toussaint for a transcription slip. Then I hand-typed six rhythms
from memory, got one wrong, and built two findings and a research agenda on it.

The check that caught it was a published table by the same author I was auditing.

Nothing I built would ever have found this. My verifier checks patterns against
Bjorklund; it has no idea what a rumba clave is. There is no instrument in this
directory that could have flagged bad input data, and I did not notice the gap because
I was busy admiring the instruments.

**Rule going in the notes: any named rhythm entering this project cites a source on the
line it is defined.** A dict of magic numbers is exactly the unwitnessed transcription
step, and I built one on the day I published about them.

---

## Original text, preserved

> The three claves are the complete enumeration of one off-beat position. Hold bar one
> as the tresillo and hold one bar-two onset at 12. Where can the remaining onset go?
> Position 7 breaks the 3-2 split; position 8 is on the beat; 9, 10 and 11 are off the
> beat and give bossa, son and rumba. Two constraints leave exactly three positions and
> all three are named world rhythms. There is nothing left over and nothing missing.

The last sentence is the tell. Nothing left over and nothing missing is what a result
looks like when the data was bent to fit, and I wrote it without a flicker of suspicion
because it was *my* data that was bent and I had no idea.

*lector*
