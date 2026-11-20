"""DR Congo: the 1984 census's 44 cities and sub-regions placed in today's 26 provinces (2015), and the counts summed to
them. Writes COD/units.csv (the mapping, one row per 1984 unit, with its basis) and COD/provinces-2015.csv (the sums).
Run from the repository root: python3 -I scripts/cod_provinces.py ../boundaries
The boundaries checkout gives geoBoundaries' spelling and ID of each province and places each 1984 city in one."""
import csv, json, glob, sys, os
B = sys.argv[1] if len(sys.argv) > 1 else '../boundaries'
# 1984 unit -> province as Loi organique 15/006 of 25 March 2015 spells it (article 2), and the basis.
SAME = 'same name as the province'
CITY = 'city; its point lies in the province in geoBoundaries ADM1'
CAP = 'city; the province\'s chef-lieu in Loi organique 15/006'
MAP = {
 'LUKUNGA': ('Kinshasa', 'part of the ville de Kinshasa, unchanged'), 'FUNA': ('Kinshasa', 'part of the ville de Kinshasa, unchanged'),
 'MONT-AMBA': ('Kinshasa', 'part of the ville de Kinshasa, unchanged'), 'TSHANGU': ('Kinshasa', 'part of the ville de Kinshasa, unchanged'),
 'MATADI': ('Kongo Central', CAP), 'BOMA': ('Kongo Central', CITY),
 'BAS-FLEUVE': ('Kongo Central', 'the whole Bas-Zaïre region became Kongo Central (Bas-Congo renamed)'),
 'CATARACTES': ('Kongo Central', 'the whole Bas-Zaïre region became Kongo Central (Bas-Congo renamed)'),
 'LUKAYA': ('Kongo Central', 'the whole Bas-Zaïre region became Kongo Central (Bas-Congo renamed)'),
 'BANDUNDU': ('Kwilu', CAP), 'KIKWIT': ('Kwilu', CITY), 'KWILU': ('Kwilu', SAME), 'KWANGO': ('Kwango', SAME), 'MAI-NDOMBE': ('Mai-Ndombe', SAME),
 'MBANDAKA': ('Equateur', CAP), 'EQUATEUR': ('Equateur', SAME), 'SUD-UBANGI': ('Sud-Ubangi', SAME), 'ZONGO': ('Sud-Ubangi', CITY),
 'NORD-UBANGI': ('Nord-Ubangi', SAME), 'MONGALA': ('Mongala', SAME), 'TSHUAPA': ('Tshuapa', SAME),
 'KISANGANI': ('Tshopo', CAP), 'TSHOPO': ('Tshopo', SAME), 'BAS-UELE': ('Bas-Uele', SAME), 'HAUT-UELE': ('Haut-Uele', SAME), 'ITURI': ('Ituri', SAME),
 'BUKAVU': ('Sud-Kivu', CAP), 'MANIEMA': ('Maniema', SAME), 'NORD-KIVU': ('Nord-Kivu', SAME), 'SUD-KIVU': ('Sud-Kivu', SAME),
 'LUBUMBASHI': ('Haut-Katanga', CITY + '; the chef-lieu is not named in the text read'),
 'LIKASI': ('Haut-Katanga', CITY), 'HAUT-SHABA': ('Haut-Katanga', 'Shaba was renamed Katanga in 1997: Haut-Shaba is the district of Haut-Katanga'),
 'KOLWEZI': ('Lualaba', CAP), 'LUALABA': ('Lualaba', SAME), 'HAUT-LOMAMI': ('Haut-Lomami', SAME), 'TANGANIKA': ('Tanganyika', SAME + ', spelled Tanganika in 1984'),
 'MBUJI-MAYI': ('Kasaï Oriental', CAP), 'TSHILENGE': ('Kasaï Oriental', 'its territory of Tshilenge lies in the province in geoBoundaries ADM1, whose chef-lieu Mbuji-Mayi it surrounds'),
 'SANKURU': ('Sankuru', SAME), 'KABINDA': ('Lomami', 'Kabinda is Lomami\'s chef-lieu in Loi organique 15/006, and Kabinda and Mwene-Ditu lie in Lomami in geoBoundaries ADM1'),
 'KANANGA': ('Kasaï Central', CAP), 'LULUA': ('Kasaï Central', 'the sub-region around Kananga, Kasaï Central\'s chef-lieu'), 'KASAI': ('Kasaï', SAME),
}
# The law's spelling -> geoBoundaries' spelling, where they differ.
GB = {'Kongo Central': 'Kongo-Central', 'Equateur': 'Équateur', 'Bas-Uele': 'Lower Uele', 'Haut-Uele': 'Upper Uele', 'Nord-Kivu': 'North Kivu',
      'Sud-Kivu': 'South Kivu', 'Kasaï Oriental': 'Kasai-Oriental', 'Kasaï Central': 'Central Kasai', 'Kasaï': 'Kasai'}
ids = {}
for f in sorted(glob.glob(os.path.join(B, 'COD/ADM1/parts/*.geojson'))):
    for ft in json.load(open(f, encoding='utf-8'))['features']:
        ids[ft['properties']['shapeName']] = ft['properties']['shapeID']
rows = list(csv.DictReader(open('COD/counts.csv', encoding='utf-8')))
units = [r for r in rows if r['level'] in ('ville', 'sous-region')]
assert set(MAP) == {r['unit'] for r in units}, 'every 1984 city and sub-region is placed, once'
with open('COD/units.csv', 'w', newline='', encoding='utf-8') as out:
    w = csv.writer(out, lineterminator='\n')
    w.writerow(['level', 'region', 'unit', 'province', 'geoboundaries_name', 'geoboundaries_id', 'basis'])
    for r in units:
        p, basis = MAP[r['unit']]; g = GB.get(p, p)
        assert g in ids, f'{g} is not a province in geoBoundaries ADM1'
        w.writerow([r['level'], r['region'], r['unit'], p, g, ids[g], basis])
sums = {}
for r in units:
    p = MAP[r['unit']][0]; s = sums.setdefault(p, {'men': 0, 'women': 0, 'total': 0, 'from': []})
    for k in ('men', 'women', 'total'): s[k] += int(r[k])
    s['from'].append(r['unit'])
assert len(sums) == 26 and set(GB.get(p, p) for p in sums) == set(ids), 'the 26 provinces, each in geoBoundaries'
country = next(r for r in rows if r['level'] == 'pays')
for k in ('men', 'women', 'total'): assert sum(s[k] for s in sums.values()) == int(country[k]), f'provinces sum to the country\'s {k}'
with open('COD/provinces-2015.csv', 'w', newline='', encoding='utf-8') as out:
    w = csv.writer(out, lineterminator='\n')
    w.writerow(['province', 'geoboundaries_name', 'geoboundaries_id', 'men', 'women', 'total', 'from_1984'])
    for p in sorted(sums, key=lambda p: GB.get(p, p)):
        s = sums[p]; g = GB.get(p, p)
        w.writerow([p, g, ids[g], s['men'], s['women'], s['total'], ' + '.join(s['from'])])
print('26 provinces; sums', {k: sum(s[k] for s in sums.values()) for k in ('men', 'women', 'total')})
