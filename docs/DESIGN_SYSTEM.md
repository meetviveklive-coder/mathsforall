# Design System

## 1. Design Direction
Style: Calm, warm, editorial — a good notebook, not a game.
Mood: Unhurried and encouraging. Nothing on screen should create pressure.
Design Principles:
- One idea per screen on mobile.
- Maths is the hero: generous size for equations and diagrams.
- Progress is shown as growth (a map lighting up), never as rank or score against others.
- No timers, no red "FAIL" screens; wrong answers lead to an explanation, not a penalty.

## 2. Brand
Brand Name: Ganit (working name)
Logo: Text wordmark only until a name is final.
Brand Voice: A patient older sibling. Short sentences. "Let's see why" rather than "Wrong!".

## 3. Color Palette
Defined as CSS tokens on `:root`, with a dark-mode set.
Primary: #2F6F62 (deep teal — actions, links)
Secondary: #C2703D (terracotta — highlights in diagrams)
Background: #FBF8F3 (paper)
Surface: #FFFFFF
Text: #1F2421
Muted Text: #5C6660
Border: #E3DDD3
Success: #2E7D4F
Warning: #B7791F
Error: #B44A3A (used for explanations of mistakes, never full-screen)
Dark mode: Background #161A18, Surface #1F2421, Text #ECE8E1, Muted #A3ABA6, Border #333A36; Primary lightened to #6FB5A5.
All text/background pairs must meet WCAG AA (4.5:1 body, 3:1 large).

## 4. Typography
Font Family: System UI stack (no web-font download — slow networks).
Heading Font: system-ui
Body Font: system-ui
Maths: KaTeX default fonts (self-hosted, subset).
H1: 1.75rem / 700 / 1.25
H2: 1.375rem / 650 / 1.3
H3: 1.125rem / 600 / 1.35
Body: 1.0625rem / 400 / 1.6 (17px — readable for children)
Small: 0.875rem / 400 / 1.5

## 5. Spacing
Base Unit: 4px
Spacing Scale: 4px / 8px / 12px / 16px / 24px / 32px / 48px / 64px / 96px
Page side gutter on mobile: 16px.

## 6. Border Radius
Small: 6px
Medium: 10px
Large: 16px
Pill: 999px

## 7. Shadows
Small: none — use borders.
Medium: 0 1px 3px rgba(0,0,0,.08) for cards only.
Large: not used.

## 8. Buttons
Primary Button: Teal fill, white text, min height 48px (touch target), radius Medium.
Secondary Button: Transparent, teal border and text.
Danger Button: Only for "Reset progress"; requires confirmation.
Disabled: 40% opacity, no pointer.
Loading: Label stays; small spinner left of label.

## 9. Inputs
Default: 48px height, 1px border, radius Small, font-size ≥ 16px (prevents mobile zoom).
Focus: 2px teal outline, offset 2px.
Error: Terracotta border plus text message below (not colour alone).
Disabled: Muted background.
Placeholder: Muted text, never used as the only label.
Numeric answers: `inputmode="decimal"`; fraction answers accept "3/4".

## 10. Cards
Padding 16px (mobile) / 24px (desktop), 1px border, radius Medium, Medium shadow.

## 11. Navigation
Header: Wordmark left; "Map" and "Review" right. No hamburger needed at MVP.
Sidebar: None.
Mobile Navigation: Lesson pages have a sticky bottom bar with Back / Next.

## 12. States
Loading: Skeleton lines, not spinners, for lesson content.
Empty: Knowledge map with nothing mastered shows "Start here" on the first available topic.
Error: Plain message plus "Try again"; content is static so errors are rare.
Success: Quiet check mark and one encouraging sentence; no confetti.
Disabled: Locked topics show a lock icon and the prerequisite's name.

## 13. Icons
Icon Library: Inline SVG, hand-picked set (no icon font).
Default Size: 20px
Icon Style: Outline, 1.75px stroke.

## 14. Responsive Design
Mobile: Single column, max content width 100%.
Tablet: Single column, max width 680px centred.
Desktop: Content max width 720px; knowledge map may use full width.
Breakpoints:
Mobile: < 640px
Tablet: 640–1023px
Desktop: ≥ 1024px

## 15. Accessibility
- Use semantic HTML
- Maintain sufficient contrast (AA)
- Support keyboard navigation for every quiz interaction
- Provide visible focus states
- Provide accessible labels; every diagram has alt text that states its mathematical content
- Do not rely only on colour (correct/incorrect also use icons and words)
- KaTeX output includes MathML for screen readers
