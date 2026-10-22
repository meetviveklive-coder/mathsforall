# Review: s0-add-sub-unlike-fractions

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 4 suggestions).

Checks run: `tools/verify_content.py` (38 pass, 0 fail, 0 warnings). I worked out every example, section claim, doubt, practice and quiz answer again with my own SymPy code, and all 23 values agree. That covers the LCMs (lcm(4,6)=12, lcm(6,8)=24), the renamings, and the mixed-number results 3 5/6, 1 3/4, 3 3/4, 2 5/6, 4 1/6, 2 7/12 and 5 1/4. I compared every visual's `alt`, `spec` and `checks` with `make.py` and the `.meta.json` files, and rendered the SVGs. The bar counts and shading all match, and the half bar is visibly longer than the third bar and the 2/5 bar, as the text says.

Match rules: p-4 asks for simplest form and uses `simplest`. p-8, p-9, q-6 and q-7 ask for a mixed number and use `mixed`. p-2 and p-3 ask for a whole number with `value`. The rest use `value`, which is right for "Work out ...".

MCQ distractors:
- p-6: 2/7 (adds tops and bottoms), 6/10 (5/10 + 1/10, top of 1/5 not multiplied) and 2/10 (1/10 + 1/10, neither top multiplied). All three are unequal to 7/10, and each matches its stated mistake.
- q-1: 14 (sum of denominators) and 8 are not multiples of 6. 48 is a common multiple but not the smallest, and the prompt says "smallest". So 24 is the only correct option.

Prerequisites: listing multiples comes from s0-factors-multiples (an ancestor). Renaming comes from s0-equivalent-fractions. Improper fractions come from s0-mixed-numbers. Nothing is used before it is taught. No sentence is over 20 words. The names and settings (kheer, rakhi, rangoli, train journey, hill trek) are natural and varied.

## Findings

1. **q-7 prompt.** SUGGESTION.
   Problem: "Sunil walks 5 1/4 km on a hill trek" can be read as "he has already walked 5 1/4 km". Then "left after lunch" has to be worked out from the context. Most children will read it correctly, but it is worth making clearer.
   Fix: "Sunil's hill trek is $5\frac{1}{4}$ km long. He stops for lunch after $2\frac{2}{3}$ km. How many kilometres are left?"

2. **sections[4].body (mixed-number subtraction).** SUGGESTION.
   Problem: the line goes from $\frac{13}{4} - \frac{6}{4}$ straight away, without showing $1\frac{1}{2} = \frac{3}{2} = \frac{6}{4}$. Example 3 shows that step, but the section does not.
   Fix: write $3\frac{1}{4} - 1\frac{1}{2} = \frac{13}{4} - \frac{3}{2} = \frac{13}{4} - \frac{6}{4} = \frac{7}{4} = 1\frac{3}{4}$.

3. **Cross-topic wording for mixed-number answers.** SUGGESTION.
   Problem: this topic says "Type your answer as a mixed number, like 2 1/3." s0-multiply-fractions p-9 says "Write the answer as a mixed number, for example 2 1/3." s0-mixed-numbers says "Type a mixed number, like 4 1/3." s0-add-sub-like-fractions says "Give your answer as a mixed number. Type it like 2 1/3." The format they ask for is the same (`mixed`), but the four wordings differ.
   Fix: agree on one phrase across the Fractions unit, for example "Type a mixed number, like 2 1/3."

4. **"Common denominator" is defined twice (with s0-comparing-fractions).** SUGGESTION.
   Problem: this topic defines a common denominator as "a number that both denominators divide into exactly", and finds it by listing multiples. s0-comparing-fractions calls it "a shared denominator", and its doubt says "Any number in both times tables works". The two ideas agree, but the wording differs. The comparing doubt's "times tables" wording also does not work beyond 10 × 10. Since s0-comparing-fractions is not a prerequisite here, defining it again is fine.
   Fix: use the same definition in both topics ("a number that both denominators divide into exactly"), and use "multiples" instead of "times tables" in s0-comparing-fractions.

## Fixes applied (content-writer)

Status set to `draft`. `verify_content.py`: PASS, 38 checks, 0 fail, 0 warnings.

1. q-7: applied as suggested ("Sunil's hill trek is 5 1/4 km long. ... How many kilometres are left?").
2. sections[4]: applied. The line now shows 13/4 - 3/2 = 13/4 - 6/4 = 7/4 = 1 3/4.
3. Mixed-number wording: applied. p-8, p-9, q-6 and q-7 end with "Type a mixed number, like 2 1/3." None of their answers is 2 1/3.
4. Common denominator: applied, using the house definition. sections[1] keeps "a number that both denominators divide into exactly". It now says the smallest one is usually the easiest to use, and that you find it by listing multiples of the bigger denominator. The halves-and-thirds example lists multiples of 3 only. The same method is now used in examples[0] and [1], summary[1], p-2 (hints and explanation), the q-1 explanation and doubts[0] and [1]. The q-1 hint already used this method. "Type a whole number." stays on p-2, because a child might type 1/12 there.
Pronouns: Nani (hook) is "she".
