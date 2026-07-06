"""
Two jobs in one pass, run in this order:

1. Privacy redaction. Unlike every other source in this repo, the SARIG
   mineral-tenements register legitimately mixes company/organisation holders
   with natural-person holders - South Australian "private mines" and some
   small mineral leases/claims can be held directly by an individual
   landholder under the Mining Act 1971, not just by a registered company.
   A direct field-name check (company-indicator keywords) is used to tell
   the two apart; any holder/applicant value that does not match a company
   indicator is treated as an individual and replaced with a fixed
   redaction marker before anything is written to raw/ or data/. This
   applies the same "no individual-identifying fields in row-level data"
   rule used elsewhere in this repo (see sa-expiation-notices) to a source
   that, uniquely so far, actually contains some.
   Because of this, raw/ here is NOT a byte-for-byte mirror of the WFS
   response the way raw/ is for every other dataset in this repo - it has
   had this one field redacted, disclosed plainly in the README rather than
   silently deviating from the usual "raw is untouched" convention.

2. Merge the (now redacted) 13 layers into three tidy CSVs: granted
   tenements, pending applications, and released/relinquished exploration
   areas. No figures are recalculated - only reshaped (per-layer JSON ->
   long CSV with a *_category column) and codes decoded. Geometry is
   reduced to a bounding-box-centre longitude/latitude pair for easy
   mapping; the full polygon geometry is preserved in raw/*.json.
"""
import csv
import json
import re
from pathlib import Path

RAW = Path(__file__).parent.parent / "raw"
OUT = Path(__file__).parent

REDACTED = "[individual holder - name withheld for privacy]"

# Values that look like a personal name under the classifier below but are
# actually an organisation/community group, confirmed by inspection.
NOT_INDIVIDUALS = {"DEM - Regulation and Compliance", "Wangka Wangka"}

COMPANY_KEYWORDS = re.compile(
    r"(pty|ltd|limited|proprietary|proprietors?|corp|corporation|council|"
    r"authority|trust|holdings|inc\b|incorporated|association|society|"
    r"co-?op|group|department|government|board|nominees|investments|"
    r"resources|mining|quarr|brick|cement|industries|development|"
    r"manufactur|contractors?|club|hotel|company|the trustee|city of|"
    r"district council|shire|university|church|school|bros\b|services|"
    r"enterprises|engineering|transport|agenc(y|ies)|resourceco|waste|"
    r"cartage|earthmov|excavat|concrete|stone(s)?\b|sands?\b|gravel|"
    r"aggregate|materials|laboratory|minerals?|metals?|steel|building|"
    r"construction|civil|operating as|formerly|liquidation|de-?registered|"
    r"administrators|superannuation|family trust)",
    re.I,
)


def redact_value(value):
    if not value:
        return value
    parts = [p.strip() for p in value.split(";")]
    out = []
    for part in parts:
        if not part:
            continue
        if part in NOT_INDIVIDUALS or COMPANY_KEYWORDS.search(part):
            out.append(part)
        else:
            out.append(REDACTED)
    return "; ".join(out)


# layer -> JSON property holding the holder/applicant name(s)
NAME_FIELD = {
    "mineral_and_or_opal_exploration_licence": "LICENCEES",
    "mineral_leases": "TENEMENT_HOLDERS",
    "extractive_mineral_leases": "TENEMENT_HOLDERS",
    "retention_leases": "TENEMENT_HOLDERS",
    "mineral_claims": "TENEMENT_HOLDERS",
    "miscellaneous_purposes_leases": "TENEMENT_HOLDERS",
    "olympic_dam_sml": "TENEMENT_HOLDERS",
    "private_mines": "TENEMENT_HOLDERS",
    "mineral_and_or_opal_exploration_licence_applications": "APPLICANTS",
    "mining_and_production_tenement_applications": "APPLICANTS",
    "mining_and_production_lease_applications": "APPLICANTS",
    "exploration_release_areas_released": "APPLICANTS",
    "relinquished_ground": "APPLICANTS",
}

redacted_count = 0
for layer, field in NAME_FIELD.items():
    path = RAW / f"{layer}.json"
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    for feat in d["features"]:
        original = feat["properties"].get(field)
        new = redact_value(original)
        if new != original:
            redacted_count += 1
        feat["properties"][field] = new
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f)
print(f"redacted {redacted_count} holder/applicant values across {len(NAME_FIELD)} raw layer files")

# South Australian Mining Act 1971 tenement/application type codes, decoded
# from SA Dept for Energy and Mining, "Types of mining tenure"
# (https://www.energymining.sa.gov.au/industry/minerals-and-mining/mining/establish-a-mine-or-quarry/types-of-mining-tenure)
TYPE_CODES = {
    "EL": "Exploration Licence",
    "ELA": "Exploration Licence Application",
    "ML": "Mining Lease (formerly Mineral Lease)",
    "EML": "Mining Lease (formerly Extractive Minerals Lease; merged into Mining Lease from 1 Jan 2021)",
    "RL": "Retention Lease",
    "MC": "Mineral Claim",
    "MCA": "Mineral Claim Application",
    "MPL": "Miscellaneous Purposes Licence",
    "MPLA": "Miscellaneous Purposes Licence Application",
    "SML": "Special Mining Lease (Olympic Dam, granted under the Roxby Downs (Indenture Ratification) Act 1982)",
    "PM": "Private Mine",
    "PMA": "Private Mine Area",
}


def bbox_centre(geometry):
    """Bounding-box centre of a Polygon/MultiPolygon - a representative point,
    not a true area-weighted centroid."""
    if geometry is None:
        return None, None
    coords = geometry.get("coordinates")
    gtype = geometry.get("type")
    pts = []

    def walk(c):
        if isinstance(c[0], (int, float)):
            pts.append(c)
        else:
            for sub in c:
                walk(sub)

    if gtype in ("Polygon", "MultiPolygon"):
        walk(coords)
    if not pts:
        return None, None
    lons = [p[0] for p in pts]
    lats = [p[1] for p in pts]
    return (min(lons) + max(lons)) / 2, (min(lats) + max(lats)) / 2


def load(layer):
    with open(RAW / f"{layer}.json", encoding="utf-8") as f:
        d = json.load(f)
    return d["features"]


def get(props, *keys):
    for k in keys:
        v = props.get(k)
        if v not in (None, ""):
            return v
    return ""


# ---------------------------------------------------------------------------
# 1. Granted tenements (currently active): exploration licences, mining
#    leases, retention leases, mineral claims, miscellaneous purposes
#    licences, the Olympic Dam special mining lease, and private mines.
# ---------------------------------------------------------------------------
GRANTED_LAYERS = [
    "mineral_and_or_opal_exploration_licence",
    "mineral_leases",
    "extractive_mineral_leases",
    "retention_leases",
    "mineral_claims",
    "miscellaneous_purposes_leases",
    "olympic_dam_sml",
    "private_mines",
]

granted_rows = []
for layer in GRANTED_LAYERS:
    for feat in load(layer):
        p = feat["properties"]
        lon, lat = bbox_centre(feat.get("geometry"))
        type_code = get(p, "TENEMENT_TYPE")
        granted_rows.append({
            "tenement_category": layer,
            "tenement_type_code": type_code,
            "tenement_type_desc": TYPE_CODES.get(type_code, ""),
            "tenement_number": get(p, "TENEMENT_NUMBER"),
            "tenement_label": get(p, "TENEMENT_LABEL"),
            "tenement_status": get(p, "TENEMENT_STATUS"),
            "holders": get(p, "TENEMENT_HOLDERS", "LICENCEES"),
            "operators": get(p, "TENEMENT_OPERATORS", "OPERATORS"),
            "location": get(p, "LOCATION"),
            "legal_area": get(p, "LEGAL_AREA", "AREA_LEGAL"),
            "area_unit": get(p, "AREA_UNIT"),
            "grant_date": get(p, "REGISTRATION_GRANT_DATE", "TENEMENT_START_DATE"),
            "surrender_date": get(p, "SURRENDER_DATE", "TENEMENT_SURRENDER_DATE"),
            "expiry_date": get(p, "EXPIRY_DATE", "TENEMENT_EXPIRY_DATE"),
            "renewal_received_date": get(p, "RENEWAL_RECEIVED_DATE", "RENEWAL_APPLICATION_DATE"),
            "transfer_received_date": get(p, "TRANSFER_RECEIVED_DATE", "TRANSFER_APPLICATION_DATE"),
            "surrender_received_date": get(p, "SURRENDER_RECEIVED_DATE"),
            "commodities": get(p, "COMMODITIES", "COMMODITIES_SOUGHT"),
            "commodity_categories": get(p, "COMMODITY_CATEGORIES"),
            "court_action_pending": get(p, "COURT_ACTION_PENDING"),
            "mpl_purpose": get(p, "MPL_PURPOSE"),
            "operation_name": get(p, "OPERATION_NAME"),
            "operation_status": get(p, "OPERATION_STATUS"),
            "operation_method": get(p, "OPERATION_METHOD"),
            "reports_and_related_records": get(p, "REPORTS_AND_RELATED_RECORDS"),
            "prior_tenement": get(p, "PRIOR_TENEMENT"),
            "subsequent_tenement": get(p, "SUBSEQUENT_TENEMENT"),
            "longitude": lon,
            "latitude": lat,
        })

with open(OUT / "sa-mineral-tenements-granted.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(granted_rows[0].keys()))
    w.writeheader()
    w.writerows(granted_rows)
print(f"granted: {len(granted_rows)} rows")

# ---------------------------------------------------------------------------
# 2. Pending applications: exploration licence, mineral claim/production
#    tenement, and mining/extractive lease applications not yet granted.
# ---------------------------------------------------------------------------
APPLICATION_LAYERS = [
    "mineral_and_or_opal_exploration_licence_applications",
    "mining_and_production_tenement_applications",
    "mining_and_production_lease_applications",
]

application_rows = []
for layer in APPLICATION_LAYERS:
    for feat in load(layer):
        p = feat["properties"]
        lon, lat = bbox_centre(feat.get("geometry"))
        type_code = get(p, "APPLICATION_TYPE", "LEASE_TYPE")
        application_rows.append({
            "application_category": layer,
            "application_type_code": type_code,
            "application_type_desc": TYPE_CODES.get(type_code, ""),
            "file_reference": get(p, "FILE_REFERENCE"),
            "project_name": get(p, "PROJECT_NAME"),
            "applicants": get(p, "APPLICANTS"),
            "location": get(p, "LOCATION"),
            "application_received_date": get(p, "APPLICATION_RECEIVED_DATE", "DATE_RECEIVED", "PEGGING_DATE"),
            "legal_area": get(p, "LEGAL_AREA"),
            "area_unit": get(p, "AREA_UNIT"),
            "commodities": get(p, "COMMODITIES_SOUGHT", "MCA_COMMODITIES", "COMMODITIES"),
            "mineral_type": get(p, "MINERAL_TYPE"),
            "mpl_purpose": get(p, "MPL_PURPOSE"),
            "prior_tenement": get(p, "PRIOR_TENEMENT"),
            "related_tenements": get(p, "RELATED_TENEMENTS"),
            "related_applications": get(p, "RELATED_APPLICATIONS"),
            "native_title": get(p, "NATIVE_TITLE"),
            "outcome_or_status": get(p, "OUTCOME", "ASSESSMENT_STATUS"),
            "outcome_date": get(p, "OUTCOME_DATE", "DATE_ASSESSMENT_COMPLETED"),
            "resulting_tenement": get(p, "RESULTING_TENEMENT", "RESULTING_CLAIM_LICENCE"),
            "longitude": lon,
            "latitude": lat,
        })

with open(OUT / "sa-mineral-tenements-applications.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(application_rows[0].keys()))
    w.writeheader()
    w.writerows(application_rows)
print(f"applications: {len(application_rows)} rows")

# ---------------------------------------------------------------------------
# 3. Released/relinquished exploration areas: ground given up by a prior
#    tenement holder and re-released for new applications.
# ---------------------------------------------------------------------------
RELEASE_LAYERS = ["exploration_release_areas_released", "relinquished_ground"]

release_rows = []
for layer in RELEASE_LAYERS:
    for feat in load(layer):
        p = feat["properties"]
        lon, lat = bbox_centre(feat.get("geometry"))
        release_rows.append({
            "area_category": layer,
            "area_type": get(p, "AREA_TYPE"),
            "era_number": get(p, "ERA_NUMBER"),
            "file_reference": get(p, "FILE_REFERENCE"),
            "location": get(p, "LOCATION"),
            "legal_area_km2": get(p, "LEGAL_AREA", "AREA_LEGAL__KM2"),
            "area_status": get(p, "AREA_STATUS"),
            "publish_date": get(p, "PUBLISH_DATE"),
            "area_start_date": get(p, "AREA_START_DATE"),
            "area_end_date": get(p, "AREA_END_DATE"),
            "application_open_date": get(p, "APPLICATION_OPEN_DATE"),
            "application_close_date": get(p, "APPLICATION_CLOSE_DATE"),
            "term_years": get(p, "TERM_YEARS"),
            "term_days": get(p, "TERM_DAYS"),
            "finalised_date": get(p, "FINALISED_DATE"),
            "applicants": get(p, "APPLICANTS"),
            "related_tenements": get(p, "RELATED_TENEMENTS"),
            "criteria": get(p, "CRITERIA", "CRITERA"),
            "longitude": lon,
            "latitude": lat,
        })

with open(OUT / "sa-mineral-tenements-released-areas.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(release_rows[0].keys()))
    w.writeheader()
    w.writerows(release_rows)
print(f"released areas: {len(release_rows)} rows")
