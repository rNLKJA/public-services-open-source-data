# DR-002: Licence Compatibility Framework

**Decision:** Accept datasets under CC BY 4.0, CC BY 3.0 AU, CC0 1.0, and Crown Copyright with explicit reuse permissions. Reject datasets under CC BY-NC (non-commercial), CC BY-ND (no derivatives), or restrictive Crown Copyright without clear reuse terms. Document every licence verbatim in the dataset README with the source URL of the licence statement.

**Context:** Government agencies use varied licences: Creative Commons (CC BY 4.0, CC BY 3.0 AU), public domain (CC0), and Crown Copyright with agency-specific terms. The catalogue must redistribute datasets and their metadata, which requires compatible licences. Ambiguity creates legal risk for users and maintainers.

**Options considered:**

1. **CC BY 4.0 only** — the most common open licence
   - **Rejected:** Excludes valuable datasets under CC BY 3.0 AU (AIHW, older ABS releases), CC0 (some SA agencies), and Crown Copyright with reuse clauses (productivity commissions, statutory bodies)
2. **Accept all Creative Commons licences** — any CC variant
   - **Rejected:** CC BY-NC prohibits commercial use (incompatible with civic tools that monetise); CC BY-ND prohibits reshaping (incompatible with analysis-ready transforms)
3. **Permissive-only framework (chosen)** — CC BY, CC0, and explicit Crown Copyright reuse
   - **Selected:** Maximises dataset availability while ensuring redistribution and derivative works are permitted

**Why:** Users need freedom to reshape (analysis-ready formats), republish (research papers, civic apps), and commercialise (policy consultancies, startups). Non-commercial and no-derivatives clauses block these use cases. Crown Copyright with explicit reuse permissions (e.g., "may be reproduced for research purposes") is functionally equivalent to CC BY.

**What happened:** 95 datasets curated (July 2024): 78 under CC BY 4.0, 9 under Crown Copyright with reuse, 6 under CC BY 3.0 AU, 2 under CC0. Zero datasets were excluded due to licence incompatibility (all candidates met the bar). Two datasets with unclear Crown Copyright terms were excluded pending clarification.

**What I'd change:** Engage with agencies publishing under Crown Copyright to request migration to CC BY 4.0 for clarity. The functional rights are equivalent, but CC BY is machine-readable and internationally recognised.

---

*Created: 2024-10-10*  
*Status: Active*  
*Author: Rin Huang*
