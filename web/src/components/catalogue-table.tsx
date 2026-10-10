'use client';

import { useState, useMemo } from 'react';
import { Search, ExternalLink } from 'lucide-react';
import type { Dataset } from '@/lib/catalogue';
import { formatBytes, getLicenceBadge } from '@/lib/catalogue';

interface CatalogueTableProps {
  datasets: Dataset[];
}

export function CatalogueTable({ datasets }: CatalogueTableProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [selectedLicence, setSelectedLicence] = useState<string>('all');

  // Extract unique domains and licences
  const allDomains = useMemo(() => {
    const domainsSet = new Set<string>();
    datasets.forEach((d) => d.domains.forEach((domain) => domainsSet.add(domain)));
    return Array.from(domainsSet).sort();
  }, [datasets]);

  const allLicences = useMemo(() => {
    const licencesSet = new Set<string>();
    datasets.forEach((d) => {
      const badge = getLicenceBadge(d.licence);
      licencesSet.add(badge.short);
    });
    return Array.from(licencesSet).sort();
  }, [datasets]);

  // Filter datasets
  const filteredDatasets = useMemo(() => {
    return datasets.filter((dataset) => {
      const matchesSearch =
        searchQuery === '' ||
        dataset.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        dataset.id.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesDomain =
        selectedDomain === 'all' || dataset.domains.includes(selectedDomain);

      const matchesLicence =
        selectedLicence === 'all' || getLicenceBadge(dataset.licence).short === selectedLicence;

      return matchesSearch && matchesDomain && matchesLicence;
    });
  }, [datasets, searchQuery, selectedDomain, selectedLicence]);

  return (
    <div className="space-y-6">
      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search datasets..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-federal-blue"
          />
        </div>

        <div className="flex gap-4">
          <select
            value={selectedDomain}
            onChange={(e) => setSelectedDomain(e.target.value)}
            className="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-federal-blue"
          >
            <option value="all">All Domains</option>
            {allDomains.map((domain) => (
              <option key={domain} value={domain}>
                {domain.charAt(0).toUpperCase() + domain.slice(1)}
              </option>
            ))}
          </select>

          <select
            value={selectedLicence}
            onChange={(e) => setSelectedLicence(e.target.value)}
            className="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-federal-blue"
          >
            <option value="all">All Licences</option>
            {allLicences.map((licence) => (
              <option key={licence} value={licence}>
                {licence}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Results count */}
      <div className="text-sm text-slate-600 dark:text-slate-400">
        Showing {filteredDatasets.length} of {datasets.length} datasets
      </div>

      {/* Table */}
      <div className="overflow-x-auto border border-slate-200 dark:border-slate-800 rounded-lg">
        <table className="w-full">
          <thead className="bg-slate-50 dark:bg-slate-900/50 border-b border-slate-200 dark:border-slate-800">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                Dataset
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                Domains
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                Licence
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                Coverage
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                Files
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                Size
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                <span className="sr-only">Link</span>
              </th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-slate-950 divide-y divide-slate-200 dark:divide-slate-800">
            {filteredDatasets.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-4 py-8 text-center text-slate-500 dark:text-slate-400">
                  No datasets found matching your filters
                </td>
              </tr>
            ) : (
              filteredDatasets.map((dataset) => (
                <DatasetRow key={dataset.id} dataset={dataset} />
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function DatasetRow({ dataset }: { dataset: Dataset }) {
  const licenceBadge = getLicenceBadge(dataset.licence);
  const githubUrl = `https://github.com/rNLKJA/public-services-open-source-data/tree/main/original/datasets/${dataset.id}`;

  return (
    <tr className="hover:bg-slate-50 dark:hover:bg-slate-900/50 transition-colors">
      <td className="px-4 py-4">
        <div className="flex flex-col">
          <span className="font-medium text-slate-900 dark:text-slate-100">{dataset.name}</span>
          <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">{dataset.id}</span>
        </div>
      </td>
      <td className="px-4 py-4">
        <div className="flex flex-wrap gap-1">
          {dataset.domains.slice(0, 2).map((domain) => (
            <span
              key={domain}
              className="inline-block px-2 py-0.5 text-xs rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
            >
              {domain}
            </span>
          ))}
          {dataset.domains.length > 2 && (
            <span className="inline-block px-2 py-0.5 text-xs rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
              +{dataset.domains.length - 2}
            </span>
          )}
        </div>
      </td>
      <td className="px-4 py-4">
        <span className={`inline-block px-2 py-1 text-xs font-medium rounded ${licenceBadge.color}`}>
          {licenceBadge.short}
        </span>
      </td>
      <td className="px-4 py-4 text-sm text-slate-600 dark:text-slate-400 font-mono">
        {dataset.temporal_coverage}
      </td>
      <td className="px-4 py-4 text-sm text-slate-600 dark:text-slate-400 tabular-nums">
        {dataset.file_count}
      </td>
      <td className="px-4 py-4 text-sm text-slate-600 dark:text-slate-400 tabular-nums">
        {formatBytes(dataset.size_bytes)}
      </td>
      <td className="px-4 py-4">
        <a
          href={githubUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-federal-blue hover:text-federal-blue/80 transition-colors"
          aria-label={`View ${dataset.name} on GitHub`}
        >
          <ExternalLink className="h-4 w-4" />
        </a>
      </td>
    </tr>
  );
}
