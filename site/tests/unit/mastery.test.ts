import { describe, expect, it } from 'vitest';
import { isMastery, missingPrerequisites, recordQuiz, score, topicState, REVIEW_INTERVALS } from '../../src/lib/mastery';

const NOW = '2026-10-22T00:00:00.000Z';

describe('score and mastery', () => {
  it('80% is mastery, below is not', () => {
    expect(isMastery(score([true, true, true, true, false]))).toBe(true); // 4/5
    expect(isMastery(score([true, true, true, true, true, false, false]))).toBe(false); // 5/7
    expect(isMastery(score([true, true, true, true, true, true, false]))).toBe(true); // 6/7
    expect(score([])).toBe(0);
  });
});

describe('recordQuiz', () => {
  it('first pass masters and schedules a review', () => {
    const p = recordQuiz(undefined, 0.8, NOW);
    expect(p.status).toBe('mastered');
    expect(p.reviewDue).toBe('2026-10-23T00:00:00.000Z');
  });
  it('failing keeps in progress and remembers best score', () => {
    const p = recordQuiz({ status: 'in_progress', best: 0.6 }, 0.4, NOW);
    expect(p).toEqual({ status: 'in_progress', best: 0.6 });
  });
  it('passing a review lengthens the interval', () => {
    const first = recordQuiz(undefined, 1, NOW);
    const second = recordQuiz(first, 1, '2026-10-23T00:00:00.000Z');
    expect(second.reviewStep).toBe(1);
    expect(second.reviewDue).toBe(`2026-10-${23 + REVIEW_INTERVALS[1]}T00:00:00.000Z`);
  });
  it('failing a review does not take mastery away', () => {
    const first = recordQuiz(undefined, 1, NOW);
    expect(recordQuiz(first, 0.2, NOW).status).toBe('mastered');
  });
});

describe('topicState', () => {
  const pub = new Set(['a', 'b']);
  const b = { id: 'b', prerequisites: ['a', 'x'] }; // x has no content yet
  it('locks a topic until published prerequisites are mastered', () => {
    expect(topicState(b, {}, pub, NOW)).toBe('locked');
    expect(missingPrerequisites(b, {}, pub)).toEqual(['a']);
  });
  it('unlocks once they are mastered; unpublished prerequisites do not block', () => {
    const progress = { a: recordQuiz(undefined, 1, NOW) };
    expect(topicState(b, progress, pub, NOW)).toBe('available');
  });
  it('shows review when due', () => {
    const progress = { a: recordQuiz(undefined, 1, NOW) };
    expect(topicState({ id: 'a', prerequisites: [] }, progress, pub, '2026-10-24T00:00:00.000Z')).toBe('review');
  });
  it('marks topics without content as coming', () => {
    expect(topicState({ id: 'z', prerequisites: [] }, {}, pub, NOW)).toBe('coming');
  });
});
