"""readpeal.py — read a pricked peal out of the 1668 text and recover its place notation.

The engine usually goes notation -> rows. This goes the other way: rows -> changes, so a
method printed only as figures (which is how Tintinnalogia prints everything) can be checked
for truth and written in modern notation without anyone transcribing it by hand.

Usage: python readpeal.py 2806        # the 1668 "Doubles and Singles on five Bells", 121 rows
       python readpeal.py 4532        # the Grandsire sixscore (should give 3.1.5... and the calls)
"""
import re
import sys
from changes import prove

TXT = open("sources/tintinnalogia-pg18567.txt", encoding="utf8").read().split("\n")


def rows_from(line):
    rows = []
    i = line - 1
    while i < len(TXT):
        s = TXT[i].strip()
        if re.fullmatch(r"[1-9]+", s):
            rows.append(tuple(int(c) for c in s))
        elif rows and s and not s.startswith("-"):
            break
        i += 1
    return rows


def change_between(a, b):
    """static places (1-indexed) taking row a to row b, or None if not an adjacent transposition."""
    n = len(a)
    static = []
    i = 0
    while i < n:
        if a[i] == b[i]:
            static.append(i + 1); i += 1
        elif i + 1 < n and a[i] == b[i + 1] and a[i + 1] == b[i]:
            i += 2
        else:
            return None
    return tuple(static)


if __name__ == "__main__":
    line = int(sys.argv[1]) if len(sys.argv) > 1 else 2806
    rows = rows_from(line)
    p = prove(rows)
    print(f"from line {line}: {len(rows)} rows, {len(set(rows))} distinct, true={p.true}, comes_round={p.comes_round}")
    changes = []
    bad = []
    for k, (a, b) in enumerate(zip(rows, rows[1:])):
        c = change_between(a, b)
        if c is None:
            bad.append((k + 1, "".join(map(str, a)), "".join(map(str, b))))
        changes.append(c)
    if bad:
        print("NOT adjacent transpositions at:", bad[:5])
    notation = ".".join("x" if c == () else "".join(map(str, c)) for c in changes if c is not None)
    print("place notation, change by change:")
    print(notation)
    # how many bells swap in each change: 'double' = two pairs, 'single' = one pair
    kinds = ["".join("ds"[(len(a) - len(c)) // 2 == 1] if c is not None else "?") for a, c in zip(rows, changes)]
    print("double/single pattern:", "".join(kinds))
