# Review: s0-percent-change

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 5 suggestions).

Checks run: `tools/verify_content.py` (48 pass, 0 fail, 0 warnings). I worked out every section claim, example, practice and quiz answer again with my own exact SymPy code. All values agree: ₹800 − 25% = ₹600 (and 800 × 0.75); ₹3000 + 5% = ₹3150 (and × 1.05); 10/40 = 25% and 10/50 = 20%; onions 20% decrease; bag 500 → 600 → 480; examples 1020 (and × 0.85), 14160 (1200 + 960, and × 1.18), 15; p-1 to p-10: 540, 1050, 70%, 88.20, 29500, 32, 50, 30, false (10/60 × 100 = 16.67 ≠ 20), 39.60; q-1 to q-8: 200, ₹680, 5040, × 1.18 (23600), 20, 25%, false (ends ₹144), 15; doubts: ₹150, 150%, 100 → 80 → 96.

Match rules and typing: money answers use `decimal` with "Type the amount in rupees, like 45.50." The parser accepts 540, 540.00, ₹540 and "540 rupees", and 88.2 for p-4. Percent answers (p-7, p-8, q-5, q-8) use "Type the number only, like 40." with `value`, as in s0-percent-meaning and s0-percent-of-quantity. No answer is 40 or 45.50.

MCQs: p-3 (70, 30, 130), q-2 (120, 680, 785, 920), q-4 (3600, 20018, 36000, 23600) and q-6 (15, 20, 25, 125) each have exactly one right option, and every why_wrong names the real mistake (discount not subtracted, ₹15 not 15%, 1.8 = 180%, dividing by the new price, new price as a percent of the old).

GST facts (GST 2.0, from 22 September 2025): roti, paneer and exercise books 0%; bicycles, toothpaste and ghee 5%; televisions and air conditioners 18%. All items are in the right slab, and the old 12% and 28% slabs are not used anywhere.

Prerequisites: 10% and 1% steps, "of means multiply" and percent as a decimal come from s0-percent-of-quantity and s0-percent-meaning (105% = 1.05 follows 150% = 1.5 there). Rounding to "about 16.7%" in p-9 is only in an explanation and uses the recurring decimal from s0-fractions-decimals-conversion.

Visuals: I re-ran make.py and rendered all four SVGs. Bar lengths are to scale, and the metadata (read back from the drawn widths) matches every label and the alt text: 600 + 200 cut; 3000 + 150 extra; 4 × 10 then 5 × 10; 500, 500 + 100, and 480 + 120 cut, with the guide at 500.

Scope and context: no exam marks, test scores or ranks. Festivals (Diwali, Eid, Onam), family members and items are varied and natural. Every learner-facing sentence is 20 words or fewer.

## Writer flags (judged)

- **Dashed ₹500 marker in pc-up-down.** Not misleading, but weak. See finding 1.
- **q-8 objective.** Correct as 2. q-8 gives both prices and asks for the percent taken off, which is a percentage decrease. Objective 0 is finding the price after a discount, which q-8 does not ask.
- **"Pishi" and "Ammachi".** Fine. Pishi (father's sister, Bengali) fits Debashish, and Ammachi (grandmother, Malayalam) fits Thomas from Kerala. Both are family words, like Nani, Bua and Dadaji used across the site, and the sentence makes clear each is a person.

## Findings

1. **visual pc-up-down and section 4: the ₹500 marker is hard to see.** SUGGESTION.
   Problem: on the first two bars the dashed mark sits exactly on a bar edge (the end of ₹500, and the join between ₹500 and +₹100). So only 3 px tips show above and below. On the third bar it is about 10 px right of the shaded end, inside the dashed ₹120 box. It is unlabelled, and it is the second dashed thing in that bar. Section 4 says "the dashed mark shows ₹500. The last bar stops short of it", so the child is sent to look for it. The ₹480 label still makes the point, so nothing is wrong, only hard to see.
   Fix (visuals): draw one full-height line at ₹500 through all three bars in a contrasting colour (or solid), and label it "₹500" at the top. Keep the alt text's sentence about the mark.

2. **Section 2, p-4, p-5, p-6, q-3: "GST is added on top of the price".** SUGGESTION.
   Problem: in Indian shops the printed price (MRP) on toothpaste or ghee already includes GST. A child who checks a real tube may be confused.
   Fix: in section 2 add "On a bill, the price before GST is shown first. Then GST is added." In prompts, write "The price before GST is ₹84."

3. **doubts[2]: "Why is there no GST on roti?" does not say why.** SUGGESTION.
   Problem: the answer only restates that it is 0%.
   Fix: "The government keeps GST at 0% on some everyday things, so that they cost less. Roti, paneer and exercise books are like this. 0% of any price is ₹0, so nothing is added."

4. **visuals[0], [1], [2] spec and visuals[1] alt: sentences over 20 words.** SUGGESTION.
   Problem: three specs have 22 to 24 words, and the pc-gst alt sentence has 21. A screen-reader user hears the alt.
   Fix: split the pc-gst alt sentence: "It has the same ₹3000 piece. A thin extra piece in a different colour, labelled GST ₹150, is added at the end." The specs are not shown to learners; splitting them is optional.

5. **Cross-topic: "original value" and "whole".** SUGGESTION.
   Problem: s0-percent-of-quantity teaches "Ask yourself, percent of what? That amount goes on the bottom." This topic introduces "original value" for the same idea, but does not link the two.
   Fix: in section 3, after the formula, add "This is the 'percent of what?' question again. The answer is the original value."

## Fixes applied (content-writer)

1. pc-up-down: make.py now draws one dashed line at ₹500 in the POINT colour, on a light halo, from a "₹500" label at the top down through all three bars. Segment labels near the line are moved clear of it (+₹100 and −₹120 now start 6 px right of it). The meta reads back `guide_text: "₹500"` and `guide_crosses_rows: 3`, and the topic's checks now include both. Re-ran make.py and rendered it. The spec and alt now describe the labelled line. Section 4 now says "the dashed line labelled ₹500 runs through all three bars. The shaded part of the last bar stops short of it."
2. GST is now described as added to "the price before GST". Section 2 adds "Many price tags in shops already include GST. On a bill, the price before GST is shown first. Then GST is added." and "GST is a percent of the price before GST." Bhavna's bicycle, example 2, p-4, p-5, p-6, q-3 and q-4 now give "the price before GST". The summary line now reads "GST is a tax added to the price before GST." In pc-gst the top bar label is now "Before GST: ₹3000" (make.py, purpose, spec, alt and checks updated). Slabs 0%, 5% and 18% are unchanged.
3. doubts[2] now says the government keeps GST at 0% on some everyday things so that they cost less.
4. pc-gst alt split as suggested. The pc-discount, pc-gst, pc-tomato and pc-up-down specs are split into sentences of 20 words or fewer.
5. Section 3, after the formula: "This is the \"percent of what?\" question again. The answer is the original value."

Also: whole-rupee answers (p-1, p-2, p-5, p-6, q-1, q-3) now end "Type the amount in rupees." Answers with paise (p-4 ₹88.20, p-10 ₹39.60) keep "like 45.50."

`verify_content`: PASS, 48 checks passed, 0 failed, 0 warnings. Status set to draft.

## Re-check

Reviewer: math-verifier, 2026-10-24. Result: **verified** (0 blocking, 0 suggestions).

Checks run: `git diff 90946ab HEAD` on the topic and visuals, `tools/verify_content.py` (48 pass, 0 fail, 0 warnings). I re-solved every changed item with my own exact SymPy code: section 2 (5% of 3000 = 150, 3000 × 1.05 = 3150), section 3 (10/40 = 25%, 10/50 = 20%), section 4 (500 → 600 → 480), example 2 (2160 GST, 14160), p-1 540, p-2 1050, p-4 88.20, p-5 29500, p-6 32, q-1 200, q-3 5040, q-4 (GST 3600, total 23600). All agree.

Visual pc-up-down: I re-ran make.py (output byte-identical to the committed SVG and meta) and rendered it in light and dark mode. With 280 px for ₹600, the guide is at x = 253.33, exactly ₹500. It runs from the teal "₹500" label at the top through all three bars: it meets the end of the first bar, the join of ₹500 and +₹100 in the second, and lies inside the dashed ₹120 box, just right of the ₹480 end, in the third. The halo keeps it visible on the teal piece in both modes. +₹100 and −₹120 labels sit 6 px right of it; 0 overlaps. Alt text, spec, section 4 and checks (`guide_text` "₹500", `guide_crosses_rows` 3) all match the drawing. pc-gst's top label now reads "Before GST: ₹3000", matching alt, spec and checks.

Findings 1 to 5 are fixed. GST appears only at 0%, 5% and 18%, and every GST question gives "the price before GST" (example 2, p-4, p-5, p-6, q-3, q-4). Whole-rupee answers say "Type the amount in rupees."; p-4 (₹88.20) and p-10 (₹39.60) keep "like 45.50". Percent answers keep "like 40" and none is 40. No exam marks. No new error.
