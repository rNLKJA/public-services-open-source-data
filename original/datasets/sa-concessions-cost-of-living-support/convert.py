"""Converts the raw DHS Concessions and Support Services docx/PDF resources into tidy CSVs.

Sources (raw/):
  cost-of-living-concessions-original.docx        -- COLC 2015-16 (prose only, no table)
  cost-of-living-concession-2016-17.docx          -- COLC 2016-17 (prose only, no table)
  emergency-electricity-payment-scheme-original.docx     -- EEPS 2015-16 (tables)
  emergency-electricity-payment-scheme-2016-17.docx      -- EEPS 2016-17 (tables)
  cost-of-living-concessions-2017-18.pdf          -- combined 2017-18 "Concessions and Support
                                                        Services Open Data" report: COLC, EEPS,
                                                        GlassesSA, Funeral Assistance SA, Personal
                                                        Alert Systems Rebate Scheme

No figure is recalculated; only reshaped into long/tidy rows exactly as published.
"""
import csv
import os

RAW = os.path.join(os.path.dirname(__file__), "raw")
DATA = os.path.join(os.path.dirname(__file__), "data")


def write_csv(name, header, rows):
    path = os.path.join(DATA, name)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


# ---------------------------------------------------------------------------
# Cost of Living Concession (COLC) recipients by household category, by year
# Source note: in 2015-16 and 2016-17 editions, the CSHC figure is explicitly
# described as "a subset of homeowner-occupiers and tenants" (overlapping, not
# additive: homeowner + tenant = total). In the 2017-18 edition, the same three
# categories instead sum exactly to the year's total (134,957 + 7,916 + 31,979
# = 174,852) -- CSHC has become its own mutually-exclusive category that year.
# This is a genuine methodology change in the source, not a transcription
# error here, and is preserved via the `category_relationship_to_total` column
# rather than silently normalised.
# ---------------------------------------------------------------------------
colc_rows = [
    ("2015-16", "Homeowner-occupier", 153846, 84.0, 182819, "part of total"),
    ("2015-16", "Tenant", 28973, 16.0, 182819, "part of total"),
    ("2015-16", "Commonwealth Seniors Health Card (CSHC) recipients", 8210, 4.5, 182819,
     "subset/overlapping of homeowner-occupier + tenant -- do not add to the other two rows"),
    ("2016-17", "Homeowner-occupier", 150212, 83.0, 180513, "part of total"),
    ("2016-17", "Tenant", 30311, 17.0, 180513, "part of total"),
    ("2016-17", "Commonwealth Seniors Health Card (CSHC) recipients", 7834, 4.0, 180513,
     "subset/overlapping of homeowner-occupier + tenant -- do not add to the other two rows"),
    ("2017-18", "Homeowner-Occupier households", 134957, 77.0, 174852, "part of total"),
    ("2017-18", "Tenant households", 31979, 18.0, 174852, "part of total"),
    ("2017-18", "All households with Commonwealth Seniors Health Card (CSHC)", 7916, 5.0, 174852,
     "part of total (mutually exclusive category this year -- see note)"),
]
write_csv(
    "cost-of-living-concessions-by-category.csv",
    ["financial_year", "recipient_category", "recipient_count", "pct_of_year_total",
     "total_recipients_that_year", "category_relationship_to_total"],
    colc_rows,
)

# ---------------------------------------------------------------------------
# Emergency Electricity Payments Scheme (EEPS) -- approved applications
# ---------------------------------------------------------------------------
eeps_totals = [
    ("2015-16", 1170),
    ("2016-17", 1020),
    ("2017-18", 1014),
]
write_csv(
    "eeps-approved-applications-totals.csv",
    ["financial_year", "total_approved_applications"],
    eeps_totals,
)

eeps_by_reason = [
    ("2015-16", "Increase in electricity use", 57, 4.87),
    ("2015-16", "Decrease in income", 251, 21.45),
    ("2015-16", "Unexpected increase in expenses", 110, 9.40),
    ("2015-16", "Familial breakdown", 137, 11.71),
    ("2015-16", "Birth of a child/children", 13, 1.11),
    ("2015-16", "Medical conditions (suffer from or caring for)", 266, 22.74),
    ("2015-16", "Increased housing stress (mortgage/rent)", 22, 1.88),
    ("2015-16", "Experiencing acute, general, financial stress", 314, 26.84),
    ("2016-17", "Increase in electricity use", 50, 4.90),
    ("2016-17", "Decrease in income", 105, 10.29),
    ("2016-17", "Unexpected increase in expenses", 92, 9.02),
    ("2016-17", "Familial breakdown", 51, 5.00),
    ("2016-17", "Birth of a child/children", 6, 0.59),
    ("2016-17", "Medical conditions (suffer from or caring for)", 95, 9.31),
    ("2016-17", "Increased housing stress (mortgage/rent)", 15, 1.47),
    ("2016-17", "Experiencing acute, general, financial stress", 505, 49.51),
    ("2016-17", "Not recorded (NULL -- lost in 2016-17 system migration)", 101, 9.90),
    ("2017-18", "Increase in electricity use", 44, 4.3),
    ("2017-18", "Decrease in income", 220, 21.7),
    ("2017-18", "Unexpected increase in expenses", 96, 9.5),
    ("2017-18", "Familial breakdown", 118, 11.6),
    ("2017-18", "Birth of a child/children", 12, 1.2),
    ("2017-18", "Medical conditions (suffer from or caring for)", 224, 22.1),
    ("2017-18", "Increased housing stress (mortgage/rent)", 26, 2.6),
    ("2017-18", "Experiencing acute, general, financial stress", 274, 27.0),
]
write_csv(
    "eeps-approved-applications-by-reason.csv",
    ["financial_year", "reason_for_application", "approved_count", "pct_of_year_total"],
    eeps_by_reason,
)

eeps_by_region = [
    ("2015-16", "Adelaide Hills", 26, 2.22),
    ("2015-16", "Barossa", 58, 4.96),
    ("2015-16", "Eastern Adelaide", 45, 3.85),
    ("2015-16", "Eyre and Western", 64, 5.47),
    ("2015-16", "Far North", 28, 2.39),
    ("2015-16", "Fleurieu and Kangaroo Island", 19, 1.62),
    ("2015-16", "Limestone Coast", 66, 5.64),
    ("2015-16", "Murray and Mallee", 63, 5.38),
    ("2015-16", "Northern Adelaide", 381, 32.56),
    ("2015-16", "Southern Adelaide", 232, 19.83),
    ("2015-16", "Western Adelaide", 119, 10.17),
    ("2015-16", "Yorke and Mid North", 69, 5.90),
    ("2016-17", "Adelaide Hills", 28, 2.75),
    ("2016-17", "Barossa", 47, 4.61),
    ("2016-17", "Eastern Adelaide", 56, 5.49),
    ("2016-17", "Eyre and Western", 65, 6.37),
    ("2016-17", "Far North", 24, 2.35),
    ("2016-17", "Fleurieu and Kangaroo Island", 15, 1.47),
    ("2016-17", "Limestone Coast", 64, 6.27),
    ("2016-17", "Murray and Mallee", 67, 6.57),
    ("2016-17", "Northern Adelaide", 335, 32.84),
    ("2016-17", "Southern Adelaide", 177, 17.35),
    ("2016-17", "Western Adelaide", 103, 10.10),
    ("2016-17", "Yorke and Mid North", 35, 3.43),
    ("2016-17", "Not recorded (NULL -- lost in 2016-17 system migration)", 4, 0.39),
    ("2017-18", "Adelaide Hills", 24, 2.4),
    ("2017-18", "Barossa", 54, 5.3),
    ("2017-18", "Eastern Adelaide", 63, 6.2),
    ("2017-18", "Eyre and Western", 81, 8.0),
    ("2017-18", "Far North", 7, 0.7),
    ("2017-18", "Fleurieu and Kangaroo Island", 23, 2.3),
    ("2017-18", "Limestone Coast", 63, 6.2),
    ("2017-18", "Murray and Mallee", 68, 6.7),
    ("2017-18", "Northern Adelaide", 307, 30.3),
    ("2017-18", "Southern Adelaide", 168, 16.6),
    ("2017-18", "Western Adelaide", 112, 11.0),
    ("2017-18", "Yorke and Mid North", 44, 4.3),
]
write_csv(
    "eeps-approved-applications-by-region.csv",
    ["financial_year", "region", "approved_count", "pct_of_year_total"],
    eeps_by_region,
)

# ATSI summary -- every year states an overall ATSI-identified count; only
# 2016-17 also publishes a full identity-category breakdown (kept as a
# separate table below rather than force-fit into the same shape).
eeps_atsi_summary = [
    ("2015-16", 1170, 130, 11.1),
    ("2016-17", 1020, 103, None),  # 2016-17 total ATSI count not stated as prose; see detail table (5 + 98 = 103, sourced from the detailed breakdown table itself, not separately restated)
    ("2017-18", 1014, 90, 8.8),
]
write_csv(
    "eeps-atsi-summary.csv",
    ["financial_year", "total_approved_applications", "atsi_identified_count", "atsi_identified_pct"],
    eeps_atsi_summary,
)

eeps_atsi_detail_2016_17 = [
    ("2016-17", "Aboriginal", 5, 0.49),
    ("2016-17", "Aboriginal and Torres Strait Islander", 98, 9.61),
    ("2016-17", "Not Aboriginal and Torres Strait Islander", 702, 68.82),
    ("2016-17", "Not Specified", 100, 9.80),
    ("2016-17", "Not recorded (NULL -- lost in 2016-17 system migration)", 115, 11.27),
]
write_csv(
    "eeps-atsi-detail-2016-17.csv",
    ["financial_year", "atsi_identity_category", "approved_count", "pct_of_year_total"],
    eeps_atsi_detail_2016_17,
)

# ---------------------------------------------------------------------------
# Bonus programs from the same 2017-18 combined "Concessions and Support
# Services Open Data" PDF -- not part of the domain's original COLC/EEPS
# framing, but published under the same report, same licence, same year.
# Single-year snapshots only (these programs have no other edition mirrored).
# ---------------------------------------------------------------------------
glassessa_monthly = [
    ("2017-18", "July", 371), ("2017-18", "August", 405), ("2017-18", "September", 344),
    ("2017-18", "October", 334), ("2017-18", "November", 378), ("2017-18", "December", 221),
    ("2017-18", "January", 460), ("2017-18", "February", 667), ("2017-18", "March", 619),
    ("2017-18", "April", 569), ("2017-18", "May", 670),
]
write_csv(
    "glassessa-approved-applications-by-month-2017-18.csv",
    ["financial_year", "month", "approved_applications_count"],
    glassessa_monthly,
)

glassessa_lens_type = [
    ("2017-18", "Single Vision", 1821, 36.0),
    ("2017-18", "Bi-Focal", 1331, 27.0),
    ("2017-18", "Multi-focal", 932, 18.0),
    ("2017-18", "Single Vision grind lenses", 807, 16.0),
    ("2017-18", "Contact lenses", 147, 3.0),
]
write_csv(
    "glassessa-by-lens-type-2017-18.csv",
    ["financial_year", "lens_type", "count", "pct_of_year_total"],
    glassessa_lens_type,
)

funeral_assistance = [
    ("2017-18", "Total funeral assistance provided", 287),
    ("2017-18", "Of which ATSI", 92),
    ("2017-18", "Of which Metro", 183),
    ("2017-18", "Of which Country", 104),
]
write_csv(
    "funeral-assistance-sa-summary-2017-18.csv",
    ["financial_year", "metric", "value"],
    funeral_assistance,
)

personal_alert_monthly = [
    ("2017-18", "July", 281), ("2017-18", "August", 273), ("2017-18", "September", 271),
    ("2017-18", "October", 469), ("2017-18", "November", 464), ("2017-18", "December", 550),
    ("2017-18", "January", 418), ("2017-18", "February", 416), ("2017-18", "March", 353),
    ("2017-18", "April", 390), ("2017-18", "May", 425),
]
write_csv(
    "personal-alert-rebate-by-month-2017-18.csv",
    ["financial_year", "month", "rebates_count"],
    personal_alert_monthly,
)

print("done")
