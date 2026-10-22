# Review: s0-fractions-meaning

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 5 suggestions).

Checks run: `tools/verify_content.py` (35 pass, 0 fail, 3 manual warnings). I worked out every example, section claim, practice and quiz answer again with my own SymPy code, and all 26 values agree. I compared every visual's `alt`, `spec` and `checks` with the `make.py` calls and the `.meta.json` files. I also reviewed the match rules, the MCQ distractors, the manual items, the prerequisites and the wording.

Manual items confirmed:
- p-3: the bar's widths are 5,1,1,1, so the shaded part is 5/8. That is not 1/4, and the answer "false" is right.
- q-3: the bar's widths are 1,1,4, so the shaded part is 1/6. That is not 1/3, and the answer "false" is right. The explanation "smaller than a third" is also correct.
- q-2: a concept MCQ. It has exactly one correct option, and both distractors are clearly wrong.

## Findings

1. **visuals v-unequal-3, v-unequal-4 (alt) and p-3 explanation.** SUGGESTION.
   Problem: the alt texts say "parts of different sizes", and the p-3 explanation says "These parts are different sizes". In fact 2 of the 3 parts (v-unequal-3) and 3 of the 4 parts (v-unequal-4) are the same size. A child who looks closely may see that the wording does not match the picture.
   Fix: say "parts that are not all the same size" in the alt texts and in p-3's explanation.

2. **visual v-equal-unequal (spec).** SUGGESTION.
   Problem: the spec says the labels are "Equal parts" and "Not equal", but make.py draws "Equal" and "Not equal".
   Fix: change the spec, or the label in make.py, so the two agree.

3. **p-8 (MCQ options).** SUGGESTION.
   Problem: the prompt asks about "one piece of the first roti or one piece of the second", but the options are written only as $\frac{1}{3}$ and $\frac{1}{6}$. The child has to turn each piece into a fraction before choosing.
   Fix: write the options as "A piece of the first roti ($\frac{1}{3}$)" and "A piece of the second roti ($\frac{1}{6}$)".

4. **hook, sections[0].body, q-4 options[1].why_wrong.** SUGGESTION.
   Problem: these sentences are 21 to 23 words long, which is over the ~20-word guide.
   Fix: split each one into two sentences.

5. **hook and p-2 (context).** SUGGESTION.
   Problem: both roti scenes show Amma cooking. This is not wrong, but it repeats the same gender role.
   Fix: give one of them to Papa or Dadaji.
