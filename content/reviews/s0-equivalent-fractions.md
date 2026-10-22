# Review: s0-equivalent-fractions

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 4 suggestions).

Checks run: `tools/verify_content.py` (33 pass, 0 fail, 1 manual warning). I worked out every example, practice and quiz answer again with my own SymPy code. That covered the products, the GCDs, the factor lists in example 2, and every simplest form (6/8, 15/25, 4/12, 8/12 and 18/24 all reduce as stated). All values agree.

Match rules: every "simplest form" question uses `simplest` with an answer in lowest terms. Fill-in-the-box questions use `value` with a whole-number answer, which is correct.

Manual item q-3: of 3/6, 5/10, 4/6 and 50/100, only 4/6 is not equal to 1/2. That gives exactly one correct option, and each distractor's explanation is accurate.

p-7 distractors: 4/5 (add 1 to top and bottom), 3/8 (multiply the bottom only) and 6/4 (multiply the top only) are all unequal to 3/4, and each one matches its stated mistake.

Visuals: the eq-nl and eq-q4 metadata place both dots at the same value (1/2 and 2/3). The eq-half-bars and eq-p1 bar counts match their alt texts.

## Findings

1. **visual eq-q4 (alt).** SUGGESTION.
   Problem: the alt says "a dot on the second mark" and "a dot on the fourth mark" without "after 0". A screen-reader user who counts the mark at 0 would get 1/3 and 3/6, which do not line up. The other number-line topics always say "after 0". The alt also does not mention the dashed guide line that the drawing includes.
   Fix: write "the second mark after 0" and "the fourth mark after 0", and add "A dashed line joins the two dots."

2. **p-1, p-2, p-3, q-1, q-7 (fill in the box).** SUGGESTION.
   Problem: a child may type the whole fraction (for example "2/6") instead of only the missing number. That is marked plain "wrong", because 2/6 is not equal to 2.
   Fix: add "Type the number that goes in the box." to each prompt.

3. **doubts[2].a: "Infinitely many!"** SUGGESTION.
   Problem: "infinitely" is not a word a 10-year-old is likely to know.
   Fix: write "So many that they never run out!"

4. **visuals[0].spec.** SUGGESTION.
   Problem: this sentence is 22 words long. It is not shown to learners.
   Fix: optional; you could split it into two sentences.
