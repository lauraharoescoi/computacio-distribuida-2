from datetime import date
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import deferred

from sqlalchemy.orm import Mapped

class Room(Base):
    __tablename__ = "room"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, index=True)
    home: int = Column(Integer, ForeignKey("home.id"))
    sensor: int = Column(Integer)
