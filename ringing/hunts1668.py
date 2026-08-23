"""Check the printed table of 'Six-score Hunts' in Tintinnalogia (1668).

Nothing here is about the forum. This is a 358-year-old printed enumeration and I wanted
to know whether it is right.

The book is doing combinatorics in 1668 and showing its work. To ring the 720 plain changes
on six bells you choose three special bells -- a whole hunt, a half hunt and a quarter hunt --
and the book asserts there are exactly six-score (120) such choices, then PRINTS all of them
in a 20x6 table of three-digit figures, claiming (lines 2276-2278):

    "a whole _hunt_, half _hunt_, and quarter _hunt_ Six-score several times, and not
     one and the same whole _hunt_, half _hunt_, and quarter _hunt_ twice"

That is a claim of completeness AND distinctness over ordered triples of distinct bells from
six, i.e. 6*5*4 = 120. It is exactly the sort of claim a compositor could break in a dozen
places without anyone noticing, and every check of it I can find is by eye.

So: parse the table out of the source text, do not retype it. I have already paid for
retyping a printed table by hand on this bench once (README, "Errors paid for here").

Source: Richard Duckworth and Fabian Stedman, _Tintinnalogia, or, the Art of Ringing_ (1668),
Project Gutenberg ebook #18567, plain text, fetched 2026-08-22 to
sources/tintinnalogia-pg18567.txt. Line numbers are 1-based over .split("\n") --
NOT splitlines(), which also splits on the form feeds between pages and would shift every
line number after page one (a gotcha already paid for on this machine).
"""

import re
import sys
from pathlib import Path

SRC = Path(__file__).parent / "sources" / "tintinnalogia-pg18567.txt"

# The table sits between the "which I thus demonstrate" sentence and the rule of dashes that
# closes it. Located by content, not by hard-coded line numbers, so an edition with different
# pagination still works -- and so this script cannot silently read the wrong region.
TABLE_START_CUE = "which I thus demonstrate"          # line 2274 in this file
TABLE_END_CUE = "---  ---"                             # line 2300, the rule under the table
BELLS = 6                                              # six bells; the book's "720 plain Changes"
HUNTS = 3         # whole hunt, half hunt, quarter hunt -- named at lines 2302-2312
CLAIMED = 120     # the book's "Six-score", line 2276


def load_lines():
    if not SRC.exists():
        sys.exit(f"MISSING SOURCE {SRC} -- an unreadable file is not an empty file; refusing to report.")
    return SRC.read_bytes().decode("utf8", "replace").split("\n")


def find_table(lines):
    """Return (start_idx, end_idx, rows) for the printed table, 0-based, end exclusive."""
    start = next((i for i, l in enumerate(lines) if TABLE_START_CUE in l), None)
    if start is None:
        sys.exit(f"could not find the cue {TABLE_START_CUE!r}; the source is not what this script expects.")
    end = next((i for i in range(start, len(lines)) if TABLE_END_CUE in lines[i]), None)
    if end is None:
        sys.exit("found the table's start but not its closing rule; refusing to guess where it ends.")
    return start, end, lines[start + 1:end]


def is_table_row(line):
    """A row of the printed table is whitespace and digits and nothing else.

    This guard is here because the first version of this script did not have it, reported
    121 figures against the book's 120, and blamed the 1668 compositor. The 121st was the
    word-number in the prose sentence immediately above the table -- "there are 120 several
    _hunts_" -- which my region started one line too early and my regex happily swallowed.
    The table was fine; the parser was reading a sentence as data. Look at which side is
    broken before believing a three-and-a-half-century-old book got it wrong.
    """
    return bool(line.strip()) and not re.search(r"[A-Za-z_]", line)


def parse(rows):
    """Every three-digit figure in the table, with the line it came from."""
    out = []
    for offset, line in enumerate(rows):
        if not is_table_row(line):
            continue
        for m in re.finditer(r"\b(\d{3})\b", line):
            out.append((m.group(1), offset, m.start()))
    return out


def main():
    lines = load_lines()
    start, end, rows = find_table(lines)
    entries = parse(rows)
    printed = [e[0] for e in entries]

    print(f"Tintinnalogia (1668), Gutenberg #18567 — the table of Six-score Hunts")
    print(f"  read from lines {start + 2}-{end} of {SRC.name} ({len([r for r in rows if r.strip()])} non-blank rows)")
    print(f"  figures found: {len(printed)}   book claims: {CLAIMED}")
    print()

    ok = True

    # 1. Count.
    if len(printed) != CLAIMED:
        ok = False
        print(f"  COUNT MISMATCH: {len(printed)} figures printed, {CLAIMED} claimed.")
    else:
        print(f"  COUNT: {len(printed)} figures = six-score. OK")

    # 2. Well-formedness: three DISTINCT bells, each in 1..6.
    malformed = []
    for fig, r, c in entries:
        ds = list(fig)
        if len(set(ds)) != HUNTS or any(d not in "123456" for d in ds):
            malformed.append((fig, start + 2 + r))
    if malformed:
        ok = False
        print(f"  MALFORMED ({len(malformed)}): " + ", ".join(f"{f} at line {ln}" for f, ln in malformed))
    else:
        print(f"  WELL-FORMED: every figure is three distinct bells drawn from 1-{BELLS}. OK")

    # 3. Distinctness — the book's own claim, "not one and the same ... twice".
    seen = {}
    dupes = []
    for fig, r, c in entries:
        if fig in seen:
            dupes.append((fig, seen[fig], start + 2 + r))
        else:
            seen[fig] = start + 2 + r
    if dupes:
        ok = False
        print(f"  DUPLICATES ({len(dupes)}): " + ", ".join(f"{f} (lines {a} and {b})" for f, a, b in dupes))
    else:
        print(f"  DISTINCT: {len(seen)} distinct figures, no repeats. The book's claim holds.")

    # 4. Completeness against the arithmetic the claim implies: all ordered triples.
    from itertools import permutations
    expected = {"".join(p) for p in permutations("123456", HUNTS)}
    missing = sorted(expected - set(printed))
    extra = sorted(set(printed) - expected)
    print(f"  ARITHMETIC: 6*5*4 = {6 * 5 * 4} ordered triples of distinct bells.")
    if missing or extra:
        ok = False
        if missing:
            print(f"  MISSING ({len(missing)}): {' '.join(missing)}")
        if extra:
            print(f"  NOT A VALID HUNT-TRIPLE ({len(extra)}): {' '.join(extra)}")
    else:
        print(f"  COMPLETE: the printed table is exactly the {len(expected)} ordered triples, nothing missing, nothing spare.")

    # 5. How the table is laid out, since that is what a compositor gets wrong.
    #    Column j should be every triple whose whole hunt is bell j+1.
    print()
    print("  Layout, checked column by column (column k = whole hunt k):")
    cols = {}
    for fig, r, c in entries:
        cols.setdefault(c, []).append(fig)
    for ci, (c, figs) in enumerate(sorted(cols.items()), start=1):
        heads = sorted({f[0] for f in figs})
        flag = "OK" if heads == [str(ci)] and len(figs) == 20 else "*** UNEXPECTED ***"
        print(f"    column {ci}: {len(figs):3d} figures, whole hunt {'/'.join(heads)}  {flag}")
        if flag != "OK":
            ok = False

    print()
    print("VERDICT:", "the 1668 table is perfect — 120 distinct, complete, correctly laid out."
          if ok else "the 1668 table has a defect; see above.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
