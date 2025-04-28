from pydantic import BaseModel
from datetime import date
from typing import Optional


class Plant(BaseModel):
    id: int
    name: str
    type_id: int
    responsible_id: int
    last_watered: date


class PlantType(BaseModel):
    id: int
    name: str
    watering_interval: int


class PlantBase(BaseModel): # для запроса post /plants
    name: str
    type_id: int
    last_watered: Optional[date] = None


class PlantUpdate(BaseModel):
    name: Optional[str] = None
    type_id: Optional[int] = None
    last_watered: Optional[date] = None


class PlantInDB(PlantBase):
    id: int
    responsible_id: int

    class Config:
        from_attributes = True


class PlantTypeBase(BaseModel): # для запроса post /plant-types
    name: str
    watering_interval: int


class PlantTypeInDB(PlantTypeBase):
    id: int

    class Config:
        from_attributes = True
