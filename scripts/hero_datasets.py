#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""
Generate hero dataset visualizations (small data samples for immediate inline display).
Outputs static JSON suitable for client-side rendering.
"""

import json
from pathlib import Path

def main():
    repo_root = Path(__file__).parent.parent
    output_path = repo_root / 'web' / 'public' / 'data' / 'hero-datasets.json'

    # Hero datasets: small, representative samples that showcase the catalogue's breadth
    # These are hand-picked, impactful datasets that visualize well
    hero_datasets = {
        'generated': '2026-10-10',
        'heroes': [
            {
                'id': 'sa-crime-statistics',
                'name': 'SA Crime Statistics',
                'description': 'Recorded crime by suburb, 2010-2026',
                'domain': 'justice',
                'viz_type': 'time_series',
                'note': 'Sample data - see full dataset for complete records'
            },
            {
                'id': 'au-cost-of-living-cpi',
                'name': 'Adelaide CPI',
                'description': 'Consumer Price Index trends',
                'domain': 'economy',
                'viz_type': 'line_chart',
                'note': 'Monthly index showing cost-of-living changes'
            },
            {
                'id': 'sa-road-crash-data',
                'name': 'SA Road Crashes',
                'description': 'Crash locations and severity, 2020-2024',
                'domain': 'infrastructure',
                'viz_type': 'heatmap',
                'note': 'Statewide crash register with location data'
            },
            {
                'id': 'sa-school-locations',
                'name': 'SA School Locations',
                'description': 'Government school and preschool sites',
                'domain': 'education',
                'viz_type': 'map',
                'note': 'Department for Education sites with zone status'
            },
            {
                'id': 'sa-health-ed-performance',
                'name': 'ED Wait Times',
                'description': 'Emergency department performance',
                'domain': 'health',
                'viz_type': 'bar_chart',
                'note': 'Median wait times by hospital'
            },
            {
                'id': 'au-small-scale-renewable-installations',
                'name': 'Renewable Installations',
                'description': 'Rooftop solar and battery installations',
                'domain': 'environment',
                'viz_type': 'growth_chart',
                'note': 'Postcode-level installation counts since 2001'
            },
        ]
    }

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(hero_datasets, f, indent=2)

    print(f"Generated {len(hero_datasets['heroes'])} hero datasets")
    print(f"Output: {output_path}")

if __name__ == '__main__':
    main()
