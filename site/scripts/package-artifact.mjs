// Package dist/ for a private Claude artifact preview (not used for real hosting).
// The artifact host wraps the main page in its own <html>/<head>/<body>, so the
// entry page's wrapper tags are removed; other pages keep their full documents.
import fs from 'node:fs';
import path from 'node:path';

const [, , outDir = 'artifact'] = process.argv;
const dist = path.resolve('dist');
const out = path.resolve(outDir);
fs.rmSync(out, { recursive: true, force: true });
fs.cpSync(dist, out, { recursive: true });
fs.rmSync(path.join(out, '_headers'), { force: true });

const index = path.join(out, 'index.html');
let html = fs.readFileSync(index, 'utf-8');
html = html
  .replace(/<!doctype html>/i, '')
  .replace(/<html[^>]*>/i, '')
  .replace(/<\/html>/i, '')
  .replace(/<head>/i, '')
  .replace(/<\/head>/i, '')
  .replace(/<body[^>]*>/i, '')
  .replace(/<\/body>/i, '')
  .replace(/<meta charset="utf-8"\s*\/?>/i, '')
  .replace(/<meta name="viewport"[^>]*>/i, '');
html = html.replace(/<title>/i, '<meta name="claude:viewport-fit-sides" content="cover"><title>');
fs.renameSync(index, path.join(out, 'home.html'));
fs.writeFileSync(path.join(out, 'home.html'), html.trimStart());

// Pages link back to index.html; keep a full-document copy under that name too.
fs.copyFileSync(path.join(dist, 'index.html'), index);

const files = [];
(function walk(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.name !== 'home.html') files.push(path.relative(out, p).split(path.sep).join('/'));
  }
})(out);
fs.writeFileSync(path.join(out, 'files.json'), JSON.stringify(files, null, 1));
console.log(`packaged ${files.length + 1} files into ${outDir}`);
