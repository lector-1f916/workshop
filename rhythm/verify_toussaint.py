"""
Check every E(k,n) = [pattern] claim in Toussaint (2005) against an independent
implementation of Bjorklund's algorithm.

Two things are being tested and they are different:
  1. Does the paper's printed pattern equal what Bjorklund produces? (typography /
     transcription check — this is the weak one, it only catches print errors)
  2. Is the printed pattern maximally even? (a property test that does not go through
     my Bjorklund at all — an actually independent path)

A claim passing (1) and failing (2), or vice versa, is the interesting case.
"""
import io
import re
import sys

from bjorklund import bjorklund, as_string, intervals, maximally_even, is_rotation_of

sys.stdout.reconfigure(encoding="utf-8")

text = io.open("toussaint2005.txt", encoding="utf-8").read()

# E(5,16)= [x . . x . . x . . x . . x . . . .] is the Bossa-Nova ...
CLAIM = re.compile(r"E\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*=?\s*\[([x\s.]+)\]([^\n\[]{0,120})")

seen = {}
for m in CLAIM.finditer(text):
    k, n = int(m.group(1)), int(m.group(2))
    printed = m.group(3).replace(" ", "").strip()
    note = " ".join(m.group(4).split())[:70]
    if not printed or set(printed) - {"x", "."}:
        continue
    # keep the occurrence carrying the most description
    if (k, n) not in seen or len(note) > len(seen[(k, n)][1]):
        seen[(k, n)] = (printed, note)

print(f"claims parsed: {len(seen)}\n")
hdr = f"{'claim':<10} {'len':>4} {'printed matches E(k,n)':<24} {'max-even':<9}  note"
print(hdr)
print("-" * len(hdr))

exact = rot = lenbad = nonme = 0
problems = []

for (k, n), (printed, note) in sorted(seen.items()):
    mine = as_string(bjorklund(k, n))
    if len(printed) != n:
        verdict = f"LENGTH {len(printed)} != n"
        lenbad += 1
        problems.append(((k, n), printed, verdict, note))
    elif printed == mine:
        verdict = "exact"
        exact += 1
    elif is_rotation_of(list(printed), list(mine)):
        verdict = "rotation"
        rot += 1
    else:
        verdict = "DIFFERENT"
        problems.append(((k, n), printed, f"mine={mine}", note))

    me = maximally_even([1 if c == "x" else 0 for c in printed]) if len(printed) == n else None
    if me is False:
        nonme += 1
    print(f"E({k},{n})".ljust(10)
          + f"{len(printed):>4} {verdict:<24} {str(me):<9}  {note[:46]}")

print(f"\nexact {exact}   rotation {rot}   length-mismatch {lenbad}   not-maximally-even {nonme}")
if problems:
    print("\nWORTH A SECOND LOOK")
    for (k, n), printed, why, note in problems:
        print(f"  E({k},{n})  printed {printed}")
        print(f"          {why}")
        print(f"          {note}")
