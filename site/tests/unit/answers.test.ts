import { describe, expect, it } from 'vitest';
import { checkNumeric, parseAnswer } from '../../src/lib/answers';

describe('parseAnswer', () => {
  it.each([
    ['3/4', { n: 3, d: 4 }],
    [' 3 / 4 ', { n: 3, d: 4 }],
    ['1 1/2', { n: 3, d: 2 }],
    ['0.75', { n: 75, d: 100 }],
    ['.5', { n: 5, d: 10 }],
    ['15', { n: 15, d: 1 }],
    ['₹1,25,000', { n: 125000, d: 1 }],
    ['125,000', { n: 125000, d: 1 }],
    ['−2', { n: -2, d: 1 }],
    ['Rs 20', { n: 20, d: 1 }],
  ])('%s', (input, want) => expect(parseAnswer(input)).toEqual(want));

  it.each(['', 'abc', '3/0', '1/2/3', '3 /', '1,2', '2 3'])('rejects %j', (input) => {
    expect(parseAnswer(input)).toBeNull();
  });
});

describe('checkNumeric', () => {
  it('accepts any equal value by default', () => {
    expect(checkNumeric('1/2', '3/6').status).toBe('correct');
    expect(checkNumeric('0.5', '3/6').status).toBe('correct');
    expect(checkNumeric('2/3', '3/6').status).toBe('wrong');
  });
  it('simplest form needs lowest terms', () => {
    expect(checkNumeric('3/4', '3/4', 'simplest').status).toBe('correct');
    expect(checkNumeric('6/8', '3/4', 'simplest').status).toBe('not-simplest');
    expect(checkNumeric('2', '2', 'simplest').status).toBe('correct');
  });
  it('exact form needs the same numerator and denominator', () => {
    expect(checkNumeric('4/3', '4/3', 'exact').status).toBe('correct');
    expect(checkNumeric('1 1/3', '4/3', 'exact').status).toBe('correct'); // mixed number parses to 4/3
    expect(checkNumeric('8/6', '4/3', 'exact').status).toBe('wrong-form');
    expect(checkNumeric('2', '10/5', 'exact').status).toBe('wrong-form');
  });
  it('reports unreadable input instead of marking it wrong', () => {
    expect(checkNumeric('three quarters', '3/4').status).toBe('unreadable');
  });
});

describe('mixed-number rule', () => {
  it('needs a mixed number with a proper fraction part', () => {
    expect(checkNumeric('2 1/3', '2 1/3', 'mixed').status).toBe('correct');
    expect(checkNumeric('7/3', '2 1/3', 'mixed').status).toBe('not-mixed');
    expect(checkNumeric('1 4/3', '2 1/3', 'mixed').status).toBe('not-mixed');
    expect(checkNumeric('2 2/6', '2 1/3', 'mixed').status).toBe('correct');
    expect(checkNumeric('2 1/2', '2 1/3', 'mixed').status).toBe('wrong');
  });
  it('accepts a whole number when the value is whole', () => {
    expect(checkNumeric('3', '3', 'mixed').status).toBe('correct');
    expect(checkNumeric('6/2', '3', 'mixed').status).toBe('correct');
  });
});

describe('improper-fraction rule', () => {
  it('needs a single fraction, not the mixed number typed back', () => {
    expect(checkNumeric('7/5', '7/5', 'improper').status).toBe('correct');
    expect(checkNumeric('14/10', '7/5', 'improper').status).toBe('correct');
    expect(checkNumeric('1 2/5', '7/5', 'improper').status).toBe('not-improper');
    expect(checkNumeric('1.4', '7/5', 'improper').status).toBe('not-improper');
    expect(checkNumeric('8/5', '7/5', 'improper').status).toBe('wrong');
  });
});

describe('decimal rule', () => {
  it('needs a decimal, not a fraction', () => {
    expect(checkNumeric('0.75', '0.75', 'decimal').status).toBe('correct');
    expect(checkNumeric('.75', '0.75', 'decimal').status).toBe('correct');
    expect(checkNumeric('0.750', '0.75', 'decimal').status).toBe('correct');
    expect(checkNumeric('3/4', '0.75', 'decimal').status).toBe('not-decimal');
    expect(checkNumeric('0.57', '0.75', 'decimal').status).toBe('wrong');
    expect(checkNumeric('₹12.50', '12.5', 'decimal').status).toBe('correct');
  });
});

describe('percent answers', () => {
  it('accepts a trailing % sign on a percent answer stored as a number', () => {
    expect(checkNumeric('25%', '25').status).toBe('correct');
    expect(checkNumeric('25 %', '25').status).toBe('correct');
    expect(checkNumeric('12.5%', '12.5', 'decimal').status).toBe('correct');
    expect(checkNumeric('20%', '25').status).toBe('wrong');
  });
});
