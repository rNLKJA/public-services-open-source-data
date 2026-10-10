# SA & AU Open Data Atlas — Web Application

A modern, searchable catalogue browser for South Australian and Australian government open datasets. This Next.js application provides an accessible interface to explore 95+ curated open data resources with rigorous quality metrics, provenance tracking, and statistical showcase analyses.

## Features

### Core Catalogue
- **Searchable Catalogue**: Browse and filter 95+ datasets by domain, licence, format, and keywords
- **Hero Datasets**: Featured high-impact datasets on the landing page
- **Responsive Design**: Mobile-first interface with dark mode support
- **Civic Design Language**: Federal blue and SA red colour palette with tabular typography
- **Accessibility**: WCAG-compliant with keyboard navigation and screen reader support

### Career-Aligned Enhancements

#### Data Governance & Quality
- **Data Quality Dashboard** (`/quality`): Completeness, timeliness, and documentation metrics with uncertainty quantification
- **Provenance Graphs** (`/provenance`): Lineage visualisation for 5 key datasets showing source → retrieval → documentation → publication
- **Decision Records**: Documented curation criteria, licence framework, and privacy policies (docs/decisions/)

#### Statistical Rigour
- **Statistical Library**: Wilson score intervals for proportions, bootstrap intervals for custom statistics, effect sizes (Cohen's d)
- **Demo Analyses** (`/analyses`): 4 cross-dataset case studies showcasing confidence intervals, sample sizes, and effect sizes
- **Unit Tests**: Full test coverage for statistical functions verified against reference values

#### Methodology Transparency
- **Methods Page** (`/methods`): Complete documentation of data provenance, curation method, quality assessment, statistical approach, and limitations
- **AI Use Statement**: BYOK (Bring Your Own Key) AI features with full transparency, audit logging, and governance alignment

#### AI Features (Optional, BYOK)
- **Dataset Recommender**: AI-powered suggestions based on research questions (requires user's own API key)
- **Audit Trail**: All AI interactions logged to IndexedDB with full transparency (viewable at `/ai-log`, exportable as JSON)
- **Privacy-First**: API keys stored in browser only (sessionStorage/localStorage), never sent to our servers, calls go directly to Anthropic/OpenAI

## Local Development

```bash
# Install dependencies
pnpm install

# Run development server
pnpm dev

# Open http://localhost:3000
```

## Build & Test

```bash
# Lint code
pnpm lint

# Type check
pnpm typecheck

# Run tests
pnpm test

# Format code
pnpm format

# Production build
pnpm build

# Start production server
pnpm start
```

## Tech Stack

- **Framework**: Next.js 16 (App Router, React Server Components)
- **Styling**: Tailwind CSS v4 with custom design tokens
- **UI Components**: shadcn/ui (Radix primitives)
- **Typography**: Inter (body) + JetBrains Mono (code)
- **Theme**: next-themes with system preference detection
- **Icons**: lucide-react
- **Testing**: Vitest
- **Package Manager**: pnpm 10.33.1

## Data Generation

The catalogue and hero dataset metadata are generated from the original 95+ datasets in the `original/` directory via Python scripts in `scripts/`. See the root README for details on data provenance and regeneration.

## Contributing

To propose a new dataset for inclusion in the catalogue, see the [contribution guide](../docs/CONTRIBUTING.md). All proposals are reviewed against the [curation criteria](../docs/decisions/DR-001-curation-criteria.md).

## Project Context

This is a personal data curation project showcasing South Australian and Australian government open data resources. The catalogue aggregates datasets from data.sa.gov.au, data.gov.au, and other civic data portals.

**Career positioning:** This project demonstrates statistical rigour (confidence intervals, effect sizes, reproducibility), GenAI governance (BYOK, audit trails, transparency), and data quality practices aligned with roles in statistical analysis, ML engineering, and algorithm development.

For methodology, see the [Methods page](https://sa-au-open-data.vercel.app/methods) or the [About page](https://sa-au-open-data.vercel.app/about).
