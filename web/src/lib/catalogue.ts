import catalogueData from '../../public/data/catalogue.json';

export interface Dataset {
  id: string;
  name: string;
  domains: string[];
  licence: string;
  temporal_coverage: string;
  file_count: number;
  size_bytes: number;
  readme_path: string;
}

export interface CatalogueData {
  generated: string;
  dataset_count: number;
  datasets: Dataset[];
}

export function getCatalogueData(): CatalogueData {
  return catalogueData as CatalogueData;
}

export function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${Math.round((bytes / Math.pow(k, i)) * 10) / 10} ${sizes[i]}`;
}

export function getLicenceBadge(licence: string): { short: string; color: string } {
  if (licence.includes('CC BY 4.0') || licence.includes('Creative Commons Attribution 4.0')) {
    return { short: 'CC BY 4.0', color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' };
  }
  if (licence.includes('Crown Copyright')) {
    return { short: 'Crown Copyright', color: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400' };
  }
  if (licence.includes('CC0')) {
    return { short: 'CC0', color: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400' };
  }
  return { short: 'Other', color: 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-400' };
}
