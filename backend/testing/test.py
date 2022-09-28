from OSMPythonTools.api import Api
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import logging

api = Api()
overpass = Overpass()
logging.getLogger("OSMPythonTools").setLevel(logging.ERROR)

# print(.tag('border_type'))
# print(api.query('way/669246263').nodes())


road = "Congress Street"
bounds = ["4th Street", "5th Street"]


query = overpassQueryBuilder(
    area="relation/174387", elementType="way", selector=f'"name"~"{road}"'
)
result = overpass.query(query)
for way in result.ways():
    for node in way.nodes(shallow=False):
        api.query(f"node/{node.id()}")
        print(node.id(), node.members())
