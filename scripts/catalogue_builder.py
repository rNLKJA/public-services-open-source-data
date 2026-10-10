#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""
Scan original/datasets/*/README.md and build web/public/data/catalogue.json
with metadata (name, domain tags, licence, temporal coverage, file count, total size).
"""

import json
import re
from pathlib import Path
from typing import Any

# Domain classification keywords (expand as needed)
DOMAIN_KEYWORDS = {
    'education': ['school', 'education', 'student', 'teacher', 'university', 'training', 'apprentice'],
    'health': ['health', 'hospital', 'medical', 'mental health', 'ed performance', 'elective surgery', 'immunisation'],
    'justice': ['police', 'crime', 'court', 'prison', 'icac', 'legal', 'criminal', 'ombudsman'],
    'infrastructure': ['road', 'crash', 'vehicle', 'transport', 'building', 'land division'],
    'environment': ['air quality', 'water', 'heritage', 'marine', 'vegetation', 'climate', 'waste', 'epa'],
    'social': ['homelessness', 'child protection', 'ndis', 'disability', 'aged care', 'concession'],
    'planning': ['land division', 'zoning', 'planning', 'building approval'],
    'economy': ['tourism', 'primary industries', 'fisheries', 'renewable', 'employment', 'labour'],
    'demographics': ['population', 'births', 'deaths', 'migration', 'census'],
    'governance': ['foi', 'election', 'government finances', 'public sector'],
}


def classify_domain(name: str, content: str) -> list[str]:
    """Classify dataset into domains based on name and content."""
    text = (name + ' ' + content).lower()
    domains = []
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            domains.append(domain)
    return domains or ['other']


def extract_metadata(readme_path: Path) -> dict[str, Any] | None:
    """Extract metadata from a dataset README.md."""
    if not readme_path.exists():
        return None

    content = readme_path.read_text(encoding='utf-8')
    dataset_name = readme_path.parent.name

    # Extract licence (common patterns)
    licence_match = re.search(r'(?i)licen[cs]e:\s*([^\n]+)', content)
    licence = licence_match.group(1).strip() if licence_match else 'Unknown'

    # Extract temporal coverage (year ranges)
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', content)
    temporal = f"{min(years)}-{max(years)}" if len(years) >= 2 else years[0] if years else 'Unknown'

    # Count files and size
    dataset_dir = readme_path.parent
    files = list(dataset_dir.glob('*'))
    file_count = len([f for f in files if f.is_file() and f.suffix in ['.csv', '.xlsx', '.json', '.geojson']])
    total_size = sum(f.stat().st_size for f in files if f.is_file())

    domains = classify_domain(dataset_name, content)

    return {
        'id': dataset_name,
        'name': dataset_name.replace('-', ' ').title(),
        'domains': domains,
        'licence': licence,
        'temporal_coverage': temporal,
        'file_count': file_count,
        'size_bytes': total_size,
        'readme_path': f"/original/datasets/{dataset_name}/README.md",
    }


def main():
    repo_root = Path(__file__).parent.parent
    datasets_dir = repo_root / 'original' / 'datasets'
    output_path = repo_root / 'web' / 'public' / 'data' / 'catalogue.json'

    if not datasets_dir.exists():
        print(f"Error: {datasets_dir} does not exist")
        return

    catalogue = []
    for dataset_dir in sorted(datasets_dir.iterdir()):
        if not dataset_dir.is_dir():
            continue
        readme = dataset_dir / 'README.md'
        metadata = extract_metadata(readme)
        if metadata:
            catalogue.append(metadata)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write catalogue
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'generated': '2026-10-10',
            'dataset_count': len(catalogue),
            'datasets': catalogue,
        }, f, indent=2)

    print(f"Built catalogue with {len(catalogue)} datasets")
    print(f"Output: {output_path}")


if __name__ == '__main__':
    main()
