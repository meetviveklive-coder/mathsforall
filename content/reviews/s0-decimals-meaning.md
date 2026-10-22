# Review: s0-decimals-meaning

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 5 suggestions).

Checks run: `tools/verify_content.py` (54 pass, 0 fail, 0 warnings). I worked out every section claim, example, practice and quiz answer again with my own SymPy code, using exact `Rational` values parsed from the decimal strings. All values agree: 7/100 = 0.07, 3.25 = 3 + 25/100, 3 m 6 cm = 3.06, 0.6, 0.47, 0.09, 0.6 = 60 hundredths, 0.05, ₹38.50 = 3850 paise, 1.35, 0.25 < 0.3, the hundredths digit of 6.248 is 4, 4.035, 0.08, 0.43 = 43/100, 0.023, 2.06, 2.08, ₹102.09 = 102 + 9/100, 10 thousandths per hundredth, 1.3, and 1.375 = 1 + 3/10 + 7/100 + 5/1000.

Match rules: every prompt that asks for a decimal ends "Type a decimal, like 0.4." and uses `decimal` (p-1, p-2, p-3, p-7, p-10, q-1, q-3, q-5, q-8). None of these answers is 0.4. Whole-number items (p-4, p-6, q-7) say "Type a whole number" and use `value`. q-2 is a fill-in-the-box item with answer 43, and p-9 asks for one digit (4). `value` is right for all of these.

MCQs: in p-5 the four options are 5/10, 5/100, 5/1000 and 5, so only 0.05 is 5 hundredths. In q-4 only 2.06 has 2 ones, 0 tenths and 6 hundredths. In q-6 only "102 rupees and 9 paise" equals ₹102.09. Every why_wrong names the right place-value slip.

Visuals: I rendered all eight SVGs and compared them with make.py, the meta files and the alt texts. dm-grid-35 has 3 full columns and 5 more (35). dm-grid-compare has 30 and 25 shaded, labelled 0.3 and 0.25. dm-p2 has 47 and dm-q1 has 8, with no full column. dm-p1 has a dot on the 6th mark, and dm-q8 has a dot on the 3rd mark after 1. dm-chart has the three rows 0.5, 0.05 and 1.375 under the right headings. dm-tenths-nl has 1/10 to 9/10 above and 0, 0.1 to 0.9, 1 below.

Prerequisites: place value (s0-place-value-thousands) and fractions on a number line are in the chain. Every sentence is 20 words or fewer.

## Findings

1. **sections[3].body: "Look again at 0.5 and 0.05 in the chart."** SUGGESTION. (Writer flag: judged.)
   Problem: the chart belongs to section 2. The picture shown with section 3 is dm-grid-compare (0.3 and 0.25). On a phone the chart has scrolled away, and a child may look for 0.5 and 0.05 in the grids. "Look again" and the second paragraph's "In these grids" soften this, so it is not blocking.
   Fix: write "Look back at the place-value chart above. Find 0.5 and 0.05." Or move the chart sentence into section 2.

2. **examples[1]: "Write 3.25 as a mixed number", answer $3\frac{25}{100}$.** SUGGESTION.
   Problem: mixed numbers (s0-mixed-numbers) are approved but are not in this topic's prerequisite chain (s0-fractions-number-line, s0-place-value-thousands). A child can unlock this topic without them. The answer is also not in simplest form ($3\frac{1}{4}$), and nothing says so.
   Fix: phrase it as "3 and 25 hundredths", as doubts[2] does, and skip the mixed-number name. Or add s0-mixed-numbers as a prerequisite in the topic map.

3. **sections[0].body: "each mark has a fraction name above it".** SUGGESTION.
   Problem: the marks at 0 and 1 have no fraction above them in dm-tenths-nl.
   Fix: "each mark between 0 and 1 has a fraction name above it".

4. **Cross-topic: place-value names and money wording.** SUGGESTION.
   Problem: this topic writes place names in lower case ("the tenths place") and says "100 paise make 1 rupee". s0-add-sub-decimals uses capitals in prose ("The Hundredths place of 12.5", "the Ones column", "the Tenths place" in p-4) and says "100 paise make ₹1". The ideas match, but the style changes between sibling topics.
   Fix: agree on lower case in prose (capitals only as chart headings) and one money sentence, for example "100 paise make 1 rupee (₹1)."

5. **p-1 and s0-comparing-decimals p-2 (duplicate question).** SUGGESTION.
   Problem: both ask for the same dot at 0.6 on a 0-to-1 line in tenths, with the same prompt. A child meets the same item twice. The two drawings also differ: cd-p2 has a longer halfway tick and dm-p1 does not.
   Fix: change one of them (for example, use 0.3 or a 1-to-2 line in s0-comparing-decimals), and use one tick style for tenths lines.

Context: "Joseph's Nani" (coriander) is natural. Nani also buys cloth in s0-comparing-decimals p-7. See the context note in s0-add-sub-decimals finding 4.
