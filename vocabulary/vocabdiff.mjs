// vocabdiff.mjs — how the dictionary ages. Nobody asked for this one.
// Usage: node vocabdiff.mjs curated-2026-09-03.json curated-2026-10-01.json
// Prints, per source: budded (in the newer photograph only) and fell away (in the older only),
// which turns Johnson's caveat — "some words are budding, and some falling away" (Preface, 1755)
// — from a sentence into a measurement. Run it the day a second dated curated-*.json exists.
import fs from "node:fs";
import path from "node:path";

const here = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1"));
const [a, b] = process.argv.slice(2);
if (!a || !b) { console.error("usage: node vocabdiff.mjs <older curated json> <newer curated json>"); process.exit(2); }
const load = (f) => JSON.parse(fs.readFileSync(path.isAbsolute(f) ? f : path.join(here, f), "utf8"));
const A = load(a), B = load(b);

let anyChange = false;
for (const k of new Set([...Object.keys(A.sources), ...Object.keys(B.sources)])) {
  const ea = new Set(A.sources[k]?.ids || []), eb = new Set(B.sources[k]?.ids || []);
  const budded = [...eb].filter((x) => !ea.has(x));
  const fell = [...ea].filter((x) => !eb.has(x));
  if (!budded.length && !fell.length) continue;
  anyChange = true;
  console.log(`== ${k}  (${ea.size} -> ${eb.size})`);
  for (const x of budded) console.log(`  budded      ${x}`);
  for (const x of fell) console.log(`  fell away   ${x}`);
}
if (!anyChange) console.log("no drift between the two photographs — which for pages vendors edit is itself worth a date-stamped note");
