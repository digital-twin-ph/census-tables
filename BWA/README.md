# Botswana — the 2022 census

The 2022 Population and Housing Census (PHC 2022), by Statistics Botswana.

- `counts.csv`: the country and its 28 census districts, totals only, from Table 1 of *Population Distribution,
  Structure and Density in Botswana* (March 2024). Typed from the report for Fieldwork's population example on
  2026-11-12; not yet re-read for this repository.
- `units.csv`: each census district's unit in geoBoundaries gbHumanitarian BWA ADM2. Eight names differ (Central
  Serowe /Palapye is Serowe Palapye, CKGR is Central Kgalagadi Game Reserve, and six more) and were matched by hand.
- `provenance.json`: the report, the terms (Statistics Botswana's terms of use: free use, naming Statistics Botswana
  as the source), and the check: the 28 districts sum to 2,359,609, the total on the office's census page.

**Open:** the office's census page now lists the paper as *Population Distribution, Structure, Density and Policy
Implications in Botswana*. Whether its Table 1 is the one read is not checked, and men and women are not transcribed.

Cite as: Statistics Botswana, Population Distribution, Structure and Density in Botswana (PHC 2022), March 2024,
Table 1. Data processed by the census-tables project.

- `districts.csv`: the 28 census districts with geoBoundaries' name for each (8 spelled differently), to relate to a map of the districts; `districts-columns.csv`, its dictionary. The counts as printed.
