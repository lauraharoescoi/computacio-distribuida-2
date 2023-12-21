from sqlalchemy import Column, Integer, String, ForeignKey
from geoalchemy2 import Geometry
from database import Base


class Home(Base):
    __tablename__ = "home"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=False, index=True)
    address: str = Column(String, unique=True, index=True)
    description: str = Column(String, unique=False, index=True)
    owner: int = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    location = Column(Geometry('POINT'))