# Malawi — the 2018 census

The 2018 Malawi Population and Housing Census (2018 PHC), September 2018, by the National Statistical Office (NSO).

- `counts.csv`: the country, its 3 regions, 28 districts and 4 cities, with men, women and total, from Table A1 of
  *Series A. Population Tables*. Read from the workbook's cells, not typed. The 2018 columns only; the 2008 columns
  are left out.
- `columns.csv`: what each column of `counts.csv` holds.
- `districts.csv`: the 28 districts with geoBoundaries' name and ID for each. geoBoundaries draws the four cities inside
  their districts, so each city's count is added to its district (Mzuzu City to Mzimba; Lilongwe, Zomba and Blantyre
  cities to their own districts), and `with_city` names it. Derived, written by `scripts/levels_today.py` from
  geoBoundaries gbOpen MWI ADM2 (9469f09); `districts-columns.csv`, its dictionary.
- `provenance.json`: the workbook, its digest, the licence and the checks.

The cities (Mzuzu, Lilongwe, Zomba, Blantyre) are their own units, counted apart from the district of the same name.

**Copy read:** HDX's, uploaded by Health Cluster, not by the NSO. HDX labels it CC BY; that is HDX's label. The NSO
states no licence that could be read: its site shows only "All Rights Reserved" in the footer.

Checks: men plus women equals the total on all 36 rows; each region's districts and cities sum to it; the regions
sum to 17,563,749, the national total as printed.

Cite as: National Statistical Office (NSO), Malawi, 2018 Malawi Population and Housing Census, Series A. Population
Tables, Table A1. Copy read from HDX (Health Cluster).
