# Review: s0-divide-fractions

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 7 suggestions).

Checks run: `tools/verify_content.py` (44 pass, 0 fail, 0 warnings). I worked out every section claim, example, practice and quiz answer again with my own SymPy code. That covered the hook (3 ÷ 1/2 = 6), section 2 (four hops reach 8/3, the 1/3 left over is half a hop, 9/2), section 3 (3/4 ÷ 2/5 = 15/8), section 4 (1/6) and section 5 (6 ÷ 1/2 = 12). It also covered every intermediate step (24/12, 3/12, 15/12, 2/12, 48/3, 36/6, 28/8). All values agree.

Match rules: q-3 asks for a mixed number and uses `mixed` with answer 3 1/2. p-5, p-7 and q-6 ask for simplest form and use `simplest` with lowest-terms answers (5/4, 1/6, 1/8). Whole-number and box questions (p-1, p-4, p-8, q-1, q-4, q-7) use `value`, which is right. p-2 uses `value`, so 1 1/2, 3/2 and 6/4 are all accepted, as its prompt promises. The site's `checkNumeric` behaves this way.

MCQ distractors:
- p-6: 15/8 flips the first fraction, 3/10 flips nothing, and 10/3 flips both. Each is wrong and matches its why_wrong.
- q-2: "one third of 5" (5/3) and "how many 5s fit into 1/3" (1/15) are both different from 15.
- q-8: 8 ÷ 2 = 4, 8 ÷ 1 = 8 and 8 × 1/2 = 4 are none of them bigger than 8. Only 8 ÷ 1/2 = 16 is.

True/false: p-9 (12 < 6 is false) and q-5 (2/3 ÷ 4/9 = 3/2 is true) are correct.

Visuals: I read make.py and every .meta.json, and rendered all six SVGs in light and dark mode. The hop counts, part-hop sizes, labels and dot positions match the alt text, the specs and the sections or questions that use them. dv-hops-3-twothirds shows 4 full hops to 2 2/3 plus a dashed half-height hop to 3. dv-hops-34-half shows 1 full hop to 2/4 and a dashed half hop to the dot at 3/4. dv-p1 shows 8 hops and dv-q1 shows 3 hops. Both modes have good contrast, and the dashed part-hops are still visible next to the dot.

Prerequisites: the lesson uses improper fractions and mixed numbers (from s0-mixed-numbers), "of means multiply" and the multiplication rule (from s0-multiply-fractions), and simplifying (from s0-equivalent-fractions). All of these are in the prerequisite chain. The one exception is finding 2 below.

## Findings

1. **p-2 prompt.** SUGGESTION.
   Problem: the prompt says "You can type a mixed number like 1 1/2 or a fraction like 3/2." Those examples are the answer itself, so the question gives the answer away.
   Fix: use examples that are not the answer, for example "like 2 1/3 or a fraction like 7/3".

2. **doubts[3].a: "Yes, if they have a common denominator."** SUGGESTION.
   Problem: the phrase "common denominator" is taught in s0-add-sub-unlike-fractions (and used in s0-comparing-fractions). Neither topic is a prerequisite of this one. The example only needs fractions with the same denominator.
   Fix: write "Yes, if they have the same denominator."

3. **lesson.summary[2]: "Sharing a fraction among n people ... multiplying by 1/n."** SUGGESTION.
   Problem: the letter n is algebra, which a 10-year-old has not met. The sentence is also 18 words long.
   Fix: use a number, for example "Sharing a fraction among 3 people means dividing by 3. That is the same as multiplying by 1/3."

4. **doubts[4].a: "no number of empty hops ever reaches anywhere".** SUGGESTION.
   Problem: an "empty hop" is not defined. The link from "you cannot divide by 0" to "0 has no reciprocal" is also left unsaid.
   Fix: "Flipping $\frac{0}{1}$ gives $\frac{1}{0}$, which means 1 ÷ 0. A hop of size 0 never moves you forward, so it can never fit into 1. So 0 has no reciprocal."

5. **sections[3] and visual dv-share-half.** SUGGESTION.
   Problem: the section says "The bars show that the half splits into 3 pieces". The bottom bar shades only 1 sixth, and nothing marks the 3 sixths that sit under the shaded half. The alt text ("Three sixths fit exactly under the shaded half") is true of the geometry, but a child has to work out the alignment on their own.
   Fix (visuals): tint or bracket the first 3 sixths of the bottom bar lightly, and keep the first sixth dark. Then the drawing shows "half = 3 pieces, each 1/6".

6. **sections[2].body: "That gives 9 ÷ 2 = 4 1/2 hops. This is the same as 3 × 3/2."** SUGGESTION.
   Problem: the step from 9 ÷ 2 to 3 × 3/2 is not shown, and it is the key link to the reciprocal rule.
   Fix: add one sentence: "$3 \times \frac{3}{2} = \frac{9}{2}$, which is also $9 \div 2$."

7. **visuals[1].spec, visuals[2].spec.** SUGGESTION.
   Problem: these sentences are 21 and 19 words long. They are not shown to learners.
   Fix: optional; you could split each one into two sentences.

## Consistency with s0-multiply-fractions (prerequisite; read only, not edited)

- Both topics type mixed numbers the same way: "2 1/3", with the `mixed` rule (q-3 here, p-9 there). Both use "simplest form" with `simplest`. The bigger/smaller wording matches: "multiplying by a fraction less than 1 gives a smaller answer" there, and "dividing by a number less than 1 gives a bigger answer" here. q-8's option 8 × 1/2 uses that rule correctly.
- The multiply topic's doubts[1] also says "common denominator" before that idea is taught, the same problem as finding 2. If the term is changed, change it in both topics.
- I noticed a separate problem in s0-multiply-fractions p-8 that is for that topic's verifier: "Dadaji makes 3 pots of kheer ... How many litres of milk does she need?" Dadaji is a grandfather, so "she" does not match. This topic is not affected.

## Fixes applied (content-writer)

Status set to `draft`. `verify_content.py`: PASS, 44 checks, 0 fail, 0 warnings.

1. p-2: applied. The examples are now "like 2 1/3 or a fraction like 7/3". `value` is kept, so 1 1/2, 3/2 and 6/4 are all still accepted.
2. doubts[3]: applied ("if they have the same denominator"). The matching change in s0-multiply-fractions doubts[1] was made too.
3. summary[2]: applied ("Sharing a fraction among 3 people means dividing by 3. That is the same as multiplying by 1/3.").
4. doubts[4]: applied as suggested.
5. dv-share-half: applied in the drawing. make.py now has a small `tinted_bars` helper, built on draw.bars. The bottom bar shows sixth 1 dark and sixths 2 and 3 lightly shaded (fill-opacity 0.32, the same as the multiply area models). The meta is read back from the final SVG and now has `tinted`. make.py was re-run. The spec, alt and checks now describe 1 dark and 2 light under the shaded half (checks: shaded 1, tinted 2). sections[3] now says the 3 coloured sixths sit under the half, with each piece (1/6) shown dark.
6. sections[2]: applied. Added "3 x 3/2 = 9/2, which is also 9 ÷ 2."
7. visuals[1] and [2] specs: applied. Each is split into shorter sentences.
House conventions: q-3 ends with "Type a mixed number, like 2 1/3." (answer 3 1/2). "Type a whole number." stays on the count questions p-1, p-8, q-1 and q-7. Nani (hook) is "she".

## Re-check

math-verifier, 2026-10-22. Result: **verified** (0 blocking, 0 new findings). Status set to `verified`.

- I read `git diff 2dc6cef HEAD`. All 7 findings are fixed. `verify_content.py`: 44 pass, 0 fail.
- dv-share-half: I rendered the SVG and read it. The top shaded half covers x = 72 to 186. In the bottom bar, the dark sixth is at 72 to 110 and the two light sixths (opacity 0.32) are at 110 to 186. The other 3 sixths are white. The 3 coloured sixths sit exactly under the shaded half. The meta (shaded 1/tinted 0 and shaded 1/tinted 2) matches the drawing, the checks, the spec and the alt. The `tinted_bars` helper reads the meta back from the final SVG, not from its inputs. sections[3] text matches the drawing.
- I re-solved with SymPy: 3 × 3/2 = 9/2 = 9 ÷ 2. Also 1/2 ÷ 3 = 1/6, 6/8 ÷ 3/8 = 2 and q-3: 7/8 ÷ 1/4 = 7/2 = 3 1/2 (`mixed`).
- p-2: the examples (2 1/3 and 7/3) no longer equal the answer, 3/2. It uses `value`, which is right because the prompt allows either form. The scan flagged the words "mixed number" here, but the prompt does not ask for one, so `mixed` would be wrong.
- doubts[3] now says "same denominator", so there is no term from outside the prerequisites. doubts[4] is clear. summary[2] has no algebra.
