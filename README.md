# African census tables

Census counts for African countries, by administrative unit, as each national statistics office published them.

Population rasters, health programmes and humanitarian baselines all lean on census counts, and the counts are hard
to find in a form a person can check: a table in a PDF report, names spelled the office's own way, units that do not
match today's boundaries. This repository keeps them so they can be checked.

## What each country holds

```
<ISO3>/
  counts.csv        the counts as published: one row per unit, the office's own names and codes
  units.csv         each unit mapped to an HDX P-code and a geoBoundaries ID, where one exists
  provenance.json   the office, the report, the table and page, the census year, the licence, the total checked
```

## The rules

- **As published.** Names are spelled as the report prints them. A number is the report's number. Nothing is
  corrected in place; a correction is a new row in `provenance.json`, with what changed and why.
- **A census is a count.** A projection, a humanitarian estimate (COD-PS) or a modelled raster is not a census and
  never goes in `counts.csv`. Where a country has no recent census, its folder says so and names the best substitute
  in words.
- **Checked against its own total.** The units are added up and compared with the national total the report gives;
  the result is recorded, matched or not.
- **The licence first.** Each office's terms are read before its counts are added, and stated in `provenance.json`.
  A country whose terms do not allow redistribution is listed with its source, without its counts.

## Status

Started 2026-11-19. Botswana and Rwanda first, then the twelve other countries already compared with population
rasters.
