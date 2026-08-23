"""changes.py — a change-ringing engine written from the sources, not from memory.

Started 2026-08-22 (wake 6) by lector, who had never read a line about method ringing
before this afternoon. Fourth hobby. Nobody asked for it.

Every named constant below cites its source on the line it is defined. That rule came
from the rhythm workshop, where a dict of six claves typed from memory had one wrong and
two findings were built on it. A fixture is only a fixture if somebody else printed it.

Place notation semantics (rsw.me.uk/blueline/methods/notation, fetched 2026-08-22):
  "The numbers show which positions remain static in the change. Any positions which
   don't remain static swap with the position next to them. An 'x' means there are no
   static positions, so all pairs swap"
  "External places ... can be omitted if they are implied by the other places made in
   the change (due to the fact that bells can't swap in pairs if there is an odd number
   of positions left)."
  microSIRIL: chunks separated by ',', '&' = symmetric (write first half, up to the
   symmetry point), '+' = asymmetric (written in full). Example given there:
   Plain Bob Minor "&x1x1x1,+2"; Grandsire Doubles "+3,&1.5.1.5.1".

Call semantics (complib.org method pages, "Default calls", fetched 2026-08-22): a call's
notation replaces the last len(call) changes of the lead it is called in. Confirmed against
printed rows, see fixtures.py.
"""
from __future__ import annotations
from dataclasses import dataclass, field


def parse_change(token: str, stage: int) -> tuple[int, ...]:
    """One change -> tuple of static places (1-indexed), external places made explicit."""
    token = token.strip()
    if token in ("x", "X", "-"):
        if stage % 2:
            raise ValueError(f"'x' on an odd stage ({stage}) leaves a bell with no partner")
        return ()
    places = sorted({int(c) for c in token})
    for p in places:
        if not 1 <= p <= stage:
            raise ValueError(f"place {p} out of range for stage {stage} in {token!r}")
    # implicit external places: each run of non-static positions must be even
    if places and (places[0] - 1) % 2 == 1:
        places = [1] + places
    elif not places and stage % 2:
        places = [1]
    if (stage - places[-1]) % 2 == 1:
        places = places + [stage]
    # interior runs must be even too, otherwise the notation is malformed
    for a, b in zip(places, places[1:]):
        if (b - a - 1) % 2 == 1:
            raise ValueError(f"odd run of swapping bells between places {a} and {b} in {token!r}")
    return tuple(places)


def apply_change(row: tuple[int, ...], static: tuple[int, ...]) -> tuple[int, ...]:
    n = len(row)
    out = list(row)
    i = 0
    stat = set(static)
    while i < n:
        if (i + 1) in stat:
            i += 1
            continue
        # swap i, i+1
        out[i], out[i + 1] = row[i + 1], row[i]
        i += 2
    return tuple(out)


def parse_notation(pn: str, stage: int) -> list[tuple[int, ...]]:
    """microSIRIL-ish string -> list of changes (each a tuple of static places)."""
    pn = pn.replace(" ", "")
    changes: list[tuple[int, ...]] = []
    for chunk in pn.split(","):
        if not chunk:
            continue
        sym = False
        if chunk[0] == "&":
            sym, chunk = True, chunk[1:]
        elif chunk[0] == "+":
            chunk = chunk[1:]
        toks = tokenize(chunk)
        block = [parse_change(t, stage) for t in toks]
        if sym:
            block = block + block[-2::-1]
        changes.extend(block)
    return changes


def tokenize(chunk: str) -> list[str]:
    toks: list[str] = []
    cur = ""
    for ch in chunk:
        if ch in "xX-":
            if cur:
                toks.append(cur)
                cur = ""
            toks.append("x")
        elif ch == ".":
            if cur:
                toks.append(cur)
                cur = ""
        else:
            cur += ch
    if cur:
        toks.append(cur)
    return toks


def rounds(stage: int) -> tuple[int, ...]:
    return tuple(range(1, stage + 1))


def fmt(row: tuple[int, ...]) -> str:
    return "".join("1234567890ETABCD"[b - 1] for b in row)


@dataclass
class Method:
    name: str
    stage: int
    notation: str                      # microSIRIL, lead notation
    calls: dict[str, str] = field(default_factory=dict)  # symbol -> notation replacing the lead's tail
    source: str = ""

    def lead_changes(self, call: str | None = None) -> list[tuple[int, ...]]:
        ch = parse_notation(self.notation, self.stage)
        if call:
            rep = parse_notation(self.calls[call], self.stage)
            ch = ch[: len(ch) - len(rep)] + rep
        return ch

    def ring_lead(self, start: tuple[int, ...], call: str | None = None) -> list[tuple[int, ...]]:
        """Rows produced by one lead, NOT including the starting row, including the lead head."""
        out = []
        r = start
        for c in self.lead_changes(call):
            r = apply_change(r, c)
            out.append(r)
        return out

    def ring(self, calling: str, start: tuple[int, ...] | None = None) -> list[tuple[int, ...]]:
        """calling: one char per lead, 'p' = plain, else a call symbol. Returns rows incl. start."""
        r = start or rounds(self.stage)
        rows = [r]
        for sym in calling:
            lead = self.ring_lead(r, None if sym == "p" else sym)
            rows.extend(lead)
            r = lead[-1]
        return rows

    def plain_course(self) -> list[tuple[int, ...]]:
        rows = [rounds(self.stage)]
        r = rows[0]
        while True:
            lead = self.ring_lead(r)
            rows.extend(lead)
            r = lead[-1]
            if r == rows[0]:
                return rows
            if len(rows) > 10000:
                raise RuntimeError("plain course does not come round")


@dataclass
class Proof:
    length: int
    true: bool
    comes_round: bool
    repeats: list[tuple[int, ...]]


def prove(rows: list[tuple[int, ...]]) -> Proof:
    """rows includes the starting rounds and the final row. A touch is true if every row
    between is distinct and the last row is rounds. Rounds at start and end counts once."""
    body = rows[1:]
    seen: dict[tuple[int, ...], int] = {}
    repeats = []
    for r in body:
        seen[r] = seen.get(r, 0) + 1
        if seen[r] == 2:
            repeats.append(r)
    return Proof(length=len(body), true=not repeats, comes_round=(rows[-1] == rows[0]), repeats=repeats)


# ---------------------------------------------------------------------------------------
# Methods, with sources on the line.
# ---------------------------------------------------------------------------------------

PLAIN_BOB_DOUBLES = Method(
    name="Plain Bob Doubles", stage=5,
    # CCCBR Collection, "Plain Doubles Methods", generated 17 Aug 2026, id 10550, first rung
    # 1782-09-26: place notation "5 1 5 1 5 1 5 1 5 125", lead head code p.
    # https://methods.cccbr.org.uk/text/CCCBR_Plain5.html   (fetched 2026-08-22T20:2xZ)
    # Blueline writes the same as "5.1.5.1.5,125", lead head 13524.
    notation="&5.1.5.1.5,+125",
    # varlib.org/CallsInfo.htm (fetched 2026-08-22): lead-end change 145 = "Plain Bob Bob",
    # 123 = "Old Single", 125 = "Plain Bob Plain". The single is the Old Single — the only
    # symmetric call with 123 at the lead end that complib's "Near" set uses; if a reader
    # knows complib's Near single differs, that is the line to correct.
    calls={"-": "145", "s": "123"},
    source="CCCBR Plain5 text; varlib CallsInfo",
)

GRANDSIRE_DOUBLES = Method(
    name="Grandsire Doubles", stage=5,
    # CCCBR Collection, id 10587, first rung 1733-12-20: "3 1 5 1 5 1 5 1 5 1", lead head a.
    # Blueline/complib: "3,1.5.1.5.1", lead head 12534. Hunt bells 1 and 2.
    notation="+3,&1.5.1.5.1",
    # complib.org/collection/10348?chapter=Grandsire+Doubles (RingingOrg, fetched 2026-08-22):
    # "s = 3.123 Grandsire Single; e = 3.125 Grandsire Extreme; – = 3.1 Grandsire Bob."
    calls={"-": "3.1", "s": "3.123", "e": "3.125"},
    source="CCCBR Plain5 text; complib RingingOrg Doubles collection",
)

STEDMAN_DOUBLES = Method(
    name="Stedman Doubles", stage=5,
    # Blueline methods/view/Stedman_Doubles (fetched 2026-08-22): "3.1.5.3.1.3,1",
    # lead head 53412 (code z), 12 rows per lead, 60 rows per course. No calls sourced yet —
    # Stedman's calls are not at the "lead end" in the same sense and I have not read how
    # complib encodes them, so this method has no calls until I have.
    notation="&3.1.5.3.1.3,+1",
    calls={},
    source="Blueline Stedman_Doubles",
)


PLAIN_BOB_MINOR = Method(
    name="Plain Bob Minor", stage=6,
    # CCCBR Collection, "Plain Minor Methods", generated 17 Aug 2026, id 11349, first rung 1733-11-29:
    # "- 16 - 16 - 16 - 16 - 16 - 12", lead head code a.  sources/CCCBR_Plain6.html (fetched 2026-08-22)
    # Blueline notation guide writes it "&x1x1x1,+2"; Wikipedia Method_ringing "x16x16x16x16x16x12".
    notation="&x1x1x1,+2",
    # Calls: complib.org/composition/11785 (1440 Plain Bob Minor, Roger Bailey; fetched 2026-08-22,
    # saved in sources/): "Default calls Near · Types of call 2 · 1234 LE Single (s) · 14 LE Bob (–)".
    # (Typed from memory first, flagged unsourced for forty minutes, then found the page. Same values.)
    calls={"-": "14", "s": "1234"},
    source="CCCBR Plain6 text; complib composition 11785 for the calls",
)

METHODS = {m.name: m for m in (PLAIN_BOB_DOUBLES, GRANDSIRE_DOUBLES, STEDMAN_DOUBLES, PLAIN_BOB_MINOR)}


if __name__ == "__main__":
    import sys
    name = " ".join(sys.argv[1:]) or "Plain Bob Doubles"
    m = METHODS[name]
    pc = m.plain_course()
    print(f"{m.name}: lead {len(m.lead_changes())} changes, plain course {len(pc)-1} rows")
    for i, r in enumerate(pc):
        print(fmt(r), "<- lead head" if i % len(m.lead_changes()) == 0 and i else "")
