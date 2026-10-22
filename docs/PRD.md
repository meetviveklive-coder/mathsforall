# Product Requirements Document

## 1. Product Overview
Product Name: Ganit (working name — rename freely)
One-Line Description: A free, grade-free website that teaches mathematics concept by concept, from counting to engineering mathematics, in an Indian context.
Product Type: Free open educational website (static)
Primary Platform: Web (mobile-first, works on low-end phones and slow networks)

## 2. Problem
What problem are we solving? School maths is organised by grade, board and exam, so learners are pushed through topics on a calendar instead of when they are ready, and learning becomes a race for marks.
Why does this problem matter? Gaps in early concepts compound; a child who never understood fractions struggles with algebra years later. Ranking-driven learning replaces curiosity with anxiety.
How are users solving this today? School textbooks, coaching classes, and paid adaptive platforms (e.g. Math Academy at about $49/month in beta pricing; no Indian context, starts at 4th-grade level).

## 3. Goal
Primary Goal: A learner can start from zero and reach engineering mathematics by mastering one topic at a time, with no grades, no certificates and no comparison with others.
Secondary Goals:
- Every answer on the site is computer-verified, not just AI-reviewed.
- Free to run indefinitely (static hosting, no per-user cost).
- Content in separate files so Hindi can be added later without a rebuild.

## 4. Target Users
### User Type 1 — The Learner
Name: Learner (first user: the founder's daughter, currently around school class 5)
Description: Any age. Learns alone or with a parent.
Needs:
- Clear explanations that build on what they already know
- Practice with hints; honest feedback on what they got wrong
Pain Points:
- Pressure of marks and ranks
- Moving on before understanding

### User Type 2 — The Parent
Name: Parent
Description: Supervises progress; not necessarily strong in maths.
Needs:
- See what has been mastered and what is weak
Pain Points:
- Cannot judge what the child actually understands

## 5. User Stories
- As a learner, I want to take a placement check so that I start at my real level, not my class.
- As a learner, I want to learn one topic at a time so that I am never overwhelmed.
- As a learner, I want hints when stuck so that I can solve problems myself.
- As a learner, I want old topics to come back for review so that I do not forget them.
- As a learner, I want to test myself so that I know whether I truly understand, without being ranked.
- As a parent, I want to see a knowledge map so that I know what my child has mastered.
- As a learner, I want my progress saved on my device so that I can continue later, without making an account.

## 6. Core Features
### Feature 1 — Topic lesson
Purpose: Teach one concept.
User Flow: Open topic → read concept → step through worked examples → practice with hints → mastery quiz.
Inputs: Learner answers.
Outputs: Feedback per answer; mastery status.
Acceptance Criteria:
- Lesson renders maths correctly (KaTeX) and diagrams (SVG) on a 360px-wide screen.
- Every practice and quiz question has a hint and an explanation.
- Wrong MCQ answers show the explanation for that specific misconception.
Edge Cases:
- Learner leaves mid-quiz: progress up to the last answer is kept.
- Learner enters "0.50" for "1/2": accepted (numeric equivalence).

### Feature 2 — Mastery and progression
Purpose: Unlock topics only when prerequisites are mastered.
Acceptance Criteria:
- Topic is "mastered" at ≥ 80% on its quiz (threshold configurable).
- Failing a quiz suggests the weakest prerequisite to revisit.
- Locked topics are visible but marked, with the prerequisite named.

### Feature 3 — Placement check
Purpose: Find the learner's starting point regardless of class.
Acceptance Criteria:
- Short adaptive check that marks prerequisite chains as mastered.
- Can be skipped (start from zero).

### Feature 4 — Spaced review
Purpose: Bring mastered topics back before they are forgotten.
Acceptance Criteria:
- Review questions mixed into sessions on an expanding schedule.

### Feature 5 — Knowledge map
Purpose: Show progress as a map, not a score.
Acceptance Criteria:
- Topics coloured by state: locked, available, in progress, mastered, due for review.

### Feature 6 — Progress export/import
Purpose: Move progress between devices without accounts.
Acceptance Criteria:
- Export produces a code/file; import restores it exactly.

## 7. Non-Goals
The following are intentionally NOT part of this version:
- Accounts, logins, or any server-side storage of learner data
- Certificates, ranks, leaderboards, percentiles, timers
- Board/grade/exam mapping
- AI tutor (text, voice or avatar) — parked; see docs/ARCHITECTURE.md §9
- Hindi — later; content structure already supports it

## 8. MVP Scope
Must Have (pilot):
- 3 consecutive Stage 0 topics, end to end, verified
- Lesson, practice, quiz, local progress
Must Have (v1 launch):
- All Stage 0–1 topics, placement check, knowledge map, spaced review, export/import, "Report a mistake" link
Nice to Have:
- Optional streaks (off by default)
- Interactive visuals
Future:
- Stages 2–8, Hindi, doubt bank search, local AI tutor

## 9. Success Metrics
Measured locally or by direct observation — no tracking on the site.
Primary Metrics:
- Pilot: the first learner completes 3 topics and can explain them back in her own words
- Zero verified-wrong answers in published content
Secondary Metrics:
- Mistake reports per topic after launch
- Lighthouse performance score ≥ 90 on a mid-range phone profile

## 10. Constraints
Technical: Static site only; no backend; no third-party tracking.
Business: Free forever; hosting must fit a free tier.
Design: Calm, non-competitive; readable by a 9-year-old and an adult.
Timeline: Pilot first; scale only after pilot feedback.

## 11. Assumptions
- Learners have a browser; many on low-end Android phones.
- A parent can help with the first session.
- AI-generated content plus code verification plus human spot-check is accurate enough.

## 12. Open Questions
- Final product name and domain.
- How "Report a mistake" is received without a backend (email link vs GitHub issue vs form service).
- Mastery threshold: 80% fixed, or per-topic?

## 13. Definition of Done
The feature/product is complete when:
- [ ] Requirements are implemented
- [ ] Critical user flows work
- [ ] `tools/verify_content.py` passes on all published topics
- [ ] Build succeeds
- [ ] Security/privacy requirements are satisfied (no learner data leaves the device)
- [ ] Documentation is updated
