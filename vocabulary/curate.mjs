// curate.mjs — cut scrape noise out of the extracted candidates. Rules are published here,
// the raw candidate lists stay in vocabulary-2026-09-03.json, so any curation call can be
// disputed by pointing at the raw page. Output: curated-2026-09-03.json.
// Known losses, accepted and stated: ids with no digit and no keep-suffix (gpt-oss, grok-stt,
// mistral-embed) are dropped by rule; the openrouter aggregator list catches most of them.
import fs from "node:fs";
import path from "node:path";

const here = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1"));
const v = JSON.parse(fs.readFileSync(path.join(here, "vocabulary-2026-09-03.json"), "utf8"));

// a candidate survives when it looks like an API identifier, not a page artifact:
const EXT = /\.(png|jpe?g|svg|gif|webp|io|com|localhost)$/;
const STOP = [
  "system-card", "-and-", "readme", "connectors", "quickstart", "plugin", "-card", "card-",
  "prompting", "evaluation", "-rag", "rag-", "-docs", "docs-", "-ui", "staging", "overview",
  "security", "analytics", "best-practices", "-skill", "iam-actions", "bedrock", "vertex",
  "foundry", "-api", "api-", "model-", "-models", "logo", "icon", "elevation", "hovercard",
  "switcher", "-font", "-grid", "-row", "-table", "table-", "-cta", "cta-", "footer",
  "resource", "bulletpoints", "description", "-title", "-width", "theme", "centered",
  "-desc", "-details", "interpreter", "tracing", "explored", "guardrails", "introduction",
  "concepts", "search-engine", "extractor", "documentchunking", "hcls", "-data", "-tool",
  "-product", "structured", "enterprise", "lechat", "compute", "-plan", "-function",
  "agents", "embeddings", "embedder", "classifier", "integration", "harness", "social",
  "-work-", "-code$", "-bot$", "-color-", "safety", "-batch", "-document$", "-image$",
  "-next$", "transcription",
];
const keep = (id) =>
  !EXT.test(id) &&
  !STOP.some((s) => s.endsWith("$") ? id.endsWith(s.slice(0, -1)) : id.includes(s)) &&
  (/\d/.test(id) || /-(embed|latest)$/.test(id));

const out = { curated_at: new Date().toISOString(), rules: "see curate.mjs in this directory", sources: {} };
for (const [k, s] of Object.entries(v.sources)) {
  if (k === "openrouter_aggregator") { out.sources[k] = { url: s.url, note: s.note, ids: s.ids }; continue; }
  const kept = s.ids.filter(keep);
  const dropped = s.ids.filter((x) => !keep(x));
  out.sources[k] = { url: s.url, ids: kept, dropped_by_rule: dropped };
  console.log(`${k.padEnd(12)} kept ${String(kept.length).padStart(4)}  dropped ${dropped.length}`);
}
fs.writeFileSync(path.join(here, "curated-2026-09-03.json"), JSON.stringify(out, null, 2));
console.log("written curated-2026-09-03.json");
