# Review: s0-add-sub-like-fractions

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 5 suggestions).

Checks run: `tools/verify_content.py` (41 pass, 0 fail, 1 manual warning for q-3). I worked out every section claim, example, practice and quiz answer again with my own SymPy code, and all values agree:
- 1/5 + 2/5 = 3/5, and 3/10 < 2/5 = 4/10.
- 3/4 + 2/4 = 5/4 = 1 1/4.
- 5/6 - 2/6 = 3/6 = 1/2, and 1 - 2/6 = 4/6.
- Examples: 5/7, 1/2 and 1 2/5.
- Practice: 5/6, 7/9, 3/10, 5/7, then 1/4 + 1/4 != 2/8, then 1/2, 1 3/8, 1/3 and 2 1/5.
- Quiz: 9/11 and 1/2. For q-3, 5/16 < 6/16 = 3/8. Then 3/10 < 2/5, the box is 3, 2/7, 1 1/2 and 2 2/3.
- Doubts: 4/4 = 1 and 3/8 - 3/8 = 0.

Match rules: p-6 asks for simplest form and uses `simplest` (answer 1/2). p-7, p-9 and q-7 ask for a mixed number and use `mixed`, with proper-fraction answers. q-7 accepts "1 2/4", which is right because the prompt does not ask for simplest form. p-8 and q-2 use `value`, so 3/9 and 5/10 are accepted, which is right. The q-5 box answer is the whole number 3.

MCQs: in p-4, 5/14, 6/7 and 1/7 are unequal to 5/7. They match "added the denominators", "multiplied the numerators" and "subtracted the numerators". In q-8, 1 2/6 (= 4/3), 1 2/3 and 2 8/3 (= 14/3) are all unequal to 8/3. Each why_wrong is accurate.

Manual item q-3: it has exactly one defensible option. "Multiply the denominators" and "no mistake" are both clearly wrong, and their why_wrong texts are correct.

Visuals: I rendered all six SVGs and compared them with make.py and the meta files.
- al-add-bar: 1 orange part, 2 green parts and 2 empty, with brackets labelled 1/5 and 2/5.
- al-nl-jumps: green dot at 3/4, two quarter jumps and an orange dot at 5/4, with every mark labelled.
- al-take-away: 5 of 6 shaded and the last 2 shaded crossed out.
- al-over-one: 4/4 and 1/4.
- al-p1: green dot at 1/6, four 1/6 jumps and an orange dot at 5/6.
- al-q6: 6 of 7 shaded and parts 3 to 6 crossed out, so 2 are left.
Each alt text, spec and prompt matches its drawing.

## Findings

1. **Prerequisites: simplest form and equivalent fractions are used, but not listed.** SUGGESTION. This is the most important finding.
   Problem: in the topic map this topic depends only on s0-mixed-numbers, which leads back to s0-fractions-number-line. s0-equivalent-fractions is not in its chain. Yet the topic uses equivalent fractions and simplest form in many places:
   - sections[1] (2/5 = 4/10) and sections[3] (3/6 = 1/2)
   - examples[1] ("simplest form")
   - p-5 explanation, p-6 (`simplest` is required), p-8 and q-2 (the stated answers are simplified)
   - q-3 why_wrong (3/8 = 6/16), q-4 and q-7 explanation (1 2/4 = 1 1/2)
   - doubts[3]
   q-4 also compares fractions with different denominators, and s0-comparing-fractions is not a prerequisite either. Because s0-equivalent-fractions is already approved, I assumed it here as the brief says. But on the live site a learner could unlock this topic without having done it, and p-6 would then ask for something never taught.
   Fix: ask curriculum-architect to add s0-equivalent-fractions as a prerequisite. Otherwise, drop the `simplest` requirement from p-6 and add "can be simplified" notes instead.

2. **q-4 (true/false, repeats the lesson).** SUGGESTION.
   Problem: the prompt tells Sunil's wrong sum and then asks whether 3/10 is less than 2/5 (answer True). A child may press "False" to mean "Sunil is wrong". The item also repeats the exact numbers and fact from the hook and sections[1], so it tests memory, not understanding.
   Fix: use new numbers and make the question clearly about the comparison. For example: "Sunil writes $\frac{2}{7} + \frac{3}{7} = \frac{5}{14}$. Is $\frac{5}{14}$ less than $\frac{3}{7}$?" The answer is true, because 3/7 = 6/14.

3. **p-1 and al-p1, al-nl-jumps (dots named only by colour).** SUGGESTION.
   Problem: the p-1 prompt picks out the dots only as "green" and "orange". Orange and green are a classic hard pair for children with red-green colour blindness. The drawing does make the start and end clear by their position.
   Fix: say "the first dot (green)" and "the dot where the jumps land (orange)", and do the same in the alt texts.

4. **Cross-topic: how mixed numbers are typed.** SUGGESTION.
   Problem: "Type it like 2 1/3." here differs from s0-mixed-numbers ("Type a mixed number, like 4 1/3.") and from s0-add-sub-unlike-fractions ("Type your answer as a mixed number, like 2 1/3").
   Fix: use one standard sentence on every site.

5. **hook: "her Mama".** SUGGESTION.
   Problem: in many Indian homes "Mama" means the mother's brother, but in English it means mother. Both readings work, but a child may wonder who is meant.
   Fix: use "Maa" or "Mama-ji" to make it clear, or keep it as it is if the ambiguity does not matter.

## Fixes applied (content-writer)

Status set to `draft`. `verify_content.py`: PASS, 41 checks, 0 fail, 1 warning (q-3 manual MCQ, as before).

1. Prerequisites: no content change needed. `curriculum/topic-map.json` already lists `s0-equivalent-fractions` as a prerequisite of this topic (prerequisites: s0-mixed-numbers, s0-equivalent-fractions). So simplest form, p-6 `simplest` and the equivalent-fraction steps are all covered. The q-4 comparison now uses fourteenths and sevenths (see 2), which needs only renaming from equivalent fractions. s0-comparing-fractions is not needed.
2. q-4: applied as suggested. "Sunil writes 2/7 + 3/7 = 5/14. Is 5/14 less than 3/7?" (true; 3/7 = 6/14). verify is `Lt(Rational(5, 14), Rational(3, 7))`. The hint and explanation are updated.
3. Dots named by colour: applied. The p-1 prompt, hint and explanation say "the first dot (green)" and "the dot where the jumps land (orange)". The al-p1 and al-nl-jumps alt texts say "The first dot (green)" and "a second dot (orange)". The drawings are unchanged (text only), so make.py was not re-run.
4. Mixed-number wording: applied. p-7, p-9 and q-7 end with "Type a mixed number, like 2 1/3." (answers 1 3/8, 2 1/5, 1 1/2). q-7 now asks "How many kilometres does she run in all?" instead of "in km".
5. Hook "her Mama": changed to "her Maa".
Pronouns: Nani (hook) and Thatha (p-8) use no pronoun.

## Re-check

math-verifier, 2026-10-22. Result: **verified** (0 blocking, 0 new findings). Status set to `verified`.

- I read `git diff 2dc6cef HEAD`. `verify_content.py`: 41 pass, 0 fail, 1 manual warning. I re-confirmed q-3 (concept MCQ): only one option is defensible.
- Finding 1: `curriculum/topic-map.json` lists s0-mixed-numbers and s0-equivalent-fractions as the prerequisites, so simplest form is covered.
- New q-4, checked with SymPy: 3/7 = 6/14 and 5/14 < 6/14, so the answer is true. 2/7 + 3/7 = 5/7, which matches the explanation. The question asks only about the comparison, so there is one reading.
- p-1, al-p1 and al-nl-jumps: the text now names each dot by its position and its colour. The rendered SVGs still show the green start dot and the orange landing dot (1/6 to 5/6, and 3/4 to 5/4).
- `mixed` is used on p-7 (11/8 = 1 3/8), p-9 (11/5 = 2 1/5) and q-7 (3/2 = 1 1/2). All three use the shared "Type a mixed number, like 2 1/3." None of them equals 2 1/3. The topic has no improper prompts.
- Hook: "Maa" is fine.
