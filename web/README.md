# SA & AU Open Data Atlas — Web Application

A modern, searchable catalogue browser for South Australian and Australian government open datasets. This Next.js application provides an accessible interface to explore 95+ curated open data resources across domains like transport, health, environment, and social services.

## Features

- **Searchable Catalogue**: Browse and filter 95+ datasets by domain, licence, format, and keywords
- **Hero Datasets**: Featured high-impact datasets on the landing page
- **Responsive Design**: Mobile-first interface with dark mode support
- **Civic Design Language**: Federal blue and SA red colour palette with tabular typography
- **Accessibility**: WCAG-compliant with keyboard navigation and screen reader support

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

## Project Context

This is a personal data curation project showcasing South Australian and Australian government open data resources. The catalogue aggregates datasets from data.sa.gov.au, data.gov.au, and other civic data portals. For more information, see the [About page](http://localhost:3000/about) or the root README.
