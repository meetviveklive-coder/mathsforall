/**
 * "Who's learning?" panel on the map page. Names are shown with textContent only.
 * Switching or changing learners reloads the page so the map redraws for that learner.
 */
import {
  learners, addLearner, switchLearner, renameLearner, removeLearner, masteredCount, MAX_LEARNERS,
} from '../lib/progress';

const list = document.getElementById('learner-list')!;
const addForm = document.getElementById('add-learner') as HTMLFormElement;
const addInput = document.getElementById('new-learner') as HTMLInputElement;
const renameForm = document.getElementById('rename-learner') as HTMLFormElement;
const renameInput = document.getElementById('rename-input') as HTMLInputElement;
const removeBtn = document.getElementById('remove-learner') as HTMLButtonElement;
const removeNote = document.getElementById('remove-note')!;
const reload = () => location.reload();

function render() {
  const s = learners();
  const active = s.list.find((l) => l.id === s.active)!;
  list.replaceChildren();
  for (const l of s.list) {
    const li = document.createElement('li');
    const b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('aria-pressed', String(l.id === s.active));
    b.textContent = l.name;
    const n = masteredCount(l.id);
    const c = document.createElement('span');
    c.className = 'count';
    c.textContent = l.id === s.active ? `Learning now · ${n} mastered` : `${n} mastered`;
    b.append(c);
    b.addEventListener('click', () => {
      if (l.id !== s.active) {
        switchLearner(l.id);
        reload();
      }
    });
    li.append(b);
    list.append(li);
  }
  document.getElementById('manage-name')!.textContent = active.name;
  renameInput.value = active.name;
  const onlyOne = s.list.length <= 1;
  removeBtn.hidden = onlyOne;
  removeNote.hidden = !onlyOne;
  addForm.hidden = s.list.length >= MAX_LEARNERS;
}

addForm.addEventListener('submit', (e) => {
  e.preventDefault();
  if (addLearner(addInput.value)) reload();
  else addInput.focus();
});

renameForm.addEventListener('submit', (e) => {
  e.preventDefault();
  if (renameLearner(learners().active, renameInput.value)) reload();
});

// Two-step remove, in the page (browser confirm dialogs are blocked in some embeds).
removeBtn.addEventListener('click', () => {
  if (removeBtn.dataset.confirm !== 'yes') {
    removeBtn.dataset.confirm = 'yes';
    removeBtn.textContent = 'Tap again to remove. This deletes their progress on this device.';
    return;
  }
  if (removeLearner(learners().active)) reload();
});

render();
