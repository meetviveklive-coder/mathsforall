# Ganit (working name)

A free, grade-free mathematics website: from counting to engineering mathematics,
one concept at a time, in an Indian context. No accounts, no ranks, no certificates.

Start with `AGENTS.md`, then `docs/PRD.md`.

## Layout
| Path | What |
|---|---|
| `docs/` | The 8 source-of-truth documents (PRD, design system, architecture, data model, security, code style, testing) |
| `AGENTS.md`, `CLAUDE.md` | Rules every agent follows (CLAUDE.md imports AGENTS.md for Claude Code) |
| `.claude/agents/` | The 5 agents: curriculum-architect, content-writer, visuals, math-verifier, site-builder |
| `curriculum/topic-map.json` | Prerequisite graph (source) |
| `curriculum/TOPIC_MAP.md` | Readable version for review (generated) |
| `schema/` | JSON Schemas for the topic map and topic files |
| `content/topics/` | One JSON file per topic |
| `tools/` | Verifier, topic-map checker, renderer, tests |
| `site/` | Astro website (phase 2) |

## Setup
```bash
pip install -r requirements.txt     # sympy, jsonschema, pytest
python3 -m pytest -q tools/tests    # tool self-tests
```

## Per-topic pipeline (in Claude Code)
1. `content-writer` → `content/topics/<id>.json` (status `draft`)
2. `visuals` → draws requested diagrams
3. `math-verifier` → runs `tools/verify_content.py`, re-solves everything; sets `verified` or writes `content/reviews/<id>.md`
4. **You** read it and set `approved`
5. `site-builder` → renders approved topics

Example prompt in Claude Code: *"Use the content-writer agent to write s0-fractions-meaning, then the visuals agent, then the math-verifier agent. Stop before approval."*

## Run the site locally
```bash
cd site
npm install
npm run dev            # http://localhost:4321 (shows draft/verified topics)
npm run build          # production build: approved topics only
npm run build:preview  # build including draft/verified topics, with a preview banner
npm test               # unit tests
```
Astro 7 needs Node.js 22.23.4 or newer (`.node-version` pins 24 for Cloudflare builds).

## Deploy (Cloudflare)
Deployed as a Cloudflare Worker with static assets. Every push to `main` builds and deploys. Settings: root directory empty (repo root), build command `npm run build` (builds `site/` via the root `package.json`), deploy command `npx wrangler deploy` (uses the root `wrangler.jsonc`). Only `approved` topics are published.

## Commands
```bash
python3 tools/check_topic_map.py     # topic map: schema, DAG, stage order
python3 tools/render_topic_map.py    # regenerate curriculum/TOPIC_MAP.md
python3 tools/verify_content.py      # verify all topic files
```

## Status
- [x] Phase 0: docs, agents, schema, verifier
- [x] Phase 1: Stage 0–1 topic map (58 topics) — approved
- [x] Phase 2: pilot — 3 fraction topics approved; site deploys to Cloudflare from `main`
- [ ] Pilot week with the first learner; log confusion points per topic
- [ ] Phase 3: rest of Stage 0–1 (fractions, decimals and percent units done; ratio started; 18 topics live)
- [ ] Phase 4: placement, knowledge map, spaced review, export/import
- [ ] Phase 5: launch
