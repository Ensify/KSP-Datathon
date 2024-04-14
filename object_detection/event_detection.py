
from ultralytics import YOLO
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient
import os
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]



load_dotenv()
client = MongoClient(os.environ.get('MONGO_URI'))

db = client['ksp-traffic']
event_collection = db['events']
instance_collection = db['instances']
vehicle_collection = db['vehicles']


class Event(BaseModel):
    """
    Container for a single event
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    node_id: int = Field(...)
    type: str = Field(...)
    start_time: datetime = Field(...)
    end_time: Optional[datetime] = Field(default=None)
    alerts_raised: int = Field(...)

class InstanceInformation(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    node_id: int = Field(...)
    time_stamp: datetime = Field(...)
    vehicle_count: int = Field(...)
    pot_hole_count: int = Field(...)
    parked_vehicle_count: int = Field(...)
    people_count: int = Field(...)
    
    
class Vehicle(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    node_id: int = Field(...)
    time_stamp: datetime = Field(...)
    auto_count: int = Field(...)
    truck_count: int = Field(...)
    bike_count: int = Field(...)
    car_count: int = Field(...)

TOLERANCE_INTERVAL = {
    'car': 10 * 60,
    'auto': 5 * 60,
    'pothole': 10
}

DISPLACEMENT_TOLERANCE = 10

UPDATE_INTERVAL = 100

class Detector:
    def __init__(self, model, node_id):
        self.model = YOLO(model)
        self.node_id = node_id
        self.object_states = {}

    def main_loop(self, video):
        self.results = self.model.track(source=video, stream=True, show = True)
        i = 0
        for result in self.results:
            boxes = result.boxes
            ids = boxes.id
            cls = boxes.cls
            xyxy = boxes.xyxy
            
            for idx, id in enumerate(ids):
                id = int(id.item())
                class_name = result.names[int(cls[idx].item())]
                if id in self.object_states:
                    if self.time_detla(id) > TOLERANCE_INTERVAL.get(class_name, 10):
                        mid = self.get_center_from_xyxy(xyxy[idx].numpy())
                        if self.distance_detla(self.object_states[id]['mid'], mid) < DISPLACEMENT_TOLERANCE:
                            self.raise_event(class_name, self.object_states[id]['begin_time'], datetime.now())
                        self.object_states[id]['mid'] = mid


                else:
                    self.object_states[id] = {
                        'cls': (result.names[int(cls[idx].item())]),
                        'mid': self.get_center_from_xyxy(xyxy[idx].numpy()),
                        'begin_time': datetime.now()
                    }
            if i % UPDATE_INTERVAL == 0:
                state = {}
                for c in cls:
                    c = result.names[int(c.item())]
                    state[c] = state.get(c, 0) + 1
                
                self.update_instance_state(state)
            i += 1

    def time_detla(self, id):
        val = (datetime.now() - self.object_states[id]['begin_time']).total_seconds()
        return val
    
    def distance_detla(self, mid1, mid2):
        x1 = mid1[0]
        y1 = mid1[1]
        x2 = mid2[0]
        y2 = mid2[1]
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    
    
    def get_center_from_xyxy(self, xyxy):
        x_mid = (xyxy[0] + xyxy[2]) / 2
        y_mid = (xyxy[1] + xyxy[3]) / 2
        return (x_mid, y_mid)

    def raise_event(self, class_name, start, end):
        event = Event(node_id=self.node_id, type=class_name, start_time=start, end_time=end, alerts_raised=0)
        event_collection.insert_one(event.dict())



    def update_instance_state(self, state):
        print(state)
        total_vehicles = state.get('auto', 0)+state.get('truck', 0)+state.get('bike', 0)+state.get('car',0)
        instance = InstanceInformation(node_id=self.node_id, time_stamp=datetime.now(), vehicle_count=total_vehicles,pot_hole_count=0, parked_vehicle_count=total_vehicles, people_count= state.get('person'))
        instance_collection.insert_one(instance.dict())

        vehicle = Vehicle(node_id=self.node_id, time_stamp=datetime.now(), auto_count=state.get('auto', 0), truck_count=state.get('truck',0), bike_count=state.get('bike', 0), car_count=state.get('car',0))
        vehicle_collection.insert_one(vehicle.dict())



if __name__ == '__main__':
    detector = Detector(model=r"models\last.pt", node_id= 1)
    detector.main_loop(video=r'test_data\Traffic Flow Optiomization and Congestion Management\Problem Statement - 3\Russel_Market_Entrance_PTZ_1.mp4')
