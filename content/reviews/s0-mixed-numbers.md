# Review: s0-mixed-numbers

Reviewer: math-verifier, 2026-10-22. Result: **not verified** (1 blocking, 3 suggestions). Status stays `draft`.

Checks run: `tools/verify_content.py` (39 pass, 0 fail, 0 warnings). I worked out every section claim, example, practice and quiz answer again with my own SymPy code, using quotient and remainder for each mixed form. All values agree: 7/3 = 2 1/3, 17/5 = 3 2/5, 3 3/4 = 15/4, 11/4 = 2 3/4, 9/4 = 2 1/4, 23/6 = 3 5/6, 1 2/5 = 7/5, 2 3/4 = 11/4, 7/4 = 1 3/4, 11 x 1/2 = 5 1/2, 8/5 = 1 3/5, 11/3 = 3 2/3, 3 1/2 != 4/2, 4 2/3 = 14/3, 3 2/5 = 17/5, 15 x 1/4 = 3 3/4 and 12/4 = 3.

Match rules: p-2, p-6, p-8, q-1, q-5 and q-7 ask for a mixed number and use `mixed`, with answers that have a proper fraction part. Fill-in-the-box items (p-1, p-3, p-5, q-4) use `value` with whole-number answers and say "Type the number that goes in the box". p-4 and q-3 are a problem (see finding 1).

MCQs: in p-7, 3/3, 5/3 and 6/3 are all unequal to 7/3. Each one matches its stated mistake (adding the whole to the top, adding 2 and 3, and forgetting the extra third). In q-6, only 13/4 lies strictly between 3 and 4. The other options are 3/4 < 1, 11/4 = 2 3/4 and 17/4 = 4 1/4, and their explanations are right.

Visuals: I rendered all four SVGs and read make.py and the meta files. mx-bars-7-thirds shows bars of 3, 3 and 1 shaded out of 3 each. mx-nl-thirds has all ten labels and a dot at 7/3. mx-p6 has a dot at 7/4, on the third mark after 1. mx-q5 has a dot at 11/4, on the third mark after 2. Each alt text, spec and prompt matches its drawing.

Prerequisites: the topic uses division with remainder (s0-division-meaning) and the number line (s0-fractions-number-line). It never asks for simplest form. That is right, because equivalent fractions is not a prerequisite here.

## Findings

1. **p-4 and q-3 ("Write $1\frac{2}{5}$ / $4\frac{2}{3}$ as an improper fraction").** BLOCKING.
   Problem: both use the default `value` rule. A child who just types the given number back ("1 2/5" or "4 2/3") is marked **correct**, because it has the same value. `exact` does not help either: `parseAnswer` turns "1 2/5" into 7/5, so it would pass the exact check too. So a child can be marked right without converting at all. "14/10" would also be accepted for 7/5. That matters less, but it is still not an improper fraction in the form taught.
   Fix (either one):
   (a) Rewrite both as fill-in-the-box items, like p-5 and q-4. For example, "$1\frac{2}{5} = \frac{\square}{5}$ Type the number that goes in the box." (answers 7 and 14).
   (b) Ask site-builder for a new match rule (for example `improper`) that rejects mixed-number input. Then use it here and record it in the schema.
   Option (a) needs no code change.

2. **p-9 and q-2 (true/false framing).** SUGGESTION.
   Problem: p-9 first reports Ravi's claim, which is false, and then asks a different question whose answer is true. A child may press "False" to mean "Ravi is wrong". q-2 is a bare statement ("Gurpreet says ...") with no question. Most true/false items in the approved topics end with "Is he right?".
   Fix: for p-9, ask only "Is $\frac{8}{5}$ the same number as $1\frac{3}{5}$?", or move Ravi's claim into the explanation. For q-2, add "Is Gurpreet right?".

3. **p-8 and q-7 (whole number times a unit fraction).** SUGGESTION.
   Problem: "11 bottles of $\frac{1}{2}$ litre" and "15 stretches of $\frac{1}{4}$ hour" quietly need $11 \times \frac{1}{2}$. Multiplying fractions comes later (s0-multiply-fractions). Only the first hint turns these into "counting halves" and "counting quarters".
   Fix: put the counting idea in the prompt. For example, "That is 11 half-litres. How many litres is that?" and "That is 15 quarter-hours. How many hours is that?".

4. **Cross-topic: how mixed numbers are typed.** SUGGESTION.
   Problem: this topic says "Type a mixed number, like 4 1/3." s0-add-sub-like-fractions says "Type it like 2 1/3." s0-add-sub-unlike-fractions says "Type your answer as a mixed number, like 2 1/3". The method is the same, but the instruction changes from topic to topic.
   Fix: use one wording on every site, for example "Type a mixed number, like 2 1/3." doubts[4] here already explains it well.

## Fixes applied (content-writer)

Status set to `draft`. `verify_content.py`: PASS, 41 checks, 0 fail, 0 warnings.

1. BLOCKING, p-4 and q-3: fixed with option (b), using the new `improper` rule (now in the schema and the verifier). Both use `"match": "improper"`, and each prompt ends with "Type one fraction, like 7/5." p-4's answer is 7/5, so its example is "like 9/4", which keeps the example from being the answer. Answers (7/5, 14/3) are unchanged. Added doubts[5], "How do I type an improper fraction here?" (example 9/4).
2. p-9 and q-2: applied. p-9 now asks only "Is 8/5 the same number as 1 3/5?", and Ravi's "wrong fraction" idea moved into the explanation. q-2 now ends with "Is Gurpreet right?", and its explanation starts "No.".
3. p-8 and q-7: applied. The prompts now say "That is 11 half-litres. How many litres is that?" and "That is 15 quarter-hours. How many hours is that?". p-8 hint 1 now says "11 half-litres".
4. Mixed-number wording: applied. All six `mixed` prompts (p-2, p-6, p-8, q-1, q-5, q-7) end with "Type a mixed number, like 2 1/3." None of their answers is 2 1/3. doubts[4] now uses 2 1/3 as its example.
Pronouns: p-8 (Dadaji) uses no pronoun. No diagram changed, so make.py was not re-run.

## Re-check

math-verifier, 2026-10-22. Result: **verified** (0 blocking, 1 suggestion). Status set to `verified`.

- I read `git diff 2dc6cef HEAD`. `verify_content.py`: 41 pass, 0 fail.
- Finding 1 (BLOCKING) is fixed. p-4 and q-3 use `"match": "improper"`. In `site/src/lib/answers.ts` the rule requires the trimmed input to match `^-?\d+\s*/\s*\d+$` after the value check. So "1 2/5" and "4 2/3" are now rejected (not-improper). "7/5", "14/3" and the equal "14/10" are accepted. A non-improper equal form such as "14/10" is a minor leniency and not blocking. With SymPy: 1 + 2/5 = 7/5 and 4 + 2/3 = 14/3. The typing examples (9/4 for p-4, 7/5 for q-3) do not equal their answers. 9/4 is the answer to p-2, which is a different question and in mixed form there, so that is harmless.
- `mixed` is used on all six "Type a mixed number, like 2 1/3." prompts: p-2 (2 1/4), p-6 (1 3/4), p-8 (5 1/2), q-1 (3 2/3), q-5 (2 3/4) and q-7 (3 3/4). None of the answers is 2 1/3. I re-solved each with divmod.
- p-9 ("Is 8/5 the same number as 1 3/5?", true) and q-2 ("Is Gurpreet right?", false; 3 1/2 = 7/2 ≠ 2) now have one clear reading. p-8 and q-7 now name the counting units (half-litres and quarter-hours), so no multiplying is needed.
- New doubts[5] matches the rule: one fraction, no space, no whole number.

Suggestion R1 (site-builder, not content). After a wrong form, the site says "Now write it as one fraction, like 7/5." That example is the answer to p-4, so a child who types "1 2/5" there is then shown the answer. The fix is to use a neutral example in `learn.ts`, for example "like 9/4", or to drop the example. This is not blocking, because the child has already shown the right value.
