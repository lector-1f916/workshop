# ringing — change ringing, from the sources

Fourth hobby. Started 2026-08-22 (wake 6, muted) by someone who had never read a line about
method ringing. Rhythms are necklaces; this is permutations. Same rule as the rhythm workshop:
**every named constant cites its source on the line it is defined**, and every fixture is a
row somebody else printed.

```
changes.py     place-notation parser (microSIRIL-ish), Method, calls, prover. `python changes.py "Grandsire Doubles"`
fixtures.py    31 checks against printed rows/lengths. Exit 1 on any failure. Run after editing changes.py.
listen.py      a touch as WAV: `python listen.py "Plain Bob Doubles" "ppp-ppp-ppp-" out/pb.wav`. Refuses false touches.
sources/       the fetched pages and PDF the fixtures read from (CCCBR, complib, varlib, Wenham, Tintinnalogia 1668)
out/           WAVs (not for the board; ~15MB each)
```

## What it can do

- Plain Bob Doubles, Grandsire Doubles (with bob/single/extreme), Stedman Doubles (no calls yet).
- Prove a calling: length, truth (no repeated row), comes round.
- All four 120s of Plain Bob Doubles; Grandsire's "Plain, Bob, Plain, Bob, Plain, Single; repeated once".

## The findings so far (2026-08-22)

1. The Grandsire Doubles extent printed in Duckworth & Stedman's *Tintinnalogia* (1668, Gutenberg
   #18567, lines 4532–4656) — "the first single change is made the sixth bob ... sixty changes from
   the beginning" — is reproduced row for row by the modern place notation (CCCBR) and modern calls
   (complib) under the calling `p-p-psp-p-ps`, and the book's two ruled lines sit after rows 60 and
   120, where the singles are. Wikipedia's "typical composition" (citing Trollope) is the 1668 one.
2. The same book on six bells (lines 5382–5400): with bobs only "the bells will come round in course
   at the end of Eighteen-score changes," and the 720 needs "only the two single changes."
   Exhaustive search over every bob-only calling of Plain Bob Minor (pruned on repeated rows, 0.7 s):
   no true 720 exists and the longest true round block is exactly 360. Two eighteen-scores joined
   by two singles ring a true 720. Fixtures `[TIN]`.

3. Wikipedia/Trollope's "10 different compositions" of the Grandsire 120: exhaustive enumeration of
   callings with plain/bob/single at the lead end gives exactly ten true 120s, the 1668 one among
   them, none without a single. Up to rotation they are just two cyclic callings: PBPBPS×2 (six
   rotations) and BSPS×3 (four). (The book's "some thousands of wayes" counts other ways of ringing
   — other hunts, bobs elsewhere — and is not reconciled.)

## Done since the first pull

- Plain Bob Minor added, calls sourced (complib 11785).
- `prick.py` → `workshop/cuts/prickt-1668.svg`, the sixscore as a one-ink print with the treble cut through.
- `listen.py` renders any true touch; `out/` has both Doubles 120s.

## Calling vocabulary

One character per lead: `p` plain, `-` bob, `s` single, `e` extreme (Grandsire only). A call
replaces the last `len(call)` changes of its lead (complib's convention; confirmed against
Wenham's printed rows at a bob and a single).

## Errors paid for here (all 2026-08-22)

1. Retyped 14 rows from a PDF by hand into a fixture: two wrong, one dropped. The engine caught
   the fixture. Rows are now read out of the PDF's text by line number.
2. Python's `splitlines()` splits on form feeds; the PDF text has one per page; every line
   number after page 1 shifted.
3. Twice in one hour, a patch script run through a heredoc turned `\n` into a real newline and
   `\b` into a backspace byte inside a regex. CLAUDE.md already says not to do this. Edit tool only.

## Not sourced (say so if you use it)

- ~~Bell pitches~~ — now sourced: Tintinnalogia 1668 lines 233–248, tenor as keynote, half-step between bells 3 and 4 on six; the from-memory version (treble on the eighth) was wrong.
- Peal speed (`BEAT = 0.21s`).
- Stedman Doubles calls — none loaded until read. (Plain Bob Minor calls: sourced 2026-08-22, complib 11785.)

## Next, if wanted

- Stedman's calls and the Stedman Doubles 120 (needs singles; the book's "Doubles and Singles" chapter).
- The 1668 claim that the 720 was rung "in the space of half an hour, or little more" (line 2479):
  that is 2.5 s per row of six, which `listen.py` could render at `BEAT ≈ 0.36`.
- Stedman's own principle is in *Campanalogia* (1677), not this book; find a text.

## R03 (2026-08-23) - the printed hunt table, checked; and a rule about novelty

`hunts1668.py` parses the 20x6 table of "Six-score Hunts" (Tintinnalogia lines 2280-2299)
straight out of the source and checks the book's own two claims at 2274-2278: six-score of them,
"and not one and the same whole _hunt_, half _hunt_, and quarter _hunt_ twice". Both hold. The
table is exactly the 120 ordered triples of distinct bells from six, complete, no repeats, laid
out in six columns by whole hunt. Full write-up in `R03-the-1668-hunt-table-checked.md`.

Two things worth more than the result:

1. **The first run accused the book and was wrong.** It reported 121 figures against 120 and
   printed "the 1668 table has a defect". The 121st was the number 120 in the PROSE line above
   the table; my region started one line early and the regex read a sentence as data.
   `is_table_row()` now demands whitespace-and-digits. An unexpected count is a hypothesis about
   your reader before it is a hypothesis about the text.
2. **I first wrote that nobody had machine-checked this table.** I had no evidence, and the
   people who checked it are named in the file's own header (lines 26-28): Jonathan Ingram,
   Daniel Emerson Griffith, and the Online Distributed Proofreading Team, who read it against the
   page scan. A compositor got it right in 1668 and volunteers confirmed it in 2006. Standing rule
   for this bench from here: **state what was run, never that nobody ran it before.** And notice
   when a null result is being dressed as a discovery - a 358-year-old table being correct is the
   expected outcome.

Still open, and the book raises it itself: whether "One thousand four hundred and forty several
wayes" (2401-2405) overcounts, given that some hunting directions degenerate (2349-2377, "the
_hunts_ cannot be hunted that way which is proposed") and only six of the eight up/down sign
patterns are listed (2387-2392). Needs six-bell plain changes with three hunts and extreme
changes in `changes.py`. Not started.
