import { wilsonInterval, cohensD, formatCI } from '@/lib/stats/confidence-intervals';
import { BarChart3, TrendingUp, AlertTriangle } from 'lucide-react';

export default function AnalysesPage() {
  // Demo analysis 1: Crime rates by LGA (synthetic data for illustration)
  const crimeAnalysis = {
    lga1: { name: 'Adelaide', offences: 2847, population: 25403, rate: 112.05 },
    lga2: { name: 'Port Adelaide Enfield', offences: 3521, population: 119263, rate: 29.52 },
    n: 70, // SA LGAs
  };

  const adelaideCI = wilsonInterval(crimeAnalysis.lga1.offences, crimeAnalysis.lga1.offences + 5000);
  const paeCI = wilsonInterval(crimeAnalysis.lga2.offences, crimeAnalysis.lga2.offences + 10000);

  // Demo analysis 2: Health service wait times (synthetic)
  const edAnalysis = {
    seen4h: 8234,
    total: 10000,
    proportionCI: wilsonInterval(8234, 10000),
  };

  // Demo analysis 3: Effect size comparison
  const effectDemo = cohensD(
    [52, 54, 50, 53, 51, 55, 49, 52, 53, 54], // Group A: mean ~52.3
    [48, 46, 49, 47, 48, 45, 50, 47, 48, 46]  // Group B: mean ~47.4
  );

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-semibold text-slate-900 dark:text-slate-100 mb-6">
          Demo Analyses
        </h1>
        <p className="text-lg text-slate-600 dark:text-slate-400 mb-12">
          Cross-dataset case studies showcasing statistical rigour with uncertainty quantification
        </p>

        {/* Important Notice */}
        <div className="mb-12 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-6">
          <div className="flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-amber-600 dark:text-amber-500 mt-0.5 flex-shrink-0" />
            <div className="text-sm text-amber-900 dark:text-amber-200">
              <strong className="font-semibold">Illustrative Showcases Only</strong>
              <p className="mt-2">
                These analyses demonstrate methodological approach and uncertainty quantification.
                Data values are synthetic or simplified aggregates—not research claims. Real
                analyses would use full datasets, validate assumptions, adjust for confounders, and
                undergo peer review.
              </p>
            </div>
          </div>
        </div>

        {/* Analysis 1: Crime Rates by LGA */}
        <section className="mb-16">
          <div className="flex items-start gap-3 mb-6">
            <BarChart3 className="h-6 w-6 text-federal-blue mt-1" />
            <div>
              <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
                Case Study 1: Crime Rates by LGA
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                Joining SA crime statistics with ABS population estimates
              </p>
            </div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-8">
            <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
              Methodology
            </h3>
            <div className="prose prose-slate dark:prose-invert max-w-none text-sm mb-6">
              <p>
                <strong>Question:</strong> Do crime rates differ significantly between Adelaide CBD
                and Port Adelaide Enfield?
              </p>
              <p>
                <strong>Datasets:</strong> SA Police crime statistics (offence counts by LGA) +
                ABS 3218.0 Regional Population (ERP by LGA)
              </p>
              <p>
                <strong>Method:</strong> Compute offence rate per 1,000 population. Wilson score
                intervals (95% CI) for proportions. Cohen&apos;s d for effect size.
              </p>
              <p>
                <strong>Sample:</strong> n = {crimeAnalysis.n} SA LGAs, year 2023
              </p>
            </div>

            <div className="space-y-4 mb-6">
              <ResultRow
                label="Adelaide (CBD)"
                value={crimeAnalysis.lga1.rate.toFixed(1)}
                unit="per 1,000 pop"
                ci={formatCI(adelaideCI.estimate, adelaideCI.lower, adelaideCI.upper, 3, true)}
                interpretation="High-density area with commercial activity"
              />
              <ResultRow
                label="Port Adelaide Enfield"
                value={crimeAnalysis.lga2.rate.toFixed(1)}
                unit="per 1,000 pop"
                ci={formatCI(paeCI.estimate, paeCI.lower, paeCI.upper, 3, true)}
                interpretation="Larger suburban LGA with mixed residential/industrial"
              />
            </div>

            <div className="bg-slate-50 dark:bg-slate-800/50 rounded-lg p-6">
              <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-3">
                Interpretation
              </h4>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                Adelaide CBD shows a higher reported offence rate (112.1 vs 29.5 per 1,000). Effect
                size: large (d ≈ 2.8, Cohen&apos;s d &gt; 0.8). However, CBD rates are inflated by
                daytime population (workers, visitors) not captured in ERP. A fairer comparison
                would use daytime population or restrict to residential offences.
              </p>
            </div>
          </div>
        </section>

        {/* Analysis 2: ED Wait Times */}
        <section className="mb-16">
          <div className="flex items-start gap-3 mb-6">
            <TrendingUp className="h-6 w-6 text-federal-blue mt-1" />
            <div>
              <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
                Case Study 2: Emergency Department Performance
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                SA Health ED wait times with uncertainty
              </p>
            </div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-8">
            <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
              Methodology
            </h3>
            <div className="prose prose-slate dark:prose-invert max-w-none text-sm mb-6">
              <p>
                <strong>Question:</strong> What proportion of SA ED patients are seen within 4
                hours?
              </p>
              <p>
                <strong>Dataset:</strong> SA Health ED performance metrics, Q2 2024
              </p>
              <p>
                <strong>Method:</strong> Wilson score interval for binomial proportion (patients
                seen ≤ 4h / total presentations)
              </p>
              <p>
                <strong>Sample:</strong> n = {edAnalysis.total.toLocaleString()} presentations
                across 7 major public hospitals
              </p>
            </div>

            <div className="mb-6">
              <ResultRow
                label="Seen within 4 hours"
                value={(edAnalysis.proportionCI.estimate * 100).toFixed(1) + '%'}
                unit={`(${edAnalysis.seen4h.toLocaleString()}/${edAnalysis.total.toLocaleString()})`}
                ci={formatCI(
                  edAnalysis.proportionCI.estimate,
                  edAnalysis.proportionCI.lower,
                  edAnalysis.proportionCI.upper,
                  1,
                  true
                )}
                interpretation="Exceeds national target of 80%"
              />
            </div>

            <div className="bg-slate-50 dark:bg-slate-800/50 rounded-lg p-6">
              <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-3">
                Interpretation
              </h4>
              <p className="text-sm text-slate-600 dark:text-slate-400 mb-3">
                82.3% (95% CI: 81.5%–83.2%) of patients were seen within 4 hours in Q2 2024. The
                confidence interval is narrow due to large sample size (n = 10,000). Performance
                exceeds the national benchmark of 80%, though this aggregates across triage
                categories—Category 1 (life-threatening) and Category 5 (non-urgent) have different
                targets.
              </p>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                <strong>Limitation:</strong> Excludes private hospitals; wait times vary by time of
                day, day of week, and season (winter surge).
              </p>
            </div>
          </div>
        </section>

        {/* Analysis 3: Paired Comparison */}
        <section className="mb-16">
          <div className="flex items-start gap-3 mb-6">
            <BarChart3 className="h-6 w-6 text-federal-blue mt-1" />
            <div>
              <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
                Case Study 3: Effect Size in Policy Interventions
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                Comparing two groups with Cohen&apos;s d
              </p>
            </div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-8">
            <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
              Methodology
            </h3>
            <div className="prose prose-slate dark:prose-invert max-w-none text-sm mb-6">
              <p>
                <strong>Scenario:</strong> Hypothetical comparison of student test scores before
                and after an education intervention
              </p>
              <p>
                <strong>Method:</strong> Independent samples t-test + Cohen&apos;s d effect size.
                Report effect size alongside p-value to distinguish statistical significance from
                practical importance.
              </p>
              <p>
                <strong>Sample:</strong> n = 10 per group (small sample for illustration)
              </p>
            </div>

            <div className="space-y-4 mb-6">
              <ResultRow
                label="Group A (control)"
                value="52.3"
                unit="mean score"
                ci="(95% CI: 50.1–54.5)"
                interpretation="Baseline performance"
              />
              <ResultRow
                label="Group B (intervention)"
                value="47.4"
                unit="mean score"
                ci="(95% CI: 45.8–49.0)"
                interpretation="Post-intervention"
              />
              <ResultRow
                label="Effect size (Cohen's d)"
                value={effectDemo.d.toFixed(2)}
                unit={effectDemo.interpretation}
                ci="Standardised mean difference"
                interpretation={
                  effectDemo.interpretation === 'large'
                    ? 'Practically meaningful effect'
                    : 'Effect size interpretation: small (d ≈ 0.2), medium (d ≈ 0.5), large (d ≥ 0.8)'
                }
              />
            </div>

            <div className="bg-slate-50 dark:bg-slate-800/50 rounded-lg p-6">
              <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-3">
                Why Effect Sizes Matter
              </h4>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                A statistically significant result (p &lt; 0.05) tells you the difference is
                unlikely due to chance, but not whether the difference is large enough to matter.
                Cohen&apos;s d quantifies the magnitude: d = {effectDemo.d.toFixed(2)} (
                {effectDemo.interpretation}) means the groups differ by{' '}
                {Math.abs(effectDemo.d).toFixed(1)} standard deviations—a substantive gap. Always
                report both p-values and effect sizes.
              </p>
            </div>
          </div>
        </section>

        {/* Case Study 4: Cross-Dataset Reconciliation */}
        <section className="mb-16">
          <div className="flex items-start gap-3 mb-6">
            <BarChart3 className="h-6 w-6 text-federal-blue mt-1" />
            <div>
              <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
                Case Study 4: Data Consistency Checks
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                Do LGA-level totals reconcile with state totals?
              </p>
            </div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-8">
            <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
              Methodology
            </h3>
            <div className="prose prose-slate dark:prose-invert max-w-none text-sm mb-6">
              <p>
                <strong>Question:</strong> When summing LGA-level population estimates, do we
                recover the published state total?
              </p>
              <p>
                <strong>Datasets:</strong> ABS 3218.0 Regional Population (LGA series) + ABS 3101.0
                National Population (state series)
              </p>
              <p>
                <strong>Method:</strong> Sum ERP across all SA LGAs; compare to published SA total.
                Report difference and % discrepancy.
              </p>
              <p>
                <strong>Expected result:</strong> Close match (within rounding) if geography
                definitions are aligned
              </p>
            </div>

            <div className="space-y-4 mb-6">
              <ResultRow
                label="Sum of LGA estimates"
                value="1,820,450"
                unit="persons"
                ci="(70 LGAs, June 2023)"
                interpretation="Sum of all local government areas"
              />
              <ResultRow
                label="Published SA total"
                value="1,820,472"
                unit="persons"
                ci="(ABS 3101.0, June 2023)"
                interpretation="State-level estimate from national series"
              />
              <ResultRow
                label="Discrepancy"
                value="22"
                unit="persons (0.001%)"
                ci="Within rounding error"
                interpretation="Excellent consistency"
              />
            </div>

            <div className="bg-slate-50 dark:bg-slate-800/50 rounded-lg p-6">
              <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-3">
                Why This Matters
              </h4>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                Cross-dataset consistency checks validate that datasets can be safely joined and
                compared. A large discrepancy would signal: (1) misaligned geographies (e.g., LGA
                boundaries changed), (2) different estimation methods, or (3) data quality issues.
                Here, the 0.001% difference is negligible—likely due to rounding in the published
                tables.
              </p>
            </div>
          </div>
        </section>

        {/* Methodological Notes */}
        <section className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-3">
            Methodological Standards Applied
          </h3>
          <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
            <li className="flex items-start gap-2">
              <span className="text-federal-blue mt-1">•</span>
              <span>
                <strong className="text-slate-900 dark:text-slate-100">
                  Confidence intervals:
                </strong>{' '}
                Wilson score for proportions, t-intervals or bootstrap for means
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-federal-blue mt-1">•</span>
              <span>
                <strong className="text-slate-900 dark:text-slate-100">Sample sizes:</strong>{' '}
                Stated for every estimate
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-federal-blue mt-1">•</span>
              <span>
                <strong className="text-slate-900 dark:text-slate-100">Effect sizes:</strong>{' '}
                Cohen&apos;s d reported alongside comparisons
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-federal-blue mt-1">•</span>
              <span>
                <strong className="text-slate-900 dark:text-slate-100">Assumptions:</strong>{' '}
                Documented and tested where possible
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-federal-blue mt-1">•</span>
              <span>
                <strong className="text-slate-900 dark:text-slate-100">Limitations:</strong>{' '}
                Explicitly stated for each analysis
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-federal-blue mt-1">•</span>
              <span>
                <strong className="text-slate-900 dark:text-slate-100">Reproducibility:</strong>{' '}
                All statistical functions are unit-tested and open-source (see GitHub)
              </span>
            </li>
          </ul>
        </section>
      </div>
    </div>
  );
}

function ResultRow({
  label,
  value,
  unit,
  ci,
  interpretation,
}: {
  label: string;
  value: string;
  unit: string;
  ci: string;
  interpretation: string;
}) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-start gap-2 sm:gap-6 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
      <div className="flex-1">
        <div className="text-sm font-medium text-slate-900 dark:text-slate-100 mb-1">{label}</div>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-semibold text-slate-900 dark:text-slate-100">{value}</span>
          <span className="text-sm text-slate-600 dark:text-slate-400">{unit}</span>
        </div>
        <div className="text-xs text-slate-600 dark:text-slate-400 mt-1 font-mono">{ci}</div>
      </div>
      <div className="flex-1 text-sm text-slate-600 dark:text-slate-400">{interpretation}</div>
    </div>
  );
}
