# Contributing to SA & AU Open Data Atlas

Thank you for your interest in contributing to this catalogue. This guide outlines the process for proposing new datasets.

## Dataset Proposal Process

We welcome proposals for new datasets that meet our [curation criteria](../decisions/DR-001-curation-criteria.md). Before proposing a dataset, please check:

1. **Is it already in the catalogue?** Search the [catalogue page](https://sa-au-open-data.vercel.app/catalogue) first
2. **Does it meet all four criteria?** (see below)
3. **Is the source URL still active?** Verify the dataset is currently available

## Curation Criteria

Every dataset must meet **all four** of these criteria:

### 1. Official Government Source
- Published by an Australian government statistical agency (ABS, AIHW, Productivity Commission)
- OR published by a state/federal government department or agency
- No unofficial extracts, third-party reshapes, or unattributed data

### 2. Aggregate or De-identified
- Summary statistics only (counts, rates, means, totals by region/demographic)
- No individual records (microdata/CURF)
- No geolocation finer than SA2 (Statistical Area Level 2)
- No individual entity time series (one school, one hospital, one business)

### 3. Open Licence
Must be licensed under one of:
- Creative Commons Attribution 4.0 International (CC BY 4.0)
- Creative Commons Attribution 3.0 Australia (CC BY 3.0 AU)
- CC0 1.0 Universal (public domain)
- Crown Copyright **with explicit reuse permissions**

**Excluded licences:**
- CC BY-NC (non-commercial restriction)
- CC BY-ND (no derivatives restriction)
- Crown Copyright without clear reuse terms
- "All rights reserved" or proprietary licences

### 4. Complete Metadata
Must be documentable with:
- Source URL (where the dataset was obtained)
- Retrieval date
- Licence verbatim from the source (with source URL of licence statement)
- Field definitions (what each column means)
- Temporal coverage (years/date range)
- Known limitations or issues

## How to Propose a Dataset

### Option 1: GitHub Issue (Preferred)

Open a [new issue](https://github.com/rNLKJA/public-services-open-source-data/issues/new) with the title format:

```
Dataset proposal: [Brief Name]
```

Include in the issue body:

```markdown
## Dataset Information

**Name:** [Full dataset name]

**Source Agency:** [e.g., Australian Bureau of Statistics, SA Health]

**Source URL:** [Direct link to the dataset]

**Licence:** [e.g., CC BY 4.0]

**Licence Source:** [URL where the licence statement appears]

**Temporal Coverage:** [e.g., 2015-2024, or "2023 only"]

**Geographic Coverage:** [e.g., SA LGAs, Australian states, national]

**Domain(s):** [Health, Justice, Education, Infrastructure, Environment, Social Services, Planning, Economy, Demographics, Governance]

**File Format(s):** [e.g., CSV, Excel, GeoJSON]

## Why This Dataset?

[1-2 sentences on why this dataset would be valuable for the catalogue]

## Metadata Checklist

- [ ] Source URL is active and publicly accessible
- [ ] Licence is CC BY, CC0, or Crown Copyright with reuse permission
- [ ] Data is aggregate (no individual records)
- [ ] Field definitions are available (in the dataset or its documentation)
- [ ] I can document the retrieval date and temporal coverage

## Additional Notes

[Any known issues, limitations, or special considerations]
```

### Option 2: Pull Request

If you have already downloaded and documented the dataset:

1. Fork the repository
2. Create a new directory in `original/datasets/[dataset-id]/`
3. Add the dataset files and a `README.md` following the existing format (see any dataset in `original/datasets/` as a template)
4. Run `uv run scripts/catalogue_builder.py` to regenerate `web/public/data/catalogue.json`
5. Open a pull request with a clear description

**Required README sections:**
- Dataset name and source
- Licence (verbatim from source, with source URL)
- Retrieval date
- Temporal coverage
- Field definitions (table with column name, description, data type, units)
- Known limitations
- Attribution requirements

## Triage Process

All proposals go through a verification checklist:

1. **Source verification** — is the source URL active and official?
2. **Licence check** — does the licence permit redistribution?
3. **Aggregation check** — confirm no individual records
4. **Documentation review** — are field definitions and metadata complete?

If all checks pass, the dataset is integrated into the catalogue. If any check fails, the proposal is declined with an explanation.

## What Happens After Acceptance

1. Dataset is added to `original/datasets/[dataset-id]/`
2. README is created or reviewed
3. Catalogue metadata is regenerated
4. Changes are committed to GitHub
5. Web app is redeployed to Vercel
6. Your contribution is credited in the commit

## Questions?

- **Technical questions:** Open a [GitHub issue](https://github.com/rNLKJA/public-services-open-source-data/issues)
- **Licence questions:** See [DR-002: Licence Compatibility](../decisions/DR-002-licence-compatibility.md)
- **Privacy questions:** See [DR-003: Aggregation and Privacy](../decisions/DR-003-aggregation-privacy.md)

## Code of Conduct

- Be respectful and constructive in all interactions
- Provide accurate information about sources and licences
- Do not propose datasets with known privacy, legal, or ethical issues
- Accept curation decisions gracefully

---

**Maintainer:** Sunchuangyu "Rin" Huang ([@rNLKJA](https://github.com/rNLKJA))
