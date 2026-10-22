# Architecture

## 1. System Overview
Two separate systems:
1. **Content pipeline (build time, on the author's machine):** AI agents write topic files; a code verifier checks every answer; a human approves; approved files are committed to Git.
2. **Website (run time, in the learner's browser):** A static site generated from the approved content files. No server, no database, no accounts. Progress lives in the learner's browser.

```
Topic map ─▶ Writer ─▶ Visuals ─▶ Verifier ─▶ Human approval ─▶ content/topics/*.json
                                                                        │
                                                       Astro build ◀────┘
                                                            │
                                         Static files on Cloudflare Pages
                                                            │
                                         Learner's browser (progress in IndexedDB)
```

## 2. Architecture Pattern
Pattern: Static site (JAMstack) + offline content pipeline.
Reason: Free to host, no per-user cost, no learner data on any server (simplest position under India's DPDP Rules for under-18 users), fast on slow networks.

## 3. Technology Stack
Frontend: Astro (static output), minimal client-side TypeScript islands for quizzes and progress.
Backend: None.
Database: None. Content = JSON files in Git. Progress = IndexedDB in the browser (localStorage fallback).
Authentication: None.
Storage: Git repository.
Hosting: Cloudflare Pages free plan (limits: 20,000 files per site, 500 builds/month — content is bundled one file per topic, not per question).
Payments / Email / Analytics: None. No analytics or tracking scripts.
Maths rendering: KaTeX, rendered at build time to HTML (no client JS needed for static maths).
Diagrams: Code-generated SVG (never AI image generation).
Content verification: Python 3 + SymPy (`tools/verify_content.py`).

## 4. System Components
### Content pipeline
Responsibilities:
- Topic map with prerequisites (`curriculum/topic-map.json`)
- One JSON file per topic (`content/topics/<topic-id>.json`) matching `schema/topic.schema.json`
- Verification of every answer and every MCQ option set
### Website
Responsibilities:
- Render lessons, practice, quizzes from topic files
- Mastery engine, unlock logic, spaced review — all client-side
- Export/import progress
### Browser storage
Responsibilities:
- Persist learner progress on-device only

## 5. Architecture Diagram
See §1.

## 6. Data Flow (learner answers a quiz question)
1. Learner submits an answer
2. Client normalises it (trims, parses fractions/decimals)
3. Client compares with the answer stored in the topic bundle
4. Feedback and explanation shown
5. Attempt recorded in IndexedDB
6. On quiz completion, mastery is recomputed; unlocked topics update on the map

## 7. Project Structure
```
AGENTS.md / CLAUDE.md     agent rules (root, so tools discover them)
docs/                     the 8 source-of-truth documents
.claude/agents/           the 5 agent definitions
curriculum/topic-map.json prerequisite graph
content/topics/           one JSON per topic (status: draft | verified | approved)
schema/                   JSON Schemas for topic map and topic files
tools/                    verify_content.py, check_topic_map.py, render_topic_map.py
site/                     Astro project (phase 2)
```

## 8. Dependency Rules
- The site reads only `approved` topic files; drafts never ship.
- Content files never contain code to execute in the browser.
- UI components never write to anything but the progress store.
- No third-party script is loaded at run time (KaTeX is self-hosted).

## 9. Key Technical Decisions
Decision: No accounts; progress on device.
Context: Free hosting; under-18 users; DPDP Rules require verifiable parental consent for processing children's personal data (most obligations from ~May 2027).
Alternatives: Accounts with a hosted database.
Reason: Zero personal data collected. Tradeoff: progress lost if browser data is cleared — mitigated by export/import.

Decision: Code verifier is the correctness gate, not an AI reviewer.
Context: Writer and reviewer on the same model share blind spots.
Alternatives: AI-only review.
Reason: SymPy computation is deterministic.

Decision: AI tutor parked.
Context: Live AI costs money per question and needs accounts; in-browser models are unreliable at maths and unavailable on most phones.
Reason: Revisit after v1; likely as "doubt bank" retrieval first.

## 10. Performance Considerations
- Lesson page ≤ 150 KB transferred excluding KaTeX fonts.
- Works on 3G: content readable before any client JS loads.

## 11. Scalability Considerations
- Static CDN; traffic does not change cost.
- File count stays well under 20,000 by bundling per topic.

## 12. Failure Scenarios
What happens if:
- Browser storage is unavailable (private mode)? Site works; banner says progress will not be saved.
- Storage is cleared? Progress lost; export reminder shown after each mastered topic.
- A published answer is wrong? "Report a mistake" link; fix, re-verify, redeploy.
- Hosting is down? Nothing learner-side to recover; redeploy elsewhere from Git.
