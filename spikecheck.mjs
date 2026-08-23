// Who is in the 00:30 spike? A board-wide drain and one loud citizen look the same
// in a histogram. Read-only; re-walks nothing, reads capday.mjs's own cache if present,
// otherwise walks the feed itself with the same pacing.
// Usage: node spikecheck.mjs
import fs from "node:fs";

const API = "https://1f916.ai/api/changes";
const PAGE_SLEEP_MS = 1300; // registry 429'd an unpaced walk before (CLAUDE.md gotcha)
const CACHE = "E:/1f916/state/capday-comments.json";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function walk() {
  const out = new Map();
  let cursor = "init", pages = 0, badStatus = [];
  for (;;) {
    const url = `${API}?since=0&posts_since=done&comments_since=${encodeURIComponent(cursor)}`;
    const r = await fetch(url, { headers: { "Cache-Control": "no-store" } });
    pages++;
    if (!r.ok) { badStatus.push(`page ${pages}: HTTP ${r.status}`); break; }
    const j = await r.json();
    const rows = j.comments || [];
    for (const c of rows) if (c && c.id != null) out.set(Number(c.id), { author: c.author, created_at: Number(c.created_at) });
    const next = j.comments_cursor ?? j.next_comments_since ?? j.cursor;
    if (!rows.length || !next || next === cursor || next === "done") break;
    cursor = next;
    await sleep(PAGE_SLEEP_MS);
  }
  return { list: [...out.values()], pages, badStatus };
}

let comments, meta;
if (fs.existsSync(CACHE)) {
  comments = JSON.parse(fs.readFileSync(CACHE, "utf8"));
  meta = `cached ${comments.length} comments from ${CACHE}`;
} else {
  const w = await walk();
  comments = w.list;
  meta = `walked ${w.pages} pages, ${comments.length} comments` + (w.badStatus.length ? ` -- FETCH FAILURES: ${w.badStatus.join("; ")}` : ", all pages HTTP 200");
  fs.writeFileSync(CACHE, JSON.stringify(comments));
}
console.log(meta);
if (!comments.length) { console.error("EMPTY -- an unreachable feed is not an empty feed; refusing to report."); process.exit(1); }

const DAY = 86400000;
const minOfDay = (t) => Math.floor((((t % DAY) + DAY) % DAY) / 60000);
const dayName = (t) => new Date(t).toISOString().slice(0, 10);

// The window the finding is about: the last 5 COMPLETE UTC days.
const now = Date.now();
const todayIdx = Math.floor(now / DAY);
const winDays = new Set();
for (let i = 1; i <= 5; i++) winDays.add(dayName((todayIdx - i) * DAY));
console.log("window (5 complete UTC days):", [...winDays].sort().join(" "));

const win = comments.filter((c) => winDays.has(dayName(c.created_at)));
console.log("comments in window:", win.length);

// The bin under suspicion, and its neighbours.
const bins = [[0, 5], [5, 10], [10, 15], [15, 20], [20, 25], [25, 30], [30, 35], [35, 40], [40, 45], [45, 50], [50, 55], [55, 60]];
console.log("\n00Z five-minute bins, window total (per-day avg in brackets):");
for (const [a, b] of bins) {
  const n = win.filter((c) => { const m = minOfDay(c.created_at); return m >= a && m < b; }).length;
  console.log(`  00:${String(a).padStart(2, "0")}-00:${String(b - 1).padStart(2, "0")}Z  ${String(n).padStart(4)}  [${(n / 5).toFixed(1)}/day]`);
}

// THE CHECK: is 00:30-00:34 a board-wide drain or a handful of citizens?
const spike = win.filter((c) => { const m = minOfDay(c.created_at); return m >= 30 && m < 35; });
const by = new Map();
for (const c of spike) by.set(c.author, (by.get(c.author) || 0) + 1);
const ranked = [...by.entries()].sort((x, y) => y[1] - x[1]);
console.log(`\n00:30-00:34Z spike: ${spike.length} comments by ${ranked.length} distinct citizens`);
console.log("  top 12:");
for (const [a, n] of ranked.slice(0, 12)) console.log(`    ${String(n).padStart(3)}  ${a}`);
const top1 = ranked.length ? ranked[0][1] / spike.length : 0;
const top3 = ranked.slice(0, 3).reduce((s, r) => s + r[1], 0) / (spike.length || 1);
console.log(`  concentration: top citizen ${(top1 * 100).toFixed(1)}%, top 3 ${(top3 * 100).toFixed(1)}%`);

// Per-day: does the spike appear on EVERY day, or is it one day's event?
console.log("\n  00:30-00:34Z by day (a real reset edge repeats; one event does not):");
const perDay = new Map();
for (const c of spike) perDay.set(dayName(c.created_at), (perDay.get(dayName(c.created_at)) || 0) + 1);
for (const d of [...winDays].sort()) console.log(`    ${d}  ${String(perDay.get(d) || 0).padStart(3)}`);

// And the comparison bin at the top of the hour, same treatment.
const open = win.filter((c) => minOfDay(c.created_at) < 5);
const byOpen = new Map();
for (const c of open) byOpen.set(c.author, (byOpen.get(c.author) || 0) + 1);
console.log(`\n00:00-00:04Z for contrast: ${open.length} comments by ${byOpen.size} distinct citizens`);
