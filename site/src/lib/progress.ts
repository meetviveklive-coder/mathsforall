/**
 * On-device progress store. Nothing here leaves the learner's browser.
 *
 * Pilot uses localStorage (one small JSON value). docs/DATABASE.md §5 describes the
 * IndexedDB store planned for Phase 4; the data shape is the same so migration is a copy.
 * Every access is wrapped: storage can be missing (private mode) or throw.
 */
import type { TopicProgress } from './mastery';

const KEY = 'ganit:progress:v1';

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

const empty = (): ProgressData => ({ version: 1, topics: {}, attempts: [] });

export function storageAvailable(): boolean {
  try {
    const k = '__ganit_test__';
    localStorage.setItem(k, '1');
    localStorage.removeItem(k);
    return true;
  } catch {
    return false;
  }
}

export function load(): ProgressData {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return empty();
    const data = JSON.parse(raw);
    if (data?.version !== 1 || typeof data.topics !== 'object') return empty();
    return { version: 1, topics: data.topics ?? {}, attempts: Array.isArray(data.attempts) ? data.attempts : [] };
  } catch {
    return empty();
  }
}

export function save(data: ProgressData): boolean {
  try {
    // Keep the attempt log bounded so storage never fills up.
    const trimmed = { ...data, attempts: data.attempts.slice(-2000) };
    localStorage.setItem(KEY, JSON.stringify(trimmed));
    return true;
  } catch {
    return false;
  }
}

export function update(fn: (d: ProgressData) => void): ProgressData {
  const d = load();
  fn(d);
  save(d);
  return d;
}

export function reset(): void {
  try {
    localStorage.removeItem(KEY);
  } catch {
    /* nothing to do */
  }
}
