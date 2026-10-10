import { describe, it, expect } from 'vitest';
import {
  wilsonInterval,
  bootstrapInterval,
  meanInterval,
  cohensD,
  formatCI,
} from './confidence-intervals';

describe('wilsonInterval', () => {
  it('handles zero sample size', () => {
    const result = wilsonInterval(0, 0);
    expect(result).toEqual({ estimate: 0, lower: 0, upper: 0, n: 0 });
  });

  it('computes correct interval for 50/100', () => {
    const result = wilsonInterval(50, 100);
    expect(result.estimate).toBe(0.5);
    expect(result.n).toBe(100);
    // Wilson interval for 50/100 at 95% confidence should be approximately [0.40, 0.60]
    expect(result.lower).toBeGreaterThan(0.39);
    expect(result.lower).toBeLessThan(0.41);
    expect(result.upper).toBeGreaterThan(0.59);
    expect(result.upper).toBeLessThan(0.61);
  });

  it('handles extreme proportions (0/100)', () => {
    const result = wilsonInterval(0, 100);
    expect(result.estimate).toBe(0);
    expect(result.lower).toBe(0);
    expect(result.upper).toBeGreaterThan(0);
    expect(result.upper).toBeLessThan(0.05);
  });

  it('handles extreme proportions (100/100)', () => {
    const result = wilsonInterval(100, 100);
    expect(result.estimate).toBe(1);
    expect(result.lower).toBeGreaterThan(0.95);
    expect(result.upper).toBeCloseTo(1, 10); // Allow for floating point precision
  });

  it('throws on invalid input', () => {
    expect(() => wilsonInterval(101, 100)).toThrow();
    expect(() => wilsonInterval(-1, 100)).toThrow();
  });

  it('matches known reference values', () => {
    // Reference: Agresti & Coull (1998) Table 1
    // For 81/263 (p=0.308), 95% Wilson interval is approximately [0.252, 0.368]
    const result = wilsonInterval(81, 263);
    expect(result.estimate).toBeCloseTo(0.308, 3);
    expect(result.lower).toBeCloseTo(0.252, 2);
    expect(result.upper).toBeCloseTo(0.368, 2);
  });
});

describe('bootstrapInterval', () => {
  const sampleData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  const mean = (data: number[]) => data.reduce((a, b) => a + b, 0) / data.length;

  it('computes interval for mean', () => {
    const result = bootstrapInterval(sampleData, mean, 0.95, 1000, 42);
    expect(result.estimate).toBe(5.5);
    expect(result.n).toBe(10);
    expect(result.lower).toBeGreaterThan(2);
    expect(result.lower).toBeLessThan(5.5);
    expect(result.upper).toBeGreaterThan(5.5);
    expect(result.upper).toBeLessThan(9);
  });

  it('is reproducible with same seed', () => {
    const result1 = bootstrapInterval(sampleData, mean, 0.95, 1000, 123);
    const result2 = bootstrapInterval(sampleData, mean, 0.95, 1000, 123);
    expect(result1.lower).toBe(result2.lower);
    expect(result1.upper).toBe(result2.upper);
  });

  it('handles empty data', () => {
    const result = bootstrapInterval([], mean);
    expect(result).toEqual({ estimate: 0, lower: 0, upper: 0, n: 0 });
  });

  it('works with custom statistics (median)', () => {
    const median = (data: number[]) => {
      const sorted = [...data].sort((a, b) => a - b);
      const mid = Math.floor(sorted.length / 2);
      return sorted.length % 2 === 0 ? (sorted[mid - 1] + sorted[mid]) / 2 : sorted[mid];
    };

    const result = bootstrapInterval(sampleData, median, 0.95, 1000, 42);
    expect(result.estimate).toBe(5.5);
    expect(result.lower).toBeLessThan(result.estimate);
    expect(result.upper).toBeGreaterThan(result.estimate);
  });
});

describe('meanInterval', () => {
  it('computes t-based interval for normal data', () => {
    // Sample of 10 from N(5, 1)
    const data = [5.1, 4.8, 5.3, 4.9, 5.2, 5.0, 4.7, 5.4, 5.1, 4.9];
    const result = meanInterval(data);

    expect(result.estimate).toBeCloseTo(5.04, 2);
    expect(result.n).toBe(10);
    expect(result.se).toBeGreaterThan(0);
    expect(result.lower).toBeLessThan(result.estimate);
    expect(result.upper).toBeGreaterThan(result.estimate);
    // For n=10, df=9, the margin should be wider than z*se
    expect(result.upper - result.estimate).toBeGreaterThan(1.96 * result.se);
  });

  it('handles single observation', () => {
    const result = meanInterval([5.0]);
    expect(result.estimate).toBe(5.0);
    expect(result.n).toBe(1);
    // With n=1, df=0, confidence interval cannot be computed (infinite width)
    // The function should handle this gracefully
    expect(result.lower).toBeLessThanOrEqual(result.estimate);
    expect(result.upper).toBeGreaterThanOrEqual(result.estimate);
  });

  it('handles empty data', () => {
    const result = meanInterval([]);
    expect(result).toEqual({ estimate: 0, lower: 0, upper: 0, se: 0, n: 0 });
  });

  it('matches known reference for large sample', () => {
    // For n > 30, t-distribution approximates z-distribution
    const data = Array.from({ length: 100 }, (_, i) => i + 1);
    const result = meanInterval(data);
    expect(result.estimate).toBe(50.5);
    expect(result.n).toBe(100);
    // Known variance for 1..100 is (100^2-1)/12 = 833.25
    const expectedSE = Math.sqrt(833.25 / 100);
    expect(result.se).toBeCloseTo(expectedSE, 1);
  });
});

describe('cohensD', () => {
  it('computes effect size for two groups', () => {
    const group1 = [1, 2, 3, 4, 5];
    const group2 = [3, 4, 5, 6, 7];
    const result = cohensD(group1, group2);

    // Mean difference is -2, pooled SD is sqrt(((5-1)*2 + (5-1)*2) / (5+5-2)) = sqrt(2.5) ≈ 1.58
    // d = -2 / 1.58 ≈ -1.26
    expect(result.d).toBeCloseTo(-1.26, 1);
    expect(result.interpretation).toBe('large');
  });

  it('returns zero for identical groups', () => {
    const group = [1, 2, 3, 4, 5];
    const result = cohensD(group, group);
    expect(result.d).toBe(0);
    expect(result.interpretation).toBe('negligible');
  });

  it('classifies effect sizes correctly', () => {
    // Need groups with actual variance where we can control the effect size
    // For small effect (d ≈ 0.2), we need mean diff / pooled SD ≈ 0.2
    // For medium (d ≈ 0.5), mean diff / pooled SD ≈ 0.5
    // For large (d ≈ 0.8+), mean diff / pooled SD ≈ 0.8+

    // Use groups with SD ≈ 10
    const group1 = [40, 45, 50, 55, 60]; // mean = 50, SD ≈ 7.9

    // Small effect: mean diff = 2, d = 2/pooled_sd ≈ 0.25
    const small = [42, 47, 52, 57, 62]; // mean = 52
    const smallResult = cohensD(group1, small);
    expect(smallResult.interpretation).toBe('small');

    // Medium effect: mean diff = 5, d = 5/pooled_sd ≈ 0.63
    const medium = [45, 50, 55, 60, 65]; // mean = 55
    const mediumResult = cohensD(group1, medium);
    expect(mediumResult.interpretation).toBe('medium');

    // Large effect: mean diff = 10, d = 10/pooled_sd ≈ 1.26
    const large = [50, 55, 60, 65, 70]; // mean = 60
    const largeResult = cohensD(group1, large);
    expect(largeResult.interpretation).toBe('large');
  });
});

describe('formatCI', () => {
  it('formats as decimal by default', () => {
    const result = formatCI(0.456, 0.401, 0.511);
    expect(result).toBe('0.46 (95% CI: 0.40–0.51)');
  });

  it('formats as percentage when requested', () => {
    const result = formatCI(0.456, 0.401, 0.511, 1, true);
    expect(result).toBe('45.6% (95% CI: 40.1–51.1%)');
  });

  it('respects decimal places', () => {
    const result = formatCI(0.456789, 0.401234, 0.511987, 4);
    expect(result).toBe('0.4568 (95% CI: 0.4012–0.5120)');
  });

  it('handles zero values', () => {
    const result = formatCI(0, 0, 0.05, 3, true);
    expect(result).toBe('0.000% (95% CI: 0.000–5.000%)');
  });
});
