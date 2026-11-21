# Sierra Leone — the 2015 census

The 2015 Population and Housing Census, by Statistics Sierra Leone (Stats SL), reference night 4 to 5 December 2015,
from the *Summary of Final Results* (December 2016).

- `counts.csv`: the country, its 4 provinces (Eastern, Northern, Southern, and Western, the Western Area), its 14
  districts, and 164 chiefdoms, with men, women and total. The country, provinces and districts are from Table 2
  (printed page 30); the chiefdoms from Table 3 (printed pages 32 to 44). Read from the PDF's text layer, not typed;
  no number needed correcting.
- `columns.csv`: what each column holds.
- `districts.csv`: the 14 districts with geoBoundaries' name and ID for each, to relate to a map of the districts;
  `districts-columns.csv`, its dictionary.
- `chiefdoms.csv`: the 164 chiefdoms and areas with their district and geoBoundaries' name and ID for each; 41 are
  spelled differently in the two (geoBoundaries cuts names at 15 characters). Kenema's Koya has no unit of its own in
  geoBoundaries and is left unpaired; geoBoundaries' Bonthe Urban and Yakemu Kpukumu have no printed row, and are likely
  the rows Bonthe's and Pujehun's chiefdoms fall short by (see Checks). `chiefdoms-columns.csv`, its dictionary. Both
  are written by `scripts/levels_today.py` from geoBoundaries gbOpen SLE ADM2 and ADM3 (9469f09). The counts as printed.
- `provenance.json`: the volume, its digest, the licence, the checks, and what the table prints in error.

**These are the units of 2015.** Sierra Leone created two more districts in 2017 (16 now), so the 14 districts here
are not today's. Table 3's chiefdom position also holds four cities (Kenema City, Koidu/New, Makeni City, Bo City) and
the areas of the Western Area (Koya, Mountain, Waterloo, York Rural; Central 1 to West 3).

Fieldwork's Sierra Leone measles example uses the 2021 Mid-Term Census, not this one.

## Checks

- Men plus women equals the total on all 183 rows.
- Each province's districts sum to it; the provinces sum to 7,092,113 as printed.
- Tables 1, 2 and 3 agree on the country and every district.
- The chiefdoms sum to their district in 12 of 14. **Bonthe and Pujehun do not**, as printed: Bonthe's chiefdoms are
  10,075 short (all urban), Pujehun's 13,824 short (all rural). The page images show the same rows as the text, so
  each looks to lack one printed row. Which unit is missing the volume does not say; no row has been added.

Cite as: Statistics Sierra Leone, 2015 Population and Housing Census, Summary of Final Results (2016), Tables 2 and 3.
Source: STATISTICS SIERRA LEONE. Contains information licensed under STATISTICS SIERRA LEONE's Open License Agreement.
