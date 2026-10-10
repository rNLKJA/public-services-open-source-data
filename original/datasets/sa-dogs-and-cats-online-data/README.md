# SA Dogs and Cats Online Data

**Source:** *Dogs and Cats Online Data* (four annual editions: 2021-22, 2022-23, 2023-24, 2024-25), published by the **Dog and Cat Management Board / Department for Environment and Water, Government of South Australia**, on [data.sa.gov.au](https://data.sa.gov.au/data/dataset/dogs-and-cats-online-data-2024-2025) (CKAN packages `dogs-and-cats-online-data-2021-2022` through `dogs-and-cats-online-data-2024-2025`). Sourced from **DogsAndCatsOnline (DACO)**, the statutory statewide dog/cat registration system councils and owners use under the *Dog and Cat Management Act 1995*.
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0) — confirmed directly via the CKAN `package_show` API for all four editions (`license_id: cc-by`, `license_title: Creative Commons Attribution`, `license_url: http://creativecommons.org/licenses/by/4.0`).
**Update frequency:** `annual` per the CKAN `update_freq` field, and genuinely current in practice — each edition is published within 4-8 weeks of its 30 May extraction date (the 2024-25 edition was published 4 July 2025). No 2025-26 edition exists yet as of this run (expected later in 2026, once FY2025-26 data is extracted).
**Coverage:** Statewide, broken down by council. Four editions covering extraction dates 30/31 May 2022, 30 May 2023, 30 May 2024 and 30 May 2025 (Animals/Owners/breed/name tables are point-in-time snapshots as of each edition's extraction date); the Incidents table separately covers financial years "bef 30 Jun 2018" through 2024/25.
**Retrieved:** 8 July 2026

## What it is

DACO is the system SA councils and animal owners use to register, transfer and manage dog and cat records under the *Dog and Cat Management Act 1995*. The Dog and Cat Management Board publishes five extracts from it each year:

- **Animals** — count of animals with status "At Home", by council (where the animal is housed), species, gender, registration status, microchipped flag and desexed flag.
- **Owners** — count of owners of animals with status "At Home", by council (where the owner resides), gender, age category, and how many dogs/cats they own.
- **Incidents** — count of recorded dog/cat incidents (attacks, harassment, etc.) by location type, time of day, season, whether the offending animal was on a leash, incident type, victim type (human/animal) and financial year.
- **Most popular breeds and names** — the most-recorded dog and cat breeds and given names statewide.
- **Top 5 dog breeds by council** — the 5 most common dog breeds recorded in each council area.

This is the first dataset in this repository covering companion-animal registration and management — a distinct regulatory domain from the wildlife/threatened-species data in [`au-threatened-species-ecological-communities`](../au-threatened-species-ecological-communities/README.md) and from local-council services more broadly.

**A genuine, older Board dataset also exists but was not used here:** `dog-and-cat-management-board-annual-report-data` (same CKAN organisation) covers financial years 2016-17 to 2018-19 and stopped being updated after January 2020 — DACO Data superseded it as the Board's current publication method. Not mirrored separately since DACO Data covers the same ground with a more recent, ongoing series.

## Fields

The source publishes one workbook per measure per edition (5 files x 4 editions = 20 raw files). Animals, Owners, the breed/name lists and the top-5-by-council table are each a **point-in-time snapshot** with no year field of their own — the four editions are merged here into one long table per measure, with `edition`/`extract_date` columns identifying which annual snapshot a row came from. Incidents is different: each edition already republishes the **full cumulative history** internally via its own `FinancialYear` column (and later editions revise earlier years' counts upward as late-reported incidents are added — the 2021-22 edition's FY2018/19 total is lower than the same FY2018/19 total in the 2024-25 edition) — so only the current (2024-25) edition is used for Incidents, to avoid duplicate or conflicting historical rows.

### `data/animal-population-by-council.csv` (7,911 rows)

| Field | Description |
|---|---|
| `edition` | Source edition, e.g. `2024-25` |
| `extract_date` | Date DACO was queried for this edition (source-published date, e.g. `2025-05-30`) |
| `council` | Council where the animal is housed (may differ from the owner's council of residence) |
| `animal_species` | `Dog` or `Cat` |
| `gender` | `Male` or `Female` |
| `registration_status` | `Registered` (registration fee paid for the financial year, or details confirmed/updated where the council charges $0) or `Unregistered` |
| `microchipped` | `Yes`/`No` |
| `desexed` | `Yes`/`No` |
| `count` | Number of animals matching this combination of characteristics |

### `data/owners-by-council.csv` (66,334 rows)

| Field | Description |
|---|---|
| `edition`, `extract_date` | As above |
| `council` | Council where the owner resides (may differ from where their animal is housed) |
| `gender` | Owner's gender |
| `age_category` | Owner's age band, e.g. `>70` |
| `num_of_dogs`, `num_of_cats` | How many dogs/cats this owner has |
| `count` | Number of owners matching this combination of characteristics |

### `data/incidents-by-financial-year.csv` (5,563 rows, 2024-25 edition only)

| Field | Description |
|---|---|
| `financial_year` | `bef 30 Jun 2018`, or `YYYY/YY` for FY2018/19 through FY2024/25 |
| `location_type` | e.g. `Beach`, `Park`, `Street` |
| `time` | Time-of-day band, e.g. `5 pm to 8 pm` |
| `season` | `Summer`/`Autumn`/`Winter`/`Spring` |
| `offending_animal_leash_status` | `No Leash`, `On Leash`, etc. |
| `incident_type` | e.g. `Attack`, `Harassment` |
| `victim_type` | `Human` or `Animal` |
| `incident_count` | Number of incidents matching this combination of characteristics |

### `data/most-popular-breeds.csv` (12,066 rows) and `data/most-popular-names.csv` (800 rows)

Breeds: `edition`, `extract_date`, `species` (`Dog`/`Cat`), `primary_breed`, `secondary_breed`, `count`. **Source format changed between editions**, kept faithfully rather than forced into one shape: the 2021-22/2022-23/2023-24 editions report a `(Primary breed, Secondary breed, Count)` triple per breed combination (DACO records a primary and secondary breed per animal; `Cross Breed` always appears as the secondary breed for mixed-breed animals whose specific mix isn't known, and purebreds repeat the same breed in both fields). The 2024-25 edition collapses this to a single `(Breed, Sum of Count)` pair — where the source's own breed label already encodes a combination it uses a `" - "` separator inside the one field (e.g. `Australian Kelpie - Border Collie`) rather than two columns; `secondary_breed` is left blank for all 2024-25 rows since the source provides no separate field for it.

Names: `edition`, `extract_date`, `species` (`Dog`/`Cat`), `name`, `count` — the top 100 most common animal given names per species per edition, unchanged in format across all four editions.

### `data/top-5-dog-breeds-by-council.csv` (1,395 rows)

Long format: `edition`, `extract_date`, `council`, `rank` (1-5), `breed` — one row per council/rank/edition, reshaped from the source's one-row-per-council-with-5-breed-columns layout. Row counts (69-70 councils per edition) vary slightly year to year, consistent with the same natural variation seen in the Animals/Owners tables.

## Access method

**Use the files under [`data/`](data/) — they're the ready-to-use, directly loadable versions.** [`raw/`](raw/) holds the 20 untouched, verbatim-as-downloaded source workbooks (one subfolder per edition), kept for provenance.

### `raw/`

- `raw/2021-22/` — 5 XLSX files, downloaded from `waterconnect.sa.gov.au` zip archives linked from the CKAN package (data.sa.gov.au's own resource `url` field points at `www.waterconnect.sa.gov.au/Content/Downloads/DEW/...zip`, not a data.sa.gov.au-hosted file, for this edition only)
- `raw/2022-23/` — 5 XLSX files, unzipped from data.sa.gov.au-hosted zip archives
- `raw/2023-24/` — 5 XLSX files, downloaded directly from data.sa.gov.au (not zipped)
- `raw/2024-25/` — 5 XLSX files, downloaded directly from data.sa.gov.au (not zipped)

All 20 files downloaded directly over plain HTTPS this run — `data.sa.gov.au` and `waterconnect.sa.gov.au` were both directly reachable, no `fetch.sh` needed.

### `data/`

[`convert.py`](convert.py) reads all 20 raw workbooks with `openpyxl`, merges each point-in-time measure (Animals/Owners/breeds/names/top-5-by-council) across the 4 editions into one tidy table with an `edition` column, and keeps Incidents as the single most-current (2024-25) edition only, for the reasons above. `Microchipped`/`Desexed` `Y`/`N` flags are decoded to `Yes`/`No`. No count or percentage is recalculated, aggregated further or reinterpreted — every number is carried through exactly as published. Regenerate with `python3 convert.py` from this directory (requires `openpyxl`).

## Privacy note

Every field in every source workbook and every converted file is an aggregate count by council, species, gender, age-band, breed, incident characteristic or (for Owners) how many animals someone has — never an individual owner's name, address, animal microchip number, or any other person- or animal-identifying field. This matches the same "no individual-level identifying fields" check applied to every other dataset in this repository (see `datasets/sa-expiation-notices/README.md` for the precedent).
