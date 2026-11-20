"""Rwanda and Botswana: each census district beside the name geoBoundaries gives it, so a census relates to a map of the
districts without anyone retyping a name. Writes RWA/districts.csv and BWA/districts.csv, with their dictionaries.
Run from the repository root: python3 -I scripts/districts_today.py ../boundaries ../example-population-models-census

Rwanda's names are geoBoundaries' RWA ADM2 (gbOpen 9469f09, in the boundaries repository) and match the NISR workbook's
exactly. Botswana's census districts are paired with the 28 units of geoBoundaries' BWA ADM2 file as the population
example's district table pairs them (data/botswana_census_2022_districts.csv): 20 by the same name, 8 where geoBoundaries
spells the district another way."""
import csv, sys, os
B = sys.argv[1] if len(sys.argv) > 1 else '../boundaries'
EX = sys.argv[2] if len(sys.argv) > 2 else '../example-population-models-census'

def write(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as out:
        w = csv.writer(out, lineterminator='\n'); w.writerow(header); w.writerows(rows)

# RWANDA
gb = {r['shapeName']: r['shapeID'] for r in csv.DictReader(open(os.path.join(B, 'RWA/ADM2/units.csv'), encoding='utf-8'))}
rows = [r for r in csv.DictReader(open('RWA/counts.csv', encoding='utf-8')) if r['level'] == 'district']
assert len(rows) == 30 and all(r['unit'] in gb for r in rows), 'every Rwandan district is a geoBoundaries unit by name'
country = next(r for r in csv.DictReader(open('RWA/counts.csv', encoding='utf-8')) if r['level'] == 'country')
for k in ('men', 'women', 'total'): assert sum(int(r[k]) for r in rows) == int(country[k]), f'Rwanda districts sum to the country {k}'
write('RWA/districts.csv', ['province', 'unit', 'geoboundaries_name', 'geoboundaries_id', 'men', 'women', 'total'],
      [[r['province'], r['unit'], r['unit'], gb[r['unit']], r['men'], r['women'], r['total']] for r in rows])
write('RWA/districts-columns.csv', ['variable', 'label', 'unit', 'description'], [
    ['province', 'Province', '', 'The province the district lies in, as the NISR workbook writes it'],
    ['unit', 'District', '', "The district's name as the NISR workbook writes it"],
    ['geoboundaries_name', 'District (geoBoundaries)', '', "The district as geoBoundaries' RWA ADM2 spells it (gbOpen 9469f09): the name to match a map of the districts on. The same as the workbook's for all 30"],
    ['geoboundaries_id', 'geoBoundaries ID', '', "The district's shapeID in that release"],
    ['men', 'Men', 'persons', 'Resident male population, August 2022 census'],
    ['women', 'Women', 'persons', 'Resident female population, August 2022 census'],
    ['total', 'Total', 'persons', 'Resident population, both sexes, August 2022 census']])

# BOTSWANA
pairs = {r['census_district']: r['name'] for r in csv.DictReader(open(os.path.join(EX, 'data/botswana_census_2022_districts.csv'), encoding='utf-8'))}
rows = [r for r in csv.DictReader(open('BWA/counts.csv', encoding='utf-8')) if r['level'] == 'census district']
assert len(rows) == 28 and all(r['unit'] in pairs for r in rows) and len(set(pairs.values())) == 28, 'each census district paired with one unit'
country = next(r for r in csv.DictReader(open('BWA/counts.csv', encoding='utf-8')) if r['level'] == 'country')
assert sum(int(r['total']) for r in rows) == int(country['total']), 'Botswana census districts sum to the country'
write('BWA/districts.csv', ['unit', 'geoboundaries_name', 'total'], [[r['unit'], pairs[r['unit']], r['total']] for r in rows])
write('BWA/districts-columns.csv', ['variable', 'label', 'unit', 'description'], [
    ['unit', 'Census district', '', 'The census district as Statistics Botswana names it'],
    ['geoboundaries_name', 'District (geoBoundaries)', '', "The district as geoBoundaries' BWA ADM2 file spells it: the name to match a map of the districts on. 20 are the census's own name; 8 differ (Sowa, Delta, CKGR and five Central sub-districts)"],
    ['total', 'Total', 'persons', 'Population, 2022 Population and Housing Census']])
differ = sorted(f'{c} = {n}' for c, n in pairs.items() if c != n)
print('Rwanda 30 districts; Botswana 28, differing:', '; '.join(differ))
