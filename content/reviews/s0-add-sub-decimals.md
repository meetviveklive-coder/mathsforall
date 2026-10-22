# Review: s0-add-sub-decimals

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 5 suggestions).

Checks run: `tools/verify_content.py` (42 pass, 0 fail, 0 warnings). I worked out every section claim, example, practice and quiz answer again with my own SymPy code, using exact `Rational` values. All values agree: 12.5 + 3.75 = 16.25; 7.4 − 2.65 = 4.75; 500 − 236.75 = 263.25; 4.6 + 2.75 = 7.35; 9 − 3.48 = 5.52; 48.50 + 125.75 = 174.25 and 500 − 174.25 = 325.75; 4.85; 7.7; 5.55; 4.70 = 4.7; 3.65; 5/10 ≠ 5/100; 48.25; 212.60; 60.05; 17.85; 8.55; 3.5 = 3.50; 5.35; 181.55; 95.50; 2.45; 35.50; doubts: 48 + 125 = 173 rupees, total ₹174.25. I also traced each column step (carries and borrows) in the sections, the examples and the explanations of p-9, q-4 and q-7. Each one is right.

The ₹499 + 100 paise shortcut (writer flag: judged sound). ₹500.00 = ₹499 + ₹1 = ₹499 and 100 paise, so the method is exact. For every rupee bill from ₹100 to ₹499 (236, 174, 287, 318 here), 499 − x needs no borrowing, because the tens and ones digits of 499 are 9 and its hundreds digit, 4, is at least x's. The same idea appears as "9.00 = 8 ones, 9 tenths and 10 hundredths" in example 2, p-5 and q-4, so the topic is consistent with itself. It matches s0-add-sub-large ("borrow across zeros"). See finding 1 for a wording point.

Match rules: non-money decimal answers (p-1, p-2, p-3, p-5, p-9, q-1, q-4) end "Type a decimal, like 0.4." and use `decimal`. None of these answers is 0.4. Money answers (p-7, p-8, q-5, q-6, q-8) use `value`. "212.6", "212.60" and "₹212.60" are all accepted, because `parseAnswer` strips ₹ and compares values. q-7 (box, 2.45) uses `value`, which is right.

MCQs: in p-4 the values 47/10, 407/100, 47/100 and 47 are distinct, and only 4.70 equals 4.7. In q-2, 2.79 matches lining up the last digits (64 + 215 = 279), and 85.5 has the right digits with a misplaced point. Both why_wrong texts are accurate.

Visuals: I rendered all five SVGs. ad-add-columns has the carried 1 over Ones, an empty Hundredths slot in 12.5, and 16.25. ad-wrong-line-up puts 1/3, 2/point, point/7 and 5/5 in columns, which matches section 1 and its alt text. ad-sub-zero has a boxed filled-in 0 and 4.75. ad-money-change has Rupees over 3 columns and Paise over 2, two boxed zeros and 263.25. ad-p1 has an empty answer row and an empty Hundredths slot in 3.6. Every alt text and spec matches. Every sentence is 20 words or fewer.

## Findings

1. **sections[3].body: "Now no column needs borrowing", followed by "Paise: 100 − 75 = 25".** SUGGESTION.
   Problem: the rupee columns need no borrowing, but 100 − 75 in the paise is not a column subtraction. Written in columns, it would need borrowing. The method is correct. Only the claim is loose.
   Fix: "Now the rupees need no borrowing, and 100 − 75 = 25 is easy to do in your head."

2. **sections[1].body and doubts[3]: "12.5 + 3.75 is about 12 + 4 = 16".** SUGGESTION.
   Problem: s0-comparing-decimals and s0-rounding-estimation teach that 5 rounds up, so 12.5 would round to 13 (13 + 4 = 17). A child who has learned the rule may think the guess is wrong. Rounding and estimation are also not in this topic's prerequisite chain (s0-decimals-meaning, s0-add-sub-large).
   Fix: say "12.5 + 3.75 is a bit more than 12 + 3 = 15 and less than 13 + 4 = 17. So 16.25 makes sense." Or round 12.5 to 13 and say "about 17".

3. **Money prompts p-7, p-8, q-5, q-6, q-8: "in rupees?" with no typing instruction.** SUGGESTION.
   Problem: every other numeric prompt in the three decimal topics ends "Type ...". A child who types "212.60 rupees" or "₹212.60/-" gets "unreadable".
   Fix: end each with "Type the amount, like 12.50." That example is not any of the answers.

4. **Context: relation words and roles (writer flag: judged).** SUGGESTION.
   "Mausi" (mother's sister) and "Ammamma" (mother's mother, used in Tamil and Telugu homes, which fits Kavya and Pongal) are correct and natural. The approved topics already use Nani and Dadaji in the same way, and the problem does not depend on the word. Across the decimal topics, though, every shopping trip by a woman is for food or cloth (Nani: coriander, cloth; Mausi: groceries; Ammamma: flowers and jaggery). The only man buys a school bag (Appa). Approved s0-fractions-meaning was asked to vary a similar repetition.
   Fix: give one grocery item to a man (for example, "Bhavesh's Mama buys groceries"), or give one woman a different purchase.

5. **Cross-topic: place-value names and the money sentence.** SUGGESTION.
   Problem: this topic capitalises place names in prose ("The Hundredths place of 12.5 is empty", "the Ones column", p-4's "Tenths place"), but s0-decimals-meaning and s0-comparing-decimals write "tenths place" in lower case. This topic says "100 paise make ₹1", and s0-decimals-meaning says "100 paise make 1 rupee".
   Fix: use lower case in prose (capitals only as headings in the diagrams) and one shared money sentence across the three topics.

## Fixes applied (content-writer)

1. sections[3]: "Now the rupees need no borrowing, and $100 - 75 = 25$ is easy to do in your head."
2. sections[1]: now "12.5 + 3.75 is more than 12 + 3 = 15. It is less than 13 + 4 = 17. So 16.25 makes sense." doubts[3] now says between 15 and 17. These bounds do not use rounding, so they cannot clash with "5 or more rounds up". Example 1 (5 + 3) and q-2 (6 + 2) already follow that rule.
3. p-7, p-8, q-5, q-6 and q-8 now end "Type the amount in rupees, like 45.50." and use `match: decimal`. 45.50 is not any answer.
4. Roles rebalanced. p-7: Thenmozhi buys tomatoes and beans. p-8: Bhavesh's Mausi buys a cricket bat. q-5: Joseph's Amma buys a set of tools. q-6: Kavya's Thatha buys the Pongal flowers, jaggery and turmeric. q-8: Simran saves for a storybook. The amounts are unchanged. Together with the sibling topics, women now buy vegetables, sports gear, tools, books and cloth, and men buy vegetables, cloth, tools, sports gear and stationery.
5. Place names are lower case in prose: sections[0], the p-1, p-3 and p-9 hints, the p-4 why_wrong, and the alt and spec texts of ad-add-columns, ad-sub-zero and ad-p1. The capitals stay only as diagram headings and as step labels at the start of a sentence. The money sentence is "100 paise make 1 rupee" in sections[3] and the summary. No drawing changed, so make.py was not re-run. The checks are unchanged.
`verify_content`: PASS, 47 checks passed, 0 failed, 0 warnings. Status set to draft.
