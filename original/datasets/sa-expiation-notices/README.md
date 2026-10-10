# SA Expiation Notice Data

**Source:** South Australia Police (SAPOL), published via [data.sa.gov.au](https://data.sa.gov.au/data/dataset/expiation-notice-system-data)
**Licence:** [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0) (CC BY 4.0)
**Update frequency:** Monthly, current + previous 3 financial years
**Temporal coverage:** 2012-07-01 onward
**Retrieved:** 6 July 2026

## What it is

The Expiation Notice Branch Offence Data Reports list every offence raised by SAPOL for expiation (South Australia's on-the-spot infringement notice system), split into three reports per financial year:

- **Camera Offence Report** — offences from fixed and mobile speed/red-light cameras.
- **Manual Notice Offence Report** — offences issued directly by a police officer.
- **Camera Not Accepted Report** — camera detections that did not result in a notice.

One row represents one offence, not one notice — a notice can carry multiple offences or be reissued (see `Event ID` / `Notice Revision` in the Camera report).

## Fields

Full official dictionary: [`raw/expiation_data_dictionary.txt`](raw/expiation_data_dictionary.txt) (mirrored verbatim from SAPOL).

No record includes a name, home address, or full vehicle registration plate — see `COMPLIANCE.md` at the repository root for the full privacy reasoning. Key fields: `Incident Start Date`, `Expiation Offence Code`/`Description`, `Camera Category` (Camera report only), `Location Code`/`Description`/`Suburb`, `Vehicle Speed`, `Expiation Zone Speed Limit`, and penalty amounts.

## Access method

Recent financial years are offered as zipped CSV archives on data.sa.gov.au, which this working environment's network policy blocks for direct download (see "Known limitation" below). Every resource is also queryable live through CKAN's open `datastore_search` API — no key required:

```
https://data.sa.gov.au/data/api/3/action/datastore_search?resource_id={id}&limit={n}&filters={"Field Name":"value"}
```

`datastore_search_sql` (server-side SQL) did not respond successfully when tried and may be disabled on this portal — `datastore_search` with `filters`/`q` covers everything used here, including cheap counts (request `limit=1` and read `result.total`).

### Resource IDs (as at 6 July 2026)

| Financial year | Report | Resource ID | Total rows at retrieval |
|---|---|---|---|
| 2023-24 | Camera Offence | `8db0706c-3646-4008-858b-fad556a19cf6` | 321,674 |
| 2023-24 | Manual Notice | `e15bd191-311e-4298-b1b0-e29b545d4de0` | not queried in full |
| 2024-25 | Camera Offence | `e8b96d68-f753-4f9c-802b-5daed9fe703d` | 400,174 |
| 2024-25 | Manual Notice | `3c1a3cbf-ed40-45f4-8be0-be6376e1fd3a` | not queried in full |
| 2025-26 (partial, data current to ~May 2026) | Camera Offence | `3ffeb133-9242-432c-b5fe-aba5b5d19649` | 217,373 |
| 2025-26 (partial) | Manual Notice | `81c3fbcd-908c-49e9-8e77-ec26595d045d` | not queried in full |

Check the [dataset page](https://data.sa.gov.au/data/dataset/expiation-notice-system-data) for newer financial years and updated resource IDs as they're published monthly.

A reusable query helper is in [`/scripts/sa_expiation_datastore_query.py`](../../scripts/sa_expiation_datastore_query.py).

## Known limitation

The zipped CSV archives (`*-camera-offence-report.zip`, `*-manual-notice-offence-report.zip`) sit on `data.sa.gov.au`, which this working environment's outbound network policy blocks for direct download (`curl`/`wget` return a proxy `403 blocked-by-allowlist`), and the web-fetch tool available here can't unpack zip archives. The `datastore_search` API above returns the same underlying rows as JSON over plain HTTPS and was used to verify structure and pull real counts for `analysis-ready/school-zone-expiation-link/`. For a full local mirror of the raw zips, run [`fetch.sh`](fetch.sh) from a machine with normal internet access — it isn't blocked there, only in this session's sandbox.

## Not included: Mobile Camera Location Codes reference table

data.sa.gov.au also publishes a `Location Code, Street, Suburb` lookup for mobile speed camera sites ([resource](https://data.sa.gov.au/data/dataset/expiation-notice-system-data/resource/892be609-41b7-4923-b0d8-da456da0357f)). It has no "school zone" flag of its own and isn't needed for the 25 km/h school-zone analysis in `analysis-ready/` (that offence type is officer-issued, not camera-issued — see that module's README) so it wasn't mirrored in this pass. It's fetchable the same way as everything else here if a later analysis needs it (e.g. for the newer 40 km/h camera-enforced precinct zones).
