# Review: s0-multiply-fractions

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 5 suggestions).

Checks run: `tools/verify_content.py` (42 pass, 0 fail, 0 warnings). I worked out every example, section claim, practice and quiz answer again with my own SymPy code, and all 23 values agree. That covers 3/4 of 12 = 9, 3/4 of 160 = 120, 2/3 × 3/4 = 1/2, 9/4 × 4/3 = 3, 7/3 × 3/2 = 3 1/2, 5/4 × 12/5 = 3 and (5/2)² = 6 1/4. I compared every visual's `alt`, `spec` and `checks` with the `area_model` helper in `make.py`, the `.meta.json` files and a rendering:
- mf-area-hook: 6 cells, 1 dark, 3 light.
- mf-area-ex: 12 cells, a dark block of 6 that is 2 wide and 3 tall, 5 light.
- mf-p3: 10 cells, 3 dark.
- mf-q2: 20 cells, 2 dark.
- mf-dots-12: 4 groups of 3, with 1 solid outline.
- mf-p1: 3 groups of 4, with 2 solid outlines.

The labels sit over the shaded columns and beside the shaded rows, as the alt texts say. Every question that uses a diagram agrees with it.

Match rules: p-5, q-2, q-3 and q-7 ask for simplest form and use `simplest`. p-9 asks for a mixed number and uses `mixed`. p-3 ("what fraction is dark?") correctly uses `value`, so 3/10 is accepted. The whole-number answers use `value`.

MCQ distractors:
- p-7: 2 1/4 (parts multiplied separately), 4 (the sum), 7 1/2 (15 over the kept denominator 2).
- q-6: 4 1/4 (Rahul's method), 5 (the sum), 4 (wholes only).
Each one is wrong and matches its stated mistake. In each question only one option is correct.

The true/false items p-6 (1/2 × 6 = 3, not more than 6) and q-4 (15 < 20) are right. Prerequisites: "of" and the area model are taught here. Simplest form and improper fractions come from prerequisites. No sentence is over 20 words.

## Findings

1. **p-8 prompt: "Dadaji ... How many litres of milk does she need?"** SUGGESTION.
   Problem: Dadaji is a grandfather, but the prompt and the explanation ("She needs 4 litres") say "she". A child may stop to wonder who is meant. The maths is not affected.
   Fix: use "he" in both places, or change the name to Dadi.

2. **Example 3, step 4 (estimate).** SUGGESTION.
   Problem: "expect a bit more than 2. An answer of 3 fits." This estimate cannot catch the mistake that section 5 warns about. Multiplying the parts separately gives $2 \times 1 + \frac{1}{4} \times \frac{1}{3} = 2\frac{1}{12}$, which is also "a bit more than 2".
   Fix: "$2\frac{1}{4} \times 1\frac{1}{3}$ is more than $2 \times 1\frac{1}{3} = 2\frac{2}{3}$. So expect more than $2\frac{2}{3}$. An answer of 3 fits."

3. **lesson.hook: "No, much less."** SUGGESTION.
   Problem: Ishaan ate $\frac{1}{6}$, which is exactly half of $\frac{1}{3}$. "Much less" overstates it a little.
   Fix: "No, less than that. He ate half as much."

4. **p-8 and q-5: "Type a whole number."** SUGGESTION.
   Problem: in a mixed-number question, this tells the child that the answer comes out whole, which weakens the check. The `value` rule would accept 12/3 or 60/20 anyway.
   Fix: optional. Drop the phrase, or use "Simplify your answer."

5. **Cross-topic wording (with s0-add-sub-unlike-fractions, s0-mixed-numbers, s0-add-sub-like-fractions).** SUGGESTION.
   Problem: p-9 says "Write the answer as a mixed number, for example 2 1/3." The sibling topics say "Type your answer as a mixed number, like 2 1/3", "Type a mixed number, like 4 1/3" and "Type it like 2 1/3". The format they ask for is the same; only the wording differs. Also, this topic says "Write the answer in simplest form", while s0-add-sub-unlike-fractions says "Give your answer in simplest form".
   Fix: use one phrase for each instruction across the Fractions unit.

## Fixes applied (content-writer)

Status set to `draft`. `verify_content.py`: PASS, 42 checks, 0 fail, 0 warnings.

1. p-8 pronoun: applied. Dadaji is now "he" in the prompt and the explanation.
2. Example 3, step 4: applied as suggested (more than 2 x 1 1/3 = 2 2/3, so 3 fits).
3. Hook: applied ("No, less than that. He ate half as much.").
4. "Type a whole number.": dropped from p-8 and q-5, as suggested. I also dropped it from q-1 (a distance, 25 km), where it gave a hint the question did not need. It stays on p-1 (count of diyas) and p-2 (rupees), where a child might otherwise type a fraction.
5. Wording: applied. p-9 now ends with "Type a mixed number, like 4 1/5." I used 4 1/5 rather than 2 1/3 because 2 1/3 appears in the question itself. Every simplest-form instruction (examples[1], p-5, q-2, q-3, q-7) now reads "Give your answer in simplest form."
House convention 4: doubts[1] no longer says "common denominator". It now asks "Do the denominators need to match before I multiply?" (raised in the divide review). No diagram changed, so make.py was not re-run.

## Re-check

math-verifier, 2026-10-22. Result: **verified** (0 blocking, 0 new findings). Status set to `verified`.

- I read `git diff 2dc6cef HEAD`. All 5 findings are fixed. `verify_content.py`: 42 pass, 0 fail.
- Example 3: 2 × 4/3 = 8/3 = 2 2/3 < 3 = 9/4 × 4/3. The new estimate is true, and it now catches the 2 1/12 mistake. The hook is right: 1/3 of 1/2 = 1/6, which is half of 1/3.
- p-8 (4/3 × 3 = 4), q-5 (5/4 × 12/5 = 3) and q-1 (5/8 of 40 = 25) still use `value`. Dropping "Type a whole number." does not change grading.
- p-9: 7/3 × 3/2 = 7/2 = 3 1/2, with `mixed`. The example 4 1/5 is not the answer and is not in the question. It differs from the house example 2 1/3 for a good reason: 2 1/3 is a factor in the question. The sentence itself is the shared wording.
- All the "simplest form" prompts (p-5, q-2, q-3, q-7) read "Give your answer in simplest form." and use `simplest`. doubts[1] no longer uses "common denominator".
