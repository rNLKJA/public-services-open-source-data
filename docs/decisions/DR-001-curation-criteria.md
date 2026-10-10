# DR-001: Dataset Curation Criteria

**Decision:** Include only datasets that meet all four criteria: (1) official government source, (2) aggregate or de-identified (no individual records), (3) open licence permitting redistribution, (4) complete metadata (source URL, retrieval date, field definitions, licence terms).

**Context:** This project curates open government data for public-service research. The catalogue aggregates datasets from data.sa.gov.au, data.gov.au, and agency portals. Without clear inclusion criteria, the catalogue risks mixing authoritative and unofficial sources, violating privacy, creating legal ambiguity, or presenting poorly documented data that users cannot trust or cite.

**Options considered:**

1. **Permissive curation** — include any publicly available dataset mentioning government
   - **Rejected:** No quality bar; risks including unofficial extracts, unattributed reshapes, or data without clear licence
2. **Official sources only, minimal metadata** — require government provenance but not full documentation
   - **Rejected:** Users cannot verify currency, understand field definitions, or comply with attribution requirements
3. **Strict four-criteria gate (chosen)** — official + aggregate + open licence + complete metadata
   - **Selected:** Balances access with rigour; every dataset is traceable, legally redistributable, and documented

**Why:** The strict gate ensures every dataset is defensible for research use. Researchers need provenance (to cite), licence clarity (to republish findings), and field definitions (to interpret correctly). Aggregate-only prevents privacy breaches and regulatory exposure.

**What happened:** Applied retroactively to 95 datasets curated July 2024. Zero removals were needed—all existing datasets met the bar. The criteria prevented inclusion of 12 candidate datasets with unclear licences or missing field definitions.

**What I'd change:** For version 2, consider a "provisional" tier for high-value datasets that meet 3/4 criteria, with a visible warning and a remediation tracker. This would surface useful-but-imperfect datasets while maintaining transparency about gaps.

---

*Created: 2024-10-10*  
*Status: Active*  
*Author: Rin Huang*
