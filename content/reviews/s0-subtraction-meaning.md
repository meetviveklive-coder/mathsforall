# Review: s0-subtraction-meaning

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 6 suggestions).

Standard used: the young-learner addendum (a reader of about 6 years old).

Checks run:
- `tools/verify_content.py`: 45 checks pass, 0 fail, 0 warnings.
- I worked out all 3 examples and all 14 practice and quiz answers again with my own SymPy code. All of them agree.
- I counted every object in all 12 SVGs. I did this from make.py, by counting the circles and the X marks (pairs of thick lines) in each SVG, and on a rendered image. Every picture matches its alt, spec, checks and question:
  - take-away: 8, with 3 crossed out.
  - p1: 6, with 2 crossed out.
  - q1: 10, with 7 crossed out.
  - order: 3, with none crossed out.
  - compare: 7 and 4 (3 extra).
  - p3: 9 and 6 (3 extra).
  - q2: 8 and 3 (5 extra).
  - check-12: 10 + 2, with the bottom row of 5 crossed out, leaving 7.
  - p2: 9, with 4 crossed out and 5 left in the top row.
  - hops: 9 to 6 back, and 4 to 7 forward.
  - p4: a dot at 12 on a line from 5 to 15.
  - q3: a dot at 6 on a line from 0 to 10.
- Each MCQ has exactly one correct option, and each distractor matches its reason:
  - p-5: 4 comes from counting 9 as a hop. 21 comes from adding.
  - q-4: 15+8 and 15+7 both add to the start number.
- All numbers are within 20. No answer is negative. "−" is taught in section 1 before any use.

Uses of addition: the topic uses these ideas from s0-addition-meaning:
- "order does not matter in adding" (the 3 + 5 example matches addition section 4);
- number-line hops;
- ten-frames;
- addition facts within 20 (7+5, 7+6, 7+8, 6+8, 6+4, 4+5).
The addition topic teaches all of these. The two topics give the ten-frame the same definition ("A ten-frame has 10 boxes").

The flagged items:
- **"Order matters" without negatives.** Acceptable. "Start with 3, take away 5? There are not enough" is true, and it does not suggest that 3 − 5 is 0. The "Not yet" in the doubt leaves room for negatives later. q-6 and example 3 ask only whether the two are the same, and "false" is the only defensible answer.
- **Plain circles as objects.** Acceptable. Every question that uses a picture says what a circle stands for ("Each circle is a bird/laddoo"). The X marks and the dashed box are clear without colour.

## Findings

1. **sections[2] body, example 2, p-5 hints, q-3 prompt: "count up".** SUGGESTION.
   Problem: s0-addition-meaning teaches this same move as "count on". A 6-year-old may think "count up" is a new skill.
   Fix: say it once in section 3: "Count up. This is counting on, like in adding." Or use "count on" throughout.

2. **Prompts p-1, q-1 ("Each circle is a ...").** SUGGESTION.
   Problem: s0-addition-meaning says "Each dot is a bird" for the same kind of drawing.
   Fix: agree on one word with the addition topic.

3. **sm-hops landing mark.** SUGGESTION.
   Problem: here the landing point is an empty ring. In s0-addition-meaning it is a filled orange dot. This is not wrong, but it is a small change for a young child.
   Fix: use the same landing mark in both topics.

4. **p-8 prompt.** SUGGESTION.
   Problem: "Anu has 4 laddoos. She can take away 6 laddoos from them." is a statement, with no question. A 6-year-old may not know what to do.
   Fix: end with "True or false?" or ask "Can she take away 6 laddoos?"

5. **Alt texts of sm-compare, sm-p3, sm-q2.** SUGGESTION.
   Problem: these alt sentences are 16 or 17 words long. The word "dashed" may also be unknown to a 6-year-old. It is used in the p-3 and q-2 hints too ("Count the marbles in the dashed box").
   Fix: split the sentences. In the hints, say "the box made of little lines" or "the box", because there is only one box.

6. **q-4 prompt "Which adding sum should give 15?"** SUGGESTION.
   Problem: "adding sum" is awkward.
   Fix: "Which sum should equal 15?" or "Which adding checks it?"

## Fixes applied (content-writer)

Date: 2026-10-24. Status set back to "draft". The existing review entry is kept.

1. "Count up" is now "count on" everywhere: section 3, example 2, the summary, the p-5 hints and explanation, the q-3 prompt and explanation, the sm-hops and sm-q3 purposes, and the make.py title. Section 3 adds: "This is counting on, like in adding."
2. "Each circle is a ..." is now "Each dot is a ..." in p-1 and q-1. All alts say "drawn as dots". "Counters" is now "dots" in section 4, p-2 and the ten-frame alts and specs, to match s0-addition-meaning.
3. sm-hops: the landing mark is now a filled dot, drawn exactly as in s0-addition-meaning (fill colour, r=7, dark stroke 1.5). make.py was changed and re-run. Only sm-hops.svg changed, and its meta did not change. The alt now says "A second dot sits on 6 / 7", the same words as am-hops-5-3. The spec says "filled landing dot". I counted again: 2 start dots, 2 landing dots, 0 rings and 6 arcs.
4. p-8 is now "Anu has 4 laddoos. She can take away 6 laddoos. True or false?"
5. The alts of sm-compare, sm-p3 and sm-q2 are split, with every sentence 12 words or fewer. They say "Lines join ... pairs" and "They sit inside a box", with no "dashed". The p-3 and q-2 hints say "Count the ... in the box". The sm-check-12 and sm-p2 alts are split too.
6. The q-4 prompt is now "Which sum should equal 15?"

Other changes (conventions):
- The true/false items now end "True or false?":
  - p-7: "Babu is right."
  - q-6: "$4 - 2$ is the same as $2 - 4$ too."
  - Their explanations start "False.".
  - Answers and verify expressions are unchanged.
- `verify_content.py`: PASS, 45 checks passed, 0 failed, 0 warnings.

## Re-check

Reviewer: math-verifier, 2026-10-24. Result: **verified** (0 blocking, 1 suggestion). Notes: re-check after fixes.

Checks run:
- `tools/verify_content.py`: PASS, 45 checks, 0 fail, 0 warnings.
- I read `git diff 616b950 HEAD`. Every change listed under "Fixes applied" is present, and there are no other changes.
- With my own SymPy code I re-solved every changed item: p-1 = 4, p-2 = 5, p-3 = 3, p-5 = 3, p-7 false, p-8 false, q-1 = 3, q-2 = 5, q-3 = 4, q-4 ($7 + 8 = 15$, and the two distractors are 23 and 22), and q-6 false. All agree.
- sm-hops, redrawn, counted from the SVG and on light and dark renders:
  - Top line: 3 back arcs (9→8→7→6), a start dot at 9 and a filled landing dot at 6.
  - Bottom line: 3 forward arcs (4→5→6→7), a start dot at 4 and a filled landing dot at 7.
  - There are no rings left. The landing mark is the same as in s0-addition-meaning.
  - The picture matches the meta, the alt and the section 3 text.
- The pictures for questions whose wording changed were also re-checked on the renders: sm-p1 (6 with 2 crossed), sm-p2 (9 with 4 crossed), sm-p3 (9/6 with 3 boxed), sm-q1 (10 with 7 crossed), sm-q2 (8/3 with 5 boxed) and sm-q3 (a dot at 6). All match.
- Findings 1–6 are fixed:
  - "count up" is gone, and "count on" is used throughout.
  - "circle", "counter" and "dashed" no longer appear in learner text.
  - p-8 now asks a question.
  - The alt sentences are 12 words or fewer.
  - q-4 reads "Which sum should equal 15?".
- Cross-topic: the terms and the landing mark match s0-addition-meaning. Each of p-7, p-8 and q-6 ends "True or false?". No numbers above 20 and no negative answers.

### Findings

1. **q-6 prompt.** SUGGESTION.
   Problem: "$4 + 2$ is the same as $2 + 4$. $4 - 2$ is the same as $2 - 4$ too. True or false?" puts a true sentence before the false claim. "False" is the only defensible answer, because "too" marks the second sentence as the claim. Still, a 6-year-old might judge the first sentence.
   Fix: optional. Make the first sentence a reminder, not a claim: "Order does not matter in adding. $4 - 2$ is the same as $2 - 4$. True or false?"
