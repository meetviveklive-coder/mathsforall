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

## Fixes applied (content-writer)

Date: 2026-10-24. Status set back to "draft". The existing review entry is kept.

1. Each three-digit distractor is replaced with an in-range error, as suggested: the carried 1 is added to the ones instead of the tens.
   - p-6: "613" is now "64" (ones 3+1=4, tens 2+4=6).
   - q-2: "714" is now "75" (ones 4+1=5, tens 5+2=7).
   - Each has its own why_wrong. Each MCQ still has exactly one correct option, and verify passes.
2. In section 2, "The new ten is in a different colour." is now "The last stick is the new ten."
   - rg-add-blocks alt: "The last stick is the new ten."
   - rg-sub-blocks alt: "A ring goes round 10 of the squares. They are the 10 ones from the broken ten."
   - The specs say that colour is only a second cue.
   - The drawings did not change, so make.py was not re-run.
3. The hook is now "They score 38 runs. Then they score 45 more runs."
4. q-6 is now "Thomas has 3 tens and 12 ones. Sana has 4 tens and 2 ones. They have the same number. True or false?" The answer is still true, and the verify expression did not change. The explanation starts with "True.".
5. The rg-47 and rg-sub-blocks alts are split, and every sentence is 15 words or fewer. "Base-ten picture" is now "A picture" in rg-47.
6. Section 2 adds "This is like filling a ten-frame." after the trade.

- `verify_content.py`: PASS, 44 checks passed, 0 failed, 0 warnings.

## Re-check

Reviewer: math-verifier, 2026-10-24. Result: **verified** (0 blocking, 0 new suggestions). Notes: re-check after fixes.

Checks run:
- `tools/verify_content.py`: PASS, 44 checks, 0 fail, 0 warnings.
- I read `git diff 616b950 HEAD`. Only the topic JSON changed. The SVGs and make.py are unchanged, so the counts from the first review still hold.
- I re-solved the changed items with my own code:
  - p-6: $29 + 44 = 73$. Simulating each error gives the distractors: no carry gives 63, and adding the carry to the ones gives 64.
  - q-2: $56 + 28 = 84$. The same two errors give 74 and 75.
  - Each MCQ has exactly one correct option, and each new why_wrong describes its error correctly.
  - q-6: $3 \cdot 10 + 12 = 4 \cdot 10 + 2 = 42$, so the answer is true.
- Findings 1–6 are fixed:
  - No three-digit number remains in any learner-facing string.
  - "different colour" is gone. "The last stick is the new ten" matches rg-add-blocks, where the eighth stick is the new one.
  - The hook no longer has "5 overs".
  - q-6 is split into short sentences.
  - All alt sentences are 15 words or fewer.
  - "This is like filling a ten-frame" uses an idea from s0-addition-meaning, which is a prerequisite through s0-subtraction-meaning.
- Cross-topic: q-6 ends "True or false?" and its explanation starts "True.". "Check by adding" and "take away" still match s0-subtraction-meaning.

### Findings

None.
