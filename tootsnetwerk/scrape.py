from requests import get
from bs4 import BeautifulSoup
from re import sub, compile
from itertools import combinations
from json import dumps, loads
from codecs import open

baseurl = 'http://www.muziekarchief.be/'
toots = baseurl + 'identitydetails.php?ID=132692'

with open('artist_country.json', 'r', "utf-8") as f:
    artist_country = loads(f.read())

edgelist = []

r = get(toots)
tootssoup = BeautifulSoup(r.text, 'html.parser')

for carrier in tootssoup.find_all(class_='carrierthumb')[0:94]: # enkel de eerste 94 albums zijn relevant hier
    plaat = baseurl + carrier.a['href']
    print(plaat)
    r = get(plaat)
    plaatsoup = BeautifulSoup(r.text, 'html.parser')
    plaatcollaborators = plaatsoup.find_all('span', attrs={'class': 'memberlist'})
    personnel = [sub(compile('\(.+?\)'), '', pc.text).strip() for pc in plaatcollaborators]
    if len(personnel) > 1 and 'Toots Thielemans' in personnel:
        for c in combinations(personnel, 2):
            edgelist.append(sorted(c))

nodes = {}
edges = {}

node_id = {}

i = 1
for edge in edgelist:
    n1, n2 = edge
    n1_uni = artist_country[n1][1] if artist_country[n1][1] != "" else n1
    n2_uni = artist_country[n2][1] if artist_country[n2][1] != "" else n2
    if n1_uni not in node_id:
        node_id[n1_uni] = i
        i += 1
    if n1_uni not in nodes:
        nodes[n1_uni] = {'id': node_id[n1_uni],
                         'label': n1_uni,
                         'group': artist_country[n1][0],
                         'title': n1_uni,
                         'value': 0}
    nodes[n1_uni]['value'] += 1

    if n2_uni not in node_id:
        node_id[n2_uni] = i
        i += 1
    if n2_uni not in nodes:
        nodes[n2_uni] = {'id': node_id[n2_uni],
                         'label': n2_uni,
                         'group': artist_country[n2][0],
                         'title': n2_uni,
                         'value': 0}
    nodes[n2_uni]['value'] += 1

    e = str(node_id[n1_uni]) + ' ' + str(node_id[n2_uni])
    if e not in edges:
        edges[e] = {'from': node_id[n1_uni],
                    'to': node_id[n2_uni],
                    'value': 0}
    edges[e]['value'] += 1

with open('toots.js', 'w', "utf-8") as f:
    network = 'var edges=' + dumps([e for e in edges.values()], indent=2) + \
              '\n\nvar nodes=' + dumps([n for n in nodes.values()], indent=2)
    f.write(network)