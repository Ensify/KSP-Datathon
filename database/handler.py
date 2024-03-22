from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os

from .models import MapNode

client = MongoClient(os.environ.get('MONGO_URI'))

db = client['ksp-traffic']
node_collection = db['nodes']
event_collection = db['events']
instance_collection = db['instances']

# with open(r"database\nodes") as f:
#     data = f.read().split("\n")
#     nodes = []
#     for i in data:
#         loc, add, name = i.split("-")
#         lat,long = map(float,loc.split(","))
#         add = add.strip()
#         name = name.strip()
#         node = MapNode(latitude=lat,longitude=long,name=name, address=add)
#         node = node_collection.insert_one(node.model_dump(by_alias=True, exclude=["id"]))
#         print(node)
#     # node = MapNode(latitude=data[0], longitude=data[1], address=)
#     # data = [MapNode(latitude=float(i[1]),longitude=float(i[0]),name=i[2], address=i[3]) for i in data]

