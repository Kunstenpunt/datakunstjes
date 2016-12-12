sql = """
select
  c.ID,
  c.Title,
  id.Name,
  g.Name,
  i.FileName
from
  carriers c
inner JOIN
  carriermainartists cm
ON
  cm.CarrierID = c.ID
INNER JOIN
  identities id
ON
  id.ID=cm.IdentityID
inner join
  dblinking dbl
on
  dbl.ObjectID = c.ID AND dbl.ObjectType = 5
inner join
  genres g
on
  g.ID = dbl.LinkID AND dbl.LinkType = 11
inner join
  dblinking dbll
on
  dbll.ObjectID = c.ID AND dbll.ObjectType = 5
inner JOIN
  images i
ON
  i.ID = dbll.LinkID AND dbll.LinkType = 9
where
  c.ReleaseDate >= "2015-12-31" AND
  c.ReleaseDate < "2017-01-01" AND
  c.Filter IN (2,3)
group by
  c.ID
"""

from pandas import read_csv
from json import dumps

df = read_csv("mcv_export_12_12_2016_17_22.txt", delimiter="\t", encoding="utf-16")

uniq_nodes = {}
uniq_edges = set()
nodes = list()
edges = list()
i = 0

for row in df.iterrows():
    release_id = int(row[1][0])
    release_titel = row[1][1]
    ma = row[1][2]
    genre = row[1][3]
    image = row[1][4]

    if release_id not in uniq_nodes.keys():
        nodes.append({
            "id": release_id,
            "title": ma + " - " + release_titel,
            "image": "http://files.muziekcentrum.be/images/" + image,
            "shape": 'image'
        })
        uniq_nodes[release_titel] = release_id

    if genre not in uniq_nodes.keys():
        nodes.append({
            "id": i,
            "label": genre,
            "title": genre,
            "value": 200,
            "shape": "dot"
        })
        uniq_nodes[genre] = i
        i += 1

    edge_uid = str(uniq_nodes[release_titel]) + "_" + str(uniq_nodes[genre])
    edge = {
        "from": uniq_nodes[release_titel],
        "to": uniq_nodes[genre]
    }
    if edge_uid not in uniq_edges:
        edges.append(edge)
        uniq_edges.add(edge_uid)

with open("nodes.js", "w") as f:
    f.write("var rawnodes = " + dumps(nodes, indent=2))

with open("edges.js", "w") as f:
    f.write("var rawedges = " + dumps(edges, indent=2))
