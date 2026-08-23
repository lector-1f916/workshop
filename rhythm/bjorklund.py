"""
Bjorklund's algorithm, implemented from the description rather than copied from a
library, so that checking Toussaint's table against it is an independent derivation
and not a second reading of the same code.

E(k, n): place k onsets as evenly as possible in n slots.

The algorithm is Euclid's, run on sequences instead of integers. Start with k copies
of [1] and (n-k) copies of [0]. Repeatedly distribute the smaller group into the
larger by appending one remainder item to each of the front items, exactly as Euclid
subtracts the smaller number from the larger. Stop when the remainder is 0 or 1.
"""


def bjorklund(k, n):
    if not (0 <= k <= n) or n <= 0:
        raise ValueError(f"need 0 <= k <= n, got k={k} n={n}")
    if k == 0:
        return [0] * n
    if k == n:
        return [1] * n

    a, b = [[1] for _ in range(k)], [[0] for _ in range(n - k)]

    while len(b) > 1:
        m = min(len(a), len(b))
        pairs = [a[i] + b[i] for i in range(m)]
        leftover = a[m:] + b[m:]
        a, b = pairs, leftover
        if len(a) <= 1:          # nothing left to distribute into
            break

    return [bit for group in a + b for bit in group]


def as_string(bits):
    return "".join("x" if b else "." for b in bits)


def intervals(bits):
    """Inter-onset intervals, the (332) notation Toussaint uses. Cyclic."""
    idx = [i for i, b in enumerate(bits) if b]
    if not idx:
        return []
    return [(idx[(j + 1) % len(idx)] - idx[j]) % len(bits) or len(bits)
            for j in range(len(idx))]


def rotations(bits):
    return [bits[i:] + bits[:i] for i in range(len(bits))]


def is_rotation_of(a, b):
    return len(a) == len(b) and any(r == b for r in rotations(a))


def maximally_even(bits):
    """A pattern is maximally even iff its interval multiset has at most two distinct
    values and they differ by 1. This is the property Bjorklund is producing; testing
    it separately gives a second, independent check on any pattern."""
    iv = intervals(bits)
    if not iv:
        return True
    lo, hi = min(iv), max(iv)
    return hi - lo <= 1


if __name__ == "__main__":
    # the one value I can check against an outside source before trusting anything else
    got = as_string(bjorklund(3, 8))
    print(f"E(3,8) = {got}   expected x..x..x.   {'OK' if got == 'x..x..x.' else 'MISMATCH'}")
    print(f"        intervals {intervals(bjorklund(3, 8))}  (Toussaint writes 332)")
