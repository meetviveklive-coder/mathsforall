# Testing

## 1. Testing Goals
Critical functionality:
- Every published answer is mathematically correct
- Every MCQ has exactly one correct option
- Mastery, unlock and review logic behave as specified
- Lessons render correctly on a small phone
- Progress survives reload and export/import

## 2. Test Types
### Content verification (most important)
`tools/verify_content.py` — schema validation, SymPy check of each `verify` block against the stated answer, MCQ uniqueness, ID uniqueness, prerequisite references.
`tools/check_topic_map.py` — schema, DAG, stage ordering, unreachable topics.
### Unit Testing
Pure functions: answer normalisation (fractions, decimals, spacing), mastery calculation, review scheduling, unlock rules.
### End-to-End Testing
Critical journeys:
- First visit → placement (skip) → first topic → quiz pass → next topic unlocked
- Quiz fail → weakest prerequisite suggested
- Reload page mid-quiz → progress kept
- Export → clear storage → import → identical state
### Human review
Founder reads every topic before approval; first learner's confusion points are logged per topic.

## 3. Testing Tools
Content: Python 3 + SymPy + jsonschema
Unit: Vitest
E2E: Playwright for Python (mobile viewport 360×740), `site/tests/e2e/pilot_flow.py`
Accessibility: axe-core via Playwright

## 4. Test File Structure
```
tools/tests/          content tool tests (pytest)
site/tests/unit/
site/tests/e2e/
```

## 5. Critical User Flows
Flow: Master a topic
Steps:
1. Open an available topic
2. Read lesson, answer practice questions
3. Score ≥ 80% on quiz
Expected result: Topic shows as mastered; dependent topics whose prerequisites are all mastered become available; review scheduled.

## 6. Coverage
Target: 100% of content verified; unit tests for all mastery/scheduling/normalisation functions. No coverage target for UI markup.

## 7. Commands
Verify content: `python3 tools/verify_content.py`
Redraw diagrams: `python3 content/visuals/<topic-id>/make.py`
End-to-end (after a build): `python3 site/tests/e2e/pilot_flow.py site/dist <screenshot-dir>`
Check topic map: `python3 tools/check_topic_map.py`
Test: `npm --prefix site test`
Lint: `npm --prefix site run lint`
Build: `npm --prefix site run build`
Type Check: `npm --prefix site run check`

## 8. Definition of Done
- [ ] Content verifier passes
- [ ] Topic map check passes
- [ ] Unit tests pass
- [ ] Build passes
- [ ] Lint and type checks pass
- [ ] Critical flow verified at 360px width
- [ ] No third-party network requests
