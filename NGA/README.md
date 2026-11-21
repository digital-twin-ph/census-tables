# Nigeria — the 2006 census

The 2006 Population and Housing Census, March 21–27, 2006, by the National Population Commission (NPC). It is
Nigeria's latest census. **These counts are twenty years old.** A rate built on them should say so.

- `counts.csv`: the country, its 36 states and the FCT, and their 774 Local Government Areas, with men, women and
  total, from *Priority Table Volume III: Population Distribution by Sex, State, LGA & Senatorial District* (NPC, April
  2010). Each LGA carries its state and its senatorial district: the letter the table prints (A, B, C) and the name its
  legend gives. One more row, Taraba's "* DISPUTED AREAS", is kept as printed. Read from the PDF's text layer, not typed.
- `columns.csv`: the data dictionary.
- `provenance.json`: the volume, where it was read, its digest, the licence (none stated), what was kept as printed,
  and the checks.

## Checks

- Men plus women equals the total on all 813 rows.
- Each state's LGAs sum to its printed total (men, women and total), all 37; each state has the number of LGAs the
  volume's list gives (774 in all).
- Each state total equals the state's row in the volume's table by states (printed page 9), and the states sum to that
  table's NIGERIA row: 71,345,488 men, 69,086,302 women, 140,431,790 in all.
- No senatorial-district totals are printed, so the LGAs cannot be checked against them.

No number needed correcting. Kept as printed: misnumbered serials in Taraba, Benue and Akwa Ibom, and three legends
cut short in print (Jigawa C, Cross River C, Akwa Ibom C); see `provenance.json`.

Cite as: National Population Commission, *2006 Population and Housing Census, Priority Table Volume III: Population
Distribution by Sex, State, LGA & Senatorial District*, Abuja, April 2010. IHSN Survey Catalog, NGA_2006_PHC_v01_M,
https://catalog.ihsn.org/catalog/3340, downloaded 2026-11-20. No licence stated.
