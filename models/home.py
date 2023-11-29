from datetime import date
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, Geometry
from database import Base
from sqlalchemy.orm import deferred

from sqlalchemy.orm import Mapped

class Home(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, index=True)
    address: str = Column(String, unique=True, index=True)
    description: str = Column(String, unique=True, index=True)
    owner: int = Column(Integer, ForeignKey("user.id"))
    location = Column(Geometry('POINT'))
    
class HomeUser(Base):
    __tablename__ = "home_user"
    id: int = Column(Integer, primary_key=True, index=True)
    home = Column(Integer, ForeignKey("home.id"))
    user = Column(Integer, ForeignKey("user.id"))