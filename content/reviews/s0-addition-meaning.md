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
