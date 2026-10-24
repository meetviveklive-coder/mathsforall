/**
 * On-device progress store, one record per learner. Nothing here leaves the browser.
 *
 * Learners ("Who's learning?") are kept so children sharing one device each get their
 * own map. A learner is only a display name typed by a parent; it is never sent anywhere.
 *
 * Keys:
 *   ganit:learners:v1          { active: id, list: [{ id, name }] }
 *   ganit:progress:v1:<id>     ProgressData for that learner
 *   ganit:progress:v1          legacy single-learner data (pilot); migrated on first use
 *
 * Every access is wrapped: storage can be missing (private mode) or throw.
 */
import type { TopicProgress } from './mastery';

const LEARNERS_KEY = 'ganit:learners:v1';
const LEGACY_KEY = 'ganit:progress:v1';
const progressKey = (id: string) => `${LEGACY_KEY}:${id}`;
export const MAX_NAME = 20;
export const MAX_LEARNERS = 6;

export interface Attempt {
  q: string; // question id
  ok: boolean;
  hint: boolean;
  at: string;
}

export interface ProgressData {
  version: 1;
  topics: Record<string, TopicProgress>;
  attempts: Attempt[];
}

export interface Learner {
  id: string;
  name: string;
}

interface LearnerState {
  active: string;
  list: Learner[];
}

const empty = (): ProgressData => ({ version: 1, topics: {}, attempts: [] });

function read(key: string): string | null {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

function write(key: string, value: string): boolean {
  try {
    localStorage.setItem(key, value);
    return true;
  } catch {
    return false;
  }
}

function remove(key: string): void {
  try {
    localStorage.removeItem(key);
  } catch {
    /* nothing to do */
  }
}

export function storageAvailable(): boolean {
  const k = '__ganit_test__';
  if (!write(k, '1')) return false;
  remove(k);
  return true;
}

/** Keep names short and plain. They are shown with textContent, never as HTML. */
export function cleanName(raw: string): string {
  return raw.replace(/\s+/g, ' ').trim().slice(0, MAX_NAME);
}

function newId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

function parseProgress(raw: string | null): ProgressData {
  if (!raw) return empty();
  try {
    const data = JSON.parse(raw);
    if (data?.version !== 1 || typeof data.topics !== 'object' || data.topics === null) return empty();
    return { version: 1, topics: data.topics, attempts: Array.isArray(data.attempts) ? data.attempts : [] };
  } catch {
    return empty();
  }
}

function saveLearners(state: LearnerState): void {
  write(LEARNERS_KEY, JSON.stringify(state));
}

/** Learner list, creating the first learner (and migrating pilot data) if needed. */
export function learners(): LearnerState {
  try {
    const raw = read(LEARNERS_KEY);
    if (raw) {
      const s = JSON.parse(raw) as LearnerState;
      if (Array.isArray(s.list) && s.list.length && s.list.some((l) => l.id === s.active)) return s;
    }
  } catch {
    /* fall through and rebuild */
  }
  const first: Learner = { id: newId(), name: 'Learner 1' };
  const legacy = read(LEGACY_KEY);
  if (legacy) {
    write(progressKey(first.id), legacy);
    remove(LEGACY_KEY);
  }
  const state = { active: first.id, list: [first] };
  saveLearners(state);
  return state;
}

export function activeLearner(): Learner {
  const s = learners();
  return s.list.find((l) => l.id === s.active)!;
}

export function addLearner(rawName: string): Learner | null {
  const name = cleanName(rawName);
  const s = learners();
  if (!name || s.list.length >= MAX_LEARNERS) return null;
  const l = { id: newId(), name };
  s.list.push(l);
  s.active = l.id;
  saveLearners(s);
  return l;
}

export function switchLearner(id: string): void {
  const s = learners();
  if (s.list.some((l) => l.id === id)) {
    s.active = id;
    saveLearners(s);
  }
}

export function renameLearner(id: string, rawName: string): boolean {
  const name = cleanName(rawName);
  const s = learners();
  const l = s.list.find((x) => x.id === id);
  if (!l || !name) return false;
  l.name = name;
  saveLearners(s);
  return true;
}

/** Remove a learner and their progress. The last learner cannot be removed. */
export function removeLearner(id: string): boolean {
  const s = learners();
  if (s.list.length <= 1 || !s.list.some((l) => l.id === id)) return false;
  s.list = s.list.filter((l) => l.id !== id);
  if (s.active === id) s.active = s.list[0].id;
  saveLearners(s);
  remove(progressKey(id));
  return true;
}

/** Progress for the active learner (or a given one). */
export function load(id: string = activeLearner().id): ProgressData {
  return parseProgress(read(progressKey(id)));
}

export function save(data: ProgressData, id: string = activeLearner().id): boolean {
  // Keep the attempt log bounded so storage never fills up.
  const trimmed = { ...data, attempts: data.attempts.slice(-2000) };
  return write(progressKey(id), JSON.stringify(trimmed));
}

export function update(fn: (d: ProgressData) => void): ProgressData {
  const id = activeLearner().id;
  const d = load(id);
  fn(d);
  save(d, id);
  return d;
}

/** Number of mastered topics, for the learner picker. */
export function masteredCount(id: string): number {
  return Object.values(load(id).topics).filter((t) => t.status === 'mastered').length;
}
