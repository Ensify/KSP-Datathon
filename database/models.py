from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class MapNode(BaseModel):
    """
    Container for a single map node, that has a cctv
    """

    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[int] = Field(default=None)  
    latitude: float = Field(...)
    longitude: float = Field(...)
    name: str = Field(...)
    address: str = Field(...)

class Event(BaseModel):
    """
    Container for a single event
    """
    id: Optional[PyObjectId] = Field(...)
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
    auto_count: Optional[int] = Field(default=0)  
    truck_count: Optional[int] = Field(default=0)  
    bike_count: Optional[int] = Field(default=0)  
    car_count: Optional[int] = Field(default=0)  
    people_count: Optional[int] = Field(default=0)


class NodeConnection(BaseModel):
    id: Optional[int] = Field(default=None)
    src_id: int = Field(...)
    dest_id: int = Field(...)
    distance: float = Field(...)

class Alert:
    def __init__(self, event_id, node_id, start_time):
        self.event_id = event_id
        self.node_id = node_id
        self.start_time = start_time
        self.alert_time = datetime.now()