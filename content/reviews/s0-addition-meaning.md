# Review: s0-addition-meaning

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 7 suggestions).

Standard used: the young-learner addendum (a reader of about 6 years old).

Checks run:
- `tools/verify_content.py`: 44 checks pass, 0 fail, 0 warnings.
- I worked out all 3 examples and all 15 practice and quiz answers again with my own SymPy code. All of them agree.
- I counted every object in all 11 SVGs. I did this from make.py, by counting the circles and rects in each SVG, and on a rendered image. Every picture matches its alt, spec, checks and the question that uses it:
  - groups-3-4: 3 and 4.
  - p1: 4 and 2.
  - p6: 4 and 4.
  - q1: 5 and 3.
  - order-3-5: 3 and 5.
  - p5: 2 and 6.
  - frame-7-5: 7+3 in the top frame, 2 in the bottom frame.
  - p7: 8+2 in the top frame, 2 in the bottom frame.
  - q4: 9+1 in the top frame, 4 in the bottom frame.
  - hops-5-3: 5 to 8.
  - p2: 6 to 9, with no landing dot.
- Each MCQ has exactly one correct option. Each distractor is wrong and matches its stated reason:
  - p-4: 10 comes from counting 8 again. 5 comes from taking away.
  - q-6: 6+3 = 9 and 5+4 = 9.
- All numbers are within 20. All answers are whole numbers. No answer is negative.
- "+" and "=" are taught in section 3 before any question uses them.
- No idea is used beyond counting to 20.

The flagged items:
- **Colour-coded second group.** Acceptable. The second group always differs by shape as well: it has a centre spot. It is also always in its own place: the second loop, the right of the row, or after the orange counters. Alt texts naming colours are fine, because the alt texts are not the only cue. See finding 1 for the lesson text.
- **Numbered hops in p-2.** Acceptable. The lesson's section 2 teaches the same picture with "Hop 1 lands on 6". See finding 3.
- **7-question quiz.** Acceptable. The pass mark of 80% still allows one slip with 7 questions, as it does with 6. See finding 4.

## Findings

1. **sections[0], [3], [4] body; q-4 and p-7 explanations.** SUGGESTION.
   Problem: the text names the two kinds of counter only by colour ("orange dots", "green counters"). A colour-blind child can still tell them apart by the centre spot and by position, so this is not misleading. But the addendum asks for no colour-only cues in the text.
   Fix: name the shape too the first time, for example "4 green dots with a spot". Or name the place: "the 3 counters that fill the frame".

2. **sections[1] heading "Count on from the bigger number".** SUGGESTION.
   Problem: the reason you may start with the bigger number comes only in section 4 ("Order does not matter"). The section 2 example (5 + 3) already starts with the bigger number, so the heading's rule is not explained there.
   Fix: change the heading to "Count on", and keep "start with the bigger number" in section 4. Section 4 already says it.

3. **am-p2 / p-2.** SUGGESTION.
   Problem: a bold green "3" sits above the last hop, right over the space between 8 and 9. A child asked "Where does the last hop land?" might type 3, the hop's number, not 9.
   Fix: make the hop numbers smaller and lighter than the number-line labels. Or add to the prompt: "Read the number under the line."

4. **quiz (7 questions).** SUGGESTION.
   Problem: the addendum says 6 are enough. q-5 and q-7 both test "order does not matter".
   Fix: optional. Drop q-7, or keep it. Nothing is wrong with 7.

5. **visuals am-p5 alt.** SUGGESTION.
   Problem: two alt sentences are 22 and 23 words long.
   Fix: split them, for example "Above the row, the dots are counted 1 to 8 from the left. An arrow points right. It is labelled 2 + 6." This is the same pattern as the am-order-3-5 alt.

6. **sections[2] body.** SUGGESTION.
   Problem: two short sentences are joined, and the dotted line ends in "**sum**". The word "sum" is then used in q-5 and in p-4's why_wrong. That is fine. But "The number we get" is vague for a 6-year-old.
   Fix: "The answer to an adding is called the **sum**. In $3 + 4 = 7$, the sum is 7."

7. **Cross-topic consistency with s0-subtraction-meaning.** SUGGESTION.
   Problem: there are three differences between the two topics.
   - This topic calls objects "dots", but subtraction calls them "circles" ("Each circle is a bird").
   - This topic marks the landing point with a filled orange dot, but subtraction uses an empty ring.
   - Subtraction says "count up" for the strategy this topic calls "count on".
   Fix: agree on one word for the drawn objects and one landing mark. Ask the subtraction writer to say "count on" (or "count up, like counting on").

## Fixes applied (content-writer)

Date: 2026-10-24. Status set back to "draft". The existing review entry is kept.

1. Colour-only cues: sections 1, 4 and 5 now name the two kinds of dot by shape: "plain dots" and "dots with a spot (in the middle)". The ten-frame text says "the top frame" and "the bottom frame". The p-7 and q-4 hints and explanations say "dots", not "green counters". All alts now use the same shape words, and "counters" became "dots" everywhere a child reads it. Specs keep the colours, next to the shape words.
2. The section 2 heading is now "Count on". "Start with the bigger number" now appears only in section 4, and in its summary line ("Order does not matter: 3 + 5 = 5 + 3. So start with the bigger number."). Summary line 2 no longer says "bigger".
3. am-p2 / p-2: both fixes are applied.
   - In make.py, the hop numbers are now 11px, normal weight and muted. The number-line labels are 15px, weight 600, in the text colour. This also changes am-hops-5-3. Both SVGs were redrawn, and their meta did not change.
   - The p-2 prompt adds "Read the number under the line."
   - Both alts and specs now say "Small numbers 1, 2 and 3 sit above the hops".
4. Dropped q-7, so the quiz has 6 questions. q-5 still covers objective 2.
5. am-p5 alt split into short sentences, using the am-order-3-5 pattern. am-order-3-5, am-groups-3-4 and the ten-frame alts were also split, to about 12 words or fewer.
6. Section 3 now ends: "The answer when you add is called the **sum**. In $3 + 4 = 7$, the sum is 7." I used this in place of "the answer to an adding", which reads awkwardly.
7. Cross-topic: s0-subtraction-meaning now says "dots" and "count on". Its landing mark is now the same filled dot as am-hops-5-3: fill-colour circle, r=7, dark stroke 1.5.

Other changes (conventions):
- The true/false items now end "True or false?":
  - p-5: "$2 + 6$ is the same as $6 + 2$."
  - q-2: "He gets 12. $9 + 4 = 12$."
  - q-5: "$4 + 6$ and $6 + 4$ give different sums."
  - Their explanations now start "True." or "False.".
  - Answers and verify expressions are unchanged.
- The p-2 explanation is split into short sentences.
- Counted again after redraw:
  - am-hops-5-3: 3 arcs and 2 dots.
  - am-p2: 3 arcs and 1 dot.
  - Solid and spotted dots in every group, row and frame SVG: 3/4, 4/2, 4/4, 5/3, 3/5, 2/6, 7/5, 8/4 and 9/5. All match their checks.
- `verify_content.py`: PASS, 43 checks passed (one fewer, because q-7 is gone), 0 failed, 0 warnings.
