# Review: s0-comparing-fractions

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 4 suggestions).

Checks run: `tools/verify_content.py` (44 pass, 0 fail, 0 warnings). I worked out every section claim, example, practice and quiz answer again with my own SymPy code. That included each renaming used in the explanations: 8/12 and 9/12; 15/18 and 14/18; 16/24 and 15/24; 21/35 and 20/35; 14/20 and 15/20; 25/30 and 24/30; 15/24 and 16/24; 21/30 and 20/30; 5/10, 4/10 and 3/10; 2/8 and 4/8. All values agree. The doubts are right too: 2/4 = 3/6 = 6/12, and 3/8 < 1/2 < 4/7.

Ordering items (example 3, p-9, q-8): each verify tuple is (min, sum - min - max, max). For three distinct values the middle entry is the remaining value, so the tuple really is the ascending order. I checked each order separately with `sorted()`. In p-9 and q-8, both wrong lists differ from the sorted tuple. One orders by numerator only and the other goes largest first, and both match their why_wrong.

MCQs: in p-3 the four values are distinct and only 3/4 is the maximum. In q-3 only 1/10 is the minimum. In p-6 and q-5 the single distractor is the larger-numerator fraction, which matches the "compare numerators only" misconception. Every why_wrong is accurate.

Match rules: "Type the bigger/smaller fraction" items use `value`, which is right (an equal form such as 8/10 for 4/5 should be accepted). Box items p-4 and q-6 have whole-number answers (9 and 21).

Visuals: I rendered all six SVGs and compared them with make.py and the meta files. The bar counts and shading in cf-same-den, cf-unit, cf-twelfths, cf-p1 and cf-q2 match their alt texts and prompts. "Twice as long" (cf-unit), "a little longer" (cf-twelfths) and "longer" (cf-q2) are all true. The cf-order-nl dots are at 1/4, 1/2 and 5/8, on the 2nd, 4th and 5th marks after 0.

Prerequisites: the topic uses equivalent fractions, times tables and the < and > signs (s0-comparing-ordering). All of these are in the prerequisite chain. Every sentence is 20 words or fewer.

## Findings

1. **Cross-topic: the meaning of "common denominator" (sections[2].body, doubts[0]).** SUGGESTION.
   Problem: here a common denominator is "a shared denominator", found as a number "in both times tables". s0-add-sub-unlike-fractions defines it as "a number that both denominators divide into exactly", and it asks for the "smallest common denominator". The ideas agree, but the wording differs, and this topic never says "smallest".
   Fix: in section 2 add "so both 3 and 4 divide into it exactly", and say that 12 is the smallest one that works. Use the same definition sentence in both topics.

2. **p-6 and q-5 (two-option MCQs).** SUGGESTION.
   Problem: with only two options, a child has a 50% chance of guessing right. The hook's misconception ("we ran the same") is not offered as an option.
   Fix: add a third option, "They are the same", with why_wrong: "Both are one part short, but the parts are different sizes."

3. **doubts[2].a: "$\frac{4}{7}$ is more than half."** SUGGESTION.
   Problem: this gives no reason, but the $\frac{3}{8}$ case just before it does.
   Fix: add "because 4 + 4 = 8, which is more than 7". Avoid "3½", because mixed numbers are not a prerequisite of this topic.

4. **examples[1].problem: "the same size of bar".** SUGGESTION.
   Problem: the wording is awkward.
   Fix: write "Lalitha eats $\frac{4}{9}$ of a mango bar of the same size."
