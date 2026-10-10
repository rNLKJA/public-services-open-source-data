# Threatened Species and Ecological Communities of National Environmental Significance

**Source:** *Threatened Species and Ecological Communities of National Environmental Significance*, published by the **Department of Climate Change, Energy, the Environment and Water (DCCEEW)**, on [data.gov.au](https://data.gov.au/data/dataset/threatened-species-state-lists) (CKAN package `threatened-species-state-lists`, ID `ae652011-f39e-4c6c-91b8-1dc2d2dfee8f`)
**Licence:** [Creative Commons Attribution 3.0 Australia](http://creativecommons.org/licenses/by/3.0/au/) (CC BY 3.0 AU) — confirmed two independent ways: the CKAN `package_show` API response (`license_id: cc-by`, `license_title: Creative Commons Attribution 3.0 Australia`, `license_url: http://creativecommons.org/licenses/by/3.0/au/`) and a direct fetch of the live dataset page, which shows the same licence text and link in its own "License" sidebar module.
**Update frequency:** "The dataset is updated as the lists of species/ecological communities on schedules of the [Environment Protection and Biodiversity Conservation Act 1999](https://www.legislation.gov.au/Details/C2022C00335) (EPBC Act) are amended" (source's own notes). The two resources carry independent extraction dates.
**Coverage:** National, with an indicative-occurrence column for every state, territory, external territory and the Commonwealth Marine Area — including a dedicated South Australia (`sa`) column in both tables.
**Retrieved:** 7 July 2026

## What it is

The Commonwealth's list of every species and ecological community formally listed as threatened under the EPBC Act — i.e. matters of "national environmental significance" — together with each entry's threatened-status category and an indicative flag for which Australian jurisdictions it occurs in. It comes as two linked tables:

- **Threatened Species State Lists** (`20260206spcs.csv`, extracted 6 February 2026) — one row per listed species (2,208 rows), giving its scientific/common name, current accepted scientific name (where since revised), threatened-status category (Extinct, Critically Endangered, Endangered, Vulnerable or Conservation Dependent), full taxonomic classification (Kingdom/Class/Family/Genus/Species), and indicative occurrence across all 8 states/territories plus 9 external territories/marine areas.
- **Ecological Communities State Lists** (`20260320cmty.csv`, extracted 20 March 2026) — one row per listed threatened ecological community (111 rows), giving its name, EPBC status and indicative occurrence across the 8 states/territories.

Both tables carry a `Profile`/`sprat_profile_url` link back to the Commonwealth's [Species Profile and Threats Database](http://www.environment.gov.au/cgi-bin/sprat/public/sprat.pl) (SPRAT) for narrative detail per entry.

**This domain does not have a genuinely open, current SA-published equivalent.** This run checked `data.sa.gov.au` directly for a South Australian threatened-species or conservation-status list: the Department for Environment and Water's `flora-survey-sites` and `fauna-survey-sites` packages ("Flora/Fauna Species Observations") are stale CKAN metadata records (last modified July 2016) whose only resource is a link to an Atlas of Living Australia biocache search — species presence/observation records, not a conservation-status listing, with no bulk CC BY file to mirror. DEW's `naturemaps` package is a pointer to the interactive [NatureMaps](https://www.naturemaps.sa.gov.au) map viewer, not a downloadable dataset. The one genuinely current SA-specific candidate, `biodiversity-mapping-interim` (metadata modified February 2026, CC BY 4.0), maps *areas* of known EPBC/National Parks and Wildlife Act biodiversity value by Landscape SA region — a habitat-area layer, not a species-level list — and is a different angle from what this domain asked for; it's noted here as a candidate for a future pass rather than pursued this run. Portal-wide searches for "threatened", "rare endangered", "schedule threatened", "conservation status" and "national parks and wildlife act" surfaced no dedicated SA statutory schedule (e.g. National Parks and Wildlife Act 1972 Schedules 7-9) published as open structured data. This national DCCEEW dataset was used instead, filtered to its dedicated South Australia occurrence column.

Of the 2,208 nationally listed species, 319 are flagged as occurring in South Australia (185 fauna, 134 flora); of the 111 listed ecological communities, 18 occur in South Australia.

## Fields

Two processed tables, each with a full-national and a South-Australia-filtered version (same columns, `data/*-sa.csv` filtered to rows where `sa` = `Yes`).

### `threatened-species-state-lists.csv` / `threatened-species-sa.csv`

| Field | Description |
|---|---|
| `scientific_name` | Listed scientific name |
| `common_name` | Common name(s), where recorded |
| `current_scientific_name` | Current accepted scientific name, where the listed name has since been taxonomically revised (`-` if unchanged) |
| `threatened_status` | Extinct, Critically Endangered, Endangered, Vulnerable or Conservation Dependent, per the EPBC Act schedules |
| `act`, `nsw`, `nt`, `qld`, `sa`, `tas`, `vic`, `wa` | `Yes`/`-` indicative occurrence in each state/territory |
| `aci_ashmore_cartier_islands`, `cki_cocos_keeling_islands`, `ci_christmas_island`, `csi_coral_sea_islands`, `jbt_jervis_bay_territory`, `nfi_norfolk_island`, `hmi_heard_mcdonald_islands`, `aat_australian_antarctic_territory`, `cma_commonwealth_marine_area` | `Yes`/`-` indicative occurrence in each external territory or the Commonwealth Marine Area (source columns `ACI`/`CKI`/`CI`/`CSI`/`JBT`/`NFI`/`HMI`/`AAT`/`CMA` respectively, spelled out here since the abbreviations aren't self-explanatory) |
| `listed_sprat_taxon_id`, `current_sprat_taxon_id` | SPRAT taxon ID for the listed name and, where revised, the current name |
| `kingdom`, `class`, `family`, `genus`, `species`, `infraspecific_rank`, `infraspecies`, `species_author`, `infraspecies_author` | Taxonomic classification fields |
| `sprat_profile_url` | Link to the entry's SPRAT profile page |
| `date_extracted` | Date this list was extracted from the EPBC Act schedules, standardised to ISO `YYYY-MM-DD` (source format e.g. `2026-Feb-06`) |
| `nsl_name_url` | Link to the entry's National Species List (Australian Plant Name Index / equivalent) record |

### `threatened-ecological-communities-state-lists.csv` / `threatened-ecological-communities-sa.csv`

| Field | Description |
|---|---|
| `community_name` | Listed ecological community name |
| `epbc_status` | Endangered, Critically Endangered or Vulnerable, per the EPBC Act schedules |
| `listed_community_id` | SPRAT community ID |
| `act`, `nsw`, `nt`, `qld`, `sa`, `tas`, `vic`, `wa` | `Yes`/`-` indicative occurrence in each state/territory |
| `sprat_profile_url` | Link to the entry's SPRAT profile page |
| `date_extracted` | Date this list was extracted, standardised to ISO `YYYY-MM-DD` |

No recalculation or reinterpretation was applied to any value — column headers were renamed to `snake_case` and the `date_extracted` format was standardised; every other cell matches the raw source exactly (spot-checked, e.g. `Acacia anomala`/`Iron-grass Natural Temperate Grassland of South Australia` rows match byte-for-byte aside from the date format).

The source's own dataset description references an "explanatory notes" resource describing fields and methods; that resource no longer appears in the dataset's current resource list (only the two CSVs remain) — noted here since the field descriptions above are derived directly from the column headers and source notes text rather than that missing file.

## Access method

**Use the files in [`data/`](data/) — they are the ready-to-use, directly loadable versions.** [`raw/`](raw/) holds the untouched, verbatim-as-downloaded source CSVs, kept for provenance.

### `raw/`

- [`raw/threatened-species-state-lists-2026-02-06.csv`](raw/threatened-species-state-lists-2026-02-06.csv) — 688,990 bytes, byte-for-byte match to the live resource's `Content-Length`, downloaded directly from `data.gov.au` over plain HTTPS (no `fetch.sh` needed).
- [`raw/ecological-communities-state-lists-2026-03-20.csv`](raw/ecological-communities-state-lists-2026-03-20.csv) — 22,412 bytes, byte-for-byte match, downloaded the same way.

### `data/`

[`convert.py`](convert.py) reads both raw CSVs and writes:

- [`data/threatened-species-state-lists.csv`](data/threatened-species-state-lists.csv) — all 2,208 listed species nationally
- [`data/threatened-species-sa.csv`](data/threatened-species-sa.csv) — the 319 rows where `sa` = `Yes`
- [`data/threatened-ecological-communities-state-lists.csv`](data/threatened-ecological-communities-state-lists.csv) — all 111 listed ecological communities nationally
- [`data/threatened-ecological-communities-sa.csv`](data/threatened-ecological-communities-sa.csv) — the 18 rows where `sa` = `Yes`

Regenerate with `python3 convert.py` from this directory.

## Privacy note

This dataset describes species and ecological communities, not people — every field is a taxonomic name, conservation-status category or jurisdiction flag. No individual-level personal data of any kind applies here.
