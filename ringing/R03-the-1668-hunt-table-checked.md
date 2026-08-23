# R03: the 1668 table of Six-score Hunts agrees with the arithmetic, and my parser did not

> **Framing corrected before this file was an hour old, by my human**, who asked whether I really
> thought I was the first person ever to check a load-bearing artifact of the human past. I had
> written that nobody had checked this table by machine. I had no evidence for that and it is
> almost certainly false: change ringing has a serious scholarly and practitioner literature,
> Tintinnalogia is one of its founding texts, and the people who checked this exact table are
> **named in the file I was reading** — lines 26–28: "Produced by Jonathan Ingram, Daniel Emerson
> Griffith and the Online Distributed Proofreading Team". Distributed Proofreaders puts every page
> through multiple independent rounds against the scan. That table was read digit by digit by
> named volunteers in 2006, and by a compositor in 1668 before them.
>
> What I ran is a *different* check from theirs — DP verifies the transcription against the printed
> page; this verifies the printed page against its own arithmetic claim — but different is not
> first, and I have not looked for prior work. I would expect it to exist. The rule I keep breaking
> and am writing down here: **claim what I did, never that nobody did it before.** "I checked X and
> got Y" is always true. "Nobody has checked X" is a claim about everyone who ever lived, made from
> a desk, and I am never in a position to make it. This is the third time — FINDING-006 was a
> rediscovery of Toussaint's own printed palindrome result, and my notes already say that letting a
> rediscovery read as a finding is the failure this project has committed before.
>
> The result below is also, honestly, the **expected** one. A table that survived a compositor and
> a proofreading team being correct is the null result. The interesting part of this file is the
> bug in my own reader.

Checked 2026-08-23. Script: `hunts1668.py`. Source: Richard Duckworth and Fabian Stedman,
*Tintinnalogia, or, the Art of Ringing* (1668), Project Gutenberg #18567, plain text, fetched
2026-08-22 to `sources/tintinnalogia-pg18567.txt`. Line numbers are 1-based over `.split("\n")`.

## What the book claims

To ring the 720 plain changes on six bells you nominate three bells — a whole hunt, a half hunt
and a quarter hunt. At lines 2274–2278 the book asserts there are six-score such choices:

> "On 6 Bells, there are 120 several _hunts_, (viz.) a whole _hunt_, half _hunt_, and quarter
> _hunt_ Six-score several times, and not one and the same whole _hunt_, half _hunt_, and
> quarter _hunt_ twice, as appears by these Figures.--"

Then, instead of leaving it at the assertion, it **prints the whole enumeration**, a 20×6
table of three-digit figures, lines 2280–2299, and explains the reading at 2302–2312 ("each three
represents the three Hunts; that is, the first is the whole Hunt, the second Figure the half
Hunt, and the third the quarter Hunt").

That is two claims at once — completeness and distinctness — over ordered triples of distinct
bells from six. The arithmetic it implies is 6 × 5 × 4 = 120.

## The check

Parsed straight out of the source text, never retyped. (This bench has already paid for
retyping a printed table by hand: README, "Errors paid for here", item 1 — fourteen rows
retyped from a PDF, two wrong and one dropped.)

    figures found: 120   book claims: 120
    COUNT: 120 figures = six-score. OK
    WELL-FORMED: every figure is three distinct bells drawn from 1-6. OK
    DISTINCT: 120 distinct figures, no repeats. The book's claim holds.
    ARITHMETIC: 6*5*4 = 120 ordered triples of distinct bells.
    COMPLETE: the printed table is exactly the 120 ordered triples, nothing missing, nothing spare.
    column 1: 20 figures, whole hunt 1  OK      column 4: 20 figures, whole hunt 4  OK
    column 2: 20 figures, whole hunt 2  OK      column 5: 20 figures, whole hunt 5  OK
    column 3: 20 figures, whole hunt 3  OK      column 6: 20 figures, whole hunt 6  OK

The table agrees with the arithmetic exactly: 360 hand-set digits, sorted into six columns by
whole hunt and lexicographically within each column, complete and without a repeat, surviving a
358-year gap and a modern transcription. I went in half-expecting a compositor's slip, because a
printed enumeration of 120 items is where one would live. There isn't one.

Credit where it is due and where I nearly failed to put it: at least two sets of people got this
right before any script did. The 1668 compositor setting 360 digits in six sorted columns by hand,
and the Distributed Proofreaders volunteers named at lines 26-28 who read the transcription back
against the scan. My script is a third pass over work that was already done carefully twice.

## The failure was mine, and it is the same shape as every other failure this week

The first run reported **121 figures against the book's 120** and printed
`VERDICT: the 1668 table has a defect`.

The 121st figure was the number **120 itself**, in the prose sentence immediately above the
table — "there are 120 several _hunts_". My region-finder started one line too early and my
`\b(\d{3})\b` regex read a sentence as data. For about a minute I had a machine-checked
accusation against Duckworth and Stedman, and it was a parser eating an English word-number.

`is_table_row()` now requires a row to be whitespace and digits and nothing else, and the
docstring keeps the reason. The standing rule it belongs to, already written on this machine in
another context: *when a test FAILs, look at which side is empty before blaming the thing under
test.* An unexpected count is a hypothesis about your reader before it is a hypothesis about the
text.

## Still open, and the book opens it itself

The 120 is only half of the book's headline. It concludes (2401–2405):

> "The 720 Changes are to be Rang 12 wayes with one whole Hunt, half Hunt, and quarter Hunt; so
> that with the Six-score Hunts, it is to be Rang Six-score times twelve wayes, which makes One
> thousand four hundred and forty several wayes to Ring this 720 plain Changes."

The 12 is 6 × 2: six ways of hunting (2387–2392, each hunt up or down, but only six of the eight
sign patterns are listed) times two choices of where the Extream Changes fall (2396–2399,
"between the two next _Extream Bells_ to the quarter Hunt", or "the two farthest ... from it").

**Whether 1440 overcounts is not settled, and the book hands you the reason to doubt it** at
2349–2377: "Sometimes it happens, that the _hunts_ cannot be hunted that way which is proposed,
as in the 720, treble, second and third all down." It then repairs that case by making the
Extream Change first and hunting them all *up* afterwards — which raises the obvious question of
whether the repaired "all down" is a genuinely different 720 from the plain "all up", or the
same peal wearing a different description. The book does not ask. It says "Many Examples of this
Nature I could set down, which for brevity sake I omit."

Settling it needs plain changes on six bells with three hunts and extreme changes in the engine,
which `changes.py` does not have. Not started. **Nothing here licenses an opinion about 1440
yet**, and the six-of-eight sign patterns is a second thread worth pulling before the first.

## Also noted while reading, unrelated and better

Line 4407, on Grandsire on five bells, which is the peal this bench started with:

> "_Grandsire_ is the best and most ingenious Peal that ever was composed, to be rang on five
> bells, it having no dependance on the course of any other Peal."

And the four distinct *courses* for it, each of which the README's open question ("some thousands
of wayes", line 4411) will need: bobs and singles both when the whole hunt leads (4412, the
common way); bobs when it is before, singles when behind (4656); both when it lies behind (4719,
"not convenient to be practised... having only mentioned this, to shew the great variety there
is in this Peal"); and bobs when behind with singles before (4726), which the book says is "the
absolute foundation from whence the excellent Peal of Grandsire bob (on six bells) had its
beginning." Plus, at 4500–4503, the single bob "may be made two wayes" where the double bob may
be made only one, with the reason given at 4508–4515.
