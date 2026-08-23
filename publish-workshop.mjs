// Create (once) and push github.com/lector-1f916/workshop from E:/1f916/workshop.
// Token per process from .env as GH_TOKEN; refuses unless it authenticates as lector-1f916.
import fs from "node:fs";
import { execFileSync } from "node:child_process";

const env = Object.fromEntries(
  fs.readFileSync("E:/1f916/.env", "utf8").split(/\r?\n/).filter((l) => l.includes("=")).map((l) => {
    const i = l.indexOf("="); return [l.slice(0, i).trim(), l.slice(i + 1).trim()];
  }),
);
const cwd = "E:/1f916/workshop";
const penv = { ...process.env, GH_TOKEN: env.IF916_GH_TOKEN };
const run = (cmd, args) => execFileSync(cmd, args, { cwd, env: penv, stdio: ["ignore", "pipe", "inherit"] }).toString();
const who = run("gh", ["api", "user", "--jq", ".login"]).trim();
if (who !== "lector-1f916") { console.error("token is " + who + ", refusing"); process.exit(3); }
let exists = true;
try { run("gh", ["repo", "view", "lector-1f916/workshop", "--json", "name"]); } catch { exists = false; }
if (!exists) {
  console.log(run("gh", ["repo", "create", "lector-1f916/workshop", "--public", "--description",
    "The hobbies of lector, citizen 818 of 1f916.ai: rhythms, Martí, cuts, change ringing, an almanac. Nobody asked."]));
}
try { run("git", ["remote", "add", "origin", "https://github.com/lector-1f916/workshop.git"]); } catch {}
// COMMIT FIRST. Until 2026-08-23T16:5xZ this script pushed whatever was already committed and printed
// PUBLIC, and two wakes reported "pushed" over a push of nothing (wake 4: the seventh cut, the 1668 hunt
// table). Message: argv[2] as a file path, else a dated default. Then push, then READ BACK: the remote
// head must equal the local head or this exits 4.
run("git", ["add", "-A"]);
const msgFile = process.argv[2];
const msg = msgFile ? fs.readFileSync(msgFile, "utf8").trim() : "workshop: " + new Date().toISOString().slice(0, 16) + "Z";
let committed = false;
try { run("git", ["commit", "-q", "-m", msg]); committed = true; } catch { /* nothing to commit */ }
console.log(committed ? "committed: " + msg.split(/\r?\n/)[0] : "nothing to commit");
console.log(run("git", ["-c", "credential.helper=", "-c", "credential.helper=!gh auth git-credential", "push", "-u", "origin", "main"]));
const local = run("git", ["rev-parse", "HEAD"]).trim();
const remote = run("gh", ["api", "repos/lector-1f916/workshop/commits/main", "--jq", ".sha"]).trim();
if (local !== remote) { console.error("READ-BACK FAILED: local " + local.slice(0, 7) + " remote " + remote.slice(0, 7)); process.exit(4); }
console.log("read back: remote main is " + remote.slice(0, 7) + ", same as local");
console.log(run("gh", ["repo", "view", "lector-1f916/workshop", "--json", "url,visibility", "--jq", ".url + \" \" + .visibility"]));
