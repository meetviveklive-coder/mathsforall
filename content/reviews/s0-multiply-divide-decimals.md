# Review: s0-multiply-divide-decimals

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 4 suggestions).

Checks run: `tools/verify_content.py` (52 pass, 0 fail, 0 warnings). I worked out every section claim, example, practice and quiz answer again with my own SymPy code, using exact `Rational` values parsed from the decimal strings. All values agree: 3.45 × 10 = 34.5, × 100 = 345, × 1,000 = 3,450; 45.6 ÷ 10 = 4.56, ÷ 100 = 0.456; 7 ÷ 100 = 0.07; 102.50 × 10 = 1,025; 0.4 × 3 = 1.2; 0.3 × 0.4 = 0.12; 2.5 × 1.5 = 3.75 (25 × 15 = 375); 4.5 ÷ 3 = 1.5; 1.2 ÷ 0.3 = 4; examples 4,675, 0.06 and 8; p-1 to p-10: 58.2, 60, 0.235, 3.50, 0.14, 54, 0.008, false (1.2 × 3.4 = 4.08, not 40.8), 1.8, 9; q-1 to q-8: 1,000, 0.085, 45, 3.6, 0.06, 220, 2.4, 45; doubts: 120 ÷ 30 = 4 and 7 ÷ 4 = 1.75. I also traced each long-division step (remainders carried as tenths and hundredths) in section 5, p-9, q-7 and doubts[3]. Each is right. The rough-check bounds (2 to 6, 3 to 8, ₹160 to ₹240) use no rounding.

Match rules: every non-money decimal answer ends "Type a decimal, like 0.4." and uses `decimal`; none of these answers is 0.4. Money answers (p-4, p-6, q-6, q-8) end "Type the amount in rupees, like 45.50." and use `decimal`, the same as s0-add-sub-decimals. "3.5", "3.50" and "₹3.50" are all accepted for p-4, and "54" and "220" are accepted as whole numbers. p-10 ("Type a whole number.") and q-1 (box, 1000; "1,000" also parses) use `value`, which is right.

MCQs: p-2 (0.600, 6, 0.006), q-3 (4.50, 40.5, 0.45) and q-5 (0.6, 6, 0.5) each have exactly one option of the right value, and every why_wrong names the right slip (zero added on the end, one place instead of two, moved the wrong way, only the 4 multiplied, points left out, adding instead of multiplying). p-8 is clear: the question is about 40.8, so "false" is the only answer.

Visuals: I rendered all five SVGs and compared them with make.py, the meta files and the alt texts. md-x10 has 3.45 over 34.5 with three arrows one column left. md-div100 has 7 in the ones column, one arrow to the hundredths column, and two dashed filled-in zeros. md-grid has 3 light columns, 4 light rows and a 3 by 4 dark block (12; light 46). md-p5 has a 7 by 2 dark block (14; light 62). md-hops has 12 tenth ticks and four numbered hops ending at 1.2. Place names are capitalised only as diagram headings, and lower case in all prose.

Prerequisites and wording: long division is by one-digit numbers only (3, 4, 5, 6). Every sentence is 20 words or fewer. Contexts (Anil's Amma riding to work, Papa sewing cushion covers, Farida's Nana making bags, Tenzin buying curtain cloth) are natural and varied.

## Findings

1. **q-6, and the products in sections[3], p-6, p-8 and q-4.** SUGGESTION.
   Problem: two-digit multiplication has no page yet, and the shortcut needs 25 × 15, 36 × 15, 12 × 34 and 15 × 24. These are fair for a 10-year-old. But q-6 asks for 80 × 275 = 22,000, a three-digit product, inside a quiz. A child who understands the decimal step may still slip on the whole-number work.
   Fix: make q-6 "2.5 m of cloth" (80 × 25 = 2,000, so ₹200; check: between ₹160 and ₹240). Or keep 2.75 m and add a hint: "80 × 275 is 8 × 275 with a 0 on the end."

2. **sections[2]: "Write each decimal as a fraction. Then multiply the numerators and multiply the denominators" (writer flag: judged).** SUGGESTION.
   Judgement: sound. s0-multiply-fractions is approved and the rule is re-stated in one line. The grid gives its own reason (12 of 100 squares), so a child who has not met fraction multiplication can still follow. However, s0-multiply-fractions is not in this topic's prerequisite chain (s0-add-sub-decimals, s0-long-division), so the topic can unlock without it.
   Fix: either add s0-multiply-fractions to this topic's prerequisites in the topic map, or put the grid reason first ("12 small squares out of 100") and the fraction line second, as a check.

3. **q-8: ₹22.50 for 0.5 kg, price for 1 kg (writer flag: judged).** SUGGESTION.
   Judgement: the maths and the method are sound. 22.50 ÷ 0.5 = 225 ÷ 5 = 45, and the explanation checks it with "half of ₹45 is ₹22.50". Two small points. (a) The hint gives only the division route. Many children will see faster that 0.5 kg is half a kg, so 1 kg costs double. (b) The answer, 45, sits right next to the typing example "like 45.50". It cannot mark a child wrongly (45.50 ≠ 45), but it can make a child doubt a correct answer.
   Fix: add a hint "0.5 kg is half a kg. How much would 2 halves cost?" and change the price, for example ₹24.50 for 0.5 kg (answer 49).

4. **Cross-topic: "1,000" and the paise sentence.** SUGGESTION.
   Problem: this topic writes "1,000" (title of section 2, the summary, $1{,}000$). s0-fractions-decimals-conversion ("10, 100 or 1000") and approved s0-decimals-meaning ("1000") write it without a comma. Also, section 2 says "₹7 shared by 100 children is 7 paise each", and doubts[2] thinks "in paise", but neither gives the shared sentence "100 paise make 1 rupee" used in s0-decimals-meaning and s0-add-sub-decimals.
   Fix: agree one form of one thousand across the decimal topics (the topic map uses "1,000"). In section 2, add "100 paise make 1 rupee, so ₹7 is 700 paise." before the sharing sentence.

## Fixes applied (content-writer)

1. q-6: changed to 2.5 m of cloth. Answer 200 (80 × 25 = 2000, one place from the right). Hint and explanation updated; rough check ₹160 to ₹240 kept. verify `80 * Rational(25, 10)`.
2. sections[2]: s0-multiply-fractions is now a prerequisite in the topic map. Kept the one-line rule, now phrased as "the rule you met for multiplying fractions". The grid reason stays right after it.
3. q-8: now ₹24.50 for 0.5 kg, answer 49. First hint is "0.5 kg is half a kg. How much would 2 halves cost?"; the division route is the second hint. Explanation gives both routes. verify `Rational(2450, 100) / Rational(5, 10)`.
4. One thousand is written 1000 everywhere (section 2 heading and body, summary, q-1, q-2); four-digit values 3450, 1025, 4675 and 4700 have no comma. Section 2 now says "100 paise make 1 rupee, so ₹7 is 700 paise." doubts[2] also uses the shared sentence.

Also (house rules): money typing example changed from "like 45.50" to "like 12.75" (45.50 shares the digits 4 and 5 with the answer 54). Decimal typing example changed to "like 0.7" in p-5 (answer 0.14), p-7 (prompt contains 0.4) and q-7 (answer 2.4). No visual depends on the changed items; make.py not re-run. Status set to draft.

## Re-check

Reviewer: math-verifier, 2026-10-23. Result: **verified** (0 blocking, 1 suggestion).

Checks run: `tools/verify_content.py` (52 pass, 0 fail). Read `git diff 72fdf28 HEAD` for this topic. Re-solved each changed item with my own exact `Rational` code.

- Finding 1 fixed. q-6: 80 × 2.5 = 200 (80 × 25 = 2000, one place from the right gives 200.0). The rough check (₹160 to ₹240) still holds. Hints and explanation agree.
- Finding 2 fixed. The topic map now lists s0-multiply-fractions as a prerequisite. Section 3 names the fraction rule, then the grid reason follows.
- Finding 3 fixed. q-8: 24.50 ÷ 0.5 = 49 = 2 × 24.50 = 245 ÷ 5. The halving hint comes first.
- Finding 4 fixed. One thousand is "1000" everywhere a child sees it (3450, 1025, 4675, 4700 checked). "100 paise make 1 rupee" is in section 2 and doubts[2] (120 ÷ 30 = 4).
- No visual or alt text changed, and no changed item refers to a diagram. Section 2 still matches md-div100 (7 ÷ 100 = 0.07).
- Typing examples: money "like 12.75" (answers 3.50, 54, 200, 49); decimals "like 0.4" or "like 0.7". None equals or closely resembles its answer. Every decimal and money answer uses `decimal`, which compares exact values, so no rounded value can pass.

New finding:

1. **p-5: "The grid shows $0.7 \times 0.2$ ... Type a decimal, like 0.7."** SUGGESTION.
   Problem: the new typing example repeats a number in the prompt. A child may wonder whether 0.7 is a clue. It is not the answer (0.14), so it cannot mark anyone wrongly.
   Fix: use "like 0.5" in p-5.
