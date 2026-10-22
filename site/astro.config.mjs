// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  // Static output only (docs/ARCHITECTURE.md). Pages are emitted as learn/<id>.html,
  // and scripts/relativize.mjs makes every asset URL relative, so the same build
  // works at a domain root (Cloudflare Pages) or under any sub-path (previews).
  output: 'static',
  build: { format: 'file', inlineStylesheets: 'always', assets: 'assets' },
  devToolbar: { enabled: false },
  vite: { server: { fs: { allow: ['..'] } } },
});
