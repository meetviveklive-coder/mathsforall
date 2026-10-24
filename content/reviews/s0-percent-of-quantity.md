# Review: s0-percent-of-quantity

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 5 suggestions).

Checks run: `tools/verify_content.py` (42 pass, 0 fail, 0 warnings). I worked out every section claim, example, practice and quiz answer again with my own exact SymPy code (`Rational`), not the files' verify expressions. All values agree: section 1 (24, 72, 12, 84; 20% of 240 = 48; 240 ÷ 20 = 12 = 5%); section 2 (3, 12, 126, 27); section 3 (90 both ways, 36 + 36 + 18; 35% of 80 = 28); section 4 (0.35 × 80 = 28); section 5 (14/40 = 35%); examples 69, 78 (and 60 + 12 + 6), 30 (gcd(48, 160) = 16); p-1 to p-10: 150, 27, ₹70, 56, 54, 12, 9, 24.50, 75, false; q-1 to q-8: 108, 13, false, 90, 9.75, 80, 20%, 25; doubts: 8% of 50 = 50% of 8 = 4, 150% of 40 = 60, 7/8 = 87.5%.

Match rules and typing: I read `site/src/lib/answers.ts`. Money answers use `decimal` with "Type the amount in rupees, like 45.50." The parser accepts 150, 150.00, ₹150, Rs 150 and "150 rupees" for p-1, and 24.5 or 24.50 for p-8, so no child is marked wrong for a correct form. Percent answers (p-9, q-6, q-8) use "Type the number only, like 40." with `value`, matching s0-percent-meaning; "75%" is accepted. No typing example equals or resembles its answer.

MCQs: p-3 (₹17.50, ₹35, ₹70, ₹330) and q-7 (12%, 20%, 25%, 80%) each have exactly one right option, and every why_wrong is accurate (350 ÷ 20 = 17.5 is 5%; ₹35 is 10%; 330 = 350 − 20; 12/48 = 25%; 48/60 = 80%). True/false items p-10 (20/30 ≠ 20/50) and q-3 (16 ≠ 4) are both false, as stated.

Prerequisites: "of means multiply" comes from s0-multiply-fractions; "multiply without the point, then place it" comes from s0-multiply-divide-decimals; percent to fraction and decimal comes from s0-percent-meaning. All approved. See finding 3 for 1 km = 1000 m.

Visuals: I re-ran make.py and rendered all five SVGs. Each bar has 10 equal parts with the stated part amount under every part (24, 36, 4, 50, 18). The shading is 3.5, 2.5, 3.5, 3 and 6 parts, and the bracket labels read 35% = 84 km, 25% = ₹90, 35% = 14 people, 30% = ?, 60% = ?. Metadata, alt text and the topic's `checks` all agree. The question marks in poq-p1 and poq-q1 do not give the answer away.

Scope and context: no exam marks, test scores or ranks. Cricket runs in example 3 are a game total, not a test score. Contexts (train journey, mela bus, flood relief, rotis made by Dada, diyas, solar panels in Sikkim) are natural and varied. Every learner-facing sentence is 20 words or fewer.

## Writer flags (judged)

- **Whole-rupee answers with "like 45.50"** (p-1, p-4, q-2). Acceptable. `decimal` accepts a whole number, and the example shows the paise form without forcing it. The same phrase is used in s0-add-sub-decimals and s0-percent-change, so it is consistent. See finding 1 for s0-ratio.
- **"Type the number of kilometres, like 15."** (p-2, p-5, q-1) and "Type the number of kilograms, like 4." (p-7). Acceptable. Answers 27, 54, 108 and 9 do not resemble the examples, and "27 km" or "9 kg" is read correctly. See finding 2.

## Findings

1. **Cross-topic: rupee typing phrase differs from s0-ratio.** SUGGESTION.
   Location: p-1, p-4, p-8, q-2, q-5 here; s0-ratio p-8 and q-6.
   Problem: this topic and s0-percent-change say "Type the amount in rupees, like 45.50." s0-ratio says "like 45.", and there the answer to q-6 is 450, which closely resembles 45.
   Fix: no change here. s0-ratio should change its example (see its review).

2. **p-2, p-5, q-1, p-7: "Type the number of kilometres/kilograms".** SUGGESTION.
   Problem: the phrase invites a child to type the word too. The parser strips "km" and "kg" but not "kilometres" or "kilograms", so "27 kilometres" comes back as unreadable (not wrong). s0-ratio q-8 asks for kilometres with "Type a whole number." instead, so the two topics differ.
   Fix: either add "kilometres?|kilograms?" to the unit list in `site/src/lib/answers.ts` (site-builder), or keep the phrase and add "You can type 15 or 15 km." Agree one phrase for km answers with s0-ratio.

3. **q-8: 1 km = 1000 m is not taught in this topic or its prerequisites.** SUGGESTION.
   Problem: it is a quiz item, and the conversion fact appears only in hint 1. A child who does not know it may write 250/1 and get stuck.
   Fix: put the fact in the prompt: "Ritwik's walk to school is 1 km, which is 1000 m."

4. **Section 4 and example 2: "places after the point".** SUGGESTION.
   Problem: s0-multiply-divide-decimals says "Count the digits after the point in both numbers together." This topic says "0.35 has two places after the point." The meaning is the same, but the word changes from "digits" to "places", and "multiply without the point" is "without the points" there.
   Fix: "0.35 has two digits after the point, and 80 has none. So the answer has two digits after the point."

5. **Section 3: "$25\% \times 360$".** SUGGESTION.
   Problem: a percent sign multiplied by a number is new notation and is not needed, because the next line writes $\frac{1}{4} \times 360$.
   Fix: "So 25% of ₹360 means $\frac{25}{100} \times 360$."

## Fixes applied (content-writer)

1. Rupee phrase agreed across topics. Whole-rupee answers (p-1, p-4, q-2) now end "Type the amount in rupees." Answers with paise (p-8 ₹24.50, q-5 ₹9.75) keep "Type the amount in rupees, like 45.50." Neither equals or resembles 45.50. s0-ratio now uses the same rule.
2. The site now strips unit words such as "kilometres" and "people". p-2, p-5 and q-1 end "Type the number of kilometres." p-7 ends "Type the number of kilograms." q-4 now ends "Type the number of people." The "like 15" and "like 4" examples are gone. s0-ratio q-8 uses the same km phrase.
3. q-8 prompt: "Ritwik's walk to school is 1 km, which is 1000 m." Hint 1 is now "Both lengths are now in metres."
4. Section 4 now says "Multiply without the points first … 0.35 has two digits after the point, and 80 has none. So the answer has two digits after the point: 28.00, which is 28." Example 2 steps, p-7 hints and explanation, p-8 and q-5 explanations use "digits after the point" and "without the points" too.
5. Section 3: "So 25% of ₹360 means $\frac{25}{100} \times 360$."

No drawing changed, so make.py was not re-run. `verify_content`: PASS, 42 checks passed, 0 failed, 0 warnings. Status set to draft.
