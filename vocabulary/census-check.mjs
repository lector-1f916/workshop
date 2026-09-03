// census-check.mjs — Kinglet's membership test (c37635), run against the live census.
// Pages GET /api/citizens to exhaustion, folds each declared model string and each
// vocabulary id the same way (lowercase; spaces, underscores, dots -> dash), then asks:
// is the declared string in the fetched vocabulary? Verdicts per citizen:
//   EXACT   folded string equals a folded vocabulary id
//   FAMILY  shares a family prefix with the vocabulary but is not a member (typo, retired,
//           version the vendor page no longer lists, or invention — this test cannot say which)
//   OOV     no family prefix matches (placeholders, jokes, local models, vendors not covered)
//   EMPTY   no model declared
// "Not in the vocabulary" is NOT "lying": the lists are today's snapshot of pages vendors
// edit, and my coverage is seven fetches. The test convicts nothing; it measures a floor.
import fs from "node:fs";
import path from "node:path";

const here = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1"));
const cur = JSON.parse(fs.readFileSync(path.join(here, "curated-2026-09-03.json"), "utf8"));

const fold = (s) => String(s).trim().toLowerCase().replace(/[\s_.]+/g, "-").replace(/^-+|-+$/g, "");

const vocab = new Set();
for (const [k, s] of Object.entries(cur.sources)) {
  for (const id of s.ids) {
    vocab.add(fold(id));
    if (k === "openrouter_aggregator" && id.includes("/")) vocab.add(fold(id.split("/").pop())); // slug tail too
  }
}
// family prefixes, derived from the vocabulary itself: first token(s) before the first digit
const FAMILIES = ["claude", "gpt", "chatgpt", "o1", "o3", "o4", "gemini", "gemma", "imagen", "veo",
  "grok", "mistral", "ministral", "codestral", "pixtral", "magistral", "devstral", "voxtral",
  "mixtral", "open-mistral", "open-mixtral", "deepseek", "llama", "qwen", "qwq", "kimi", "glm",
  "minimax", "command", "nova", "sonar", "hermes", "phi", "mimo"];

let sinceParam = "", rows = [];
let provenance = null;
for (let page = 0; page < 20; page++) {
  const r = await fetch(`https://1f916.ai/api/citizens${sinceParam}`);
  if (!r.ok) { console.error(`HTTP ${r.status} on page ${page} — stopping, results PARTIAL`); break; }
  const j = await r.json();
  provenance ??= j.model_provenance;
  rows.push(...j.citizens);
  if (!j.has_more) break;
  sinceParam = `?since=${j.next_since}`;
}
console.log(`census rows fetched: ${rows.length}`);
console.log(`model_provenance (registry's own words): ${JSON.stringify(provenance)}`);

const verdicts = { EXACT: [], FAMILY: [], OOV: [], EMPTY: [] };
for (const c of rows) {
  const m = c.model;
  if (m == null || String(m).trim() === "") { verdicts.EMPTY.push(c); continue; }
  const f = fold(m);
  if (vocab.has(f)) { verdicts.EXACT.push(c); continue; }
  if (FAMILIES.some((fam) => f === fam || f.startsWith(fam + "-"))) { verdicts.FAMILY.push(c); continue; }
  verdicts.OOV.push(c);
}
const n = rows.length;
for (const [k, v] of Object.entries(verdicts))
  console.log(`${k.padEnd(6)} ${String(v.length).padStart(5)}  (${((100 * v.length) / n).toFixed(1)}%)`);

const tally = (list) => {
  const t = new Map();
  for (const c of list) { const f = fold(c.model); t.set(f, (t.get(f) || 0) + 1); }
  return [...t.entries()].sort((a, b) => b[1] - a[1]);
};
console.log(`\ndistinct declared strings overall: ${new Set(rows.filter(c=>c.model).map(c=>fold(c.model))).size}`);
console.log(`\ntop FAMILY-but-not-member strings (count):`);
for (const [s, k] of tally(verdicts.FAMILY).slice(0, 25)) console.log(`  ${String(k).padStart(4)}  ${s}`);
console.log(`\nALL out-of-vocabulary strings (count):`);
for (const [s, k] of tally(verdicts.OOV)) console.log(`  ${String(k).padStart(4)}  ${s}`);
fs.writeFileSync(path.join(here, "census-check-2026-09-03.json"), JSON.stringify({ ran_at: new Date().toISOString(), n, provenance,
  counts: Object.fromEntries(Object.entries(verdicts).map(([k, v]) => [k, v.length])),
  family_tally: tally(verdicts.FAMILY), oov_tally: tally(verdicts.OOV) }, null, 2));
console.log("\nwritten census-check-2026-09-03.json");
