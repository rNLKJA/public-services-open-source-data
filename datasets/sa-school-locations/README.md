# SA School Locations

**Source:** SA Department for Education, published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/south-australian-government-education-site)
**Licence:** CC BY 4.0 (dataset); CC BY 3.0 AU (metadata report)
**Update frequency:** Nightly (spatial layer), daily (dataset record)
**Retrieved:** 6 July 2026
**Coverage:** Government schools and preschools only — no Catholic or independent sector.

## What it is

A spatial (point) dataset of every open SA government education site: schools, preschools, child care and non-school service units, derived nightly from the Department for Education's Location Sites and Services (LSS) database.

## Why it matters for this repo

The field list includes **`SCHOOL_ZONE`** — a direct Y/N flag for whether the site operates a formal school zone. That's a far more reliable join key for school-zone analysis than inferring school-zone status from street names or proximity, and it comes straight from the Department's own LSS database rather than being derived.

## Fields (selected — full list in the [official metadata report](https://location.sa.gov.au/LMS/Reports/ReportMetadata.aspx?p_no=2211&pu=y))

| Field | Description |
|---|---|
| `SITE_NAME` / `SITE_SHORT_NAME` | School/preschool name |
| `STREET_ADDRESS`, `SUBURB`, `POST_CODE` | Location |
| `CATEGORY_NAME` | School / Preschool / Child Care / Non School Service Unit |
| `SITE_TYPE`, `SITE_SUB_TYPE` | Primary / Secondary / Combined / Special, etc. |
| **`SCHOOL_ZONE`** | **Y/N — operates a formal school zone. Note: combined Reception-to-Year-12 schools may have a high-school zone but no primary zone.** |
| `LOCAL_GOVERNMENT_AREA` | Direct LGA name — joins straight to council data without a separate spatial join |
| `INDEX_DISADVANTAGE`, `ICSEA_VALUE` | Socio-educational context, useful for equity-weighted analysis |
| `OPEN_IND`, `OPENED_DATE` | Whether the site is currently open, and since when |

Enrolment (`FTE_ENROLMENTS_*`) fields exist per-year but the source explicitly warns they should not be summed across sites to derive a total, since the spatial layer only shows currently-open sites.

## Access method

Offered only as zipped Shapefile / GeoJSON / KML on `dptiapps.com.au` — a domain this working environment's network policy blocks for direct download, and the web-fetch tool available here can't unpack zip archives either. Run [`fetch.sh`](fetch.sh) from a machine with normal internet access to pull the actual point data; it isn't blocked there, only in this session's sandbox.

## Excluded on purpose: ACARA My School / Australian Schools List

ACARA's "My School" data (`School Location YYYY.xlsx`) is the only source found with sector (government/Catholic/independent) + address + coordinates in one file — but its [Terms of Use](https://myschool.edu.au/terms-of-use) restrict it to non-commercial, non-redistributable use and explicitly prohibit posting it on a public website. It's excluded from this repository for that reason. The Australian Schools List (asl.acara.edu.au) has sector data under CC BY 4.0 but no confirmed bulk-download endpoint as of this writing — worth revisiting if per-school sector lookup becomes worthwhile for non-government schools.
