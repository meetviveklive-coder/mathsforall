# AI Coding Agent Instructions

## 1. Project Context
Project: Ganit (working name)
Purpose: Free, grade-free maths learning website, zero to engineering maths, Indian context, no ranks or certificates.
Primary Users: Learners of any age (first user: a child around school class 5) and their parents.

## 2. Source of Truth
Before significant changes, read the relevant documents in /docs:
- docs/PRD.md — what we are building and what we are not
- docs/DESIGN_SYSTEM.md — look, feel, tone
- docs/ARCHITECTURE.md — static site + offline content pipeline
- docs/DATABASE.md — content files and browser progress store
- docs/SECURITY.md — children's privacy, no data collection
- docs/CODE_STYLE.md — code and content writing conventions
- docs/TESTING.md — verification and tests
Content rules: `schema/topic.schema.json`, `curriculum/topic-map.json`.
Do not contradict these documents without first identifying the conflict.

## 3. The agents
Defined in `.claude/agents/`:
| Agent | Owns | Never does |
|---|---|---|
| curriculum-architect | `curriculum/topic-map.json` | write lessons |
| content-writer | `content/topics/*.json` (draft) | mark anything verified/approved |
| visuals | `content/visuals/**` SVG generators | use AI image generation |
| math-verifier | runs tools, sets `status: verified` | edit lesson prose or answers |
| site-builder | `site/**` | edit content files |
Status flow: draft → verified (math-verifier) → approved (human only).

## 4. General Rules
- Understand existing files before modifying them
- Follow the docs above; do not invent requirements
- Do not add accounts, tracking, analytics, or third-party scripts
- Do not add grades, ranks, timers, certificates, or leaderboards
- Avoid unnecessary dependencies and unrelated changes

## 5. Planning
Before a non-trivial task: read relevant docs and files, list affected files, identify tests, write a short plan.

## 6. Implementation
Make focused changes, reuse established patterns, preserve existing behaviour.

## 7. Validation
After content changes: `python3 tools/verify_content.py`
After topic-map changes: `python3 tools/check_topic_map.py`
After site changes: test, lint, type check, build (see docs/TESTING.md §7).
Review changed files for unintended edits. Never claim a check passed unless it was run.

## 8. Documentation
Update docs when product behaviour, architecture, data model, security rules or conventions change.

## 9. Conflict Handling
If requirements conflict: do not guess. State the conflict and ask.

## 10. Completion Criteria
A task is complete only when requirements are met, the relevant checks pass, no unintended files changed, privacy rules are respected, and docs are updated where needed.
