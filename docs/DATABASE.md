# Data Model

There is no server database. This document defines the two data stores that do exist:
the **content files** (in Git) and the **progress store** (in the learner's browser).
The blueprint's DATABASE.md template is adapted accordingly.

## 1. Engines
Content: JSON files validated by JSON Schema (`schema/*.schema.json`).
Progress: IndexedDB (database `ganit`, version 1), localStorage fallback.
Pilot (Phase 2) stores the same shape as one localStorage value `ganit:progress:v1` (`site/src/lib/progress.ts`); Phase 4 moves it to IndexedDB.

## 2. Naming Conventions
Topic IDs: `s<stage>-<kebab-name>`, e.g. `s0-place-value`. Never renamed once approved (progress references them).
Question IDs: `<topic-id>/<p|q|c>-<n>` — p = practice, q = quiz, c = checkpoint.
JSON keys: snake_case.
Timestamps: ISO 8601 strings, UTC.

## 3. Content: topic map (`curriculum/topic-map.json`)
Purpose: The prerequisite graph.
Fields per topic: id, title, stage, prerequisites[], objectives[], misconceptions[], est_minutes.
Rules: must be a DAG; prerequisites must exist and be in the same or an earlier stage.

## 4. Content: topic file (`content/topics/<id>.json`)
Purpose: Everything needed to teach and test one topic. See `schema/topic.schema.json`.
Sections: meta (id, status, version), lesson (sections, worked examples), visuals, practice[], quiz[], doubts[].
Every question has: prompt, answer, hints[], explanation, verify{}.
MCQs also have: options[], and for each wrong option the misconception it targets.

## 5. Progress store (browser)
### object store `topic_state`
Key: topic_id
Fields: status (locked | available | in_progress | mastered), best_quiz_pct, mastered_at, review_due_at, review_interval_days
### object store `attempts`
Key: auto
Fields: question_id, correct (bool), answered_at, hint_used (bool)
### object store `settings`
Key: name
Fields: value (e.g. streaks_enabled, mastery_threshold)

## 6. Relationships
topic-map topic 1 → 1 topic file (once written)
topic file 1 → many questions
topic_state 1 → many attempts (by question_id prefix)

## 7. Constraints
Required: every question has `verify` unless `verify.kind = "manual"` with a reason.
Unique: topic ids, question ids.
Status flow: draft → verified (verifier passed) → approved (human). Only `approved` ships.

## 8. Data Validation
- `tools/check_topic_map.py`: schema + DAG + stage ordering
- `tools/verify_content.py`: schema + SymPy check of every answer + MCQ has exactly one correct option

## 9. Soft Delete
Not applicable. Retired topics are kept with `status: retired` so old progress still resolves.

## 10. Auditing
Git history is the audit trail for content. Learner data: none leaves the device.

## 11. Sensitive Data
Sensitive fields: none collected. Progress contains no name, age, email or identifier.
Export file contains only topic states and attempt counts.

## 12. Migration Rules
Progress schema changes must:
1. Bump the IndexedDB version
2. Include an upgrade function that preserves existing progress
3. Be tested with a fixture of the previous version
4. Keep export files from older versions importable

## 13. Seed Data
`tools/tests/fixtures/s0-sample.json` — a minimal valid topic used by the verifier tests (not shipped).
