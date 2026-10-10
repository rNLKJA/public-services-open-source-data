#!/usr/bin/env python3
"""Convert the DCCEEW threatened species / ecological communities state lists into tidy CSVs."""
import csv
import re
from pathlib import Path

RAW = Path(__file__).parent / "raw"
OUT = Path(__file__).parent / "data"
OUT.mkdir(exist_ok=True)

SPECIES_RENAME = {
    "Scientific Name": "scientific_name",
    "Common Name": "common_name",
    "Current Scientific Name": "current_scientific_name",
    "Threatened status": "threatened_status",
    "ACT": "act",
    "NSW": "nsw",
    "NT": "nt",
    "QLD": "qld",
    "SA": "sa",
    "TAS": "tas",
    "VIC": "vic",
    "WA": "wa",
    "ACI": "aci_ashmore_cartier_islands",
    "CKI": "cki_cocos_keeling_islands",
    "CI": "ci_christmas_island",
    "CSI": "csi_coral_sea_islands",
    "JBT": "jbt_jervis_bay_territory",
    "NFI": "nfi_norfolk_island",
    "HMI": "hmi_heard_mcdonald_islands",
    "AAT": "aat_australian_antarctic_territory",
    "CMA": "cma_commonwealth_marine_area",
    "Listed SPRAT TaxonID": "listed_sprat_taxon_id",
    "Current SPRAT TaxonID": "current_sprat_taxon_id",
    "Kingdom": "kingdom",
    "Class": "class",
    "Profile": "sprat_profile_url",
    "Date extracted": "date_extracted",
    "NSL Name": "nsl_name_url",
    "Family": "family",
    "Genus": "genus",
    "Species": "species",
    "Infraspecific Rank": "infraspecific_rank",
    "Infraspecies": "infraspecies",
    "Species Author": "species_author",
    "Infraspecies Author": "infraspecies_author",
}

COMMUNITY_RENAME = {
    "Community": "community_name",
    "EPBC Status": "epbc_status",
    "ID": "listed_community_id",
    "ACT": "act",
    "NSW": "nsw",
    "NT": "nt",
    "QLD": "qld",
    "SA": "sa",
    "TAS": "tas",
    "VIC": "vic",
    "WA": "wa",
    "Profile": "sprat_profile_url",
    "Date extracted": "date_extracted",
}

MONTHS = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
    "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
}


def iso_date(value):
    m = re.match(r"^(\d{4})-([A-Za-z]{3})-(\d{2})$", value.strip())
    if not m:
        return value
    year, mon, day = m.groups()
    return f"{year}-{MONTHS[mon]}-{day}"


def convert(raw_name, rename, out_name, sa_out_name):
    with open(RAW / raw_name, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    fieldnames = [rename[h] for h in reader.fieldnames]
    processed = []
    for row in rows:
        new_row = {rename[k]: v for k, v in row.items()}
        new_row["date_extracted"] = iso_date(new_row["date_extracted"])
        processed.append(new_row)

    with open(OUT / out_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed)

    sa_rows = [r for r in processed if r["sa"].strip() == "Yes"]
    with open(OUT / sa_out_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sa_rows)

    return len(processed), len(sa_rows)


if __name__ == "__main__":
    n_species, n_species_sa = convert(
        "threatened-species-state-lists-2026-02-06.csv",
        SPECIES_RENAME,
        "threatened-species-state-lists.csv",
        "threatened-species-sa.csv",
    )
    n_comm, n_comm_sa = convert(
        "ecological-communities-state-lists-2026-03-20.csv",
        COMMUNITY_RENAME,
        "threatened-ecological-communities-state-lists.csv",
        "threatened-ecological-communities-sa.csv",
    )
    print(f"Species: {n_species} total, {n_species_sa} SA-occurring")
    print(f"Ecological communities: {n_comm} total, {n_comm_sa} SA-occurring")
