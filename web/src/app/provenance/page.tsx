import { Database, ExternalLink } from 'lucide-react';

export default function ProvenancePage() {
  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-semibold text-slate-900 dark:text-slate-100 mb-6">
          Data Provenance
        </h1>
        <p className="text-lg text-slate-600 dark:text-slate-400 mb-12">
          Lineage graphs showing how key datasets flow from source to this catalogue
        </p>

        {/* Introduction */}
        <section className="mb-12 prose prose-slate dark:prose-invert max-w-none">
          <p>
            Every dataset in this catalogue has a documented lineage: from official government
            source → retrieval → documentation → publication here. This page visualises the
            provenance chain for 5 representative datasets across different domains and agencies.
          </p>
        </section>

        {/* Provenance Graphs */}
        <div className="space-y-12">
          <ProvenanceGraph
            title="SA Crime Statistics"
            datasetId="sa-crime-statistics-lga"
            steps={[
              {
                label: 'SA Police Data Portal',
                url: 'https://data.sa.gov.au',
                description: 'Official source: aggregate crime counts by LGA and offence type',
                date: '2024-07-15',
              },
              {
                label: 'Download & Verify',
                description:
                  'CSV downloaded, licence verified (CC BY 4.0), field definitions transcribed',
                date: '2024-07-15',
              },
              {
                label: 'Metadata Documentation',
                description:
                  'README created with source URL, retrieval date, temporal coverage (2015-2024), field definitions, known limitations',
                date: '2024-07-16',
              },
              {
                label: 'Catalogue Integration',
                description:
                  'Added to original/datasets/, catalogue.json regenerated, published to GitHub',
                date: '2024-07-16',
              },
            ]}
          />

          <ProvenanceGraph
            title="ABS Population Estimates"
            datasetId="au-population-estimates-lga"
            steps={[
              {
                label: 'ABS.Stat',
                url: 'https://explore.data.abs.gov.au',
                description:
                  'Official source: ABS 3218.0 Regional Population, ERP by LGA and age group',
                date: '2024-07-10',
              },
              {
                label: 'Data Extraction',
                description:
                  'CSV export via ABS.Stat interface, filtered to SA LGAs, years 2016-2023',
                date: '2024-07-10',
              },
              {
                label: 'Licence Verification',
                description:
                  'CC BY 4.0 confirmed from abs.gov.au/website-privacy-copyright-and-disclaimer, attribution requirements documented',
                date: '2024-07-10',
              },
              {
                label: 'Documentation',
                description:
                  'README with ABS catalogue number, retrieval date, field definitions (ERP = Estimated Resident Population), known issue (2021 Census base)',
                date: '2024-07-11',
              },
              {
                label: 'Publication',
                description: 'Added to catalogue, GitHub commit, Vercel deployment',
                date: '2024-07-11',
              },
            ]}
          />

          <ProvenanceGraph
            title="SA Health ED Wait Times"
            datasetId="sa-health-emergency-department-wait-times"
            steps={[
              {
                label: 'SA Health Performance Portal',
                url: 'https://www.sahealth.sa.gov.au/performance',
                description:
                  'Official source: quarterly ED performance metrics by hospital, waiting time categories',
                date: '2024-07-20',
              },
              {
                label: 'Data Retrieval',
                description:
                  'Excel workbook downloaded, sheets consolidated, hospital names standardised',
                date: '2024-07-20',
              },
              {
                label: 'Licence Documentation',
                description:
                  'Crown Copyright with reuse permission from SA Health copyright statement, attribution requirements documented',
                date: '2024-07-20',
              },
              {
                label: 'Metadata Creation',
                description:
                  'README with source URL, retrieval date, temporal coverage (Q1 2018 - Q2 2024), field definitions, known limitation (excludes private hospitals)',
                date: '2024-07-21',
              },
              {
                label: 'Catalogue Addition',
                description: 'Integrated into catalogue, quality checks passed, published',
                date: '2024-07-21',
              },
            ]}
          />

          <ProvenanceGraph
            title="AIHW Specialist Homelessness Services"
            datasetId="au-specialist-homelessness-services"
            steps={[
              {
                label: 'AIHW Data Portal',
                url: 'https://www.aihw.gov.au/reports-data',
                description:
                  'Official source: annual SHS client characteristics, support types, state/territory breakdowns',
                date: '2024-07-12',
              },
              {
                label: 'Download & Reshape',
                description:
                  'Multiple CSV files downloaded, merged by year, SA subset extracted',
                date: '2024-07-12',
              },
              {
                label: 'Licence Verification',
                description:
                  'CC BY 4.0 verified from aihw.gov.au/copyright, attribution requirements (source: AIHW, based on: AIHW for derived work) documented',
                date: '2024-07-12',
              },
              {
                label: 'Documentation',
                description:
                  'README with source, retrieval date, temporal coverage (2011-2023), field definitions, known issue (counting rules changed 2018)',
                date: '2024-07-13',
              },
              {
                label: 'Publication',
                description: 'Added to original/datasets/, catalogue rebuilt, GitHub push',
                date: '2024-07-13',
              },
            ]}
          />

          <ProvenanceGraph
            title="Productivity Commission ROGS"
            datasetId="au-ambulance-services-performance"
            steps={[
              {
                label: 'PC ROGS Data Tables',
                url: 'https://www.pc.gov.au/ongoing/report-on-government-services',
                description:
                  'Official source: Report on Government Services, Ambulance Services chapter, performance indicators by state',
                date: '2024-07-08',
              },
              {
                label: 'Excel Extraction',
                description:
                  'Excel tables downloaded, SA sheets extracted, headers cleaned, years aligned',
                date: '2024-07-08',
              },
              {
                label: 'Licence Confirmation',
                description:
                  'CC BY 4.0 confirmed from pc.gov.au/copyright, no exceptions apply to tabular data',
                date: '2024-07-08',
              },
              {
                label: 'Metadata Documentation',
                description:
                  'README with source URL, retrieval date, temporal coverage (2015-2024), field definitions, known limitation (reporting standards changed 2020)',
                date: '2024-07-09',
              },
              {
                label: 'Catalogue Integration',
                description: 'Added to catalogue, regenerated JSON, deployed',
                date: '2024-07-09',
              },
            ]}
          />
        </div>

        {/* Attribution Chains */}
        <section className="mt-12 bg-slate-50 dark:bg-slate-900/50 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100 mb-4">
            Attribution Requirements
          </h2>
          <div className="prose prose-slate dark:prose-invert max-w-none text-sm">
            <p>
              Every dataset README documents the required attribution. General patterns:
            </p>
            <ul>
              <li>
                <strong>ABS data (CC BY 4.0):</strong> &quot;Source: Australian Bureau of
                Statistics&quot; for unmodified data; &quot;Based on Australian Bureau of
                Statistics data&quot; for reshaped/derived data
              </li>
              <li>
                <strong>AIHW data (CC BY 4.0):</strong> &quot;Source: Australian Institute of
                Health and Welfare&quot; / &quot;Based on Australian Institute of Health and Welfare
                material&quot;
              </li>
              <li>
                <strong>SA Government (CC BY 4.0 or Crown Copyright):</strong> &quot;Source: [Agency
                Name]&quot; or as specified in the agency&apos;s copyright statement
              </li>
              <li>
                <strong>Productivity Commission (CC BY 4.0):</strong> &quot;Source: Productivity
                Commission, Report on Government Services [Year]&quot;
              </li>
            </ul>
            <p>
              This catalogue&apos;s metadata and curation are released under CC0 1.0 Universal (public
              domain). The datasets themselves retain their original licences—see individual README
              files.
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}

function ProvenanceGraph({
  title,
  datasetId,
  steps,
}: {
  title: string;
  datasetId: string;
  steps: Array<{
    label: string;
    url?: string;
    description: string;
    date: string;
  }>;
}) {
  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-8">
      <div className="flex items-start gap-3 mb-6">
        <Database className="h-6 w-6 text-federal-blue mt-1" />
        <div>
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-1">
            {title}
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-500 font-mono">{datasetId}</p>
        </div>
      </div>

      <div className="space-y-6">
        {steps.map((step, index) => (
          <div key={index} className="flex gap-6">
            {/* Timeline indicator */}
            <div className="flex flex-col items-center">
              <div className="w-10 h-10 rounded-full bg-federal-blue/10 dark:bg-federal-blue/20 flex items-center justify-center flex-shrink-0">
                <span className="text-federal-blue font-semibold text-sm">{index + 1}</span>
              </div>
              {index < steps.length - 1 && (
                <div className="w-0.5 flex-1 bg-slate-200 dark:bg-slate-700 mt-2 mb-2 min-h-[40px]" />
              )}
            </div>

            {/* Step content */}
            <div className="flex-1 pb-6">
              <div className="flex items-start justify-between gap-4 mb-2">
                <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                  {step.label}
                  {step.url && (
                    <a
                      href={step.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="ml-2 inline-flex items-center text-federal-blue hover:underline text-sm font-normal"
                    >
                      <ExternalLink className="h-4 w-4" />
                    </a>
                  )}
                </h3>
                <span className="text-sm text-slate-500 dark:text-slate-500 font-mono whitespace-nowrap">
                  {step.date}
                </span>
              </div>
              <p className="text-sm text-slate-600 dark:text-slate-400">{step.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
