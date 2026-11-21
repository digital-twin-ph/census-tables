# Kenya — the 2019 census

The 2019 Kenya Population and Housing Census (KPHC), August 2019, by KNBS, the Kenya National Bureau of Statistics.

The copy read is not from KNBS's own site. It is a workbook on HDX, uploaded by the organisation account
"Kenya National Bureau of Statistics (inactive)", in an archived dataset added 5 November 2019 and last modified
20 March 2020. HDX does not say which census volume the table is from.

- `counts.csv`: 349 sub-county rows and Tharaka Nithi's county row, with men, women, total, land area (km²) and
  population density, from the workbook *Distribution of Population by Sex, Number of Households, Land Area,
  Population Density and Sub County*. Read from the workbook's cells, not typed. The workbook prints no national row
  and no other county rows, so none is written here: the sub-counties sum to 47,564,296, KNBS's national figure, as a
  check. It holds no household or intersex counts, despite its title.
- `columns.csv`: what each column holds.
- `counties.csv`: the 47 counties, each the sum of its sub-counties, with geoBoundaries' name and ID (Tharaka Nithi is
  geoBoundaries' "Tharaka"). Derived, written by `scripts/levels_today.py` from geoBoundaries gbOpen KEN ADM1 (9469f09);
  `counties-columns.csv`, its dictionary. geoBoundaries' ADM2 holds the 290 constituencies, not the 349 sub-counties,
  so the sub-counties have no geoBoundaries names here.
- `provenance.json`: the workbook, its digest, the licence (HDX's label, Public Domain / CC0, set by the uploading
  account; KNBS's site says "All Rights Reserved" and gives no terms), every correction, and the checks:
  - men plus women equals the total on 45 of 346 rows. On the other 301 the total is larger, by 1 to 62
    (`total_less_men_and_women`), 1,524 in all. The census counted intersex persons; the workbook has no column for
    them.
  - Tharaka Nithi's printed county row equals the sum of its sub-counties.
  - the counties sum to 47,564,296, the national total given with the brief; the workbook prints no national total.

Cite as: Kenya National Bureau of Statistics (KNBS), 2019 Kenya Population and Housing Census, Distribution of
Population by Sex, Number of Households, Land Area, Population Density and Sub County; copy on HDX,
https://data.humdata.org/dataset/kenya-population-per-county-from-census-report-2019, retrieved 2026-11-20.
