# Original Data Catalogue

This directory contains the original curated collection of 95+ South Australian and Australian government datasets, preserved exactly as collected and documented.

## Structure

- **`datasets/`** — 95+ dataset folders, each containing:
  - Raw data files (CSV, Excel, GeoJSON)
  - `README.md` with source, licence, retrieval date, field definitions, coverage period and known issues
  - `PROVENANCE.md` tracing the data lineage back to official government sources
- **`analysis-ready/`** — Worked examples joining multiple datasets for specific research questions
- **`scripts/`** — Small query helpers for live government APIs referenced in the datasets
- **`CATALOGUE.md`** — Full listing of all 95+ datasets with descriptions

## How to Use

Each dataset folder is self-contained and documented. To use a dataset:

1. Read its `README.md` for source, licence, field definitions and known issues
2. Check `PROVENANCE.md` for the complete data lineage
3. Review the licence terms (predominantly CC BY 4.0, some Crown Copyright with reuse permissions)
4. Cite the original government source as documented

## How to Cite

When using these datasets, cite the **original government source** documented in each dataset's README, not this catalogue. For example:

> South Australia Police. (2025). *Crime Statistics by Suburb*. Retrieved from data.sa.gov.au

This catalogue's contribution is curation, documentation and provenance tracking. The data itself belongs to the listed government agencies.

## Compliance

All data is aggregate or de-identified public releases. No individual-level records are included. See the root `COMPLIANCE.md` for detailed privacy, licensing and FAIR principles reasoning.
