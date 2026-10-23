# Review: s0-percent-meaning

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 4 suggestions).

Checks run: `tools/verify_content.py` (44 pass, 0 fail, 0 warnings). I worked out every section claim, example, practice and quiz answer again with my own SymPy code, using exact `Rational` values. All values agree: 37% = 37/100 = 0.37 (and 37/100 > 1/3, so "a bit more than a third" is right); 30% = 3/10 = 0.3; 5% = 0.05; 0.5 = 50%; 0.83 = 83%, 0.6 = 60%, 0.07 = 7%; 3/4 = 75%, 7/20 = 35%; 50%, 25%, 10% = 1/2, 1/4, 1/10; 150% = 1.5; examples 9/20 (and 0.45 < 1/2), 60 and 125; p-1 to p-10: 63, 0.03, 85, 0.05, 1/5, 55, 10, true, 75, 130; q-1 to q-8: 9, 0.08, 90, 3/20, 36, 25%, false (1.5 > 1), 0.01; doubts: 3/8 = 37.5% and 1/3 = 33⅓% exactly.

Match rules: every question whose answer is a number of percent (p-1, p-3, p-6, p-9, p-10, q-1, q-3, q-5) ends "Type the number only, like 40." and uses `value`. None of these answers is 40. "63" and "63%" are both accepted, because `parseAnswer` strips a final %. A child who types 0.63 is marked wrong, which is right for "type the number only". p-7 (box, 10) correctly uses the box phrase instead. Decimal answers (p-2, q-8) use "Type a decimal, like 0.4." and `decimal`. Simplest-form answers (p-5, q-4) use `simplest`, and a typed decimal gets "write it as a fraction". No answer in this topic is 1/3 or 2/3, and no recurring decimal is typed.

MCQs: p-4 (0.5, 5, 0.005), q-2 (0.8, 8) and q-6 (4%, 40%) each have one right option. Every why_wrong is accurate (0.5 = 50%, 5 = 500%, 0.005 is thousandths, 0.8 = 80%, 8 = 800%, 40% mixes 1/4 with 4 tenths).

Scope: no exam marks, test scores or ranks appear (the only "marks" are inside "benchmarks"). The topic never finds a percent of an amount or a percentage change. Section 5, p-10 and q-7 describe rain as 150% or 130% "of its usual rain", but only to read 1.5 or 1.3 as a percent. I judge this within scope: it answers the misconception "a percent cannot be more than 100" without computing a percentage of a quantity.

Visuals: I rendered all six SVGs and compared them with make.py, the meta files and the alt texts. pm-grid-37 has 3 full columns and 7 more (37). pm-grid-5-50 has 5 and 50. pm-benchmarks has 50 (5 columns), 25 (5 by 5 block) and 10 (1 column), each labelled with its fraction. pm-150 has 100 and 50 with the caption "150% = 1.5". pm-p1 has 63 and pm-q1 has 9 (the bottom square of column 1 is clearly empty, and q-1's first hint asks about full columns).

Wording: every sentence is 20 words or fewer. Contexts (power bank, torch, stadiums, monsoon rain in Shillong) are natural and avoid marks.

## Findings

1. **p-5 and q-4: "Write 20% (15%) as a fraction in simplest form." with no typing phrase.** SUGGESTION.
   Problem: every other typed answer in this topic ends with "Type ...". The sibling s0-fractions-decimals-conversion ends every simplest-form prompt with "Type a fraction, like 3/10." A child who has just answered "Type the number only, like 40." may type 20 or 20% here and be marked wrong without knowing why.
   Fix: end both prompts with "Type a fraction, like 3/10." Neither answer is 3/10.

2. **doubts[3] (37.5%) and doubts[4] (33 and one third percent) (writer flags: judged).** SUGGESTION.
   Judgement: both are mathematically right, and as optional doubts they are fair for a 10-year-old. 3 ÷ 8 = 0.375 is worked in s0-fractions-decimals-conversion, so it is known. Three wording points:
   (a) "37 hundredths and half of one more" is hard to parse. "37 and a half hundredths" is clearer.
   (b) doubts[4] writes "0.333..." with plain dots, while the conversion topic teaches $0.333\ldots = 0.\dot{3}$.
   (c) "People often round it to 33%" does not say that 33% is not exact. The conversion topic's key message is that 0.33 is a little less than 1/3.
   Fix: "That is 37 and a half hundredths, so it is 37.5%." And: "$\frac{1}{3} = 0.\dot{3}$. So it is $33\frac{1}{3}\%$ exactly. People often say about 33%, but 33% is a little less than $\frac{1}{3}$."

3. **q-2: "Which decimal of a full charge is that?"** SUGGESTION.
   Problem: "decimal of a full charge" is an unusual phrase for a child. The question only asks for 8% as a decimal.
   Fix: "Mrinalini's torch battery shows 8%. Which decimal is the same as 8%?"

4. **Cross-topic: the paise sentence in doubts[2].** SUGGESTION.
   Problem: "like paise in a rupee" does not use the shared sentence "100 paise make 1 rupee" from s0-decimals-meaning and s0-add-sub-decimals.
   Fix: "Hundredths also match paise: 100 paise make 1 rupee. So 37% is 0.37, just as 37 paise is ₹0.37."
