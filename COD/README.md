# DR Congo — the 1984 census

The *Recensement scientifique de la population* of July 1984 is the country's only census. A second (RGPH-2) was in
its preparatory phase in September 2026, with no published date for enumeration. **These counts are more than forty
years old.** A rate built on them should say so; a modelled estimate (GRID3/WorldPop bottom-up estimates for 2022 to
2024, or US Census Bureau projections) is a substitute, not a count, and does not belong in this folder.

- `counts.csv`: the country, its 9 regions of 1984, and their 44 cities (villes) and sub-regions (sous-régions), with
  men, women and total, from tables T-01 and T-02 of the *Totaux définitifs*. A ville is a unit of the same level as a
  sous-région: a region's total is the sum of both.
- `provenance.json`: the volume, where it was read, its digest, the licence (none stated), every correction made to the
  scan's text layer, and the checks: men plus women equals the total on all 54 rows, each region's units sum to it, and
  the regions sum to 30,729,443.

The 1984 regions are not today's 26 provinces (2015). Most sub-regions became provinces of the same name; cities went
to the province they lie in.

- `units.csv`: each of the 44 cities and sub-regions, the province it went to (as the 2015 law spells it, and as
  geoBoundaries does, with its ID), and the basis for placing it.
- `provinces-2015.csv`: the 1984 counts summed to the 26 provinces, with `geoboundaries_name` to match a map of today's
  provinces on. **Derived, and still 1984's counts.** The provinces sum to the country's 30,729,443.
- `provinces-2015-columns.csv`: its data dictionary.

What the mapping does not establish is in `provenance.json` under `provinces_2015`: chiefly that the 1984 sub-regions'
limits are the 2015 provinces', and where the land of the later Plateaux district (Mai-Ndombe today) was counted.
