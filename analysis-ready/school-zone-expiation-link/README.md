# School zone speed limits × expiation notice volume

A worked, sourced starting point for examining whether SA school-zone speed-limit changes relate to expiation notice volume. This module joins `datasets/sa-school-locations/`, `datasets/sa-expiation-notices/`, and a dated evidence log of the relevant policy change.

## The policy event

From **29 September 2025**, SA introduced a second, time-based 40 km/h "school precinct" speed limit alongside the existing 25 km/h "when children present" school zone limit. Full citations and dates: [`evidence/school-zone-speed-rule-change-2025.md`](evidence/school-zone-speed-rule-change-2025.md).

## Key methodology finding

The two school-zone-related speed limits are **enforced through, and recorded in, different reports** — this matters for anyone querying this data:

| Limit | Enforcement | Report | Confirmed by |
|---|---|---|---|
| 25 km/h "children present" (existing) | Predominantly officer-issued | **Manual Notice Offence Report** | Sampled records carry `Expiation Offence Description` = "EXCEED SCHOOL ZONE SPEED BY 10-19 KPH" (offence code A030) at `Expiation Zone Speed Limit` = "25" |
| 40 km/h time-based precinct (new, from Sep 2025) | Fixed/mobile camera | **Camera Offence Report** | New precinct signage includes electronic/camera-style time-of-operation signs, per DIT |

A naive filter on `Expiation Zone Speed Limit = "25"` against the **Camera** Offence Report returns **zero rows in all three financial years checked** (FY23-24, FY24-25, FY25-26) — the 25 km/h school-zone limit essentially isn't camera-enforced in this data. The same filter against the **Manual** Notice report returns real, on-topic records. Start from the Manual report for the 25 km/h side, and don't assume the two speed limits are interchangeable or additive.

The 40 km/h precinct zone is too new and too small (3 sites live from November 2025, expanding to ~150 by end of 2026, per DIT) to cleanly separate from ordinary 40 km/h camera enforcement using the speed-limit field alone — most 40 km/h camera offences are just everyday urban street enforcement, unrelated to school precincts. That split needs a live-site list matched by location and date, which DIT has not published in structured form as of this writing. Treat any "40 km/h" count from the Camera report as **general 40 km/h enforcement, not precinct-specific**, until that list exists.

## What's in `data/`

[`school_zone_expiation_counts_by_fy.csv`](data/school_zone_expiation_counts_by_fy.csv) — offence counts at `Expiation Zone Speed Limit = "25"` in the Manual Notice Offence Report, by financial year, pulled live via the CKAN `datastore_search` API (method documented in [`/scripts/sa_expiation_datastore_query.py`](../../scripts/sa_expiation_datastore_query.py)):

| Financial year | Count | Note |
|---|---|---|
| 2023-24 | 747 | Full year, before the Sep 2025 change |
| 2024-25 | 828 | Full year, before the Sep 2025 change |
| 2025-26 | 787 | Partial year (data current to ~May 2026); includes the Sep 2025 change and the start of the 40 km/h rollout |

**This is a starting point, not a finished analysis.** Before drawing any conclusion from these three numbers:

1. **Normalise for exposure.** FY25-26 is roughly 10 months of data, not 12 — 787 over ~10 months is a higher monthly rate than 828 over 12, but that alone doesn't establish anything about the rule change; school-term calendars, weather and enrolment growth all move this number too.
2. **Get monthly granularity.** The API supports date-range filtering on `Incident Start Date` — pull month-by-month counts and plot against 29 September 2025 and the (currently unpublished) phased rollout dates for individual schools.
3. **Watch the denominator.** A new 40 km/h precinct at a given school doesn't mechanically change that school's *25 km/h* count — they're different enforcement channels covering different times of day. If the real research question is specifically about the new 40 km/h precinct, that requires the live-site list (not yet published), not this table.
4. **Spatial join is available but not yet used here.** `datasets/sa-school-locations/` carries a `SCHOOL_ZONE` (Y/N) flag and `SUBURB`/`LOCAL_GOVERNMENT_AREA` fields; `datasets/sa-expiation-notices/` carries `Location Suburb` on the Camera report (the Manual report has no location field at all — only `District/Service Area`, a coarser policing region). A suburb-level join is possible for the Camera side; the Manual (25 km/h) side can only be joined at the District/Service Area level unless SAPOL publishes a finer location field for manually-issued notices.

## Reproducing or extending this

Every count above was pulled with a plain HTTPS GET against `data.sa.gov.au`'s public CKAN API — no authentication, no download required:

```
GET https://data.sa.gov.au/data/api/3/action/datastore_search
    ?resource_id={manual_notice_resource_id}
    &filters={"Expiation Zone Speed Limit":"25"}
    &limit=1
```

`result.total` in the response is the count — no need to page through actual rows just to count them. See [`/scripts/sa_expiation_datastore_query.py`](../../scripts/sa_expiation_datastore_query.py) for a small Python wrapper, and swap in resource IDs from `datasets/sa-expiation-notices/README.md` for other financial years or the Camera report.

Note: this API worked from the web-fetch tool available in the session that built this repository, but the *same session's* bash/curl sandbox was blocked from reaching `data.sa.gov.au` entirely (network allowlist). If you're scripting this yourself, a normal internet connection is enough — nothing about the API requires anything unusual.
