/**
 * Lesson page behaviour: practice feedback and hints, the mastery check, and saving progress.
 * All feedback text is pre-rendered in the page; this script only shows, hides and copies it.
 */
import { checkNumeric, type MatchRule } from '../lib/answers';
import { missingPrerequisites, recordQuiz, score, isMastery, REVIEW_INTERVALS } from '../lib/mastery';
import { load, update, storageAvailable } from '../lib/progress';

interface ClientQuestion {
  id: string;
  type: 'numeric' | 'mcq' | 'true_false' | 'text';
  answer: string;
  match: MatchRule;
  accept: string[];
  correct: number;
}
interface PageData {
  topic: { id: string; prerequisites: string[] };
  published: string[];
  titles: Record<string, string>;
  next: { id: string; title: string } | null;
}

type Verdict = { ok: boolean; message: string; chosen?: number; empty?: boolean };

const page = JSON.parse(document.getElementById('page-data')!.textContent!) as PageData;
const nowIso = () => new Date().toISOString();

// ---------------------------------------------------------------- gate: unmastered prerequisites
{
  const progress = load().topics;
  const missing = missingPrerequisites(page.topic, progress, new Set(page.published));
  if (missing.length) {
    const list = document.getElementById('gate-list')!;
    missing.forEach((id, i) => {
      if (i) list.append(', ');
      const a = document.createElement('a');
      a.href = `${id}.html`;
      a.textContent = page.titles[id];
      list.append(a);
    });
    document.getElementById('gate')!.hidden = false;
  }
}

// ---------------------------------------------------------------- grading
function judge(card: HTMLElement): Verdict {
  const q = JSON.parse(card.dataset.q!) as ClientQuestion;
  if (q.type === 'mcq' || q.type === 'true_false') {
    const picked = card.querySelector<HTMLInputElement>('input[type=radio]:checked');
    if (!picked) return { ok: false, empty: true, message: 'Choose an answer first.' };
    const chosen = Number(picked.value);
    const correct = q.type === 'mcq' ? q.correct : q.answer === 'true' ? 0 : 1;
    return { ok: chosen === correct, chosen, message: chosen === correct ? 'Correct.' : 'Not quite.' };
  }
  const input = card.querySelector<HTMLInputElement>('input[type=text]')!;
  const value = input.value.trim();
  if (!value) return { ok: false, empty: true, message: 'Type your answer first.' };
  if (q.type === 'text') {
    const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
    const ok = [q.answer, ...q.accept].some((a) => norm(a) === norm(value));
    return { ok, message: ok ? 'Correct.' : 'Not quite.' };
  }
  const r = checkNumeric(value, q.answer, q.match);
  switch (r.status) {
    case 'correct': return { ok: true, message: 'Correct.' };
    case 'unreadable': return { ok: false, empty: true, message: 'Type a number like 3/4, 1 1/2 or 0.75.' };
    case 'not-simplest': return { ok: false, message: 'That is the right amount, but it can be simplified further.' };
    case 'wrong-form': return { ok: false, message: 'That is the right amount, but write it the way the question asks.' };
    case 'not-mixed': return { ok: false, message: 'That is the right amount. Now write it as a mixed number, like 2 1/3.' };
    default: return { ok: false, message: 'Not quite.' };
  }
}

function showFeedback(card: HTMLElement, v: Verdict, withExplanation: boolean) {
  const box = card.querySelector<HTMLElement>('[data-feedback]')!;
  box.className = `feedback ${v.ok ? 'ok' : v.empty ? '' : 'no'}`;
  box.replaceChildren();
  const head = document.createElement('p');
  head.innerHTML = `<strong>${v.ok ? '✓ ' : ''}${v.message}</strong>`;
  box.append(head);
  if (!v.ok && v.chosen !== undefined) {
    const why = card.querySelector<HTMLTemplateElement>(`template[data-why="${v.chosen}"]`);
    if (why) box.append(why.content.cloneNode(true));
  }
  if (withExplanation) {
    const ex = card.querySelector<HTMLTemplateElement>('template[data-explain]');
    if (ex) box.append(ex.content.cloneNode(true));
  }
  card.querySelectorAll('.option').forEach((el) => el.classList.remove('is-right', 'is-wrong'));
  if (v.chosen !== undefined) {
    card.querySelectorAll('.option')[v.chosen]?.classList.add(v.ok ? 'is-right' : 'is-wrong');
  }
}

function logAttempt(card: HTMLElement, ok: boolean, hint: boolean) {
  const q = JSON.parse(card.dataset.q!) as ClientQuestion;
  update((d) => d.attempts.push({ q: q.id, ok, hint, at: nowIso() }));
}

// ---------------------------------------------------------------- practice
document.querySelectorAll<HTMLElement>('.q[data-mode=practice]').forEach((card) => {
  let tries = 0;
  let hintsShown = 0;
  let logged = false;
  const hints = card.querySelectorAll<HTMLElement>('[data-hint]');
  const hintBtn = card.querySelector<HTMLButtonElement>('[data-hint-btn]')!;
  const reveal = card.querySelector<HTMLButtonElement>('[data-reveal]')!;

  const check = () => {
    const v = judge(card);
    if (v.empty) return showFeedback(card, v, false);
    tries += 1;
    if (!logged) {
      logAttempt(card, v.ok, hintsShown > 0);
      logged = true;
    }
    showFeedback(card, v, v.ok);
    if (!v.ok && tries >= 2) reveal.hidden = false;
  };
  card.querySelector('[data-check]')!.addEventListener('click', check);
  card.querySelector('input[type=text]')?.addEventListener('keydown', (e) => {
    if ((e as KeyboardEvent).key === 'Enter') check();
  });
  hintBtn.addEventListener('click', () => {
    if (hintsShown < hints.length) hints[hintsShown++].hidden = false;
    if (hintsShown >= hints.length) hintBtn.disabled = true;
  });
  reveal.addEventListener('click', () => {
    showFeedback(card, { ok: false, message: 'Here is how to get it:' }, true);
    reveal.hidden = true;
  });
});

// ---------------------------------------------------------------- mastery check
const form = document.getElementById('quiz-form') as HTMLFormElement;
const intro = document.getElementById('quiz-intro')!;
const result = document.getElementById('quiz-result')!;

document.getElementById('quiz-start')!.addEventListener('click', () => {
  intro.hidden = true;
  form.hidden = false;
  form.querySelector<HTMLElement>('.q input')?.focus();
});

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const cards = [...form.querySelectorAll<HTMLElement>('.q')];
  const verdicts = cards.map(judge);
  const unanswered = verdicts.filter((v) => v.empty).length;
  // In-page confirmation (browser confirm() dialogs are blocked in some embeds).
  const submitBtn = form.querySelector<HTMLButtonElement>('button[type=submit]')!;
  if (unanswered && submitBtn.dataset.confirm !== 'yes') {
    submitBtn.dataset.confirm = 'yes';
    submitBtn.textContent = `${unanswered} not answered. Check anyway`;
    cards.find((c, i) => verdicts[i].empty)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }
  submitBtn.dataset.confirm = '';
  submitBtn.textContent = 'Check my answers';

  cards.forEach((card, i) => {
    const v = verdicts[i].empty ? { ok: false, message: 'Not answered.' } : verdicts[i];
    showFeedback(card, v, !v.ok);
    logAttempt(card, v.ok, false);
  });
  const results = verdicts.map((v) => v.ok);
  const s = score(results);
  const got = results.filter(Boolean).length;
  const saved = update((d) => {
    d.topics[page.topic.id] = recordQuiz(d.topics[page.topic.id], s, nowIso());
  }).topics[page.topic.id];

  result.replaceChildren();
  const scoreP = document.createElement('p');
  scoreP.className = 'score';
  scoreP.textContent = `${got} of ${results.length} right`;
  result.append(scoreP);
  const msg = document.createElement('p');
  if (isMastery(s)) {
    result.className = 'card result mastered';
    const days = REVIEW_INTERVALS[saved.reviewStep ?? 0];
    msg.textContent = `You have mastered this topic. It will come back for a short review in ${days} day${days > 1 ? 's' : ''}, so it stays fresh.`;
    result.append(msg);
    if (page.next) {
      const a = document.createElement('a');
      a.className = 'btn';
      a.href = `${page.next.id}.html`;
      a.textContent = `Next: ${page.next.title}`;
      result.append(a);
    }
  } else {
    result.className = 'card result keep-going';
    msg.textContent = 'Not mastered yet, and that is fine. Read the explanations above, look back at the lesson, and try again when you are ready. There is no limit and no penalty.';
    result.append(msg);
    const again = document.createElement('button');
    again.type = 'button';
    again.className = 'btn secondary';
    again.textContent = 'Try the check again';
    again.addEventListener('click', () => {
      form.reset();
      cards.forEach((c) => {
        c.querySelector('[data-feedback]')!.replaceChildren();
        c.querySelectorAll('.option').forEach((el) => el.classList.remove('is-right', 'is-wrong'));
      });
      result.hidden = true;
      cards[0].scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    result.append(again);
  }
  if (!storageAvailable()) {
    const warn = document.createElement('p');
    warn.className = 'small muted';
    warn.textContent = 'Your browser is not saving progress on this device, so this result will not be kept.';
    result.append(warn);
  }
  result.hidden = false;
  result.scrollIntoView({ behavior: 'smooth', block: 'start' });
});
