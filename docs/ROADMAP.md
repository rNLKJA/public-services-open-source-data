# Roadmap

## Completed (Upgrade: Career-Aligned)

- ✅ Statistical rigour library (Wilson intervals, bootstrap CIs, Cohen's d)
- ✅ Data quality dashboard with completeness, timeliness, documentation metrics
- ✅ Provenance visualization for key dataset lineage chains
- ✅ Methods page with transparent methodology documentation
- ✅ Decision records (DR-001 to DR-003) with retrospective assessment
- ✅ Demo analyses showcasing uncertainty quantification
- ✅ AI client library (Anthropic/OpenAI adapters, audit logging, key management)
- ✅ Contribution workflow documentation

## In Progress

### AI Features Implementation
**Status**: Design complete, UI integration pending  
**Blocking**: Requires UI components and feature integration

The AI client library (`src/lib/ai/`) is complete with:
- Provider adapters (Anthropic Messages API, OpenAI Chat Completions)
- Structured output validation with zod
- Audit logging to browser IndexedDB
- Key storage in sessionStorage/localStorage (never server-side)

**Remaining work:**
1. Build AI settings dialog component
   - Provider selection (Anthropic/OpenAI)
   - API key input with show/hide toggle
   - Storage preference (session vs. persistent)
   - "Forget key" button
2. Dataset recommender UI (`/analyses` or dedicated `/recommend`)
   - Research question input
   - AI-powered suggestions with rule-based baseline comparison
   - "AI-generated" labels on outputs
3. Text-to-catalogue-query interface
   - Natural language query input
   - Structured response from catalogue metadata
   - Link to matching datasets
4. Wire audit logging to user-facing interactions
   - Log every AI call with full context (no keys)
   - Track human decisions (accepted/edited/rejected)
5. `/ai-log` page currently shows empty state correctly but will remain empty until features integrated

### Evaluation Harness (Critical for ML Engineer Positioning)
**Status**: Not started  
**Required by**: Upgrade standard section 4

Build a comparison harness for dataset recommendation:
- **Baseline**: Rule-based recommender using keyword matching on domains/descriptions
- **AI method**: LLM-based semantic recommendation
- **Test set**: 20 research questions with ground-truth relevant datasets
- **Metrics**: Precision@3, recall@5, latency (ms), cost per query (token usage × model price)
- **Output**: Side-by-side results table with 95% Wilson CIs for precision/recall
- **Export**: CSV download for external analysis

This harness fulfills the "LLM-eval showcase" requirement and demonstrates:
- Experimental design (paired comparisons, fixed test set)
- Rigorous evaluation (metrics with uncertainty)
- Cost-benefit transparency (accuracy vs. latency vs. cost tradeoffs)

**Implementation plan:**
1. Create test set of 20 queries with human-labeled ground truth (5 datasets each)
2. Implement rule-based baseline (TF-IDF or BM25 on dataset metadata)
3. Build evaluation runner (`src/lib/evaluation/recommender-eval.ts`)
4. Create results page (`/evaluation/recommender`) with comparison table
5. Add CSV export functionality

## Future Work

### Data Infrastructure
- Automated sync: weekly scraper to check source URLs for updates
- Data validation: parse CSV/Excel files to verify schema matches README
- Cross-dataset join keys: document common identifiers (LGA codes, SA2 codes)
- Real consistency checks: validate that LGA-level totals reconcile with state totals

### Analysis Enhancements
- Interactive parameter exploration for demo analyses (seed, bootstrap samples, CI level)
- Downloadable R/Python scripts reproducing each analysis
- Additional cross-dataset analyses (health × census, crime × socioeconomic indicators)

### Documentation
- Video walkthrough of data quality dashboard
- Contribution case study (full lifecycle from proposal to merge)
- Blog posts on statistical method choices (why Wilson over Wald, bootstrap implementation notes)

## Non-Goals

- Server-side AI: No AI budget; BYOK only
- Real-time sync: Snapshot approach matches portfolio context
- Microdata: Aggregate-only per DR-003
- Formal compliance certification: Portfolio project, not production infrastructure
