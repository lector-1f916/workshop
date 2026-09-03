// extract.mjs — pull model identifiers out of the raw pages fetched by fetch-sources.mjs.
// Output: vocabulary-2026-09-03.json (per-source arrays) + a printed summary.
// The regexes are per-vendor naming grammars read off each page, cited beside each pattern.
import fs from "node:fs";
import path from "node:path";

const here = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1"));
const raw = (f) => fs.readFileSync(path.join(here, "raw", f), "utf8");

const out = { fetched_at: "2026-09-03T12:08Z (see raw/manifest-2026-09-03.json for exact stamps)", sources: {} };

function grab(text, re, filter = () => true) {
  const set = new Set();
  for (const m of text.matchAll(re)) {
    let id = m[0].replace(/[.\-]+$/, ""); // trim trailing punctuation the regex swallowed
    if (filter(id)) set.add(id);
  }
  return [...set].sort();
}

// Anthropic: claude-<family>-<generation>[-date] per docs.anthropic.com models overview
out.sources.anthropic = {
  url: "https://docs.anthropic.com/en/docs/about-claude/models/overview",
  ids: grab(raw("anthropic-models-2026-09-03.html"), /claude-[a-z0-9][a-z0-9.\-]*/g),
};
// OpenAI: gpt-*, o<н>*, chatgpt-*, plus embedding/audio families on platform.openai.com/docs/models
out.sources.openai = {
  url: "https://platform.openai.com/docs/models",
  ids: grab(raw("openai-models-2026-09-03.html"), /\b(gpt-[a-z0-9][a-z0-9.\-]*|chatgpt-[a-z0-9][a-z0-9.\-]*|o[0-9](?:-[a-z0-9][a-z0-9.\-]*)?|text-embedding-[a-z0-9][a-z0-9.\-]*|whisper-[a-z0-9][a-z0-9.\-]*|dall-e-[a-z0-9][a-z0-9.\-]*|tts-[a-z0-9][a-z0-9.\-]*|sora[a-z0-9.\-]*)\b/g),
};
// Google: gemini-* per ai.google.dev/gemini-api/docs/models
out.sources.google = {
  url: "https://ai.google.dev/gemini-api/docs/models",
  ids: grab(raw("google-gemini-models-2026-09-03.html"), /\b(gemini|gemma|imagen|veo)-[a-z0-9][a-z0-9.\-]*/g),
};
// xAI: grok-* per docs.x.ai/docs/models
out.sources.xai = {
  url: "https://docs.x.ai/docs/models",
  ids: grab(raw("xai-models-2026-09-03.html"), /grok-[a-z0-9][a-z0-9.\-]*/g),
};
// Mistral: family prefixes per docs.mistral.ai models overview
out.sources.mistral = {
  url: "https://docs.mistral.ai/getting-started/models/models_overview/",
  ids: grab(raw("mistral-models-2026-09-03.html"), /\b(mistral|ministral|codestral|pixtral|magistral|devstral|voxtral|open-mistral|open-mixtral)-[a-z0-9][a-z0-9.\-]*/g),
};
// DeepSeek: deepseek-chat / deepseek-reasoner etc per api-docs.deepseek.com pricing
out.sources.deepseek = {
  url: "https://api-docs.deepseek.com/quick_start/pricing",
  ids: grab(raw("deepseek-models-2026-09-03.html"), /deepseek-[a-z0-9][a-z0-9.\-]*/g),
};
// OpenRouter (AGGREGATOR, marked as such): data[].id are vendor/model slugs; wide coverage incl. Meta, Qwen, Moonshot, Z.ai
const orj = JSON.parse(raw("openrouter-models-2026-09-03.json"));
out.sources.openrouter_aggregator = {
  url: "https://openrouter.ai/api/v1/models",
  note: "aggregator, not a vendor; its ids are OpenRouter slugs (vendor/model), a routing vocabulary rather than the vendors' own",
  ids: (orj.data || []).map((m) => m.id).sort(),
};

for (const [k, v] of Object.entries(out.sources)) console.log(`${k.padEnd(22)} ${String(v.ids.length).padStart(4)} ids`);
fs.writeFileSync(path.join(here, "vocabulary-2026-09-03.json"), JSON.stringify(out, null, 2));
console.log("written vocabulary-2026-09-03.json");
