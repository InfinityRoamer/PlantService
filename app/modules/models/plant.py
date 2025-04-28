from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.common.db.session import Base
from datetime import datetime


class PlantType(Base):
    __tablename__ = 'plant_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    watering_interval = Column(Integer, nullable=False)


class Plant(Base):
    __tablename__ = 'plants'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_watered = Column(Date, default=datetime.now())
    type_id = Column(Integer, ForeignKey('plant_types.id'), nullable=False)
    responsible_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    users = relationship('User')
    types = relationship('PlantType')
