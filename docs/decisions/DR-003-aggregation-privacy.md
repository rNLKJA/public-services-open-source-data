# DR-003: Aggregation Levels and Privacy

**Decision:** Include only aggregate or summary statistics. Exclude unit record files (microdata), geolocation below SA2 level (suburb), and time series at individual entity level. Every dataset README must state the aggregation level and confirm no individual records are included.

**Context:** Open government data balances transparency with privacy. Statistical agencies release both aggregate tables (counts, means, totals by region/demographic) and unit record files (one row per person/event with identifying variables removed). Unit records carry re-identification risk despite de-identification. Geolocation below SA2 (suburbs with 3,000–25,000 people) and individual time series (one school, one hospital) can expose sensitive patterns.

**Options considered:**

1. **Include microdata** — accept CURF (Confidentialised Unit Record Files) from ABS
   - **Rejected:** Requires user registration, signed agreements, and restricted-use environments. Incompatible with open redistribution. Re-identification risk even with confidentialisation.
2. **Include fine geolocation** — SA1 (neighbourhoods, ~400 people) or postcode
   - **Rejected:** Small-area data can expose individuals in sparsely populated areas. Postcode boundaries don't align with statistical boundaries, creating analysis issues.
3. **Aggregate-only with SA2+ geography (chosen)** — summary statistics, SA2 or broader regions
   - **Selected:** Zero re-identification risk. Enables regional analysis without privacy exposure. Consistent with ABS's open-access tier.

**Why:** The catalogue serves researchers, journalists, and civic builders who need aggregate insights (regional health outcomes, justice trends, infrastructure gaps), not individual-level analysis. Aggregate data is legally safe, ethically defensible, and redistributable without restriction. SA2 (suburbs) is the finest geography that balances granularity with privacy—below that, suppression rules fragment datasets.

**What happened:** Applied to 95 datasets curated July 2024. All datasets are aggregate: counts/rates by region, demographic, or time period. Geography is predominantly state-wide, LGA (Local Government Area, ~70 in SA), or SA2 (~250 in SA). Zero individual records are included. This excluded 8 candidate datasets that were available only as microdata or fine geocoded points.

**What I'd change:** For datasets where SA2-level data exists but is suppressed due to small counts (n<5), document the suppression logic and state the coverage loss (e.g., "87% of SA2s reported; 13% suppressed"). This clarifies data quality without violating privacy.

---

*Created: 2024-10-10*  
*Status: Active*  
*Author: Rin Huang*
