releases_sql = """
select
  c.ID,
  c.Title,
  id.Name,
  g.ID,
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

genres_sql = """
select gg.ID, gg.Name, g.ID, g.Name
from genres gg
left join genres g on g.ID = gg.ParentID
"""

from pandas import read_csv
from json import dumps

df = read_csv("mcv_export_15_12_2016_17_44.txt", delimiter="\t", encoding="utf-16", header=None)
genres = read_csv("mcv_genres.txt", delimiter="\t", encoding="utf-16", header=None)

uniq_nodes = set()
uniq_edges = set()
nodes = list()
edges = list()

nodes.append({
    "id": 999,
    "label": "2016",
    "title": "2016",
    "shape": "dot",
    "value": 300
})

for row in df.iterrows():
    release_id = int(row[1][0])
    release_titel = row[1][1]
    ma = row[1][2]
    genre_id = row[1][3]
    genre_naam = row[1][4]
    image = row[1][5]

    if genre_id not in uniq_nodes:
        nodes.append({
            "id": genre_id,
            "label": genre_naam,
            "title": genre_naam,
            "shape": "dot",
            "value": 200
        })
        uniq_nodes.add(genre_id)

    if release_id not in uniq_nodes:
        nodes.append({
            "id": release_id,
            "title": ma + " - " + release_titel,
            "image": "http://files.muziekcentrum.be/listimages/" + image,
            "shape": 'image'
        })
        uniq_nodes.add(release_id)

    edge_uid = str(release_id) + "_" + str(genre_id)
    edge = {
        "from": release_id,
        "to": genre_id
    }
    if edge_uid not in uniq_edges:
        edges.append(edge)
        uniq_edges.add(edge_uid)

for row in genres.iterrows():
    genre_id = row[1][0]
    parent_id = row[1][2]
    edge_uid = str(genre_id) + "_" + str(parent_id)
    edge = {
        "from": genre_id,
        "to": parent_id
    }
    if genre_id in uniq_nodes:
        if edge_uid not in uniq_edges and parent_id != 0:
            edges.append(edge)
            uniq_edges.add(edge_uid)

    if parent_id not in uniq_nodes:
        edges.append({
            "from": genre_id,
            "to": 999
        })
        uniq_edges.add(str(genre_id) + "_999")

    if parent_id == 0 and str(genre_id) + "_999" not in uniq_edges:
        edges.append({
            "from": genre_id,
            "to": 999
        })
        uniq_edges.add(str(genre_id) + "_999")

with open("nodes.js", "w") as f:
    f.write("var rawnodes = " + dumps(nodes, indent=2))

with open("edges.js", "w") as f:
    f.write("var rawedges = " + dumps(edges, indent=2))
