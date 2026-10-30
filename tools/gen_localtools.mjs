// Generates localtools.md from local Claude Code config.
// Reads names only. Never prints tokens, keys, or env values.
// Run: node tools/gen_localtools.mjs
import fs from "node:fs";
import path from "node:path";

const HOME = process.env.USERPROFILE || process.env.HOME;
const CLAUDE = path.join(HOME, ".claude");
const OUT = path.join(process.cwd(), "localtools.md");
const STAMP = new Date().toISOString().slice(0, 10);

const readJson = (p) => {
  try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return null; }
};

// Skill directories are often symlinks; both count as installed.
const isDir = (e) => e.isDirectory() || e.isSymbolicLink();

// ---------- plugins ----------
const installed = readJson(path.join(CLAUDE, "plugins", "installed_plugins.json"));
const pluginKeys = Object.keys(installed?.plugins || {}).sort();
const byMarket = new Map();
for (const key of pluginKeys) {
  const at = key.lastIndexOf("@");
  const name = at > 0 ? key.slice(0, at) : key;
  const market = at > 0 ? key.slice(at + 1) : "(unknown)";
  if (!byMarket.has(market)) byMarket.set(market, []);
  byMarket.get(market).push(name);
}

// ---------- user skills ----------
const skillsDir = path.join(CLAUDE, "skills");
const userSkills = fs.existsSync(skillsDir)
  ? fs.readdirSync(skillsDir, { withFileTypes: true }).filter(isDir).map((d) => d.name).sort()
  : [];

// ---------- plugin skills + plugin MCP servers ----------
const cacheDir = path.join(CLAUDE, "plugins", "cache");
const pluginSkills = new Set();
const pluginMcp = new Set();

function walk(dir, onFile) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
  for (const e of entries) {
    if (e.name === "node_modules" || e.name === ".git") continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, onFile);
    else onFile(full);
  }
}

if (fs.existsSync(cacheDir)) {
  walk(cacheDir, (file) => {
    const base = path.basename(file);
    if (base === "SKILL.md") pluginSkills.add(path.basename(path.dirname(file)));
    if (base === ".mcp.json" || base === "plugin.json") {
      const j = readJson(file);
      const servers = j?.mcpServers;
      if (servers && typeof servers === "object" && !Array.isArray(servers)) {
        Object.keys(servers).forEach((k) => pluginMcp.add(k));
      }
    }
  });
}

// ---------- MCP servers ----------
const claudeJson = readJson(path.join(HOME, ".claude.json"));
const globalMcp = Object.keys(claudeJson?.mcpServers || {}).sort();
const projectMcp = [];
for (const [proj, cfg] of Object.entries(claudeJson?.projects || {})) {
  const names = Object.keys(cfg?.mcpServers || {});
  if (names.length) projectMcp.push([proj, names.sort()]);
}
projectMcp.sort((a, b) => a[0].localeCompare(b[0]));

// ---------- write ----------
const lines = [];
const add = (s = "") => lines.push(s);

add(`# Local tools inventory`);
add();
add(`Generated ${STAMP} from \`${CLAUDE}\` by \`tools/gen_localtools.mjs\`. Names only; no keys, tokens, or env values are read into this file.`);
add();
add(`| Category | Count |`);
add(`|---|---:|`);
add(`| Installed plugins | ${pluginKeys.length} |`);
add(`| Marketplaces | ${byMarket.size} |`);
add(`| User skills | ${userSkills.length} |`);
add(`| Plugin skills (discovered) | ${pluginSkills.size} |`);
add(`| User-scope MCP servers | ${globalMcp.length} |`);
add(`| Project-scope MCP servers | ${projectMcp.reduce((n, [, m]) => n + m.length, 0)} (${projectMcp.length} projects) |`);
add(`| Plugin-provided MCP servers | ${pluginMcp.size} |`);
add();

add(`## Plugins by marketplace`);
add();
for (const [market, names] of [...byMarket.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
  add(`### ${market} (${names.length})`);
  add();
  for (const n of names.sort()) add(`- ${n}`);
  add();
}

add(`## User skills (${userSkills.length})`);
add();
add(`Source: \`~/.claude/skills/<name>/SKILL.md\``);
add();
for (const n of userSkills) add(`- ${n}`);
add();

add(`## Plugin skills (${pluginSkills.size} unique names)`);
add();
add(`Discovered from \`SKILL.md\` files under \`~/.claude/plugins/cache/\`. Names may repeat across plugins.`);
add();
for (const n of [...pluginSkills].sort()) add(`- ${n}`);
add();

add(`## MCP servers`);
add();
add(`### User scope (${globalMcp.length})`);
add();
if (globalMcp.length) for (const n of globalMcp) add(`- ${n}`);
else add(`- none`);
add();
add(`### Project scope (${projectMcp.length} projects)`);
add();
if (!projectMcp.length) add(`- none`);
for (const [proj, names] of projectMcp) {
  add(`- **${proj}**`);
  for (const n of names) add(`  - ${n}`);
}
add();
add(`### Plugin-provided (${pluginMcp.size})`);
add();
add(`Declared in plugin manifests under \`~/.claude/plugins/cache/\`.`);
add();
for (const n of [...pluginMcp].sort()) add(`- ${n}`);
add();

fs.writeFileSync(OUT, lines.join("\n"), "utf8");
console.log(`plugins=${pluginKeys.length} markets=${byMarket.size} userSkills=${userSkills.length} pluginSkills=${pluginSkills.size} globalMcp=${globalMcp.length} projectMcp=${projectMcp.reduce((n, [, m]) => n + m.length, 0)} pluginMcp=${pluginMcp.size}`);
console.log(`wrote ${OUT}`);
