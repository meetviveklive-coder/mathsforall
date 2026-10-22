// Rewrite root-absolute asset URLs ("/assets/...") to relative ones after `astro build`,
// so the static site works at any base path. Also fails the build if any page would
// load something from another origin (docs/SECURITY.md: no third-party requests).
import fs from 'node:fs';
import path from 'node:path';

const dist = path.resolve('dist');
let changed = 0;
const external = [];

function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (/\.(html|css|js)$/.test(e.name)) fix(p);
  }
}

function fix(file) {
  const depth = path.relative(dist, path.dirname(file)).split(path.sep).filter(Boolean).length;
  const prefix = depth ? '../'.repeat(depth) : './';
  const src = fs.readFileSync(file, 'utf-8');
  const out = src.replace(/(["'(=]\s*)\/assets\//g, `$1${prefix}assets/`);
  if (out !== src) {
    fs.writeFileSync(file, out);
    changed++;
  }
  if (file.endsWith('.html')) {
    const re = /\b(?:src|href)\s*=\s*["'](?:https?:)?\/\/[^"']+/gi;
    for (const m of out.matchAll(re)) external.push(`${path.relative(dist, file)}: ${m[0]}`);
  }
}

walk(dist);
if (external.length) {
  console.error('External URLs found (not allowed):\n' + external.join('\n'));
  process.exit(1);
}
console.log(`relativize: rewrote ${changed} file(s); no external URLs.`);
