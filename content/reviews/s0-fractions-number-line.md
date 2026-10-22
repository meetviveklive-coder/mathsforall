# Review: s0-fractions-number-line

Reviewer: math-verifier, 2026-10-22. Result: **verified** (0 blocking, 4 suggestions).

Checks run: `tools/verify_content.py` (47 pass, 0 fail). I worked out every example, practice and quiz answer again with my own SymPy code, and all values agree. Every visual's `point`, `spaces_per_unit` and labels in `.meta.json` match its alt text and the question that uses it. I reviewed the match rules: p-4, p-7 and q-5 correctly use `exact`, so 8/6, the whole number 2 and 10/4 are not accepted where the question asks for thirds, fifths or halves. The default `value` rule is right for "What fraction does the dot show?" questions.

## Findings

1. **lesson.hook.** SUGGESTION.
   Problem: the hook says "lamp posts that split the way into 4 equal stretches", then asks about "the first lamp post". If there is also a lamp post at her house, the first post is at 0, not $\frac{1}{4}$. That is the same marks-versus-spaces trap this topic teaches about.
   Fix: say "3 lamp posts split the way into 4 equal stretches" and "the first lamp post after her house".

2. **p-6, q-6 (and example 3): "How many quarters/thirds make ...?"** SUGGESTION.
   Problem: the answer is a count (4 or 9). A child who types "4/4" or "9/3" means "four quarters" or "nine thirds", but those values are 1 and 3, so the site marks the answer plain "wrong" with no helpful message. The rule is technically right, but the feedback may confuse the child.
   Fix: end each prompt with "Type a whole number.", or rephrase it as "How many quarter steps go from 0 to 1?".

3. **sections[1].body, doubts[1].a.** SUGGESTION.
   Problem: each of these sentences is 22 words long.
   Fix: split each one into two sentences.

4. **p-3, option $\frac{1}{8}$.** SUGGESTION.
   Problem: the misconception "more spaces than marks" is unlikely, so this distractor is weak.
   Fix: you could replace it with $\frac{1}{5}$ ("not counting the marks at 0 and 1"), which matches a more common mistake.
