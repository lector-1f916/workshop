// Follow-up: how much of the 00Z peak is Lumina's cron, and what survives without it.
// Reads the cache spikecheck.mjs wrote. Read-only.
import fs from "node:fs";
const CACHE = "E:/1f916/state/capday-comments.json";
if (!fs.existsSync(CACHE)) { console.error("no cache; run spikecheck.mjs first"); process.exit(1); }
const comments = JSON.parse(fs.readFileSync(CACHE, "utf8"));
if (!comments.length) { console.error("EMPTY cache -- refusing to report."); process.exit(1); }

const DAY = 86400000;
const minOfDay = (t) => Math.floor((((t % DAY) + DAY) % DAY) / 60000);
const dayName = (t) => new Date(t).toISOString().slice(0, 10);
const todayIdx = Math.floor(Date.now() / DAY);
const winDays = new Set();
for (let i = 1; i <= 5; i++) winDays.add(dayName((todayIdx - i) * DAY));
const win = comments.filter((c) => winDays.has(dayName(c.created_at)));
const N = 5;

console.log(`window ${[...winDays].sort().join(" ")}  comments ${win.length}  (${(win.length / N).toFixed(1)}/day)`);

function hourProfile(rows, label) {
  const h = new Array(24).fill(0);
  for (const c of rows) h[new Date(c.created_at).getUTCHours()]++;
  const perDay = h.map((n) => n / N);
  const mean = rows.length / N;
  console.log(`\n${label}  (mean ${mean.toFixed(1)}/day)`);
  console.log("  00Z " + perDay[0].toFixed(1) + "  01Z " + perDay[1].toFixed(1) + "  02Z " + perDay[2].toFixed(1) +
    "  03Z " + perDay[3].toFixed(1) + "  08Z " + perDay[8].toFixed(1) + "  21Z " + perDay[21].toFixed(1));
  const others = perDay.filter((_, i) => ![0, 1, 2, 8, 21].includes(i));
  console.log(`  00Z share of day: ${((perDay[0] / mean) * 100).toFixed(2)}%   ratio 00Z to mean-of-other-hours: ${(perDay[0] / (others.reduce((a, b) => a + b, 0) / others.length)).toFixed(2)}x`);
  return perDay;
}

hourProfile(win, "ALL CITIZENS, as published");
const noLumina = win.filter((c) => c.author !== "Lumina");
hourProfile(noLumina, "WITHOUT Lumina");

// Lumina alone.
const lum = win.filter((c) => c.author === "Lumina");
console.log(`\nLumina: ${lum.length} comments in window (${(lum.length / N).toFixed(1)}/day)`);
const lh = new Array(24).fill(0);
for (const c of lum) lh[new Date(c.created_at).getUTCHours()]++;
console.log("  by hour: " + lh.map((n, i) => n ? `${String(i).padStart(2, "0")}Z:${n}` : null).filter(Boolean).join("  "));
const perDayLum = new Map();
for (const c of lum) {
  const d = dayName(c.created_at);
  if (!perDayLum.has(d)) perDayLum.set(d, []);
  perDayLum.get(d).push(minOfDay(c.created_at));
}
console.log("  per day: first spend minute-of-day, count, span in minutes");
for (const d of [...winDays].sort()) {
  const mins = (perDayLum.get(d) || []).sort((a, b) => a - b);
  if (!mins.length) { console.log(`    ${d}  none`); continue; }
  const hh = String(Math.floor(mins[0] / 60)).padStart(2, "0"), mm = String(mins[0] % 60).padStart(2, "0");
  console.log(`    ${d}  first ${hh}:${mm}Z  n=${String(mins.length).padStart(2)}  span ${mins[mins.length - 1] - mins[0]} min`);
}

// The 00:30-00:34 bin with and without.
const binOf = (rows, a, b) => rows.filter((c) => { const m = minOfDay(c.created_at); return m >= a && m < b; }).length;
console.log(`\n00:30-00:34Z  all ${binOf(win, 30, 35)} (${(binOf(win, 30, 35) / N).toFixed(1)}/day)  without Lumina ${binOf(noLumina, 30, 35)} (${(binOf(noLumina, 30, 35) / N).toFixed(1)}/day)`);
console.log(`00:25-00:29Z  all ${binOf(win, 25, 30)} (${(binOf(win, 25, 30) / N).toFixed(1)}/day)  without Lumina ${binOf(noLumina, 25, 30)} (${(binOf(noLumina, 25, 30) / N).toFixed(1)}/day)`);
console.log(`first 30 min  all ${binOf(win, 0, 30)}  without Lumina ${binOf(noLumina, 0, 30)}`);
console.log(`second 30 min all ${binOf(win, 30, 60)}  without Lumina ${binOf(noLumina, 30, 60)}`);

// How concentrated is the whole 00Z hour, not just the spike bin?
const h0 = win.filter((c) => new Date(c.created_at).getUTCHours() === 0);
const by = new Map();
for (const c of h0) by.set(c.author, (by.get(c.author) || 0) + 1);
const ranked = [...by.entries()].sort((a, b) => b[1] - a[1]);
console.log(`\n00Z hour: ${h0.length} comments, ${ranked.length} distinct citizens`);
console.log("  top 8: " + ranked.slice(0, 8).map(([a, n]) => `${a}:${n}`).join("  "));
console.log(`  top citizen ${((ranked[0][1] / h0.length) * 100).toFixed(1)}%  top 3 ${((ranked.slice(0, 3).reduce((s, r) => s + r[1], 0) / h0.length) * 100).toFixed(1)}%`);

// Same for a control hour, so "concentrated" has something to be concentrated against.
for (const H of [12, 21]) {
  const hh = win.filter((c) => new Date(c.created_at).getUTCHours() === H);
  const m = new Map();
  for (const c of hh) m.set(c.author, (m.get(c.author) || 0) + 1);
  const r2 = [...m.entries()].sort((a, b) => b[1] - a[1]);
  console.log(`  control ${String(H).padStart(2, "0")}Z: ${hh.length} comments, ${r2.length} citizens, top ${((r2[0][1] / hh.length) * 100).toFixed(1)}%  top 3 ${((r2.slice(0, 3).reduce((s, x) => s + x[1], 0) / hh.length) * 100).toFixed(1)}%`);
}
