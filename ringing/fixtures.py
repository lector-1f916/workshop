"""fixtures.py — every check here compares the engine against rows or lengths that
SOMEBODY ELSE PRINTED. Nothing in this file was typed from memory. Run it after touching
changes.py. Exit 1 if anything fails.

Sources (all fetched 2026-08-22, wake 6; URL on each fixture):
  [TG]  treblesgoing.org.uk/conductingbobdoubles.html — "Here is the Plain Course of Plain
        Bob Doubles written out in full" (40 rows in four columns) and the bobbed lead ends.
  [PDW] Peter D Wenham, "Bell Ringing by Instalments", instalment 5, Grandsire & Stedman,
        www.pdg.org.uk/pdw/PDW_RbI_05_Grandsire_and_Stedman.pdf — rows at a bob and at a
        single "called at the first lead" of Grandsire Doubles, and the plain course's tail.
  [WP]  en.wikipedia.org/wiki/Grandsire (raw wikitext): "A typical composition shown by the
        sequential treble leads to get 120 changes is: Plain, Bob, Plain, Bob, Plain, Single;
        repeated once." (cites Trollope p.16; "There are 10 different compositions")
  [BL]  rsw.me.uk/blueline — lead heads and course lengths for the three methods.
"""
import re
import sys
from changes import METHODS, PLAIN_BOB_DOUBLES as PB, GRANDSIRE_DOUBLES as GS, STEDMAN_DOUBLES as ST, PLAIN_BOB_MINOR as PBM, fmt, prove, rounds

fails = 0


def check(label, got, want):
    global fails
    ok = got == want
    print(("ok   " if ok else "FAIL ") + label + ("" if ok else f"\n       got  {got}\n       want {want}"))
    if not ok:
        fails += 1


# --- [TG] Plain Bob Doubles plain course, four columns of ten rows, then the next lead head.
TG_TOKENS = ("12345 13524 15432 14253 21435 31254 51342 41523 24153 32145 53124 45132 "
             "42513 23415 35214 54312 45231 24351 32541 53421 54321 42531 23451 35241 "
             "53412 45213 24315 32514 35142 54123 42135 23154 31524 51432 41253 21345 "
             "13254 15342 14523 12435 13524 15432 14253 12345").split()
# the page prints the course across four columns; read column c as tokens[c::4][:10] + tokens[40+c]
tg_rows = []
for c in range(4):
    col = TG_TOKENS[c::4][:10]
    tg_rows.extend(col)
tg_rows.append(TG_TOKENS[43])          # final 12345
pc = [fmt(r) for r in PB.plain_course()]
check("[TG] Plain Bob Doubles plain course, all 41 printed rows in order", pc, tg_rows)
check("[BL] Plain Bob Doubles lead head 13524", pc[10], "13524")

# --- [TG] bobbed lead ends: "Plain lead / Bobbed lead" pairs printed on the page.
#   long 5ths:  12435 -> 12345 plain, 14235 bob
#   in:         14523 -> 14253 plain, 15423 bob
#   out:        15342 -> 15432 plain, 13542 bob
#   fourths:    13254 -> 13524 plain, 12354 bob
from changes import apply_change, parse_change
for before, plain, bob in [("12435", "12345", "14235"), ("14523", "14253", "15423"),
                           ("15342", "15432", "13542"), ("13254", "13524", "12354")]:
    b = tuple(int(x) for x in before)
    check(f"[TG] PB plain lead end {before}->{plain}", fmt(apply_change(b, parse_change("125", 5))), plain)
    check(f"[TG] PB bob      {before}->{bob}", fmt(apply_change(b, parse_change("145", 5))), bob)

# --- [TG] "a plain course with a bob at the end ... 2345 3524 5432 4253 - 4235 Repeat twice"
#   = bob at the fourth lead of every course, three courses: the 120 with the 5th unaffected.
rows = PB.ring("ppp-" * 3)
p = prove(rows)
check("[TG] PB 120, bob every 4th lead x3: length 120", p.length, 120)
check("[TG] PB 120: true and comes round", (p.true, p.comes_round), (True, True))
check("[TG] PB lead heads of first course+bob", [fmt(rows[i]) for i in (10, 20, 30, 40)], ["13524", "15432", "14253", "14235"])
# the page says the same works from each of the four positions ("there are four ways to call a 120")
for k in range(4):
    calling = ("p" * k + "-" + "p" * (3 - k)) * 3
    pr = prove(PB.ring(calling))
    check(f"[TG] PB 120 with bob at lead {k+1} of each course ({calling})", (pr.length, pr.true, pr.comes_round), (120, True, True))

# --- [PDW] rows are READ FROM THE PDF'S TEXT, not retyped. The first version of this file
#     retyped the tail of the plain course by hand and got two rows wrong and dropped a third
#     (journal 2026-08-22, wake 6) — the engine caught the fixture, not the other way round.
PDW_TXT = open("sources/PDW_RbI_05_Grandsire_and_Stedman.txt", encoding="utf8").read().split("\n")   # not splitlines(): the PDF text has form feeds, which splitlines() also breaks on and which shift every line number after page 1
def pdw_rows(first_line, last_line):
    out = []
    for ln in PDW_TXT[first_line - 1:last_line]:
        m = re.match(r"\s*([1-5]) ([1-5]) ([1-5]) ([1-5]) ([1-5])", ln)
        if m:
            out.append("".join(m.groups()))
    return out
PDW_FIRST_LEAD = pdw_rows(35, 56)      # p.1-2: "Starting from rounds, 3 makes thirds place..." 14 rows
PDW_TAIL = pdw_rows(440, 480)          # p.5: the column beside "When a bob or single is called, 2 will come out of the hunt"
gpc = [fmt(r) for r in GS.plain_course()]
check("[PDW] Grandsire plain course: first 14 printed rows", gpc[:len(PDW_FIRST_LEAD)], PDW_FIRST_LEAD)
check("[PDW] Grandsire plain course: last 14 printed rows", gpc[-len(PDW_TAIL):], PDW_TAIL)
check("[PDW]/[BL] Grandsire plain course 30 rows", len(gpc) - 1, 30)
check("[BL] Grandsire lead head 12534", gpc[10], "12534")

# --- [PDW] "If a bob is called at the first lead, the figures are:" (eight rows)
PDW_BOB = pdw_rows(207, 224)      # p.4: "If a bob is called at the first lead, the figures are:"
# --- [PDW] "If a single is called at the first lead:" (eight rows)
PDW_SINGLE = pdw_rows(275, 292)   # p.4: "If a single is called at the first lead:"
bob_rows = [fmt(r) for r in GS.ring("-p")]
sgl_rows = [fmt(r) for r in GS.ring("sp")]
# the printed eight start at row 6 of the first lead (45312) and run into the second lead
check("[PDW] Grandsire bob at first lead: the eight printed rows", bob_rows[6:14], PDW_BOB)
check("[PDW] Grandsire single at first lead: the eight printed rows", sgl_rows[6:14], PDW_SINGLE)

# --- [WP] Grandsire 120: "Plain, Bob, Plain, Bob, Plain, Single; repeated once"
pr = prove(GS.ring("p-p-ps" * 2))
check("[WP] Grandsire PBPBPS x2 = 120, true, comes round", (pr.length, pr.true, pr.comes_round), (120, True, True))
# --- [PDW] "20 changes (two bobs)" and "40 changes (four singles)"
pr = prove(GS.ring("--"))
check("[PDW] Grandsire 20 changes: two bobs", (pr.length, pr.true, pr.comes_round), (20, True, True))
pr = prove(GS.ring("ssss"))
check("[PDW] Grandsire 40 changes: four singles", (pr.length, pr.true, pr.comes_round), (40, True, True))

# --- [TIN] Duckworth & Stedman, Tintinnalogia (1668), Project Gutenberg #18567,
#     sources/tintinnalogia-pg18567.txt lines 4532-4656: "I have here set down this Peal of
#     Grandsire, making the treble the whole Hunt, and the tenor the half Hunt, and the first
#     single change is made the sixth bob; that is, the third double bob, which is sixty
#     changes from the beginning of the Peal". 121 printed rows, rounds to rounds.
TIN = open("sources/tintinnalogia-pg18567.txt", encoding="utf8").read().split(chr(10))
TIN_ROWS = [l.strip() for l in TIN[4531:4656] if re.fullmatch(r"[1-5]{5}", l.strip())]
check("[TIN] 1668 pricking: 121 rows, 120 distinct, rounds to rounds",
      (len(TIN_ROWS), len(set(TIN_ROWS)), TIN_ROWS[0] == TIN_ROWS[-1] == "12345"), (121, 120, True))
check("[TIN] 1668 pricking == engine's p-p-psp-p-ps, every row", [fmt(r) for r in GS.ring("p-p-ps" * 2)], TIN_ROWS)
# the book draws a line before the single: "that next after the line is the single"; the line sits
# between printed rows 60 and 61 — the two '-----' lines in the block. Check they are where the singles are.
TIN_LINES = [k for k, l in enumerate(x.strip() for x in TIN[4531:4656]) if l.startswith("-----")]
TIN_SINGLE_AT = [sum(1 for x in TIN[4531:4531 + k] if re.fullmatch(r"[1-5]{5}", x.strip())) for k in TIN_LINES]
check("[TIN] the book's two rules sit after rows 60 and 120 (the singles)", TIN_SINGLE_AT, [60, 120])

# --- [BL] Stedman Doubles plain course 60 rows, lead head 53412
spc = [fmt(r) for r in ST.plain_course()]
check("[BL] Stedman Doubles plain course 60 rows", len(spc) - 1, 60)
check("[BL] Stedman Doubles lead head 53412", spc[12], "53412")

# --- [CC6]/[WP] Plain Bob Minor: plain course is "60 of the 720" (Wikipedia Change_ringing, Listen caption); lead head code a
mpc = [fmt(r) for r in PBM.plain_course()]
check("[WP] Plain Bob Minor plain course 60 rows", len(mpc) - 1, 60)
check("[CC6] Plain Bob Minor lead length 12", len(PBM.lead_changes()), 12)


# --- [TIN] Tintinnalogia (1668) on "Grandsire Bob. On six Bells" (= modern Plain Bob Minor per
#     Wikipedia's Fabian Stedman article), lines 5382-5400: "in any Peal of Grandsire bob, the bells
#     will come round in course at the end of Eighteen-score changes, if you make no single change
#     to carry it on farther to the end of the Seven-hundred and twenty" ... "all the changes
#     throughout the Seven-hundred and twenty, are treble and double, except only the two single
#     changes". Checked by exhaustive search over bob-only callings (pruned on repeated rows; the
#     whole tree is ~0.7 s) and by joining two eighteen-scores with two singles.
#     The Minor calls were from memory when this was first written; complib composition 11785 now
#     sources them (14 bob, 1234 single, both at the lead end), see changes.py.
import sys as _sys
_sys.setrecursionlimit(10000)
def _bobs_only_longest(M):
    R = rounds(M.stage); best = [0, ""]
    def dfs(r, seen, calling, n):
        if r == R and n:
            if n > best[0]: best[0], best[1] = n, calling
            return n == 720
        for sym in ("p", "-"):
            lead = M.ring_lead(r, None if sym == "p" else sym)
            if any(x in seen for x in lead[:-1]) or (lead[-1] in seen and lead[-1] != R):
                continue
            for x in lead:
                if x != R: seen.add(x)
            if dfs(lead[-1], seen, calling + sym, n + len(lead)): return True
            for x in lead:
                if x != R: seen.discard(x)
        return False
    full = dfs(R, set(), "", 0)
    return full, best[0], best[1]
_full, _longest, _calling = _bobs_only_longest(PBM)
check("[TIN] Plain Bob Minor, bobs only: no true 720 exists (exhaustive)", _full, False)
check("[TIN] Plain Bob Minor, bobs only: longest true round block is Eighteen-score (360)", _longest, 360)
_A = _calling                                     # one eighteen-score, e.g. pppp-ppp-- x3
_pr = prove(PBM.ring(_A[:-1] + "s" + _A[:-1] + "s"))
check("[TIN] two eighteen-scores joined by two singles = 720, true, round", (_pr.length, _pr.true, _pr.comes_round), (720, True, True))


# --- [TIN] the book's own descriptions of two prickings, checked from the rows alone (readpeal.py):
#     "Doubles and Singles on five Bells" (line 2735ff; rows from 2806): "sixty of which are double
#     changes, and sixty are single; ... one change is double, and the next single ... Every double
#     change is made between the four foremost bells".
#     Grandsire (line 4404ff): "the changes are all double except two, which are single".
from readpeal import rows_from, change_between
_ds = rows_from(2806)
_dsc = [change_between(a, b) for a, b in zip(_ds, _ds[1:])]
_kind = "".join("ds"[(5 - len(c)) // 2 == 1] for c in _dsc)
check("[TIN] Doubles and Singles: 121 rows, true, round", (len(_ds), prove(_ds).true, prove(_ds).comes_round), (121, True, True))
check("[TIN] Doubles and Singles: strictly alternating double/single, 60 each", (_kind, _kind.count("d"), _kind.count("s")), ("ds" * 60, 60, 60))
check("[TIN] Doubles and Singles: every double change is '5' (four foremost bells)", {c for c in _dsc if len(c) == 1}, {(5,)})
_gr = rows_from(4532)
_grc = [change_between(a, b) for a, b in zip(_gr, _gr[1:])]
_gk = "".join("ds"[(5 - len(c)) // 2 == 1] for c in _grc)
check("[TIN] Grandsire: all double except two singles, at changes 60 and 120", [i + 1 for i, k in enumerate(_gk) if k == "s"], [60, 120])


# --- [WP] Grandsire article: "There are 10 different compositions which can achieve this" (the 120,
#     citing Trollope p.16). Exhaustive search over callings with plain / bob / single at the lead end,
#     pruned on repeated rows. The count of distinct true 120s is the check.
def _all_120s(M, syms):
    R = rounds(M.stage); found = []
    def dfs(r, seen, calling, n):
        if r == R and n:
            if n == 120: found.append(calling)
            return
        for sym in syms:
            lead = M.ring_lead(r, None if sym == "p" else sym)
            if any(x in seen for x in lead[:-1]) or (lead[-1] in seen and lead[-1] != R):
                continue
            for x in lead:
                if x != R: seen.add(x)
            dfs(lead[-1], seen, calling + sym, n + len(lead))
            for x in lead:
                if x != R: seen.discard(x)
    dfs(R, set(), "", 0)
    return found
_g120 = _all_120s(GS, "p-s")
check("[WP]/Trollope: exactly 10 true 120s of Grandsire Doubles with bobs and singles at lead ends", len(_g120), 10)
check("[TIN] none of the ten uses zero singles (the 720/120 both need singles)", sum(1 for c in _g120 if "s" not in c), 0)
check("[TIN] the 1668 pricking is one of the ten", "p-p-psp-p-ps" in _g120, True)

print()
print("FAILURES:", fails)
sys.exit(1 if fails else 0)
