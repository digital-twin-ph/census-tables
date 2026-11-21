"""Nigeria: each state and LGA of the 2006 census beside the name geoBoundaries gives it, so the census relates to a map of
the states or the LGAs without anyone retyping a name. Writes NGA/states.csv and NGA/lgas.csv, with their dictionaries.
Run from the repository root: python3 -I scripts/nigeria_today.py <folder holding the two geoBoundaries files>

The files are geoBoundaries' gbOpen NGA ADM1 and ADM2, release 9469f09 (GRID3, CC BY 4.0), simplified:
geoBoundaries-NGA-ADM1_simplified.geojson and geoBoundaries-NGA-ADM2_simplified.geojson, from
https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/NGA/. They are read, not kept here.

States: the volume prints "JIGAWA STATE"; geoBoundaries writes "Jigawa", and "Abuja Federal Capital Territory" for ABUJA FCT.
LGAs: geoBoundaries' ADM2 file does not say which state an LGA lies in, and some names occur in two states (Surulere, Obi,
Bassa, Irepodun...). Each geoBoundaries LGA is placed in the state its polygon lies in; a printed LGA is then matched by
name within its state, ignoring case, spaces and punctuation, or by a spelling the two sources differ on (SPELLED below).
An LGA whose polygon lies over a state line in the simplified files is matched by name over the country, when the name is
unique. Every printed LGA is paired with one geoBoundaries unit, and every unit with one LGA."""
import json, csv, sys, os, re, collections
G = sys.argv[1]

# Printed name -> geoBoundaries' name, where the two spell an LGA differently. Read from the two lists, state by state.
# "STATE|NAME" where the printed name is also an LGA elsewhere spelled alike (NASARAWA LGA of Nasarawa State).
SPELLED = {
    'ISIUKWUATO': 'Isuikwuato', 'OBI NGWA': 'Obi Nwga', 'ABUJA MUNICIPAL (AMAC)': 'Municipal Area Council', 'DAMBAN': 'Dambam',
    'BEKWARA': 'Bekwarra', 'IGUEBEN': 'Iguegben', 'AIYEKIRE (GBONYIN)': 'Gbonyin', 'ILEJEMEJI': 'Ilejemeje',
    'NAFADA (BAJOGA)': 'Nafada', 'MBAITOLI': 'Mbatoli', 'UNUIMO': 'Onuimo', 'KIRI KASAMMA': 'Kiri Kasama',
    'GARUM MALLAM': 'Garun Malam', 'KANO STATE|NASARAWA': 'Nassarawa', 'BAGUDO': 'Bagudu', 'OLAMABOLO': 'Olamaboro',
    'NASARAWA-EGGON': 'Nasarawa Egon', 'MUYA': 'Munya', 'EGBADO NORTH': 'Yewa North', 'EGBADO SOUTH': 'Yewa South',
    'AIYEDADE': 'Ayedade', 'AIYEDIRE': 'Ayedire', 'ATAKUMOSA EAST': 'Atakunmosa East', 'ATAKUMOSA WEST': 'Atakunmosa West',
    'ATIGBO': 'Atisbo', 'IBADAN CENTRAL [IBADAN NORTH EAST]': 'Ibadan North East', 'BARIKIN LADI': 'Barkin Ladi',
    'EMOHUA': 'Emuoha', 'OBIA/AKPOR': 'Obio/Akpor', 'TARMUA': 'Tarmuwa', 'BIRNIN MAGAJI': 'Birnin Magaji-Kiyaw'}

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
def write(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as out:
        w = csv.writer(out, lineterminator='\n'); w.writerow(header); w.writerows(rows)

states = json.load(open(os.path.join(G, 'geoBoundaries-NGA-ADM1_simplified.geojson'), encoding='utf-8'))['features']
lgas = json.load(open(os.path.join(G, 'geoBoundaries-NGA-ADM2_simplified.geojson'), encoding='utf-8'))['features']
assert len(states) == 37 and len(lgas) == 774
def state_of(f):
    big = max(polygons(f), key=lambda p: area(p[0]))[0]
    votes = collections.Counter()
    for k, pt in enumerate([centroid(big)] + big[::max(1, len(big) // 25)]):
        for s in states:
            if any(inside(pt, q) for q in polygons(s)): votes[s['properties']['shapeName']] += 3 if k == 0 else 1
    return votes.most_common(1)[0][0]

counts = list(csv.DictReader(open('NGA/counts.csv', encoding='utf-8')))
country = next(r for r in counts if r['level'] == 'country')
def gb_state(printed): return 'Abuja Federal Capital Territory' if printed == 'ABUJA FCT' else printed.removesuffix(' STATE').title()
sid = {s['properties']['shapeName']: s['properties']['shapeID'] for s in states}

srows = [r for r in counts if r['level'] == 'state']
assert len(srows) == 37 and all(gb_state(r['unit']) in sid for r in srows), 'every state is a geoBoundaries unit'
for k in ('men', 'women', 'total'): assert sum(int(r[k]) for r in srows) == int(country[k]), f'states sum to the country {k}'
write('NGA/states.csv', ['unit', 'geoboundaries_name', 'geoboundaries_id', 'men', 'women', 'total'],
      [[r['unit'], gb_state(r['unit']), sid[gb_state(r['unit'])], r['men'], r['women'], r['total']] for r in srows])

placed = collections.defaultdict(dict)
for f in lgas: placed[state_of(f)][norm(f['properties']['shapeName'])] = f['properties']
used, rows, across = set(), [], []
for r in (r for r in counts if r['level'] == 'lga'):
    s, want = gb_state(r['state']), norm(SPELLED.get(f"{r['state']}|{r['unit']}", SPELLED.get(r['unit'], r['unit'])))
    p = placed[s].get(want)
    if p is None or p['shapeID'] in used:
        cands = [f['properties'] for f in lgas if norm(f['properties']['shapeName']) == want and f['properties']['shapeID'] not in used]
        assert len(cands) == 1, f"{r['unit']} ({s}): no unique geoBoundaries unit"
        p = cands[0]; across.append(f"{r['unit']} ({s})")
    used.add(p['shapeID'])
    rows.append([r['state'], s, r['senatorial_district'], r['unit'], p['shapeName'], p['shapeID'], r['men'], r['women'], r['total']])
assert len(rows) == 774 and len(used) == 774, 'each printed LGA paired with one unit, and each unit with one LGA'
disputed = [r for r in counts if r['level'] == 'disputed areas']
for sr in srows:
    got = sum(int(x[8]) for x in rows if x[0] == sr['unit']) + sum(int(d['total']) for d in disputed if d['state'] == sr['unit'])
    assert got == int(sr['total']), f"{sr['unit']}: LGAs sum to {got}, state prints {sr['total']}"
write('NGA/lgas.csv', ['state', 'state_geoboundaries', 'senatorial_district', 'unit', 'geoboundaries_name', 'geoboundaries_id', 'men', 'women', 'total'], rows)

common = [['men', 'Men', 'persons', 'Male population, 2006 census (March 21-27, 2006)'],
          ['women', 'Women', 'persons', 'Female population, 2006 census'],
          ['total', 'Total', 'persons', 'Population, both sexes, 2006 census; men plus women']]
write('NGA/states-columns.csv', ['variable', 'label', 'unit', 'description'], [
    ['unit', 'State', '', 'The state as Priority Table Volume III prints it, e.g. JIGAWA STATE, ABUJA FCT'],
    ['geoboundaries_name', 'State (geoBoundaries)', '', "The state as geoBoundaries' NGA ADM1 spells it (gbOpen 9469f09): the name to match a map of the states on"],
    ['geoboundaries_id', 'geoBoundaries ID', '', "The state's shapeID in that release"]] + common)
write('NGA/lgas-columns.csv', ['variable', 'label', 'unit', 'description'], [
    ['state', 'State', '', 'The state the LGA lies in, as the volume prints it'],
    ['state_geoboundaries', 'State (geoBoundaries)', '', "That state as geoBoundaries' NGA ADM1 spells it"],
    ['senatorial_district', 'Senatorial district', '', 'The letter (A, B or C) the table prints'],
    ['unit', 'LGA', '', "The Local Government Area as printed; the FCT's six are its Area Councils"],
    ['geoboundaries_name', 'LGA (geoBoundaries)', '', "The LGA as geoBoundaries' NGA ADM2 spells it (gbOpen 9469f09): the name to match a map of the LGAs on. "
     f'{len(SPELLED)} are spelled differently from the volume'],
    ['geoboundaries_id', 'geoBoundaries ID', '', "The LGA's shapeID in that release"]] + common)
print(f'Nigeria: 37 states; 774 LGAs, {len(SPELLED)} spelled differently; matched over a state line: ' + '; '.join(across))
print('disputed areas left out of lgas.csv:', [(d['state'], d['total']) for d in disputed])
