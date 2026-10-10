"""Convert the raw NNTT FeatureServer JSON pulls into tidy, ready-to-use CSVs.

Source: National Native Title Tribunal (NNTT) spatial data, fetched directly
from the live ArcGIS FeatureServer (see README "Access method"). No figures
are recalculated - only field names are standardised to lower_snake_case,
epoch-millisecond dates are converted to ISO dates, and the returned
centroid point is added as plain longitude/latitude columns.

The ILUA layer's `Applicant` field is a free-text party-name field that, for
individually-held ILUAs (as opposed to state/council/corporate parties),
names the specific native title claimants or private counterparties acting
as the registered applicant - see README "Privacy check" for why these are
redacted here following this repository's standing rule against
individual-identifying fields in row-level data.
"""
import json
import csv
import re
from datetime import datetime, timezone


def epoch_ms_to_iso(value):
    if value is None:
        return ""
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


ORG_KEYWORDS = [
    "state of", "commonwealth", "shire of", "city of", "town of", "district council",
    "regional council", "municipal council", "corporation", "pty ltd", "pty limited", "ltd",
    "limited", "trust", "incorporated", "inc.", " inc ", "association", "authority",
    "department", "rntbc", "land council", "holdings", "enterprises", "mining",
    "resources", "operations", "joint venture", "council of", "agency", "commission", "board",
    "the honourable", "attorney-general", "minister", "governor", "crown in right",
    "university", "institute", "ministry", "abn ", "acn ", "icn ", "co-operative",
    "cooperative", "company", " co ", "railways", "water corporation", "electricity",
    "power", "gas", "network", "pipeline", "aboriginal corporation", "native title service",
    "trustee", "queensland", "tasmania", "victoria", "new south wales", "western australia",
    "northern territory", "australian capital territory", "south australia", "national parks",
    "forestry", "council", "regional", "shire", "the crown", "zinc", "metals",
    "convention centre", "southern cross", "ergon", "energex", "steel", "coal", "petroleum",
    "pastoral", "station pty", "solar", "wind farm", "hydro", "renewable", "exploration",
    "catholic", "anglican", "diocese", "uniting church", "tafe", "hospital", "health service",
    "airport", "port authority", "rail ", " rail", "stadium", "racing", "golf club", "rsl",
    "telstra", "optus", "nbn", "qantas", "partnership", "pty. ltd", "plc", "nl ", " nl",
    "holding pty",
]

# Phrases marking the start of a descriptive/legal "tail" clause that is never
# itself a party name (native title claim group boilerplate, capacity
# descriptions, quoted party labels) - text from the first match onward is
# left untouched rather than fed into name-segment classification.
TAIL_MARKERS = [
    "on behalf of", "on their own behalf", "on his own behalf", "on her own behalf",
    "in his capacity", "in her capacity", "as trustee", "acting through",
    "as the registered native title claimant", "the native title part",
    "being the persons who", "as the applicant", "as the persons", "for and on behalf",
    "native title claim group", "native title parties", "federal court proceedings",
    "together with their successors", "attention:",
]

# A bare personal name (or first-name fragment of one, e.g. the "Alan" in
# "Alan and Karen Pedersen"): 1-6 capitalised words, allowing hyphens/
# apostrophes/initials, no digits, no company-style punctuation.
PERSON_NAME_RE = re.compile(
    r"^(?:[A-Z][a-zA-Z'.\-]*\s*){1,6}$"
)

REDACTED_APPLICANT = "[individual applicant(s) - name(s) withheld for privacy]"


def _split_core_tail(value):
    low = value.lower()
    earliest = len(value)
    for marker in TAIL_MARKERS:
        idx = low.find(marker)
        if idx != -1 and idx < earliest:
            earliest = idx
    return value[:earliest], value[earliest:]


def _classify_segment(segment):
    seg = segment.strip().strip(",")
    if not seg:
        return None
    low = seg.lower()
    if any(k in low for k in ORG_KEYWORDS):
        return "org"
    # Strip a trailing/embedded parenthetical (e.g. "(formerly Whyman)", a
    # former surname) before testing whether the remainder is a bare name -
    # the parenthetical is dropped along with the rest of the segment below
    # if it turns out to just be more identifying detail about the same person.
    base = re.sub(r"\([^)]*\)", "", seg).strip()
    if PERSON_NAME_RE.match(base):
        return "person"
    return "other"


def redact_applicant(value):
    if not value or not value.strip():
        return ""
    core, tail = _split_core_tail(value.strip())
    # Top-level split only (commas / standalone "and"/"&") - good enough for
    # the party-list patterns this field actually uses.
    segments = re.split(r",| and | & ", core)
    out_parts = []
    prev_was_person = False
    for seg in segments:
        kind = _classify_segment(seg)
        if kind is None:
            continue
        if kind == "person":
            if not prev_was_person:
                out_parts.append(REDACTED_APPLICANT)
            prev_was_person = True
        else:
            out_parts.append(seg.strip())
            prev_was_person = False
    if not out_parts:
        # Nothing recognisable survived (e.g. the whole core was a bare name) -
        # fall back to a single redaction marker rather than an empty string.
        out_parts = [REDACTED_APPLICANT]
    result = ", ".join(out_parts)
    tail = tail.strip()
    if tail:
        result = f"{result} {tail}"
    return result


def load_features(path):
    with open(path) as f:
        return json.load(f)["features"]


DETERMINATION_FIELDS = [
    ("Tribunal_ID", "tribunal_id", None),
    ("Name", "name", None),
    ("FC_No", "federal_court_no", None),
    ("FC_Name", "federal_court_case_name", None),
    ("Determination_Date", "determination_date", epoch_ms_to_iso),
    ("NNTR_Registration_Date", "nntr_registration_date", epoch_ms_to_iso),
    ("Determined_Method", "determined_method", None),
    ("Determination_Type", "determination_status", None),
    ("Determined_Outcome", "determined_outcome", None),
    ("RNTBC_Name", "rntbc_name", None),
    ("Related_NTDA", "related_native_title_determination_application", None),
    ("Area_Sqkm", "area_sqkm", None),
    ("Date_Currency", "date_currency", epoch_ms_to_iso),
    ("Linked_File_No", "linked_federal_court_judgment_url", None),
    ("Jurisdiction", "jurisdiction", None),
    ("Overlap", "overlap_note", None),
    ("Date_extracted", "date_extracted", epoch_ms_to_iso),
    ("Claimant_Type", "claimant_type", None),
]

ILUA_FIELDS = [
    ("Tribunal_ID", "tribunal_id", None),
    ("Name", "name", None),
    ("Agreement_Status", "agreement_status", None),
    ("Date_Lodged", "date_lodged", epoch_ms_to_iso),
    ("Date_Notified", "date_notified", epoch_ms_to_iso),
    ("Date_Registered", "date_registered", epoch_ms_to_iso),
    ("Agreement_Type", "agreement_type", None),
    ("Applicant", "applicant", redact_applicant),
    ("Area_Sqkm", "area_sqkm", None),
    ("Date_Currency", "date_currency", epoch_ms_to_iso),
    ("Jurisdiction", "jurisdiction", None),
    ("Overlap", "overlap_note", None),
    ("Date_extracted", "date_extracted", epoch_ms_to_iso),
]


def convert(raw_path, out_path, field_map):
    features = load_features(raw_path)
    header = [dest for _src, dest, _fn in field_map] + ["centroid_longitude", "centroid_latitude"]
    rows = []
    for feat in features:
        attrs = feat["attributes"]
        row = []
        for src, _dest, fn in field_map:
            value = attrs.get(src)
            row.append(fn(value) if fn else (value if value is not None else ""))
        centroid = feat.get("centroid") or {}
        row.append(centroid.get("x", ""))
        row.append(centroid.get("y", ""))
        rows.append(row)
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n_det = convert(
        "raw/native-title-determinations.json",
        "data/au-native-title-determinations.csv",
        DETERMINATION_FIELDS,
    )
    n_ilua = convert(
        "raw/indigenous-land-use-agreements.json",
        "data/au-indigenous-land-use-agreements.csv",
        ILUA_FIELDS,
    )
    print(f"Wrote {n_det} determination rows, {n_ilua} ILUA rows")
