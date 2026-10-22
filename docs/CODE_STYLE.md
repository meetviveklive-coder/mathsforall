# Code Style & Conventions

## 1. General Principles
- Prefer readable code
- Keep functions focused
- Avoid unnecessary abstractions
- Reuse existing components and utilities
- Prefer consistency over novelty
- Content is data, not code: never put logic in topic JSON

## 2. Naming
Components: PascalCase (`QuizCard.astro`)
Functions: camelCase (TypeScript), snake_case (Python)
Variables: camelCase (TS), snake_case (Python)
Constants: UPPER_SNAKE_CASE
Files: kebab-case, except components
Content keys: snake_case
Topic IDs: `s<stage>-<kebab-name>`

## 3. Folder Structure
See docs/ARCHITECTURE.md §7. Site code lives only under `site/`. Authoring tools only under `tools/`.

## 4. Imports
- Relative imports within a feature folder; `@/` alias for `site/src`
- No new dependency without a one-line reason in the PR/commit message

## 5. Components
Components should:
- Have a single responsibility
- Render correctly with JavaScript disabled where possible (lessons must; quizzes may need JS)
- Take content via props; never fetch content themselves

## 6. Functions
Functions should:
- Do one logical thing
- Have clear names
- Be pure where possible (mastery and scheduling logic must be pure and unit-tested)

## 7. Error Handling
Use: explicit result checks; show a learner-friendly message and keep the page usable.
Do not: swallow errors silently; show stack traces to learners.

## 8. Comments
Comments should explain why something exists, important tradeoffs, and non-obvious behaviour (especially in maths answer normalisation).

## 9. Logging
Authoring tools: print clear PASS/FAIL lines with IDs.
Site: no runtime logging.

## 10. Formatting
Formatter: Prettier (TS/Astro), Ruff format (Python)
Linter: ESLint (TS), Ruff (Python)
Type Checking: `astro check` / `tsc --noEmit`

## 11. Writing style for content
- Short sentences. Second person ("you"). No "simply" or "obviously".
- Indian context where natural: rupees, kilometres, lakh/crore alongside million, familiar names from all regions.
- Use the Indian place-value system first, international alongside it.
- Use "×" and "÷" in early stages; "·" and "/" only after algebra is introduced.

## 12. Do
- Reuse existing patterns
- Keep changes focused
- Follow project conventions
- Remove dead code

## 13. Don't
- Create duplicate utilities
- Introduce unnecessary dependencies
- Ignore existing architecture
- Change unrelated files
- Hand-edit an `approved` topic without re-running the verifier
