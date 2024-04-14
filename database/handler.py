from pymongo import MongoClient
from dotenv import load_dotenv
import os
import math
from models import MapNode, NodeConnection, Event, InstanceInformation
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional


load_dotenv()
client = MongoClient(os.environ.get('MONGO_URI'))

db = client['ksp-traffic']
node_collection = db['nodes']
event_collection = db['events']
instance_collection = db['instances']
collection_auto_increment = db["auto-increment-data"]
edge_collection = db['edges']


def get_next_version_id(collection_auto_increment, coll_name, scan=None):
    counter_doc = collection_auto_increment.find_one(
        {"versionId": "versionId", "collName": coll_name}
    )

    if counter_doc is None:
        collection_auto_increment.insert_one(
            {"versionId": "versionId", "collName": coll_name, "seq": 0}
        )
    result = collection_auto_increment.find_one_and_update(
        {"versionId": "versionId", "collName": coll_name},
        {"$inc": {"seq": 1}},
        return_document=True,
    )

    return 1 if not result else result["seq"]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    distance_m = distance * 1000
    return distance_m


def add_nodes():
    with open(r"database/nodes") as f:
        data = f.read().split("\n")
        nodes = []
        for i in data:
            loc, add, name = i.split("-")
            lat,long = map(float,loc.split(","))
            add = add.strip()
            name = name.strip()
            id = get_next_version_id(collection_auto_increment, "nodes")
            node = MapNode(id=id, latitude=lat,longitude=long,name=name, address=add)
            node = node_collection.insert_one(node.model_dump())
            print(node, id)
    # node = MapNode(latitude=data[0], longitude=data[1], address=)
    # data = [MapNode(latitude=float(i[1]),longitude=float(i[0]),name=i[2], address=i[3]) for i in data]

def add_edges():

    with open("database/edges") as of:
        data = of.read().split("\n")
        edges = []
        for i in data:
            src, dest = i.split("-")
            src = int(src)
            dest = int(dest)
         
            id = get_next_version_id(collection_auto_increment, "edges")
            node_src = node_collection.find_one({"id": src})
            node_dest = node_collection.find_one({"id": dest})
            dist = haversine(node_src['latitude'], node_src['longitude'], node_dest['latitude'], node_dest['longitude'])
            edge = NodeConnection(id=id, src_id=src, dest_id=dest, distance=dist)
            edge = edge_collection.insert_one(edge.model_dump())
            print(edge, id, dist)
    



def insert_dummy_events():
    dummy_events = [
        Event(id=1, node_id=1, type="A", start_time=datetime(2024, 4, 13, 21, 15), alerts_raised=0),
        Event(id=2, node_id=2, type="B", start_time=datetime(2024, 4, 13, 21, 0), alerts_raised=0),
        Event(id=3, node_id=3, type="C", start_time=datetime(2024, 4, 13, 21, 0), alerts_raised=0),
        Event(id=4, node_id=4, type="A", start_time=datetime(2024, 4, 13, 20, 0), alerts_raised=0),
        Event(id=5, node_id=5, type="B", start_time=datetime(2024, 4, 13, 21, 18), alerts_raised=0),
        Event(id=6, node_id=6, type="A", start_time=datetime(2024, 4, 13, 20, 0), alerts_raised=0),
        Event(id=7, node_id=7, type="B", start_time=datetime(2024, 4, 13, 21, 19), alerts_raised=0),
        Event(id=8, node_id=8, type="A", start_time=datetime(2024, 4, 13, 21, 15), alerts_raised=0),
        Event(id=9, node_id=9, type="C", start_time=datetime(2024, 4, 13, 20, 0), alerts_raised=0),
    ]


    for event in dummy_events:
        event_dict = event.dict()
        event_collection.insert_one(event_dict)
        print(event_dict)


def insert_dummy_instance():
    dummy_instance = [
        InstanceInformation(id=1, node_id=1, time_stamp=datetime(2024, 4, 13, 21, 15), vehicle_count=2, pot_hole_count=1, parked_vehicle_count=2, people_count=15),
        InstanceInformation(id=2, node_id=1, time_stamp=datetime(2024, 4, 13, 23, 15), vehicle_count=5, pot_hole_count=1, parked_vehicle_count=3, people_count=10),
        InstanceInformation(id=3, node_id=2, time_stamp=datetime(2024, 4, 13, 22, 15), vehicle_count=2, pot_hole_count=1, parked_vehicle_count=2, people_count=18),
        InstanceInformation(id=4, node_id=2, time_stamp=datetime(2024, 4, 13, 22, 50), vehicle_count=6, pot_hole_count=1, parked_vehicle_count=2, people_count=15),
        InstanceInformation(id=5, node_id=3, time_stamp=datetime(2024, 4, 13, 23, 15), vehicle_count=4, pot_hole_count=2, parked_vehicle_count=2, people_count=14),
        InstanceInformation(id=7, node_id=3, time_stamp=datetime(2024, 4, 13, 23, 55), vehicle_count=9, pot_hole_count=2, parked_vehicle_count=2, people_count=22),
        InstanceInformation(id=8, node_id=4, time_stamp=datetime(2024, 4, 13, 21, 15), vehicle_count=13, pot_hole_count=1, parked_vehicle_count=2, people_count=39),
        InstanceInformation(id=9, node_id=5, time_stamp=datetime(2024, 4, 13, 21, 15), vehicle_count=19, pot_hole_count=1, parked_vehicle_count=2, people_count=15),
        InstanceInformation(id=10, node_id=6, time_stamp=datetime(2024, 4, 13, 21, 15), vehicle_count=24, pot_hole_count=1, parked_vehicle_count=2, people_count=15),
        InstanceInformation(id=11, node_id=7, time_stamp=datetime(2024, 4, 13, 21, 15), vehicle_count=26, pot_hole_count=1, parked_vehicle_count=2, people_count=14)

    ]
    for instance in dummy_instance:
        instance_dict = instance.dict()
        instance_collection.insert_one(instance_dict)
        print(instance_dict)


if __name__ == "__main__":
    # add_nodes()
    # add_edges()
    # insert_dummy_events()
    insert_dummy_instance()
    pass