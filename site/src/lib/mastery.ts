/**
 * Mastery, unlocking and review scheduling. Pure functions; unit-tested.
 */

export const MASTERY_THRESHOLD = 0.8;
/** Days until the next review after each successful review (expanding intervals). */
export const REVIEW_INTERVALS = [1, 3, 7, 14, 30, 60];

export interface TopicProgress {
  status: 'in_progress' | 'mastered';
  best: number; // best quiz score 0..1
  masteredAt?: string; // ISO date
  reviewDue?: string; // ISO date
  reviewStep?: number; // index into REVIEW_INTERVALS
}

export type TopicState = 'coming' | 'locked' | 'available' | 'in_progress' | 'mastered' | 'review';

export interface MapTopic {
  id: string;
  prerequisites: string[];
}

export function score(results: boolean[]): number {
  return results.length ? results.filter(Boolean).length / results.length : 0;
}

export function isMastery(fraction: number): boolean {
  // Compare with a small tolerance so 4/5 counts as 80%.
  return fraction + 1e-9 >= MASTERY_THRESHOLD;
}

export function addDays(iso: string, days: number): string {
  const d = new Date(iso);
  d.setUTCDate(d.getUTCDate() + days);
  return d.toISOString();
}

/** Record a finished quiz and return the new progress for the topic. */
export function recordQuiz(prev: TopicProgress | undefined, fraction: number, nowIso: string): TopicProgress {
  const best = Math.max(prev?.best ?? 0, fraction);
  if (!isMastery(fraction)) {
    return prev?.status === 'mastered' ? { ...prev, best } : { status: 'in_progress', best };
  }
  if (prev?.status === 'mastered') {
    // Passing again (a review) moves to the next, longer interval.
    const step = Math.min((prev.reviewStep ?? 0) + 1, REVIEW_INTERVALS.length - 1);
    return { ...prev, best, reviewStep: step, reviewDue: addDays(nowIso, REVIEW_INTERVALS[step]) };
  }
  return { status: 'mastered', best, masteredAt: nowIso, reviewStep: 0, reviewDue: addDays(nowIso, REVIEW_INTERVALS[0]) };
}

/**
 * State of a topic on the knowledge map.
 * Pilot rule: a prerequisite with no published content yet counts as satisfied,
 * because there is no way to learn it here (the placement check will replace this).
 */
export function topicState(
  topic: MapTopic,
  progress: Record<string, TopicProgress>,
  published: Set<string>,
  nowIso: string,
): TopicState {
  if (!published.has(topic.id)) return 'coming';
  const p = progress[topic.id];
  if (p?.status === 'mastered') {
    return p.reviewDue && p.reviewDue <= nowIso ? 'review' : 'mastered';
  }
  const ready = topic.prerequisites.every((id) => !published.has(id) || progress[id]?.status === 'mastered');
  if (!ready) return 'locked';
  return p ? 'in_progress' : 'available';
}

/** Prerequisites that block a topic, for the "learn this first" message. */
export function missingPrerequisites(
  topic: MapTopic,
  progress: Record<string, TopicProgress>,
  published: Set<string>,
): string[] {
  return topic.prerequisites.filter((id) => published.has(id) && progress[id]?.status !== 'mastered');
}
