from OSMPythonTools.api import Api
from OSMPythonTools.overpass import Overpass
import logging

overpass = Overpass()
# logging.getLogger("OSMPythonTools").setLevel(logging.ERROR)


# road = "Hill Street"
# bounds = ["Liberty Street", "Ida Street"]
road = "Congress Street"
bounds = ["Brunswick Avenue", "11th Street"]


query = f"""
way[highway][name="{road}"];node(w)->.n1;
way[highway][name="{bounds[0]}"];node(w)->.n2;
way[highway][name="{bounds[1]}"];node(w)->.n3;
(node.n1.n2; node.n1.n3;);
out body;"""

bbox = {"bbox": "42.6940400, -73.7064390, 42.7952720, -73.6491630"}

from pprint import pprint

coords = overpass.query(query, settings=bbox).elements()

lats = []
lons = []

for elt in coords:
    lats.append(elt.lat())
    lons.append(elt.lon())

bbox2 = {"bbox": f"{min(lats)}, {min(lons)}, {max(lats)}, {max(lons)}"}

query2 = f"""
way[highway][name="{road}"];node(w)->.n1;
node.n1;
out body;
"""

# query2 = f"""
# way[highway][name="{road}"];node(w);
# (._;>;);
# out body;
# """

result = overpass.query(query2, settings=bbox2)
nodes = {}
pprint(result.toJSON())
for elt in result.elements():
    nodes[elt.id()] = [elt.lat(), elt.lon()]
pprint(nodes)


def distance(lat, lon, lat2, lon2):
    return pow(pow(abs(lat) - abs(lat2), 2) + pow(abs(lon) - abs(lon2), 2), 0.5)


nodes_backup = nodes.copy()
cur = [lats[1], lons[1]]
ids = []
while len(nodes.keys()) != 0:
    mindist = -1
    curmin = None
    print(len(nodes))
    for key in nodes:
        dist = distance(*cur, *nodes[key])
        if dist < mindist or mindist == -1:
            mindist = dist
            curmin = key

    ids.append(nodes[curmin])

    # if nodes[curmin] == [lats[0], lons[1]]: break

    del nodes[curmin]

pprint(ids)
