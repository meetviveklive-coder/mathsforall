"""End-to-end check of the built pilot site at phone size (360x740).

Usage: python3 tests/e2e/pilot_flow.py <dist-dir> <screenshot-dir>
Serves dist on localhost, then: map renders, practice feedback works, a perfect quiz
masters the topic, the map updates, no console errors, no requests leave localhost.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

dist, shots = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
shots.mkdir(parents=True, exist_ok=True)
REPO = Path(__file__).resolve().parents[3]
topic = json.loads((REPO / "content/topics/s0-fractions-meaning.json").read_text(encoding="utf-8"))

server = subprocess.Popen([sys.executable, "-m", "http.server", "8765", "--directory", str(dist)],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
BASE = "http://localhost:8765"
errors, foreign = [], []
failures = []


def expect(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        failures.append(msg)


def answer_card(card, q):
    if q["type"] == "numeric":
        card.locator("input[type=text]").fill(q["answer"])
    elif q["type"] == "true_false":
        card.locator("input[type=radio]").nth(0 if q["answer"] == "true" else 1).check()
    elif q["type"] == "mcq":
        idx = next(i for i, o in enumerate(q["options"]) if o["correct"])
        card.locator("input[type=radio]").nth(idx).check()


try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 360, "height": 740}, device_scale_factor=2)
        page = ctx.new_page()
        page.on("console", lambda m: m.type == "error" and errors.append(m.text))
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("request", lambda r: (not r.url.startswith(BASE) and not r.url.startswith("data:")) and foreign.append(r.url))

        page.goto(f"{BASE}/index.html")
        page.wait_for_selector("#next-card:not([hidden])")
        expect(page.locator("#next-title").inner_text().strip() != "", "map suggests a next topic")
        expect(page.locator("[data-learner-name]").inner_text() == "Learner 1", "first visit creates 'Learner 1'")
        expect(page.locator('[data-topic="s0-fractions-number-line"]').get_attribute("data-state") == "locked",
               "second topic is locked before the first is mastered")
        page.screenshot(path=str(shots / "01-map.png"))
        width = page.evaluate("document.documentElement.scrollWidth")
        expect(width <= 360, f"no horizontal scroll on map (scrollWidth={width})")

        page.goto(f"{BASE}/learn/s0-fractions-meaning.html")
        page.wait_for_load_state("load")
        expect(page.locator("h1").inner_text() == "Fractions as equal parts", "lesson page opens")
        expect(page.locator(".katex").count() > 10, "maths is rendered with KaTeX")
        expect(page.locator(".visual svg").count() >= 4, "lesson diagrams are inline SVG")
        page.screenshot(path=str(shots / "02-lesson-top.png"))
        page.locator(".lesson-section").nth(1).scroll_into_view_if_needed()
        page.screenshot(path=str(shots / "03-lesson-fraction.png"))
        width = page.evaluate("document.documentElement.scrollWidth")
        expect(width <= 360, f"no horizontal scroll on lesson (scrollWidth={width})")

        # Practice: wrong, hint, then right
        card = page.locator(".q[data-mode=practice]").nth(0)
        card.locator("input[type=text]").fill("1/2")
        card.locator("[data-check]").click()
        expect("Not quite" in card.locator("[data-feedback]").inner_text(), "wrong practice answer gets 'Not quite'")
        card.locator("[data-hint-btn]").click()
        expect(card.locator("[data-hint='0']").is_visible(), "first hint appears")
        card.locator("input[type=text]").fill("1/3")
        card.locator("[data-check]").click()
        expect("Correct" in card.locator("[data-feedback]").inner_text(), "right practice answer gets 'Correct'")
        card.scroll_into_view_if_needed()
        page.screenshot(path=str(shots / "04-practice.png"))

        # MCQ wrong option shows its misconception text
        mcq = page.locator(".q[data-mode=practice]").nth(7)
        mcq.locator("input[type=radio]").nth(1).check()
        mcq.locator("[data-check]").click()
        expect("more" in mcq.locator("[data-feedback]").inner_text().lower(), "wrong MCQ option explains the misconception")

        # Quiz: one wrong first (not mastered), then all right (mastered)
        page.click("#quiz-start")
        cards = page.locator("#quiz-form .q")
        for i, q in enumerate(topic["quiz"]):
            answer_card(cards.nth(i), q)
        cards.nth(0).locator("input[type=text]").fill("3/7")
        cards.nth(4).locator("input[type=text]").fill("6")
        page.click("#quiz-submit")
        expect("5 of 7" in page.locator("#quiz-result").inner_text(), "quiz scores 5 of 7")
        expect("Not mastered" in page.locator("#quiz-result").inner_text(), "5/7 is not mastery")
        page.screenshot(path=str(shots / "05-quiz-keep-going.png"))
        page.get_by_text("Try the check again").click()
        for i, q in enumerate(topic["quiz"]):
            answer_card(cards.nth(i), q)
        page.click("#quiz-submit")
        expect("7 of 7" in page.locator("#quiz-result").inner_text(), "perfect quiz scores 7 of 7")
        expect("mastered this topic" in page.locator("#quiz-result").inner_text(), "topic is mastered")
        page.screenshot(path=str(shots / "06-quiz-mastered.png"))

        page.goto(f"{BASE}/index.html")
        page.wait_for_selector("#next-card:not([hidden])")
        expect(page.locator('[data-topic="s0-fractions-meaning"]').get_attribute("data-state") == "mastered",
               "map shows first topic mastered")
        expect(page.locator('[data-topic="s0-fractions-number-line"]').get_attribute("data-state") == "available",
               "second topic unlocks")
        page.screenshot(path=str(shots / "07-map-after.png"))

        # Second learner: own empty map; switching back restores the first learner's progress
        page.fill("#new-learner", "Meera")
        page.click("#add-learner button[type=submit]")
        page.wait_for_load_state("load")
        page.wait_for_selector("#next-card:not([hidden])")
        expect(page.locator("[data-learner-name]").inner_text() == "Meera", "new learner becomes active")
        expect(page.locator('[data-topic="s0-fractions-meaning"]').get_attribute("data-state") != "mastered",
               "new learner starts with nothing mastered")
        page.locator("#learners").scroll_into_view_if_needed()
        page.screenshot(path=str(shots / "09-learners.png"))
        page.locator("#learner-list button", has_text="Learner 1").click()
        page.wait_for_load_state("load")
        page.wait_for_selector("#next-card:not([hidden])")
        expect(page.locator('[data-topic="s0-fractions-meaning"]').get_attribute("data-state") == "mastered",
               "switching back restores the first learner's progress")
        page.fill("#new-learner", "<img src=x onerror=alert(1)>")
        page.click("#add-learner button[type=submit]")
        page.wait_for_load_state("load")
        expect(page.locator("#learner-list img").count() == 0, "learner names are shown as text, never HTML")

        # Dark mode
        dark = browser.new_context(viewport={"width": 360, "height": 740}, color_scheme="dark", device_scale_factor=2)
        dp = dark.new_page()
        dp.goto(f"{BASE}/learn/s0-equivalent-fractions.html")
        dp.locator(".lesson-section").nth(0).scroll_into_view_if_needed()
        dp.screenshot(path=str(shots / "08-dark.png"))
        for name in ["s0-fractions-number-line", "s0-equivalent-fractions"]:
            page.goto(f"{BASE}/learn/{name}.html")
            expect(page.evaluate("document.documentElement.scrollWidth") <= 360, f"no horizontal scroll on {name}")
        browser.close()
finally:
    server.terminate()

expect(not errors, f"no console errors {errors[:3]}")
expect(not foreign, f"no requests leave the site {foreign[:3]}")
sys.exit(1 if failures else 0)
