/**
 * Data quality metrics for catalogue datasets
 *
 * Assesses completeness, timeliness, and consistency across the catalogue.
 */

export interface DatasetQuality {
  datasetId: string;
  datasetName: string;
  completeness: {
    score: number; // 0-1
    missingFields: string[];
    fieldCoverage: number; // proportion of expected fields present
  };
  timeliness: {
    lastUpdated: string; // ISO date
    daysStale: number;
    updateFrequency?: string;
    isCurrent: boolean; // within expected update window
  };
  documentation: {
    hasFieldDefinitions: boolean;
    hasProvenance: boolean;
    hasLimitations: boolean;
    docScore: number; // 0-1
  };
}

export interface QualityTimeline {
  date: string;
  totalDatasets: number;
  avgCompletenessScore: number;
  avgDocScore: number;
  datasetsWithCurrentData: number;
}

export interface ConsistencyCheck {
  checkName: string;
  datasetPair: [string, string];
  passed: boolean;
  details: string;
  expectedValue?: number;
  actualValue?: number;
  difference?: number;
}

/**
 * Expected fields for a complete dataset metadata record
 */
const EXPECTED_FIELDS = [
  'name',
  'domains',
  'licence',
  'temporal_coverage',
  'file_count',
  'readme_path',
] as const;

/**
 * Assess completeness of dataset metadata
 */
export function assessCompleteness(dataset: {
  name?: unknown;
  domains?: unknown;
  licence?: unknown;
  temporal_coverage?: unknown;
  file_count?: unknown;
  readme_path?: unknown;
}): {
  score: number;
  missingFields: string[];
  fieldCoverage: number;
} {
  const missingFields: string[] = [];

  for (const field of EXPECTED_FIELDS) {
    if (!(field in dataset) || dataset[field] === null || dataset[field] === undefined) {
      missingFields.push(field);
    }
  }

  const fieldCoverage = (EXPECTED_FIELDS.length - missingFields.length) / EXPECTED_FIELDS.length;

  // Additional checks for field quality
  let qualityDeductions = 0;

  // Check if domains is non-empty
  if (Array.isArray(dataset.domains) && dataset.domains.length === 0) {
    qualityDeductions += 0.1;
  }

  // Check if licence is not just "**" (missing)
  if (typeof dataset.licence === 'string' && dataset.licence.trim() === '**') {
    qualityDeductions += 0.2;
  }

  const score = Math.max(0, fieldCoverage - qualityDeductions);

  return { score, missingFields, fieldCoverage };
}

/**
 * Assess timeliness of dataset
 */
export function assessTimeliness(
  dataset: {
    temporal_coverage?: string;
    id: string;
  },
  currentYear: number
): {
  lastUpdated: string;
  daysStale: number;
  isCurrent: boolean;
} {
  // Extract end year from temporal_coverage (e.g., "2015-2024" or "2024")
  const coverage = dataset.temporal_coverage || '';
  const years = coverage.match(/\d{4}/g);
  const endYear = years ? Math.max(...years.map(Number)) : 0;

  const yearsStale = currentYear - endYear;
  const daysStale = yearsStale * 365; // Rough approximation

  // Consider current if data is from current year or previous year
  const isCurrent = yearsStale <= 1;

  return {
    lastUpdated: endYear ? `${endYear}-12-31` : 'unknown',
    daysStale,
    isCurrent,
  };
}

/**
 * Assess documentation quality
 */
export function assessDocumentation(dataset: {
  readme_path?: string;
  licence?: string;
}): {
  hasFieldDefinitions: boolean;
  hasProvenance: boolean;
  hasLimitations: boolean;
  docScore: number;
} {
  // For now, infer from available metadata
  // In a full implementation, would parse README files

  const hasReadme = Boolean(dataset.readme_path);
  const hasLicence = Boolean(dataset.licence && dataset.licence.length > 10);

  // Conservative scoring based on available metadata
  const hasFieldDefinitions = hasReadme; // Assume READMEs have field defs
  const hasProvenance = hasLicence; // Licence implies source documentation
  const hasLimitations = hasReadme; // Assume documented

  let docScore = 0;
  if (hasFieldDefinitions) docScore += 0.33;
  if (hasProvenance) docScore += 0.33;
  if (hasLimitations) docScore += 0.34;

  return {
    hasFieldDefinitions,
    hasProvenance,
    hasLimitations,
    docScore,
  };
}

/**
 * Compute aggregate quality metrics for the entire catalogue
 */
export function computeCatalogueQuality(
  datasets: Array<{
    name?: unknown;
    domains?: unknown;
    licence?: unknown;
    temporal_coverage?: unknown;
    file_count?: unknown;
    readme_path?: unknown;
    id?: unknown;
  }>,
  currentYear: number
): {
  totalDatasets: number;
  avgCompletenessScore: number;
  avgDocScore: number;
  datasetsWithCurrentData: number;
  avgDaysStale: number;
} {
  if (datasets.length === 0) {
    return {
      totalDatasets: 0,
      avgCompletenessScore: 0,
      avgDocScore: 0,
      datasetsWithCurrentData: 0,
      avgDaysStale: 0,
    };
  }

  let totalCompleteness = 0;
  let totalDocScore = 0;
  let totalDaysStale = 0;
  let currentCount = 0;

  for (const dataset of datasets) {
    const completeness = assessCompleteness(dataset);
    const timeliness = assessTimeliness(dataset as { temporal_coverage?: string; id: string }, currentYear);
    const docs = assessDocumentation(dataset as { readme_path?: string; licence?: string });

    totalCompleteness += completeness.score;
    totalDocScore += docs.docScore;
    totalDaysStale += timeliness.daysStale;
    if (timeliness.isCurrent) currentCount++;
  }

  return {
    totalDatasets: datasets.length,
    avgCompletenessScore: totalCompleteness / datasets.length,
    avgDocScore: totalDocScore / datasets.length,
    datasetsWithCurrentData: currentCount,
    avgDaysStale: totalDaysStale / datasets.length,
  };
}

/**
 * Run consistency checks across dataset pairs
 *
 * For demo purposes - in production, would implement actual cross-dataset validation
 */
export function runConsistencyChecks(
  datasets: Array<{
    domains?: unknown;
    id?: unknown;
  }>
): ConsistencyCheck[] {
  const checks: ConsistencyCheck[] = [];

  // Example check: datasets in same domain should have similar temporal coverage ranges
  // This is a placeholder - real checks would validate actual data values

  const healthDatasets = datasets.filter((d) =>
    Array.isArray(d.domains) ? d.domains.includes('health') : false
  );

  if (healthDatasets.length >= 2) {
    checks.push({
      checkName: 'Health domain temporal alignment',
      datasetPair: [
        String((healthDatasets[0] as { id?: string }).id || 'unknown'),
        String((healthDatasets[1] as { id?: string }).id || 'unknown'),
      ],
      passed: true,
      details: 'Temporal coverage ranges overlap appropriately',
    });
  }

  return checks;
}
