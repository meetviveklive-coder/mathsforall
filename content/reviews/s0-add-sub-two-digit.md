# Review: s0-add-sub-two-digit

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 6 suggestions).

Standard used: the young-learner addendum, at about 7 years old (sentences of up to about 15 words, numbers within 100).

Checks run:
- `tools/verify_content.py`: 44 checks pass, 0 fail, 0 warnings.
- I worked out all 3 examples and all 15 practice and quiz answers again with my own SymPy code. All of them agree.
- I counted every stick, square, ring and cross in all 8 SVGs. I did this from make.py, and on a rendered image.
  - rg-47: 4 sticks and 7 squares.
  - rg-p1: 6 sticks and 14 squares, in rows of 5/5/4.
  - rg-p4: 4 sticks and 3 squares.
  - rg-q5: 3 sticks and 15 squares, in rows of 5/5/5.
  - rg-add-blocks has four rows:
    - 38;
    - 45;
    - 7 sticks and 13 squares, with exactly 10 squares inside the ring;
    - 8 sticks and 3 squares, where the last stick is the new one.
  - rg-sub-blocks has three rows:
    - 52;
    - 4 sticks and 12 squares, with the 10 new ones ringed;
    - 2 of 4 sticks crossed and 7 of 12 squares crossed, leaving 2 tens and 5 ones (25).
  - Both column diagrams have the right digits, the right carry or borrow marks, and the right answers.
  - Every picture matches its alt, spec, checks and question.
- MCQ distractors. Each matches its stated misconception:
  - p-6: 63 forgets the carry. 613 writes "13" in the ones.
  - q-2: 74 and 714, the same two errors.
  - p-7: 44 swaps the digits (7−3). 46 borrows but leaves the tens unchanged.
  - q-4: 46 swaps the digits. 44 forgets to reduce the tens.
  - q-7: "1 one" and "13 ones".
  - Each MCQ has exactly one correct option.
- Prerequisites. These ideas come from s0-numbers-to-100: tens and ones, and the word "digit". These come from s0-subtraction-meaning: "−", "how many more", and check by adding. The phrase "Check by adding back" matches subtraction's "Check by adding". Adding with a carry is taught in this topic before it is used to check.
- Every "₹" answer is accepted as a plain number (site/src/lib/answers.ts strips ₹ and "rupees").

The flagged items:
- **Distractors 613/714 and 46.** 46 is fine. 613 and 714 are real errors, but see finding 1.
- **"Different colour" in section 2.** See finding 2.
- **Alt text length.** Alt sentences run to 17 words. This is a small problem, because alt text is read aloud to the child. See finding 5.

## Findings

1. **p-6 option "613", q-2 option "714".** SUGGESTION.
   Problem: these are three-digit numbers. The child knows numbers only to 100 and cannot read "six hundred thirteen". The error they stand for is real. But the child will reject the option because it looks strange, not because they understand why it is wrong.
   Fix: drop these options. Two or three options are enough at this age. Or replace each with an in-range error, such as adding the carry to the ones.

2. **sections[1] body: "The new ten is in a different colour."** SUGGESTION.
   Problem: this is a colour-only cue in the text the learner reads. In the picture the new ten is also the last (eighth) stick, so the picture itself is fine.
   Fix: "The last stick is the new ten." Make the same change in the rg-add-blocks and rg-sub-blocks alts: "the last stick" and "the 10 ringed squares".

3. **hook: "They score 38 runs in the first 5 overs."** SUGGESTION.
   Problem: the extra number 5 appears just before "$8 + 5 = 13$", where the 5 comes from 45. A 7-year-old may think the 5 overs are being added.
   Fix: drop "in the first 5 overs" (for example, "They score 38 runs. Then they score 45 more.").

4. **q-6 prompt.** SUGGESTION.
   Problem: one sentence is 17 words long.
   Fix: "Thomas says: 3 tens and 12 ones is the same as 4 tens and 2 ones. Is he right?" Or split it into two sentences.

5. **Alts of rg-47, rg-sub-blocks.** SUGGESTION.
   Problem: three alt sentences are 17 words long.
   Fix: split each into two sentences.

6. **Cross-topic note.** SUGGESTION.
   Problem: none of the words for the method conflict between topics: "carrying" and "borrowing" are new here, and "take away" and "check by adding" match s0-subtraction-meaning. One small point: s0-addition-meaning's "make 10" (fill a ten-frame) is the same idea as "trade 10 ones for 1 ten", but this topic never says so.
   Fix: optional. Add to section 2: "This is like filling a ten-frame."
