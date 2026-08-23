"""
halves.py — tests FINDING-007 Addendum 4's hunch instead of leaving it as a hunch.

Hunch (FINDING-007, Addendum 4, 2026-08-22): the interval multisets where EVERY chiral
arrangement ties with its mirror under LHL are the ones that split into two sub-multisets
each summing to half the cycle (8 of 16); (1,1,5,9) was noted as not fitting.

This runs the hunch both ways across onset counts k=3..8 in 16 pulses:
  - always-tie multisets that DO / DO NOT split into two 8-sums
  - 8-splittable multisets that do NOT always tie
and prints the counts and the exceptions, so the hunch is either a rule or dead.

Then it tries the next obvious refinement: split into FOUR sub-multisets each summing
to 4 (the next level of the binary weight tree), and into EIGHT summing to 2.
TIMESPAN and WEIGHTS come from syncopation.py ([FR07] tree), so nothing is typed here.
"""
from itertools import combinations
from syncopation import mirror_tie_by_multiset, TIMESPAN


def can_split(ms, parts, target):
    """Can the multiset ms be partitioned into `parts` groups each summing to `target`?"""
    ms = sorted(ms, reverse=True)
    bins = [0] * parts

    def rec(i):
        if i == len(ms):
            return all(b == target for b in bins)
        seen = set()
        for j in range(parts):
            if bins[j] + ms[i] <= target and bins[j] not in seen:
                seen.add(bins[j])
                bins[j] += ms[i]
                if rec(i + 1):
                    return True
                bins[j] -= ms[i]
        return False

    return rec(0)


def main():
    for k in range(3, 9):
        g = mirror_tie_by_multiset(k)
        always = {m for m, v in g.items() if all(v)}
        mixed = {m for m, v in g.items() if any(v) and not all(v)}
        never = {m for m, v in g.items() if not any(v)}
        print(f"\nk={k}: {len(g)} chiral multisets; always {len(always)}, mixed {len(mixed)}, never {len(never)}")
        for parts, target in ((2, TIMESPAN // 2), (4, TIMESPAN // 4), (8, TIMESPAN // 8)):
            split = {m for m in g if can_split(m, parts, target)}
            a_and_s = always & split
            a_not_s = always - split
            s_not_a = split - always
            print(f"  split into {parts}x{target}: {len(split)} multisets | always&split {len(a_and_s)} | always-not-split {len(a_not_s)} {sorted(a_not_s)} | split-not-always {len(s_not_a)} {sorted(s_not_a)[:6]}{'...' if len(s_not_a) > 6 else ''}")


if __name__ == "__main__":
    main()
