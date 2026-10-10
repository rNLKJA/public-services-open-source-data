/**
 * Statistical confidence interval calculations
 *
 * Provides rigorous uncertainty quantification for proportions and means.
 * All methods return 95% confidence intervals unless specified otherwise.
 */

/**
 * Wilson score interval for binomial proportions (Agresti & Coull, 1998)
 *
 * More accurate than the Wald interval, especially for small samples or proportions near 0 or 1.
 *
 * @param successes - Number of successes
 * @param n - Total number of trials
 * @param confidence - Confidence level (default 0.95)
 * @returns Object with point estimate, lower and upper bounds
 *
 * Reference: Agresti, A., & Coull, B. A. (1998). Approximate is better than "exact"
 * for interval estimation of binomial proportions. The American Statistician, 52(2), 119-126.
 */
export function wilsonInterval(
  successes: number,
  n: number,
  confidence = 0.95
): { estimate: number; lower: number; upper: number; n: number } {
  if (n === 0) {
    return { estimate: 0, lower: 0, upper: 0, n: 0 };
  }

  if (successes < 0 || successes > n) {
    throw new Error('successes must be between 0 and n');
  }

  const p = successes / n;
  const z = getZScore(confidence);
  const z2 = z * z;

  const denominator = 1 + z2 / n;
  const center = (p + z2 / (2 * n)) / denominator;
  const margin = (z / denominator) * Math.sqrt((p * (1 - p)) / n + z2 / (4 * n * n));

  return {
    estimate: p,
    lower: Math.max(0, center - margin),
    upper: Math.min(1, center + margin),
    n,
  };
}

/**
 * Bootstrap percentile confidence interval for any statistic
 *
 * Non-parametric method that makes no distributional assumptions.
 * Suitable for means, medians, or any other statistic.
 *
 * @param data - Array of numeric observations
 * @param statFn - Function that computes the statistic (e.g., mean, median)
 * @param confidence - Confidence level (default 0.95)
 * @param nBootstrap - Number of bootstrap samples (default 10000)
 * @param seed - Random seed for reproducibility
 * @returns Object with point estimate, lower and upper bounds
 */
export function bootstrapInterval(
  data: number[],
  statFn: (sample: number[]) => number,
  confidence = 0.95,
  nBootstrap = 10000,
  seed?: number
): { estimate: number; lower: number; upper: number; n: number } {
  if (data.length === 0) {
    return { estimate: 0, lower: 0, upper: 0, n: 0 };
  }

  const rng = seed !== undefined ? seededRandom(seed) : Math.random;
  const n = data.length;
  const estimate = statFn(data);

  // Generate bootstrap samples
  const bootstrapStats: number[] = [];
  for (let i = 0; i < nBootstrap; i++) {
    const sample: number[] = [];
    for (let j = 0; j < n; j++) {
      sample.push(data[Math.floor(rng() * n)]);
    }
    bootstrapStats.push(statFn(sample));
  }

  // Sort and extract percentiles
  bootstrapStats.sort((a, b) => a - b);
  const alpha = 1 - confidence;
  const lowerIndex = Math.floor((alpha / 2) * nBootstrap);
  const upperIndex = Math.ceil((1 - alpha / 2) * nBootstrap) - 1;

  return {
    estimate,
    lower: bootstrapStats[lowerIndex],
    upper: bootstrapStats[upperIndex],
    n,
  };
}

/**
 * Confidence interval for the mean using t-distribution
 *
 * Assumes normally distributed data. For non-normal data, use bootstrapInterval.
 *
 * @param data - Array of numeric observations
 * @param confidence - Confidence level (default 0.95)
 * @returns Object with mean, lower and upper bounds, standard error
 */
export function meanInterval(
  data: number[],
  confidence = 0.95
): { estimate: number; lower: number; upper: number; se: number; n: number } {
  if (data.length === 0) {
    return { estimate: 0, lower: 0, upper: 0, se: 0, n: 0 };
  }

  const n = data.length;
  const mean = data.reduce((sum, x) => sum + x, 0) / n;

  if (n === 1) {
    // Cannot compute confidence interval with df=0
    return { estimate: mean, lower: mean, upper: mean, se: 0, n: 1 };
  }

  const variance = data.reduce((sum, x) => sum + Math.pow(x - mean, 2), 0) / (n - 1);
  const se = Math.sqrt(variance / n);
  const t = getTScore(confidence, n - 1);
  const margin = t * se;

  return {
    estimate: mean,
    lower: mean - margin,
    upper: mean + margin,
    se,
    n,
  };
}

/**
 * Get z-score for a given confidence level (two-tailed)
 */
function getZScore(confidence: number): number {
  // Common confidence levels
  const zScores: Record<number, number> = {
    0.90: 1.645,
    0.95: 1.96,
    0.99: 2.576,
    0.999: 3.291,
  };

  if (confidence in zScores) {
    return zScores[confidence];
  }

  // Approximate for other levels using inverse normal
  // This is a rough approximation - for production use, consider a proper implementation
  throw new Error(`Unsupported confidence level: ${confidence}. Use 0.90, 0.95, 0.99, or 0.999`);
}

/**
 * Get t-score for a given confidence level and degrees of freedom
 *
 * Uses approximations for common confidence levels.
 * For df > 30, approximates with z-score.
 */
function getTScore(confidence: number, df: number): number {
  if (df > 30) {
    return getZScore(confidence);
  }

  // Critical values for 95% confidence, selected degrees of freedom
  const t95: Record<number, number> = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    15: 2.131, 20: 2.086, 25: 2.060, 30: 2.042,
  };

  if (confidence === 0.95) {
    if (df in t95) {
      return t95[df];
    }
    // Linear interpolation for intermediate values
    const keys = Object.keys(t95).map(Number).sort((a, b) => a - b);
    for (let i = 0; i < keys.length - 1; i++) {
      if (df > keys[i] && df < keys[i + 1]) {
        const t1 = t95[keys[i]];
        const t2 = t95[keys[i + 1]];
        const ratio = (df - keys[i]) / (keys[i + 1] - keys[i]);
        return t1 + ratio * (t2 - t1);
      }
    }
  }

  throw new Error(`Unsupported confidence level or df: ${confidence}, ${df}`);
}

/**
 * Simple seeded pseudo-random number generator (Linear Congruential Generator)
 *
 * Returns a function that generates pseudo-random numbers in [0, 1).
 * Used for reproducible bootstrap sampling.
 */
function seededRandom(seed: number): () => number {
  let state = seed;
  return () => {
    // LCG parameters from Numerical Recipes
    state = (state * 1664525 + 1013904223) % 4294967296;
    return state / 4294967296;
  };
}

/**
 * Calculate effect size (Cohen's d) for two independent samples
 *
 * @param group1 - First group observations
 * @param group2 - Second group observations
 * @returns Cohen's d and interpretation
 */
export function cohensD(
  group1: number[],
  group2: number[]
): { d: number; interpretation: string } {
  const mean1 = group1.reduce((sum, x) => sum + x, 0) / group1.length;
  const mean2 = group2.reduce((sum, x) => sum + x, 0) / group2.length;

  const var1 = group1.reduce((sum, x) => sum + Math.pow(x - mean1, 2), 0) / (group1.length - 1);
  const var2 = group2.reduce((sum, x) => sum + Math.pow(x - mean2, 2), 0) / (group2.length - 1);

  const pooledSD = Math.sqrt((var1 + var2) / 2);
  const d = (mean1 - mean2) / pooledSD;

  let interpretation = 'negligible';
  const absD = Math.abs(d);
  if (absD >= 0.8) interpretation = 'large';
  else if (absD >= 0.5) interpretation = 'medium';
  else if (absD >= 0.2) interpretation = 'small';

  return { d, interpretation };
}

/**
 * Format a confidence interval for display
 *
 * @param estimate - Point estimate
 * @param lower - Lower bound
 * @param upper - Upper bound
 * @param decimals - Number of decimal places (default 2)
 * @param asPercentage - Format as percentage (default false)
 * @returns Formatted string like "0.45 (95% CI: 0.40–0.50)"
 */
export function formatCI(
  estimate: number,
  lower: number,
  upper: number,
  decimals = 2,
  asPercentage = false
): string {
  const multiplier = asPercentage ? 100 : 1;
  const suffix = asPercentage ? '%' : '';

  const est = (estimate * multiplier).toFixed(decimals);
  const lo = (lower * multiplier).toFixed(decimals);
  const up = (upper * multiplier).toFixed(decimals);

  return `${est}${suffix} (95% CI: ${lo}–${up}${suffix})`;
}
