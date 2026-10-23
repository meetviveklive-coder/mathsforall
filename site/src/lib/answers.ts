/**
 * Parse and check learner answers. Pure functions; unit-tested in tests/unit/answers.test.ts.
 *
 * Accepted input forms: "3/4", "3 / 4", "1 1/2" (mixed number), "0.75", "15", "₹1,250", "-2".
 */

export interface Frac {
  n: number; // numerator as typed (may be negative)
  d: number; // denominator as typed (> 0)
}

export type MatchRule = 'value' | 'simplest' | 'exact' | 'mixed' | 'improper' | 'decimal';

export function gcd(a: number, b: number): number {
  a = Math.abs(a);
  b = Math.abs(b);
  while (b) [a, b] = [b, a % b];
  return a;
}

export function reduce(f: Frac): Frac {
  const g = gcd(f.n, f.d) || 1;
  return { n: f.n / g, d: f.d / g };
}

/** Parse a typed answer. Returns null if it is not a number we understand. */
export function parseAnswer(raw: string): Frac | null {
  let t = raw
    .trim()
    .replace(/[₹]/g, '')
    .replace(/^rs\.?\s*/i, '')
    .replace(/[−–]/g, '-') // unicode minus and en dash
    .replace(/\s*\/\s*/g, '/')
    // Percent questions store the number of percent ("25"); a typed "25%" or "25 %" means the same.
    .replace(/\s*%$/, '')
    .trim();
  if (/^-?\d{1,3}(,\d{2,3})+(\.\d+)?$/.test(t)) t = t.replace(/,/g, ''); // 1,25,000 or 125,000

  let m = t.match(/^(-?)(\d+) (\d+)\/(\d+)$/); // mixed number
  if (m) {
    const [, sign, whole, num, den] = m;
    const d = Number(den);
    if (d === 0) return null;
    const n = Number(whole) * d + Number(num);
    return { n: sign ? -n : n, d };
  }
  m = t.match(/^(-?\d+)\/(\d+)$/);
  if (m) {
    const d = Number(m[2]);
    return d === 0 ? null : { n: Number(m[1]), d };
  }
  m = t.match(/^(-?)(\d*)\.(\d+)$/);
  if (m) {
    const d = 10 ** m[3].length;
    const n = Number(m[2] || '0') * d + Number(m[3]);
    return { n: m[1] ? -n : n, d };
  }
  if (/^-?\d+$/.test(t)) return { n: Number(t), d: 1 };
  return null;
}

export function sameValue(a: Frac, b: Frac): boolean {
  return a.n * b.d === b.n * a.d;
}

export type CheckResult =
  | { status: 'correct' }
  | { status: 'wrong' }
  | { status: 'unreadable' }
  | { status: 'not-simplest' } // right value, but the question asks for simplest form
  | { status: 'wrong-form' } // right value, but the question asks for a specific denominator
  | { status: 'not-mixed' } // right value, but the question asks for a mixed number
  | { status: 'not-improper' } // right value, but the question asks for a single fraction like 7/5
  | { status: 'not-decimal' } // right value, but the question asks for a decimal
  | { status: 'not-fraction' }; // right value typed as a decimal, but the question asks for a fraction

/** True when the input is typed as a mixed number with a proper fraction part, e.g. "2 1/3". */
export function isMixedForm(raw: string): boolean {
  const m = raw.trim().replace(/\s*\/\s*/g, '/').match(/^-?(\d+) (\d+)\/(\d+)$/);
  return !!m && Number(m[2]) < Number(m[3]) && Number(m[3]) > 0;
}

/** Check a typed numeric answer against the stored answer using the question's match rule. */
export function checkNumeric(input: string, answer: string, rule: MatchRule = 'value'): CheckResult {
  const got = parseAnswer(input);
  if (!got) return { status: 'unreadable' };
  const want = parseAnswer(answer);
  if (!want) throw new Error(`Stored answer is not a number: ${answer}`);
  if (!sameValue(got, want)) return { status: 'wrong' };
  if (rule === 'simplest' && input.includes('.')) return { status: 'not-fraction' };
  if (rule === 'simplest' && gcd(got.n, got.d) !== 1) return { status: 'not-simplest' };
  if (rule === 'exact' && (got.n !== want.n || got.d !== want.d)) return { status: 'wrong-form' };
  if (rule === 'decimal' && input.includes('/')) return { status: 'not-decimal' };
  if (rule === 'improper' && !/^-?\d+\s*\/\s*\d+$/.test(input.trim())) return { status: 'not-improper' };
  if (rule === 'mixed' && !isMixedForm(input) && !(got.d === 1 || got.n % got.d === 0)) return { status: 'not-mixed' };
  return { status: 'correct' };
}
