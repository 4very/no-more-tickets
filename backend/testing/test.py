from OSMPythonTools.api import Api
from OSMPythonTools.overpass import Overpass
import logging

overpass = Overpass()
# logging.getLogger("OSMPythonTools").setLevel(logging.ERROR)


road = "Division Street"
bounds = ["4th Street", "1st Street"]

query = f'''
way[highway][name="{road}"];node(w)->.n1;
way[highway][name="{bounds[0]}"];node(w)->.n2;
way[highway][name="{bounds[1]}"];node(w)->.n3;
(node.n1.n2; node.n1.n3;);
out body;'''

bbox = {'bbox': "42.6940400, -73.7064390, 42.7952720, -73.6491630"}

from pprint import pprint
coords = overpass.query(query, settings=bbox).elements()

lats = []
lons = []
for elt in coords:
    lats.append(elt.lat())
    lons.append(elt.lon())
    
bbox2 = {"bbox": f"{min(lats)}, {min(lons)}, {max(lats)}, {max(lons)}"}

query2 = f'''
way[highway][name="{road}"];node(w)->.n1;
node.n1;
out body;
'''

pprint(overpass.query(query2, settings=bbox2).toJSON())
