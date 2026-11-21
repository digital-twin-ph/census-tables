"""Sierra Leone, Malawi and Kenya: each census unit beside the name geoBoundaries gives it, so a census relates to a map
without anyone retyping a name. Writes SLE/districts.csv, SLE/chiefdoms.csv, MWI/districts.csv and KEN/counties.csv,
with their dictionaries. Run from the repository root:
  python3 -I scripts/levels_today.py <folder holding the geoBoundaries files>

The files are geoBoundaries' gbOpen release 9469f09, simplified, read and not kept here:
geoBoundaries-SLE-ADM2_simplified.geojson, -SLE-ADM3-, -MWI-ADM2- and -KEN-ADM1-, from
https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/<ISO>/<ADM>/.

Sierra Leone's chiefdoms are matched within their district, each geoBoundaries ADM3 unit placed in the ADM2 district its
polygon lies in; 41 are spelled differently in the two (geoBoundaries cuts names at 15 characters) and are paired by
the list below. Malawi's districts are drawn by geoBoundaries with the cities inside them, so each city's count is
added to its district. Kenya's counties are summed from the printed sub-counties."""
import json, csv, sys, os, re, collections
G = sys.argv[1]

def polygons(f):
    g = f['geometry']; return g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
def inside(pt, poly):
    x, y = pt; ins = False
    for ring in poly:
        for i in range(len(ring)):
            (x1, y1), (x2, y2) = ring[i], ring[(i + 1) % len(ring)]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: ins = not ins
    return ins
def area(r): return abs(sum(r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1] for i in range(len(r) - 1))) / 2
def centroid(r):
    a = cx = cy = 0
    for i in range(len(r) - 1):
        (x1, y1), (x2, y2) = r[i], r[i + 1]; c = x1 * y2 - x2 * y1; a += c; cx += (x1 + x2) * c; cy += (y1 + y2) * c
    return (cx / (3 * a), cy / (3 * a)) if a else r[0]
def norm(s): return re.sub(r'[^a-z]', '', s.lower())
def gb(name): return json.load(open(os.path.join(G, f'geoBoundaries-{name}_simplified.geojson'), encoding='utf-8'))['features']
def containing(pt, units): return [u['properties']['shapeName'] for u in units if any(inside(pt, q) for q in polygons(u))]
def place(f, units):
    big = max(polygons(f), key=lambda p: area(p[0]))[0]; votes = collections.Counter()
    for k, pt in enumerate([centroid(big)] + big[::max(1, len(big) // 25)]):
        for n in containing(pt, units): votes[n] += 3 if k == 0 else 1
    return votes.most_common(1)[0][0]
def write(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as out:
        w = csv.writer(out, lineterminator='\n'); w.writerow(header); w.writerows(rows)
def dictionary(path, rows): write(path, ['variable', 'label', 'unit', 'description'], rows)
def counts(iso): return list(csv.DictReader(open(f'{iso}/counts.csv', encoding='utf-8')))
def total(rows, k): return sum(int(r[k] or 0) for r in rows)  # a count printed "-" (Kenya's forests, Lake Baringo) adds nothing

# SIERRA LEONE
SLE_SPELLED = {  # district|printed -> geoBoundaries ADM3, read from the two lists, district by district
    'Bo|Bagbwe': 'Bagbwe(Bagbe)', 'Bo|Baoma': 'Boama', 'Bo|Bumpe Ngawo': 'Bumpe Ngao', 'Bo|Wunde': 'Wonde', 'Bo|Bo City': 'Bo Town',
    'Bombali|Gbanti-Kamaranka': 'Gbanti Kamarank', 'Bombali|Gbendembu Ngowahun': 'Gbendembu Ngowa',
    'Bombali|Magbaimba Ndorhahun': 'Magbaimba Ndorh', 'Bombali|Sanda Tendaren': 'Sanda Tendaran', 'Bombali|Tambakka': 'Tambakha',
    'Bombali|Makeni City': 'Makeni Town', 'Bonthe|Imperi': 'Imperri', 'Bonthe|Kpanga Kemo': 'Kpanda Kemo', 'Bonthe|Sogbini': 'Sogbeni',
    'Kenema|Kandu Lekpeama': 'Kandu Leppiama', 'Kenema|Kenema City': 'Kenema Town',
    'Koinadugu|Dembelia Sinkunia': 'Dembelia - Sink', 'Koinadugu|Follosaba Dembelia': 'Folosaba Dembel',
    'Koinadugu|Wara Wara Bafodia': 'Wara Wara Bafod', 'Koinadugu|Wara Wara Yagala': 'Wara Wara Yagal', 'Kono|Koidu/New': 'Koidu Town',
    'Port Loko|BKM': 'Bureh Kasseh Ma', 'Port Loko|Sanda Magbolontor': 'Sanda Magbolont',
    'Pujehun|Gallinas Peri': 'Galliness Perri', 'Pujehun|Kpanga-Kabonde': 'Panga Kabonde', 'Pujehun|Mano Sakrim': 'Mono Sakrim',
    'Pujehun|Pejeh': 'Pejeh(Futa peje', 'Tonkolili|Kafe Simira': 'Kafe Simiria', 'Tonkolili|Kolifa Rowalla': 'Kholifa Rowala',
    'Tonkolili|Kunike Sanda': 'Kunike', 'Western Area Rural|Koya': 'Koya Rural', 'Western Area Rural|Mountain': 'Mountain Rural',
    'Western Area Rural|Waterloo': 'Waterloo Rural', **{f'Western Area Urban|{a} {n}': f'{a} {r}' for a in ('Central', 'East', 'West')
        for n, r in (('1', 'I'), ('2', 'II'), ('3', 'III'))}}
del SLE_SPELLED['Western Area Urban|Central 3']
# Kenema's Koya has no unit of its own in geoBoundaries' ADM3 (its one Koya lies in Port Loko); two units have no printed
# row: Bonthe Urban and Yakemu Kpukumu, where the printed chiefdoms fall short of Bonthe (urban) and Pujehun (rural).
SLE_NONE = {'Kenema|Koya'}
c = counts('SLE'); country = next(r for r in c if r['level'] == 'country')
d2, d3 = gb('SLE-ADM2'), gb('SLE-ADM3')
did = {u['properties']['shapeName']: u['properties']['shapeID'] for u in d2}
drows = [r for r in c if r['level'] == 'district']
assert len(drows) == 14 and all(r['unit'] in did for r in drows), 'every Sierra Leone district is a geoBoundaries unit by name'
for k in ('men', 'women', 'total'): assert total(drows, k) == int(country[k])
write('SLE/districts.csv', ['province', 'unit', 'geoboundaries_name', 'geoboundaries_id', 'men', 'women', 'total'],
      [[r['province'], r['unit'], r['unit'], did[r['unit']], r['men'], r['women'], r['total']] for r in drows])
placed = collections.defaultdict(dict)
for u in d3: placed[place(u, d2)][norm(u['properties']['shapeName'])] = u['properties']
used, rows = set(), []
for r in (r for r in c if r['level'] == 'chiefdom'):
    key = f"{r['district']}|{r['unit']}"
    if key in SLE_NONE: rows.append([r['province'], r['district'], r['unit'], '', '', r['men'], r['women'], r['total']]); continue
    p = placed[r['district']].get(norm(SLE_SPELLED.get(key, r['unit'])))
    assert p and p['shapeID'] not in used, f'{key}: no geoBoundaries unit'
    used.add(p['shapeID']); rows.append([r['province'], r['district'], r['unit'], p['shapeName'], p['shapeID'], r['men'], r['women'], r['total']])
assert len(rows) == 164 and len(used) == 163
unpaired = sorted(u['properties']['shapeName'] for u in d3 if u['properties']['shapeID'] not in used)
assert unpaired == ['Bonthe Urban', 'Yakemu Kpukumu'], unpaired
write('SLE/chiefdoms.csv', ['province', 'district', 'unit', 'geoboundaries_name', 'geoboundaries_id', 'men', 'women', 'total'], rows)
people = [['men', 'Men', 'persons', 'Male population, 2015 census (December 2015)'], ['women', 'Women', 'persons', 'Female population, 2015 census'],
          ['total', 'Total', 'persons', 'Population, both sexes, 2015 census']]
dictionary('SLE/districts-columns.csv', [['province', 'Province', '', 'The province the district lies in, as Table 2 prints it'],
    ['unit', 'District', '', 'The district as Table 2 prints it'],
    ['geoboundaries_name', 'District (geoBoundaries)', '', "The district as geoBoundaries' SLE ADM2 spells it (gbOpen 9469f09): the same as the census's for all 14"],
    ['geoboundaries_id', 'geoBoundaries ID', '', "The district's shapeID in that release"]] + people)
dictionary('SLE/chiefdoms-columns.csv', [['province', 'Province', '', 'The province, as Table 3 prints it'],
    ['district', 'District', '', 'The district the unit lies in, as Table 3 prints it'],
    ['unit', 'Chiefdom', '', "The unit in Table 3's chiefdom position as printed: a chiefdom, a city, or an area of the Western Area"],
    ['geoboundaries_name', 'Chiefdom (geoBoundaries)', '', "The unit as geoBoundaries' SLE ADM3 spells it (gbOpen 9469f09), names cut at 15 characters: "
     f"the name to match a map of the chiefdoms on. {len(SLE_SPELLED)} are spelled differently; empty for Kenema's Koya, which has no unit of its own there"],
    ['geoboundaries_id', 'geoBoundaries ID', '', "The unit's shapeID in that release"]] + people)

# MALAWI
CITY_IN = {'Mzuzu City': ('Mzimba', (34.02, -11.46)), 'Lilongwe City': ('Lilongwe', (33.79, -13.97)),
           'Zomba City': ('Zomba', (35.32, -15.39)), 'Blantyre City': ('Blantyre', (35.01, -15.79))}  # (lon, lat), city centre, approximate
c = counts('MWI'); country = next(r for r in c if r['level'] == 'country')
m2 = gb('MWI-ADM2'); mid = {u['properties']['shapeName']: u['properties']['shapeID'] for u in m2}
drows = [r for r in c if r['level'] == 'district']; cities = [r for r in c if r['level'] == 'city']
assert len(drows) == 28 and all(r['unit'] in mid for r in drows) and len(mid) == 28, 'every Malawi district is a geoBoundaries unit by name'
assert sorted(r['unit'] for r in cities) == sorted(CITY_IN)
for city, (district, pt) in CITY_IN.items(): assert containing(pt, m2) == [district], f'{city} lies in {containing(pt, m2)}'
out = []
for r in drows:
    inner = [x for x in cities if CITY_IN[x['unit']][0] == r['unit']]
    out.append([r['region'], r['unit'], '; '.join(x['unit'] for x in inner), r['unit'], mid[r['unit']]]
               + [int(r[k]) + total(inner, k) for k in ('men', 'women', 'total')])
for i, k in enumerate(('men', 'women', 'total')): assert sum(x[5 + i] for x in out) == int(country[k]), f'Malawi districts with their cities sum to the country {k}'
write('MWI/districts.csv', ['region', 'unit', 'with_city', 'geoboundaries_name', 'geoboundaries_id', 'men', 'women', 'total'], out)
dictionary('MWI/districts-columns.csv', [['region', 'Region', '', 'The region the district lies in, as Table A1 prints it'],
    ['unit', 'District', '', 'The district as Table A1 prints it'],
    ['with_city', 'City added', '', "The city counted apart in Table A1 whose count is added here, because geoBoundaries draws it inside this district: Mzuzu City in Mzimba, and Lilongwe, Zomba and Blantyre cities in their districts. Empty for the other 24"],
    ['geoboundaries_name', 'District (geoBoundaries)', '', "The district as geoBoundaries' MWI ADM2 spells it (gbOpen 9469f09): the same as the census's for all 28"],
    ['geoboundaries_id', 'geoBoundaries ID', '', "The district's shapeID in that release"],
    ['men', 'Men', 'persons', 'Male population, 2018 census, with the city added where with_city names one'],
    ['women', 'Women', 'persons', 'Female population, 2018 census, likewise'], ['total', 'Total', 'persons', 'Population, both sexes, 2018 census, likewise']])

# KENYA
KEN_SPELLED = {'Tharaka Nithi': 'Tharaka'}
c = counts('KEN'); k1 = gb('KEN-ADM1')
kn = {norm(u['properties']['shapeName']): u['properties'] for u in k1}  # matched ignoring case, spaces and hyphens
subs = [r for r in c if r['level'] == 'sub-county']; by = collections.defaultdict(list)
for r in subs: by[r['county']].append(r)
assert len(by) == 47 and all(norm(KEN_SPELLED.get(k, k)) in kn for k in by) and len(kn) == 47, 'every Kenyan county is a geoBoundaries unit'
assert total(subs, 'total') == 47564296, "the sub-counties sum to KNBS's national figure"
tn = next(r for r in c if r['level'] == 'county')
assert all(total(by['Tharaka Nithi'], k) == int(tn[k]) for k in ('men', 'women', 'total')), "Tharaka Nithi's printed row"
write('KEN/counties.csv', ['unit', 'sub_counties', 'geoboundaries_name', 'geoboundaries_id', 'men', 'women', 'total'],
      [[k, len(v), kn[norm(KEN_SPELLED.get(k, k))]['shapeName'], kn[norm(KEN_SPELLED.get(k, k))]['shapeID'], total(v, 'men'), total(v, 'women'), total(v, 'total')] for k, v in by.items()])
dictionary('KEN/counties-columns.csv', [['unit', 'County', '', 'The county as the workbook names it beside its sub-counties'],
    ['sub_counties', 'Sub-counties summed', '', 'How many printed sub-county rows were added to make the county; four, printed "-" (Lake Baringo, two Mau Forest rows, Tinderet Forest), add nothing'],
    ['geoboundaries_name', 'County (geoBoundaries)', '', "The county as geoBoundaries' KEN ADM1 spells it (gbOpen 9469f09): the census's name for 46; Tharaka Nithi is \"Tharaka\""],
    ['geoboundaries_id', 'geoBoundaries ID', '', "The county's shapeID in that release"],
    ['men', 'Men', 'persons', 'Male population, 2019 census, the sum of the county\'s sub-counties'],
    ['women', 'Women', 'persons', 'Female population, 2019 census, likewise'],
    ['total', 'Total', 'persons', 'Population, 2019 census, likewise; it includes intersex persons, so it can exceed men plus women']])
print(f'Sierra Leone: 14 districts; 164 chiefdoms, {len(SLE_SPELLED)} spelled differently, Koya (Kenema) unpaired; unpaired units: {unpaired}')
print('Malawi: 28 districts, 4 cities added. Kenya: 47 counties summed from', len(subs), 'sub-counties')
