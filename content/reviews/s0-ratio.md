# Review: s0-ratio

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 5 suggestions).

Checks run: `tools/verify_content.py` (47 pass, 0 fail, 0 warnings). I worked out every section claim, example, practice and quiz answer again with my own exact SymPy code. All values agree: 24 : 16 = 3 : 2 (gcd 8); 4 : 3 ≠ 2 : 1 and 2 : 1 = 4 : 2; ₹500 in 3 : 2 is ₹300 and ₹200; examples 18 : 12 = 3 : 2 (gcd 6), 3 cups, 36 runs; p-1 to p-10: 7 : 4, 3, 3, 2, 6 : 3, 3/7, 8, 90, 9, true; q-1 to q-8: 5 : 9, 1/5, 4, 3, false (5/3 < 2 < 3), 450, 6, 120; doubts: ₹100 in 4 : 6 and in 2 : 3 both give ₹40 and ₹60; 1000 : 500 = 2 : 1.

Typed ratios: no question asks the child to type a ratio. Simplifying items (p-3, p-4, q-3, q-4) and p-2 use a box with "Type the number that goes in the box.", like s0-equivalent-fractions. Example 1 asks to "write" a ratio, but examples are not typed.

MCQ ratio options (verified as a/b): p-1 {7/4, 4/7, 7/11, 4/11}, p-5 {2, 3/2, 4, 1/2} and q-1 {9/5, 5/9, 5/14} contain no two equal ratios. Each has exactly one option equal to the right value, and both orders of the pair are offered as separate, unequal values, so order is tested correctly. p-6, q-2 and q-7 have distinct values with one right option. Every why_wrong matches its stated mistake (wrong order, comparing with the total, adding instead of multiplying, 2/3 instead of 2/5).

Prerequisites: "biggest common factor", "no common factor except 1" and "simplest form" are worded exactly as in s0-equivalent-fractions. Fractions of a whole come from s0-fractions-meaning. Nothing else is assumed. Doubt 5 states 1 kg = 1000 g itself.

Visuals: I re-ran make.py and rendered all six SVGs. Block counts and labels match the metadata, the alt texts and the questions: rice 2 / dal 1; yellow 2 + red 3 = 5; Asha 3 × ₹100 / Tenzing 2 × ₹100 = ₹500; red 4 / white 3 (p-2 answer 3); blue 3 + white 4 = 7 (p-6 answer 3/7); Ishita 2 / Kunal 1 with "3 equal parts make 12 laddoos" (p-7 answer 8). All blocks are the same size.

Scope and context: no exam marks, test scores or ranks. "Scored" appears only for cricket runs (section 3, example 3, q-4), which are game totals, not test scores. Khichdi, idli batter, rangoli, laddoos and tulsi are natural. Every learner-facing sentence is 20 words or fewer.

## Writer flag (judged)

- **Example 1 verified as a relation.** Acceptable. The answer is a ratio, which `sympy` cannot store as a number, and examples are not typed. `And(Eq(gcd(18, 12), 6), Eq(18/12, 3/2), Eq(gcd(3, 2), 1))` checks the factor, the value and that 3 : 2 is simplest. Because 12/18 ≠ 3/2, it also fixes the red-first order. The site does not show an example's `answer` field, so "true" is never shown. The same pattern is in the approved s0-equivalent-fractions.

## Findings

1. **q-6: "Type the amount in rupees, like 45." when the answer is 450.** SUGGESTION.
   Problem: the typing example closely resembles the answer (45 and 450). p-8 (answer 90) uses the same phrase. s0-percent-of-quantity and s0-percent-change use "like 45.50" for every rupee answer.
   Fix: use "Type the amount in rupees, like 45.50." in p-8 and q-6. The answers are whole numbers and `value` accepts them.

2. **q-8: "They go by bus and then by train, in the ratio 1 : 4."** SUGGESTION.
   Problem: it does not say what is in that ratio (distance or time). Only distance gives an answer, but a careful child may pause.
   Fix: "Rehana's family travels 150 km to Kochi. They go part of the way by bus and the rest by train. The bus distance and the train distance are in the ratio 1 : 4."

3. **Cross-topic: km answer phrasing.** SUGGESTION.
   Problem: q-8 asks for kilometres with "Type a whole number." s0-percent-of-quantity asks for kilometres with "Type the number of kilometres, like 15."
   Fix: agree one phrase for both. "Type the number of kilometres, like 15." is clear, and 15 does not resemble 120.

4. **p-6 and q-2: objective tag.** SUGGESTION.
   Problem: both ask what fraction of the whole one part is. They are tagged objective 0 ("Write a ratio to compare two quantities"), but they test the misconception "2 : 3 is 2/3 of the whole". This is reasonable, but the quiz then has no item that asks for the parts-of-the-whole idea under the sharing objective, where it is used.
   Fix: optional. Leave as is, or tag q-2 as objective 2, since sharing uses "add the parts".

5. **Cricket appears four times** (p-1, section 3, example 3, q-4). SUGGESTION.
   Problem: comparing two named children's runs in section 3 and q-4 is close to ranking one child against another, which the site avoids. s0-percent-of-quantity also uses cricket in example 3.
   Fix: change section 3 or q-4 to a non-competitive context, for example "Farida's family grows 24 kg of potatoes and 16 kg of onions."

## Fixes applied (content-writer)

1. p-8 (₹90) and q-6 (₹450) now end "Type the amount in rupees." Both answers are whole rupees. Under the rule agreed across the three topics, "like 45.50" is only for answers that may have paise. "like 45" is gone.
2. q-8 prompt: "Rehana's family travels 150 km to Kochi. They go part of the way by bus and the rest by train. The bus distance and the train distance are in the ratio $1 : 4$."
3. q-8 now ends "Type the number of kilometres.", the same as s0-percent-of-quantity. The site accepts "120" or "120 km".
4. q-2 is now tagged objective 2 (sharing uses "add the parts"). p-6 stays on objective 0.
5. Section 3 now uses "Farida's family grows 24 kg of potatoes and 16 kg of onions" ($24 : 16 = 3 : 2$, "For every 3 kg of potatoes, they grow 2 kg of onions"). q-4 now uses a shop in Ludhiana that sells 45 kg of rice and 30 kg of wheat. The answer (3) and the verify expression are unchanged. Cricket remains in p-1 (one player's sixes and fours) and example 3 (two batters' shared total), which do not rank one child against another.

No drawing changed, so make.py was not re-run. `verify_content`: PASS, 47 checks passed, 0 failed, 0 warnings. Status set to draft.
