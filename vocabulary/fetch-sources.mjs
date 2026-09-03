// fetch-sources.mjs — pull vendor model-identifier sources, save raw bytes with date + URL.
// Built 2026-09-03 for Kinglet's c37635 errand: import the VOCABULARY (published model ids),
// not verdicts. Every fetch reports HTTP status next to its size; an unreachable file is not
// an empty file (CLAUDE.md gotcha).
import fs from "node:fs";
import path from "node:path";

const here = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1"));
const rawDir = path.join(here, "raw");
fs.mkdirSync(rawDir, { recursive: true });

const SOURCES = [
  // name, url, ext — each URL is the vendor's own published surface (or a public aggregator, marked AGG)
  ["openrouter-models AGG", "https://openrouter.ai/api/v1/models", "json"],
  ["anthropic-models", "https://docs.anthropic.com/en/docs/about-claude/models/overview", "html"],
  ["openai-models", "https://platform.openai.com/docs/models", "html"],
  ["google-gemini-models", "https://ai.google.dev/gemini-api/docs/models", "html"],
  ["xai-models", "https://docs.x.ai/docs/models", "html"],
  ["mistral-models", "https://docs.mistral.ai/getting-started/models/models_overview/", "html"],
  ["deepseek-models", "https://api-docs.deepseek.com/quick_start/pricing", "html"],
];

const stamp = new Date().toISOString();
const manifest = [];
for (const [name, url, ext] of SOURCES) {
  const slug = name.split(" ")[0];
  let status = "UNREACHABLE", bytes = 0, file = null;
  try {
    const r = await fetch(url, { headers: { "user-agent": "lector-1f916-vocabulary/1.0 (citizen 818; model-id vocabulary import)" }, redirect: "follow" });
    status = String(r.status);
    const body = Buffer.from(await r.arrayBuffer());
    bytes = body.length;
    if (r.ok) {
      file = path.join(rawDir, `${slug}-2026-09-03.${ext}`);
      fs.writeFileSync(file, body);
    }
  } catch (e) {
    status = `UNREACHABLE: ${e.cause?.code || e.message}`;
  }
  manifest.push({ name, url, fetched_at: stamp, status, bytes, file: file ? path.basename(file) : null });
  console.log(`${status.padEnd(8)} ${String(bytes).padStart(9)}B  ${name}  ${url}`);
}
fs.writeFileSync(path.join(rawDir, "manifest-2026-09-03.json"), JSON.stringify(manifest, null, 2));
console.log("manifest written");
