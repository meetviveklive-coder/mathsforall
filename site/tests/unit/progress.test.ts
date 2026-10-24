import { beforeEach, describe, expect, it } from 'vitest';

class MemStorage {
  m = new Map<string, string>();
  getItem(k: string) { return this.m.has(k) ? this.m.get(k)! : null; }
  setItem(k: string, v: string) { this.m.set(k, String(v)); }
  removeItem(k: string) { this.m.delete(k); }
  clear() { this.m.clear(); }
}
const mem = new MemStorage();
(globalThis as unknown as { localStorage: MemStorage }).localStorage = mem;

const P = await import('../../src/lib/progress');

beforeEach(() => mem.clear());

describe('learners', () => {
  it('creates a first learner on first use', () => {
    const s = P.learners();
    expect(s.list).toHaveLength(1);
    expect(P.activeLearner().name).toBe('Learner 1');
  });

  it('migrates pilot progress to the first learner', () => {
    mem.setItem('ganit:progress:v1', JSON.stringify({ version: 1, topics: { a: { status: 'mastered', best: 1 } }, attempts: [] }));
    expect(P.load().topics.a.status).toBe('mastered');
    expect(mem.getItem('ganit:progress:v1')).toBeNull();
  });

  it('keeps each learner\'s progress separate', () => {
    const first = P.activeLearner();
    P.update((d) => { d.topics.x = { status: 'mastered', best: 1 }; });
    const second = P.addLearner('  Meera  ')!;
    expect(second.name).toBe('Meera');
    expect(P.activeLearner().id).toBe(second.id);
    expect(P.load().topics.x).toBeUndefined();
    P.switchLearner(first.id);
    expect(P.load().topics.x.status).toBe('mastered');
    expect(P.masteredCount(first.id)).toBe(1);
    expect(P.masteredCount(second.id)).toBe(0);
  });

  it('renames, limits names, and refuses empty names', () => {
    const id = P.activeLearner().id;
    expect(P.renameLearner(id, 'A very long name that goes on and on')).toBe(true);
    expect(P.activeLearner().name).toHaveLength(P.MAX_NAME);
    expect(P.renameLearner(id, '   ')).toBe(false);
    expect(P.addLearner('')).toBeNull();
  });

  it('removes a learner and their progress, but never the last one', () => {
    const first = P.activeLearner();
    expect(P.removeLearner(first.id)).toBe(false);
    const second = P.addLearner('Asha')!;
    P.update((d) => { d.topics.y = { status: 'mastered', best: 1 }; });
    expect(P.removeLearner(second.id)).toBe(true);
    expect(P.activeLearner().id).toBe(first.id);
    expect(mem.getItem(`ganit:progress:v1:${second.id}`)).toBeNull();
  });

  it('caps the number of learners', () => {
    for (let i = 0; i < 10; i++) P.addLearner(`L${i}`);
    expect(P.learners().list).toHaveLength(P.MAX_LEARNERS);
  });
});
