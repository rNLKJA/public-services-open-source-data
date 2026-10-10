import Link from 'next/link';
import { Database, Search, BarChart3, Download, ArrowRight } from 'lucide-react';
import { HeroDatasets } from '@/components/hero-datasets';

export default function Home() {
  return (
    <div className="flex flex-col">
      {/* Hero section */}
      <section className="relative bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950 border-b border-slate-200 dark:border-slate-800">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-federal-blue/10 dark:bg-federal-blue/20 text-federal-blue text-sm font-medium mb-6">
              <Database className="h-4 w-4" />
              95+ Government Datasets
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight text-slate-900 dark:text-slate-100 mb-6">
              SA & AU Open Data Atlas
            </h1>
            <p className="text-lg sm:text-xl text-slate-600 dark:text-slate-400 mb-8 leading-relaxed">
              A curated, sourced collection of South Australian and Australian government datasets
              for public-service research, policy analysis and civic tools. Every dataset traces
              back to an official government source with licence, retrieval date and field
              definitions documented.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                href="/catalogue"
                className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-federal-blue text-white font-medium hover:bg-federal-blue/90 transition-colors"
              >
                Browse Catalogue
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                href="/about"
                className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-medium hover:bg-slate-100 dark:hover:bg-slate-900 transition-colors"
              >
                About This Project
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Hero datasets showcase */}
      <section className="py-16 bg-white dark:bg-slate-950">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl sm:text-3xl font-semibold text-slate-900 dark:text-slate-100 mb-3">
            Featured Datasets
          </h2>
          <p className="text-slate-600 dark:text-slate-400 mb-8">
            Explore a selection of high-impact datasets from across the catalogue
          </p>
          <HeroDatasets />
        </div>
      </section>

      {/* Features section */}
      <section className="py-16 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl sm:text-3xl font-semibold text-slate-900 dark:text-slate-100 mb-12 text-center">
            What You&apos;ll Find
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <FeatureCard
              icon={<Search className="h-6 w-6" />}
              title="Searchable Catalogue"
              description="Filter by domain, licence, and temporal coverage to find the datasets you need"
            />
            <FeatureCard
              icon={<BarChart3 className="h-6 w-6" />}
              title="Metadata Quality"
              description="Every dataset includes source, licence, retrieval date, field definitions and known issues"
            />
            <FeatureCard
              icon={<Database className="h-6 w-6" />}
              title="Diverse Domains"
              description="95+ datasets across health, justice, education, infrastructure, environment and more"
            />
            <FeatureCard
              icon={<Download className="h-6 w-6" />}
              title="Open Access"
              description="Predominantly CC BY 4.0 licenced data from official government sources"
            />
          </div>
        </div>
      </section>

      {/* Domains section */}
      <section className="py-16 bg-white dark:bg-slate-950">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl sm:text-3xl font-semibold text-slate-900 dark:text-slate-100 mb-8">
            Data Domains
          </h2>
          <div className="flex flex-wrap gap-3">
            {[
              'Health',
              'Justice',
              'Education',
              'Infrastructure',
              'Environment',
              'Social Services',
              'Planning',
              'Economy',
              'Demographics',
              'Governance',
            ].map((domain) => (
              <Link
                key={domain}
                href={`/catalogue?domain=${domain.toLowerCase().replace(' ', '-')}`}
                className="px-4 py-2 rounded-full border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:border-federal-blue hover:text-federal-blue dark:hover:border-federal-blue dark:hover:text-federal-blue transition-colors text-sm font-medium"
              >
                {domain}
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* CTA section */}
      <section className="py-16 bg-slate-50 dark:bg-slate-900/50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-2xl sm:text-3xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
            Start Exploring
          </h2>
          <p className="text-slate-600 dark:text-slate-400 mb-8 max-w-2xl mx-auto">
            Browse the full catalogue to discover open government data for your research, analysis
            or civic project.
          </p>
          <Link
            href="/catalogue"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-federal-blue text-white font-medium hover:bg-federal-blue/90 transition-colors"
          >
            View All Datasets
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="flex flex-col items-start gap-3">
      <div className="p-3 rounded-lg bg-federal-blue/10 dark:bg-federal-blue/20 text-federal-blue">
        {icon}
      </div>
      <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">{title}</h3>
      <p className="text-sm text-slate-600 dark:text-slate-400">{description}</p>
    </div>
  );
}
