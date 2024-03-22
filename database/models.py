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
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    latitude: float = Field(...)
    longitude: float = Field(...)
    name: str = Field(...)
    address: str = Field(...)

class Event(BaseModel):
    """
    Container for a single event
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    node_id: str = Field(...)
    type: str = Field(...)
    start_time: datetime = Field(...)
    end_time: Optional[datetime] = Field(...)
    alerts_raised: int = Field(...)

class InstanceInformation(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    node_id: str = Field(...)
    time_stamp: datetime = Field(...)
    vehicle_count: int = Field(...)
    pot_hole_count: int = Field(...)
    parked_vehicle_count: int = Field(...)
    people_count: int = Field(...)
    

