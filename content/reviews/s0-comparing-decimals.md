# Review: s0-comparing-decimals

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 5 suggestions).

Checks run: `tools/verify_content.py` (49 pass, 0 fail, 0 warnings). I worked out every section claim, example, practice and quiz answer again with my own SymPy code. Every rounding answer was re-solved exactly as `floor(x * 10^k + 1/2) / 10^k` on `Rational` values, not floats. All values agree: 2.4 > 2.35; 0.3 > 0.25; 0.405 < 0.45 < 0.5 < 0.6; 3.67 → 3.7; ₹48.60 → ₹49; 5.384 → 5.38; 0.7 > 0.65; heaviest 1.5 kg (order 1.05, 1.25, 1.5); 12.46 → 12.5; 0.8; 0.6; 0.125 < 0.5; 4.28; 3.09 < 3.1; 7.3 → 7; 2.648 → 2.6; ₹86.75 → ₹87; max 0.6; 4.50 = 4.5; middle weight 1.2; 6.53; halfway 0.35; ₹64.50 → ₹65 (half rounds up, as in s0-rounding-estimation); 3.749 → 3.7, and stepwise rounding gives 3.8, which is the q-7 distractor; 9.96 → 10.0.

Ordering MCQ p-4 (writer flag: judged sound). Each option's value is `And(Lt(a, b), Lt(b, c))`, where a, b, c are the three numbers in the order the option lists them. That is true exactly when the list is strictly increasing, so it proves the stated order. The correct option evaluates to True and both wrong options to False. `verify.expr` is `true`, so the verifier finds exactly one matching option. I checked the order separately with `sorted()`: 0.09, 0.62, 0.7. The three options are permutations of the same three numbers. Both why_wrong texts match their lists ("7, 9, 62" as whole numbers; 0.09 read as 0.9).

q-3's verify takes the median of three values as the minimum of the pairwise maxima. That is correct for three values, and it gives 1.2.

Match rules: decimal-answer prompts (p-2, p-5, p-8, q-3, q-4) end "Type a decimal, like 0.4." and use `decimal`. None of these answers is 0.4. Whole-rupee and whole-metre rounding (p-7, p-9, q-6) and "Type the bigger number" (p-1) use `value`, which is right.

MCQs: q-1 has four distinct values, and only 0.6 is the largest. q-5: only 0.35 = (0.3 + 0.4)/2. q-7: 3.8, 3.75 and 4 are each wrong for the reason given.

Visuals: I rendered all seven SVGs. cd-jump and cd-longer have 10 hundredth-steps per tenth, with dots at 2.35 / 2.4 and 0.25 / 0.3 and labels above. cd-zoom has a dot on the 7th mark. cd-round has 3.65 labelled at the halfway mark and a dot on the 7th mark. cd-p2 has a dot on the 6th mark, one past the longer halfway tick. cd-p5 has a dot on the 8th mark and cd-q4 on the 3rd. Every alt text matches. Every sentence is 20 words or fewer.

## Findings

1. **p-6: "On a number line, 3.09 is to the right of 3.1."** SUGGESTION.
   Problem: this is a bare statement with no question. The other true/false items in this topic (p-3, q-2) end "Is Kavya/Anjali right?". The mixed-numbers review asked for the same fix.
   Fix: add "Is this true?" to the end.

2. **p-7, p-9, q-6 (rounding to a whole) and p-1: no typing instruction.** SUGGESTION.
   Problem: every other numeric prompt in the three decimal topics ends "Type ...". A child who types "7 m" or "87 rupees" gets "unreadable". That does not mark them wrong, but it is a needless stumble.
   Fix: end each with "Type a whole number." For p-1, use "Type the bigger number, like 0.4."

3. **q-5 option "0.7" why_wrong: "That adds 0.3 and 0.4."** SUGGESTION.
   Problem: adding decimals (s0-add-sub-decimals) is not a prerequisite of this topic. The sum is easy (3 tenths + 4 tenths), but it is not yet taught.
   Fix: "That adds 3 tenths and 4 tenths to get 7 tenths. That is not even between 0.3 and 0.4."

4. **p-8 (`decimal` rule, rounding to 1 decimal place).** SUGGESTION.
   Problem: "2.60" is accepted, because it has the same value, but it is written to 2 places. This is a minor leniency, not a wrong mark.
   Fix: none needed in content. Site-builder could later add a "places" check if rounding questions grow.

5. **p-2 duplicates s0-decimals-meaning p-1.** SUGGESTION.
   Problem: both are the same question (a dot at 0.6 on a 0-to-1 tenths line), and the two drawings use different tick styles.
   Fix: change this one, for example to a dot at 1.7 on a 1-to-2 line. Keep one tick style for tenths lines across topics.

Cross-topic: "Type a decimal, like 0.4." and "a zero at the end does not change the value" match the sibling topics. "1 decimal place" is defined here ("the nearest tenth") and is not used in the sibling topics, so nothing conflicts. Nani buys cloth (p-7); see s0-add-sub-decimals finding 4 on who does the shopping.

## Fixes applied (content-writer)

1. p-6: added "Is this true?"
2. p-1 now ends "Type the bigger number, like 0.4." p-7 ends "Type a whole number." p-9 and q-6 are money prompts. Under the shared convention they end "Type the amount in rupees, like 45.50." and use `match: decimal`. A whole answer (87, 65) is still accepted.
3. q-5 option 0.7: why_wrong now says "That adds 3 tenths and 4 tenths to get 7 tenths. That is not even between 0.3 and 0.4." It keeps the zoom-in sentence.
4. No content change, as the review advises. The "places" check is left to site-builder.
5. p-2 now asks for a dot at 1.7 on a 1-to-2 line, with new hints, explanation and verify (`1 + 7 * Rational(1, 10)`). I changed make.py so cd-p2 is drawn with `draw.number_line`. That is the same tick style as dm-p1 and dm-q8, with no longer halfway tick. I re-ran make.py, and the cd-p2 purpose, spec, alt and checks match the new meta (start 1, end 2, 10 spaces, labels 1 and 2, point 17/10).

Context (roles): p-7 is now "Ravi's Dadaji buys 7.3 m of cloth". p-9 is "Shreya's Papa buys a hammer". q-6 is "Gurpreet buys a skipping rope". The prices are unchanged.
`verify_content`: PASS, 51 checks passed, 0 failed, 0 warnings. Status set to draft.
