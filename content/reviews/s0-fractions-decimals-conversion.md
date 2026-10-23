# Review: s0-fractions-decimals-conversion

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 3 suggestions).

Checks run: `tools/verify_content.py` (54 pass, 0 fail, 0 warnings). I worked out every section claim, example, practice and quiz answer again with my own SymPy code, using exact `Rational` values. All values agree: 0.4 = 2/5, 0.35 = 7/20, 0.125 = 1/8, 3/4 = 0.75, 2/5 = 0.4, 3/8 = 0.375, 3 × 0.33 = 0.99, 0.3 < 1/3 < 0.4, 0.6 < 2/3 < 0.7; examples 9/20, 0.625 and false (0.66 ≠ 2/3); p-1 to p-10: 2/5, 17/20, 2/25, 0.6, 0.25, 0.35, 0.125, 1/3, false, 2; q-1 to q-8: 3/50, 13/20, 0.36, 0.875, 0.2, false, 2/3, between 0.8 and 0.9 (5/6 = 0.8333…); doubts: 1/6 = 0.1666… and 1.5 = 3/2. Every simplest-form answer has gcd 1. I traced each long-division step (3 ÷ 8, 5 ÷ 8, 1 ÷ 8, 7 ÷ 8, 1 ÷ 3, 2 ÷ 3, 5 ÷ 6). Each remainder is right.

Recurring decimals: no question asks the child to type a recurring decimal. The only items whose answer is 1/3 or 2/3 are p-8 and q-7, which are MCQs, so the `value` rule never meets them. p-10's typed answer is the numerator 2. p-9 and q-6 are true/false. The site compares exact fractions, so 0.33 can never be accepted for 1/3 anywhere in this topic.

Match rules: every "write as a fraction in simplest form" item (p-1, p-2, p-3, q-1, q-2) ends "Type a fraction, like 3/10." and uses `simplest`. None of the answers is 3/10. A child who types the decimal (for example 0.4 on p-1) now gets "write it as a fraction", which is the right message. Fraction-to-decimal items use `decimal`. p-4 says "like 0.3" instead of "like 0.4"; I judge this right, because 0.4 is printed beside the box in fd-p4.

MCQs: p-5 (1.4, 0.14, 0.4) and q-5 (1.5, 0.5, 0.15) each match a named slip. p-8's 3/10, 33/100 and 333/1000 are all less than 1/3. q-8's options are exclusive ranges and only 0.8 to 0.9 contains 5/6; the 0.6 to 0.7 why_wrong correctly says that is where 2/3 falls.

Visuals: I rendered all four SVGs and compared them with make.py, the meta files and the alt texts. fd-quarters joins 1/4, 2/4, 3/4 to 0.25, 0.5, 0.75. fd-thirds joins only 0 and 1; the 1/3 and 2/3 marks fall between 0.3 and 0.4 and between 0.6 and 0.7. fd-p4 has the box under 3/5 between 0.4 and 0.8. fd-q8 has the dot on the fifth sixth, above a point between 0.8 and 0.9.

Prerequisites and wording: "biggest common factor" matches the approved fraction topics. Long division is by one-digit numbers only. Every sentence is 20 words or fewer. Place names are lower case in prose.

## Findings

1. **q-7: "Which of these fractions gives a decimal that never ends?" (writer flag: judged).** SUGGESTION.
   Problem: the `verify` expression is `Rational(2, 3)`, which only confirms that the marked option has the value 2/3. It does not prove that 2/3 never ends, or that the other three end. I checked this myself by the prime factors of each denominator in simplest form: 4, 5 and 8 have only 2s and 5s, and 3 does not, so the answer and every why_wrong are correct. The item is safe now, but a later edit to an option would not be caught.
   Fix: verify the property, for example a `relation` such as `And(*[set(factorint(d)) <= {2, 5} for d in (4, 5, 8)], Not(set(factorint(3)) <= {2, 5}))`, if the tool allows it. Otherwise record the reasoning in a `manual` note.

2. **Cross-topic: "1000" here, "1,000" in s0-multiply-divide-decimals.** SUGGESTION.
   Problem: section 1 and section 2's heading write "10, 100 or 1000", as approved s0-decimals-meaning does. The sibling s0-multiply-divide-decimals writes "1,000" throughout. A child moving between them sees two styles.
   Fix: agree one form across the decimal topics. The topic map uses "1,000".

3. **Context: hook and the Ajji items.** SUGGESTION.
   Problem: the hook has Tanvi's Bua buying tomatoes, and s0-multiply-divide-decimals q-8 also has a woman (Sohan's Mami) buying tomatoes. Here both grandmothers (Prakash's Ajji, Shreya's Ajji) appear in kitchen or temple roles. None is wrong, and Bhaskar's Chacha cycling balances it a little. The approved decimal topics were asked to vary similar repetition.
   Fix: give the hook to a man (for example, "Tanvi's Chacha asks for 3/4 kg of tomatoes"), or give one Ajji a different activity, such as walking to the bus stop or a market.

## Fixes applied (content-writer)

1. q-7: explanation now states a fixed reason: "The bottom is 3. 3 cannot be made into 10, 100 or 1000 by multiplying.", and notes that 4, 5 and 8 can be made into 100, 10 and 1000. The verify block stays `sympy` `Rational(2, 3)`: the tool's whitelist has no `factorint`, and a `relation` check needs a true/false answer, so it cannot be used on an MCQ. The reason in the explanation is the checkable record.
2. One thousand stays "1000" (no comma), the agreed form across the decimal topics; s0-multiply-divide-decimals was changed to match. No number here has 5 or more digits.
3. Hook: "Tanvi's Bua" is now "Tanvi's Mama" (not Chacha, which Bhaskar's item already uses). q-5: Shreya's Ajji now walks to the market, not the temple.

Also (house rules): q-1 typing example changed to "like 7/10." because the answer 3/50 shares its numerator with 3/10. No visual changed. Status set to draft.
