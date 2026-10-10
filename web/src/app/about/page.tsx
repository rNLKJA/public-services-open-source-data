import { Database, FileText, Shield, Globe } from 'lucide-react';

export const metadata = {
  title: 'About - SA & AU Open Data Atlas',
  description:
    'Learn about the SA & AU Open Data Atlas: a personal data curation project documenting 95+ open government datasets.',
};

export default function AboutPage() {
  return (
    <div className="py-12 bg-white dark:bg-slate-950">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
        <h1 className="text-3xl sm:text-4xl font-semibold text-slate-900 dark:text-slate-100 mb-8">
          About This Project
        </h1>

        <div className="prose prose-slate dark:prose-invert max-w-none">
          <section className="mb-12">
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
              What This Is
            </h2>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed mb-4">
              The SA & AU Open Data Atlas is a curated collection of 95+ open South Australian and
              Australian government datasets for public-service research, policy analysis and civic
              tools. Every dataset in the catalogue traces back to an official government source
              with licence, retrieval date and field definitions documented.
            </p>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
              This is a <strong>personal data curation project</strong> started in July 2026. The
              contribution here is documentation, provenance tracking and metadata quality — not
              original statistical analysis or research findings.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
              What You&apos;ll Find
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <FeatureBox
                icon={<Database className="h-6 w-6" />}
                title="95+ Datasets"
                description="Spanning education, health, justice, infrastructure, environment, social services, planning, economy, demographics and governance"
              />
              <FeatureBox
                icon={<FileText className="h-6 w-6" />}
                title="Complete Documentation"
                description="Every dataset includes source URL, licence, retrieval date, field definitions, coverage period and known issues"
              />
              <FeatureBox
                icon={<Shield className="h-6 w-6" />}
                title="Traced Provenance"
                description="PROVENANCE.md files document data lineage from original government publication to processed files"
              />
              <FeatureBox
                icon={<Globe className="h-6 w-6" />}
                title="Open Licences"
                description="Predominantly CC BY 4.0 from ABS, SA Government agencies, Productivity Commission and AIHW"
              />
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
              Data Sources
            </h2>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed mb-4">
              All datasets are aggregate or de-identified public releases from official sources:
            </p>
            <ul className="list-disc list-inside text-slate-600 dark:text-slate-400 space-y-2">
              <li>Australian Bureau of Statistics (ABS)</li>
              <li>SA Government agencies (CBS, DIT, DEW, SA Health, SA Police, EPA, PIRSA)</li>
              <li>Productivity Commission</li>
              <li>Australian Institute of Health and Welfare (AIHW)</li>
              <li>Federal agencies and statutory bodies</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
              Civic Purpose
            </h2>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
              This catalogue supports transparency, evidence-based policy and civic participation.
              Open government data enables researchers, journalists, community organisations and
              citizens to understand public services, track outcomes and build tools that serve the
              public interest. By documenting and linking these datasets, this project lowers the
              barrier to working with Australian public data.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
              Technical Stack
            </h2>
            <div className="bg-slate-50 dark:bg-slate-900/50 rounded-lg p-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
                <div>
                  <h3 className="font-semibold text-slate-900 dark:text-slate-100 mb-2">
                    Original Catalogue
                  </h3>
                  <ul className="space-y-1 text-slate-600 dark:text-slate-400">
                    <li>CSV, Excel, GeoJSON</li>
                    <li>Python data processing</li>
                    <li>Markdown documentation</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900 dark:text-slate-100 mb-2">
                    Web Application
                  </h3>
                  <ul className="space-y-1 text-slate-600 dark:text-slate-400">
                    <li>Next.js 16 (App Router)</li>
                    <li>TypeScript, React 19</li>
                    <li>Tailwind CSS v4</li>
                    <li>Deployed on Vercel</li>
                  </ul>
                </div>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
              Licences
            </h2>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed mb-4">
              <strong>Catalogue metadata:</strong> CC0 1.0 Universal — the documentation, curation
              and metadata are dedicated to the public domain.
            </p>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
              <strong>Datasets:</strong> Each dataset retains its original government licence
              (predominantly CC BY 4.0 or Crown Copyright with reuse permissions). See individual
              dataset README files for specific licence terms and attribution requirements.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
              Repository
            </h2>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed mb-4">
              The full catalogue, including raw data files, documentation and this web application,
              is available on GitHub:
            </p>
            <a
              href="https://github.com/rNLKJA/public-services-open-source-data"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-900 dark:bg-slate-800 text-white font-medium hover:bg-slate-800 dark:hover:bg-slate-700 transition-colors"
            >
              <Globe className="h-4 w-4" />
              View on GitHub
            </a>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
              Contact
            </h2>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
              This project is maintained by{' '}
              <a
                href="https://github.com/rNLKJA"
                target="_blank"
                rel="noopener noreferrer"
                className="text-federal-blue hover:underline"
              >
                Sunchuangyu &quot;Rin&quot; Huang
              </a>
              . For questions about the catalogue or to suggest datasets, please open an issue on
              the GitHub repository.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}

function FeatureBox({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="flex gap-4">
      <div className="flex-shrink-0 p-2 rounded-lg bg-federal-blue/10 dark:bg-federal-blue/20 text-federal-blue h-fit">
        {icon}
      </div>
      <div>
        <h3 className="font-semibold text-slate-900 dark:text-slate-100 mb-1">{title}</h3>
        <p className="text-sm text-slate-600 dark:text-slate-400">{description}</p>
      </div>
    </div>
  );
}
