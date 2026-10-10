import Link from 'next/link';
import { FileText, Database, Shield, AlertCircle } from 'lucide-react';

export default function MethodsPage() {
  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-semibold text-slate-900 dark:text-slate-100 mb-6">
          Methods & Methodology
        </h1>
        <p className="text-lg text-slate-600 dark:text-slate-400 mb-12">
          Transparency in data curation, quality assessment, and analytical methods
        </p>

        {/* Data Provenance */}
        <section className="mb-12">
          <div className="flex items-start gap-3 mb-4">
            <Database className="h-6 w-6 text-federal-blue mt-1" />
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
              Data Provenance
            </h2>
          </div>
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <p>
              All datasets in this catalogue originate from official Australian government sources:
            </p>
            <ul>
              <li>
                <strong>Australian Bureau of Statistics (ABS)</strong> — national statistical
                agency; all ABS data released under CC BY 4.0
              </li>
              <li>
                <strong>South Australian Government agencies</strong> — SA Health, SA Police, DEW,
                DIT, CBS, EPA, PIRSA; mix of CC BY 4.0 and Crown Copyright with reuse permissions
              </li>
              <li>
                <strong>Federal agencies</strong> — AIHW, Productivity Commission, Attorney-General&apos;s
                Department, NIAA; predominantly CC BY 4.0
              </li>
            </ul>
            <p>
              Every dataset includes a README with: source URL, retrieval date, licence verbatim
              from the source, field definitions, temporal coverage, and known limitations. No
              unofficial or unattributed data is included.
            </p>
            <p>
              <Link
                href="/provenance"
                className="text-federal-blue hover:underline font-medium"
              >
                View detailed provenance graphs →
              </Link>
            </p>
          </div>
        </section>

        {/* Curation Method */}
        <section className="mb-12">
          <div className="flex items-start gap-3 mb-4">
            <FileText className="h-6 w-6 text-federal-blue mt-1" />
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
              Curation Method
            </h2>
          </div>
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <p>
              Datasets are manually curated (July 2024) using a four-criteria gate documented in{' '}
              <Link
                href="#decision-records"
                className="text-federal-blue hover:underline"
              >
                DR-001
              </Link>
              :
            </p>
            <ol>
              <li>
                <strong>Official source</strong> — published by a government statistical agency or
                department
              </li>
              <li>
                <strong>Aggregate or de-identified</strong> — no individual records; see{' '}
                <Link
                  href="#decision-records"
                  className="text-federal-blue hover:underline"
                >
                  DR-003
                </Link>
              </li>
              <li>
                <strong>Open licence</strong> — CC BY, CC0, or Crown Copyright with explicit reuse
                permissions; see{' '}
                <Link
                  href="#decision-records"
                  className="text-federal-blue hover:underline"
                >
                  DR-002
                </Link>
              </li>
              <li>
                <strong>Complete metadata</strong> — source, retrieval date, field definitions,
                licence
              </li>
            </ol>
            <p>
              This process curated 95 datasets from an initial scan of 120+ candidates. The 25
              excluded datasets failed licence compatibility (8), metadata completeness (9), or
              were microdata-only (8).
            </p>
          </div>
        </section>

        {/* Quality Assessment */}
        <section className="mb-12">
          <div className="flex items-start gap-3 mb-4">
            <Shield className="h-6 w-6 text-federal-blue mt-1" />
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
              Quality Assessment
            </h2>
          </div>
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <p>
              The catalogue tracks three quality dimensions for each dataset:
            </p>
            <ul>
              <li>
                <strong>Completeness</strong> — proportion of expected metadata fields present
                (name, domains, licence, temporal coverage, file count, README path)
              </li>
              <li>
                <strong>Timeliness</strong> — days since last data update; datasets with data from
                the current or previous year are considered current
              </li>
              <li>
                <strong>Documentation</strong> — presence of field definitions, provenance, and
                known limitations in the README
              </li>
            </ul>
            <p>
              Aggregate metrics and per-dataset quality scores are available on the{' '}
              <Link
                href="/quality"
                className="text-federal-blue hover:underline font-medium"
              >
                Data Quality Dashboard
              </Link>
              .
            </p>
          </div>
        </section>

        {/* Statistical Rigour */}
        <section className="mb-12">
          <div className="flex items-start gap-3 mb-4">
            <AlertCircle className="h-6 w-6 text-federal-blue mt-1" />
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
              Statistical Rigour
            </h2>
          </div>
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <p>
              All quantitative results shown on this site include uncertainty quantification:
            </p>
            <ul>
              <li>
                <strong>Proportions</strong> — Wilson score intervals (95% confidence), more
                accurate than Wald intervals for small samples or extreme proportions
              </li>
              <li>
                <strong>Means and custom statistics</strong> — bootstrap percentile intervals
                (10,000 resamples, seeded for reproducibility)
              </li>
              <li>
                <strong>Comparative analyses</strong> — effect sizes (Cohen&apos;s d) reported alongside
                p-values
              </li>
            </ul>
            <p>
              Sample sizes (n) are stated for every estimate. Seeds are fixed and displayed for
              reproducibility. Statistical helper functions are unit-tested against reference values
              from scipy (Python) and R.
            </p>
            <p>
              <Link
                href="/analyses"
                className="text-federal-blue hover:underline font-medium"
              >
                View demo analyses with full uncertainty →
              </Link>
            </p>
          </div>
        </section>

        {/* AI Use Statement */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
            AI Use Statement
          </h2>
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-3">
              Optional AI Features (Bring Your Own Key)
            </h3>
            <div className="prose prose-slate dark:prose-invert max-w-none text-sm">
              <p>
                This site offers <strong>optional</strong> AI-enhanced features that require your
                own API key (Anthropic or OpenAI). The site is fully functional without AI.
              </p>
              <p>
                <strong>What AI does:</strong>
              </p>
              <ul>
                <li>
                  Dataset recommender — suggests relevant datasets based on your research question
                </li>
                <li>
                  Text-to-catalogue-query — answers questions about dataset metadata (not the data
                  itself)
                </li>
              </ul>
              <p>
                <strong>What AI never does:</strong>
              </p>
              <ul>
                <li>Generate statistical results or quantitative claims</li>
                <li>Make policy recommendations or interpret findings</li>
                <li>Access or analyse the actual dataset files (only metadata)</li>
              </ul>
              <p>
                <strong>Privacy & transparency:</strong>
              </p>
              <ul>
                <li>
                  Your API key is stored in your browser (sessionStorage by default, or
                  localStorage if you opt in). It is <strong>never sent to our servers</strong>.
                </li>
                <li>
                  API calls go directly from your browser to Anthropic/OpenAI (Anthropic requires
                  the header <code>anthropic-dangerous-direct-browser-access: true</code>).
                </li>
                <li>
                  Every AI output is visibly labelled &quot;AI-generated&quot; and logged to an audit trail
                  (stored in your browser&apos;s IndexedDB, viewable at{' '}
                  <Link
                    href="/ai-log"
                    className="text-federal-blue hover:underline"
                  >
                    /ai-log
                  </Link>
                  ).
                </li>
                <li>
                  The audit log records: timestamp, feature, provider, model, input (your
                  question), output (AI response), latency, token usage, and your decision
                  (accepted/edited/rejected).
                </li>
                <li>
                  You can export the audit log as JSON for your records or clear it at any time.
                </li>
              </ul>
              <p>
                <strong>Governance alignment:</strong> This approach is informed by the Australian
                DTA&apos;s responsible AI policy (transparency, human oversight, audit trails) and EU AI
                Act transparency principles. It is not a claim of formal compliance.
              </p>
            </div>
          </div>
        </section>

        {/* Assumptions & Limitations */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
            Assumptions & Limitations
          </h2>
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <ul>
              <li>
                <strong>Snapshot at a point in time</strong> — datasets were curated July 2024.
                Government agencies publish updates continuously; this catalogue is not
                automatically synced.
              </li>
              <li>
                <strong>No data validation</strong> — metadata is transcribed from source READMEs.
                The actual data files are not checked for consistency, completeness, or accuracy.
              </li>
              <li>
                <strong>No inferential statistics on original data</strong> — the demo analyses are
                illustrative showcases of method, not research claims. They use synthetic or
                aggregate data only.
              </li>
              <li>
                <strong>Licence interpretation</strong> — licence compatibility decisions (DR-002)
                reflect the maintainer&apos;s interpretation of open licence terms. Users should verify
                licence compliance for their use case.
              </li>
            </ul>
          </div>
        </section>

        {/* What I'd Change */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
            What I&apos;d Change
          </h2>
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <ul>
              <li>
                <strong>Automated sync</strong> — run a weekly scraper to check source URLs for
                updates and flag stale datasets
              </li>
              <li>
                <strong>Data validation</strong> — parse CSV/Excel files to verify field counts,
                data types, and value ranges match README documentation
              </li>
              <li>
                <strong>Cross-dataset join keys</strong> — document common identifiers (LGA codes,
                SA2 codes, year) to enable linked analyses
              </li>
              <li>
                <strong>Contribution workflow</strong> — accept dataset proposals via GitHub issues
                with a structured template (see{' '}
                <a
                  href="https://github.com/rNLKJA/public-services-open-source-data/blob/main/docs/CONTRIBUTING.md"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-federal-blue hover:underline"
                >
                  contribution guide
                </a>
                )
              </li>
              <li>
                <strong>Real consistency checks</strong> — validate that LGA-level totals reconcile
                with state totals across paired datasets (e.g., population estimates vs. health
                service usage)
              </li>
            </ul>
          </div>
        </section>

        {/* Decision Records */}
        <section className="mb-12" id="decision-records">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
            Decision Records
          </h2>
          <p className="text-slate-600 dark:text-slate-400 mb-6">
            Key curation and design decisions, documented with context, options considered, and
            retrospective assessment.
          </p>
          <div className="space-y-4">
            <DecisionRecordCard
              number="001"
              title="Dataset Curation Criteria"
              summary="Four-criteria gate: official source, aggregate data, open licence, complete metadata"
              slug="curation-criteria"
            />
            <DecisionRecordCard
              number="002"
              title="Licence Compatibility Framework"
              summary="Accept CC BY, CC0, and Crown Copyright with reuse; reject NC/ND restrictions"
              slug="licence-compatibility"
            />
            <DecisionRecordCard
              number="003"
              title="Aggregation Levels and Privacy"
              summary="Aggregate-only, SA2+ geography, no microdata or individual time series"
              slug="aggregation-privacy"
            />
          </div>
        </section>
      </div>
    </div>
  );
}

function DecisionRecordCard({
  number,
  title,
  summary,
  slug,
}: {
  number: string;
  title: string;
  summary: string;
  slug: string;
}) {
  return (
    <Link
      href={`https://github.com/rNLKJA/public-services-open-source-data/blob/main/docs/decisions/DR-${number}-${slug}.md`}
      target="_blank"
      rel="noopener noreferrer"
      className="block p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg hover:border-federal-blue dark:hover:border-federal-blue transition-colors"
    >
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0">
          <div className="w-12 h-12 rounded-lg bg-federal-blue/10 dark:bg-federal-blue/20 flex items-center justify-center">
            <span className="text-federal-blue font-mono font-semibold">{number}</span>
          </div>
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-2">
            DR-{number}: {title}
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400">{summary}</p>
        </div>
        <div className="flex-shrink-0">
          <FileText className="h-5 w-5 text-slate-400" />
        </div>
      </div>
    </Link>
  );
}
